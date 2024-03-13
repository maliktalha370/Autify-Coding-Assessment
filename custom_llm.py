# Import necessary libraries
from transformers import AutoTokenizer, AutoModelForCausalLM

# Load Code Llama model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("codellama/CodeLlama-7b-Python-hf")
model = AutoModelForCausalLM.from_pretrained("codellama/CodeLlama-7b-Python-hf")

def generate_code_snippet(prompt):
  """Generates a code snippet based on the given prompt using Code Llama."""
  generate_code_prompt = f"""
      The following is an agent that only outputs python code to a user question.
      The agent answers non-coding questions with an error message.

      Customer: How do I implement a bubble sort algorithm?
      Agent: def bubble_sort(arr):
                 n = len(arr)
                 for i in range(n-1):
                     for j in range(0, n-i-1):
                         if arr[j] > arr[j+1]:
                             arr[j], arr[j+1] = arr[j+1], arr[j]
                 return arr

      Customer: Explain the concept of object-oriented programming.
      Agent: Invalid request. Please provide a programming-related question.

      Customer: Write a function in Python to calculate the factorial of a number.
      Agent: def factorial(n):
                 if n == 0:
                     return 1
                 else:
                     return n * factorial(n-1)

      Customer: Provide code to find the sum of all even numbers in a list.
      Agent: def sum_of_even(lst):
                 return sum(num for num in lst if num % 2 == 0)

      Customer: Write a program to find the largest element in an array.
      Agent: def find_largest(arr):
                 return max(arr)

      Customer: Write me python code to my question: "{prompt}". Return an error message if my question is not programming related.
      Agent:
  """

  # Tokenize the prompt
  inputs = tokenizer(generate_code_prompt, return_tensors="pt")  # Or "tf" for TensorFlow

  # Generate code with the model
  outputs = model.generate(**inputs)

  # Decode the generated text
  response = tokenizer.decode(outputs[0], skip_special_tokens=True)

  return response

# Example usage
if __name__ == "__main__":
  prompt = "Write a Python function to add two numbers"
  print(generate_code_snippet(prompt))
