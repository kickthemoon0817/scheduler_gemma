import torch
import time
import random
import numpy as np
from sklearn.model_selection import train_test_split
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    TrainingArguments,
    BitsAndBytesConfig,
    TrainerCallback,
    EarlyStoppingCallback,
    DataCollatorWithPadding,
)
from torch.utils.data import Dataset, DataLoader, Subset
import bitsandbytes as bnb
from peft import LoraConfig, PeftModel
from trl import SFTTrainer

# Set seed for reproducibility
seed = 42
random.seed(seed)
np.random.seed(seed)
torch.manual_seed(seed)

# Step 1: Define device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"We are using: {device}")

# Step 2: Load the Tokenizer
tokenizer_path = './model'  # Adjust this path to where your local tokenizer files are located
tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
print("Tokenizer Loaded")

# Step 3: Set up 4-bit quantization configuration
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_compute_dtype=torch.float16,  # Use float16 for computations
    bnb_4bit_use_double_quant=True,  # Enable double quantization for better precision
    bnb_4bit_quant_type="nf4"  # NormalFloat4 quantization type
)

# Step 4: Load the Model with 4-bit Quantization
model_path = './model'  # Adjust this path to where your model files are located
model = AutoModelForCausalLM.from_pretrained(
    model_path, 
    device_map="auto",  # Automatically map model to available devices
    quantization_config=quantization_config
)
print("4-bit quantized Gemma Model Loaded")

# Step 5: Prepare the Dataset for Fine-Tuning
class SchedulingDataset(Dataset):
    def __init__(self, file_path, tokenizer, block_size=512):
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.read().split('<eos>')

        self.examples = []
        for line in lines:
            if line.strip():
                encoded = tokenizer(
                    line.strip(),
                    truncation=True,
                    padding='max_length',
                    max_length=block_size,
                    return_tensors="pt"
                )
                # Mask padding tokens in labels by setting them to -100
                encoded['labels'] = encoded['input_ids'].clone()
                encoded['labels'][encoded['input_ids'] == tokenizer.pad_token_id] = -100
                self.examples.append(encoded)

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, idx):
        item = self.examples[idx]
        return {
            'input_ids': item['input_ids'].squeeze(),
            'attention_mask': item['attention_mask'].squeeze(),
            'labels': item['labels'].squeeze()
        }

dataset_path = './data/formatted_korean_scheduling_data.txt'  # Update the dataset path
full_dataset = SchedulingDataset(file_path=dataset_path, tokenizer=tokenizer)
print("Dataset Loaded and Tokenized")

# Step 6: Split Dataset into Training and Validation
train_indices, val_indices = train_test_split(list(range(len(full_dataset))), test_size=0.2, random_state=seed)
train_dataset = Subset(full_dataset, train_indices)
val_dataset = Subset(full_dataset, val_indices)

# Step 7: Create Data Collator and DataLoader
data_collator = DataCollatorWithPadding(tokenizer=tokenizer, padding=True)

# Step 8: LoRA Configuration for Fine-Tuning
lora_config = LoraConfig(
    r=6,
    lora_alpha=8,
    lora_dropout=0.05,
    target_modules=["q_proj", "o_proj", "k_proj", "v_proj", "gate_proj", "up_proj", "down_proj"],
    task_type="CAUSAL_LM",
)

# Step 9: Define the Trainer with Early Stopping Callback
class TimeLimitCallback(TrainerCallback):
    def __init__(self, max_time_seconds):
        self.max_time_seconds = max_time_seconds
        self.start_time = None

    def on_train_begin(self, args, state, control, **kwargs):
        self.start_time = time.time()

    def on_step_end(self, args, state, control, **kwargs):
        elapsed_time = time.time() - self.start_time
        if elapsed_time >= self.max_time_seconds:
            print(f"Training stopped after reaching time limit: {self.max_time_seconds} seconds")
            control.should_training_stop = True
        return control

time_limit_callback = TimeLimitCallback(max_time_seconds=43200)
early_stopping_callback = EarlyStoppingCallback(
    early_stopping_patience=5  # Stop training if no improvement for 5 evaluations
)

trainer = SFTTrainer(
    model=model,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    max_seq_length=512,
    args=TrainingArguments(
        output_dir="./finetuned_gemma_4bit",
        max_steps=1000,  # Number of training steps
        per_device_train_batch_size=1,  # Adjust according to your GPU memory
        gradient_accumulation_steps=8,  # Gradient accumulation to handle small batch sizes
        optim="paged_adamw_8bit",  # Optimizer for 4-bit
        warmup_steps=30,
        learning_rate=2e-4,
        fp16=True,  # Mixed precision for faster training
        evaluation_strategy="steps",  # Evaluate the model every `eval_steps`
        eval_steps=50,  # Evaluation frequency (adjust based on dataset size)
        logging_steps=10,
        push_to_hub=False,
        report_to='none',
        save_total_limit=3,  # Limit number of checkpoints to save
        load_best_model_at_end=True,
    ),
    peft_config=lora_config,
    callbacks=[time_limit_callback, early_stopping_callback],
)

# Step 10: Fine-Tuning the Model
trainer.train()

# Step 11: Save the Fine-Tuned Adapter Model
ADAPTER_MODEL = "./finetuned_gemma_4bit/lora_adapter"
trainer.model.save_pretrained(ADAPTER_MODEL)

# Load the model and merge LoRA adapters
model = AutoModelForCausalLM.from_pretrained(model_path, device_map="auto", torch_dtype=torch.float16)
model = PeftModel.from_pretrained(model, ADAPTER_MODEL, device_map='auto', torch_dtype=torch.float16)

# Merge LoRA adapter into the model weights and unload adapter
model = model.merge_and_unload()

# Save the final merged model
model.save_pretrained('finetuned_gemma_4bit')

print("Fine-tuning complete and model saved.")
