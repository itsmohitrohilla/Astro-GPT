from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load the tokenizer from Google FLAN-T5 base model
tokenizer = T5Tokenizer.from_pretrained('itsmohitrohilla/Astro-GPT')

# Load your fine-tuned model
model = T5ForConditionalGeneration.from_pretrained('itsmohitrohilla/Astro-GPT')

# Define a function to generate a response
def generate_response(input_text, question):
    # Combine input text with the question
    combined_input = f"{input_text} Question: {question}"
    
    # Tokenize the combined input
    inputs = tokenizer(combined_input, return_tensors='pt', padding=True, truncation=True)

    # Generate the output
    output_sequences = model.generate(
        input_ids=inputs['input_ids'],
        attention_mask=inputs['attention_mask'],
        max_length=128,  # Adjust max_length as needed
        num_beams=4,     # You can adjust beam search parameters
        early_stopping=True
    )

    # Decode the output
    generated_text = tokenizer.decode(output_sequences[0], skip_special_tokens=True)
    return generated_text

# Input text
input_text = "Venus is at 165.2 in Aquarius and is direct, Mars is at 300.2 in Cancer and is retrograde, Jupiter is at 195.2 in Leo and is direct, Saturn is at 45.6 in Pisces and is direct, Neptune is at 120.4 in Scorpio and is retrograde"

# Ask for user input
question = "What should I focus on to create more harmony in my relationship?"

# Generate and print the response
response = generate_response(input_text, question)
print("Generated Response:", response)
