import sys
import os
import torch
import gradio as gr

from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
)
from peft import PeftModel

# Step 1: Define device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"We are using: {device}")

# Step 2: Load the Tokenizer
tokenizer_path = './model'  # Adjust this path
tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
print("Tokenizer Loaded")

# Add special tokens if not already present
special_tokens = {
    "bos_token": "<bos>",
    "eos_token": "<eos>",
    "pad_token": "<pad>",
    "additional_special_tokens": ["<start_of_turn>", "<end_of_turn>"]
}
tokenizer.add_special_tokens(special_tokens)

# Step 3: Load the Model with 4-bit Quantization
adapter_path = "./finetuned_gemma_4bit/lora_adapter"
model_path = './model'  # Adjust this path

quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
)

model = AutoModelForCausalLM.from_pretrained(
    model_path,
    device_map="auto",
    quantization_config=quantization_config,
    offload_buffers=True  # Added to handle memory warning
)

model = PeftModel.from_pretrained(model, adapter_path)

# Resize model embeddings if tokenizer was updated
model.resize_token_embeddings(len(tokenizer))

print("Finetuned Gemma Model Loaded")

# Ensure tokenizer has pad_token_id
if not hasattr(tokenizer, 'pad_token_id') or tokenizer.pad_token_id is None:
    tokenizer.pad_token_id = tokenizer.eos_token_id
    print('pad_token_id set to eos_token_id')

# Format the conversation manually with schedule summarization
def format_conversation(conversation, schedules_summary=""):
    """
    Format the conversation into a string suitable for model input.
    """
    formatted_conversation = "<bos>\n"
    # Add system summary, if any
    if schedules_summary:
        formatted_conversation += f"<start_of_turn>assistant\n{str(schedules_summary)}<end_of_turn>\n"
        
    # Add each message in the conversation
    for turn in conversation:
        role = turn['role']
        content = turn['content']
        formatted_conversation += f"<start_of_turn>{role}\n{content}<end_of_turn>\n"
    
    # Add the current assistant response start token
    formatted_conversation += "<start_of_turn>assistant\n"
    return formatted_conversation

# Generate text function using the formatted conversation
def generate_text(model, tokenizer, conversation, device, max_new_tokens=150, temperature=0.9, top_p=0.85, top_k=50):
    # Prepare the conversation history
    previous_schedules = [turn['content'] for turn in conversation if turn['role'] == 'user']
    
    # Generate schedule summary if multiple schedules exist
    schedules_summary = ""
    if len(previous_schedules) > 1:
        # Generate the schedule summary
        schedules_summary = "이전에 말씀하신 일정은 다음과 같습니다:\n" + "\n".join(
            f"- {schedule}" for schedule in previous_schedules[:-1]
        )

    # Format the conversation prompt with summary
    prompt = format_conversation(conversation, schedules_summary=schedules_summary)
    
    # Tokenize and move input to the correct device
    input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to(device)

    # Generate output using the model's generate method
    generated_ids = model.generate(
        input_ids=input_ids,
        max_new_tokens=max_new_tokens,  # Use max_new_tokens instead of max_length
        temperature=temperature,
        top_p=top_p,
        top_k=top_k,
        do_sample=True,
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id,
    )
    
    # Decode and clean the generated output
    generated_text = tokenizer.decode(generated_ids[0], skip_special_tokens=False)
    
    # Extract the assistant's reply between <start_of_turn>assistant and <end_of_turn>
    start_token = "<start_of_turn>assistant\n"
    end_token = "<end_of_turn>"
    start_index = generated_text.find(start_token)
    if start_index != -1:
        start_index += len(start_token)
        end_index = generated_text.find(end_token, start_index)
        if end_index != -1:
            assistant_reply = generated_text[start_index:end_index].strip()
        else:
            assistant_reply = generated_text[start_index:].strip()
    else:
        assistant_reply = generated_text.strip()
    
    return assistant_reply

# Initialize conversation history
conversation_history = []

# Gradio Chat Interface
def respond(user_input, chat_history):
    # Append the user's input to the conversation history
    conversation_history.append({'role': 'user', 'content': user_input})
    
    # Generate the assistant's response
    assistant_response = generate_text(model, tokenizer, conversation_history, device)
    
    # Append the assistant's response to conversation and chat history
    conversation_history.append({'role': 'assistant', 'content': assistant_response})
    chat_history.append((user_input, assistant_response))
    
    return "", chat_history

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
