# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("HuggingFaceH4/starchat-beta")
model = AutoModelForCausalLM.from_pretrained("HuggingFaceH4/starchat-beta")
    
def generate_response(prompt):
    encoded_input = tokenizer.encode(prompt, return_tensors='pt')
    output = model.generate(encoded_input, max_length=50, do_sample=True)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response

# Example usage
prompt = "Hello, how are you?"
response = generate_response(prompt)
print("Generated response:", response)

