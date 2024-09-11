from transformers import T5Tokenizer, T5ForConditionalGeneration

tokenizer = T5Tokenizer.from_pretrained('itsmohitrohilla/Astro-GPT')
model = T5ForConditionalGeneration.from_pretrained('itsmohitrohilla/Astro-GPT')


def generate_response(input_text, question):

    combined_input = f"{input_text} Question: {question}"
    inputs = tokenizer(combined_input, return_tensors='pt', padding=True, truncation=True)

    output_sequences = model.generate(
        input_ids=inputs['input_ids'],
        attention_mask=inputs['attention_mask'],
        max_length=128,  
        num_beams=4,     
        early_stopping=True
    )

    # output
    generated_text = tokenizer.decode(output_sequences[0], skip_special_tokens=True)
    return generated_text


input_text = "Venus is at 165.2 in Aquarius and is direct, Mars is at 300.2 in Cancer and is retrograde, Jupiter is at 195.2 in Leo and is direct, Saturn is at 45.6 in Pisces and is direct, Neptune is at 120.4 in Scorpio and is retrograde"
question = "What should I focus on to create more harmony in my relationship?"


response = generate_response(input_text, question)
print("Generated Response:", response)
