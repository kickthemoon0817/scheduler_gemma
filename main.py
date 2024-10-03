import torch
import gradio as gr
import logging
from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel

# Step 1: Define device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"We are using: {device}")

# Step 2: Load the Tokenizer
tokenizer_path = './model'  # Update this to your model path
tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
print("Tokenizer Loaded")

# Add special tokens if they are not already present
special_tokens = {
    "bos_token": "<bos>",
    "eos_token": "<eos>",
    "pad_token": "<pad>",
    "additional_special_tokens": ["<start_of_turn>", "<end_of_turn>"]
}
tokenizer.add_special_tokens(special_tokens)

# Step 3: Load the Model with 4-bit Quantization
adapter_path = "./finetuned_gemma_4bit/lora_adapter"
model_path = './model'

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4"
)

model = AutoModelForCausalLM.from_pretrained(
    model_path,
    device_map="auto",  # Automatically maps the model to the appropriate device
    quantization_config=quantization_config,
    offload_buffers=True
)

# Load LoRA adapter
model = PeftModel.from_pretrained(model, adapter_path)
model.resize_token_embeddings(len(tokenizer))

print("Finetuned Gemma Model Loaded")

# Ensure the tokenizer has a pad_token_id
if not hasattr(tokenizer, 'pad_token_id') or tokenizer.pad_token_id is None:
    tokenizer.pad_token_id = tokenizer.eos_token_id
    print('pad_token_id set to eos_token_id')

# Step 4: Create a pipeline for generation without specifying `device`
text_generation_pipeline = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=150,
    temperature=0.9,
    top_p=0.85,
    top_k=50,
    do_sample=True  # Enable sampling
)

# Function to format the conversation with apply_chat_template
def format_prompt(conversation):
    """
    Format the conversation using the tokenizer's apply_chat_template method.
    """
    messages = []
    for turn in conversation:
        messages.append({"role": turn["role"], "content": turn["content"]})
    
    # Use the apply_chat_template method to format the conversation
    prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    logging.debug("Formatted Prompt:\n" + prompt)
    return prompt

# Function to generate text from formatted conversation
def generate_text(conversation):
    # Format the conversation using apply_chat_template
    prompt = format_prompt(conversation)

    # Generate output using the pipeline
    outputs = text_generation_pipeline(prompt)

    # Extract and log generated output
    generated_text = outputs[0]["generated_text"][len(prompt):].strip()
    logging.debug("Generated Text:\n" + generated_text)

    return generated_text

# Initialize conversation history
conversation_history = []

# Gradio Chat Interface
def respond(user_input, chat_history):
    # Append the user's input to the conversation history
    conversation_history.append({'role': 'user', 'content': user_input})
    
    # Generate the assistant's response
    assistant_response = generate_text(conversation_history)
    
    # Append the assistant's response to conversation history and chat history
    conversation_history.append({'role': 'assistant', 'content': assistant_response})
    chat_history.append((user_input, assistant_response))
    
    return "", chat_history

# Set up Gradio UI
with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 📅 당신의 일정 관리 AI 비서")
    gr.Markdown("당신의 일정을 말씀해주신다면, 제가 관리해드릴게요!")
    chatbot = gr.Chatbot()
    with gr.Row():
        msg = gr.Textbox(
            placeholder="여기에 메시지를 입력하세요...",
            show_label=False
        )
        send = gr.Button("Send")
    send.click(respond, [msg, chatbot], [msg, chatbot])
    msg.submit(respond, [msg, chatbot], [msg, chatbot])

demo.launch(share=True)
