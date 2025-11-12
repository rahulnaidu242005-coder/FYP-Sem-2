# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

model_dir = "./Foundation-Sec-8B-Instruct"
tokenizer = AutoTokenizer.from_pretrained(model_dir)
quantization_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype="float16")
model = AutoModelForCausalLM.from_pretrained(
    model_dir,
    device_map="auto",
    quantization_config=quantization_config,
    offload_folder="offload"
)
messages = [
    {"role": "user", "content": "How to do triage for L1 SOC Analyst? Explain the full process."},
]
inputs = tokenizer.apply_chat_template(
	messages,
	add_generation_prompt=True,
	tokenize=True,
	return_dict=True,
	return_tensors="pt",
).to(model.device)

outputs = model.generate(**inputs, max_new_tokens=4000)
generated_text = tokenizer.decode(
    outputs[0][inputs["input_ids"].shape[-1]:], skip_special_tokens=True
)
print(generated_text)
