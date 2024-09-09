from transformers import T5Tokenizer, T5ForConditionalGeneration

tokenizer = T5Tokenizer.from_pretrained('itsmohitrohilla/Astro-GPT')
model = T5ForConditionalGeneration.from_pretrained('itsmohitrohilla/Astro-GPT')

def astro_gpt_llm(pre_prompt, query):
    # Combine pre-prompt and user query into a coherent input string
    combined_input = f"{pre_prompt}\n\nQuestion: {query}"
    
    # Tokenize the input text with padding and truncation
    inputs = tokenizer(combined_input, return_tensors='pt', padding=True, truncation=True)
    
    # Generate response using beam search for better quality output
    output_sequences = model.generate(
        input_ids=inputs['input_ids'],
        attention_mask=inputs['attention_mask'],
        max_length=150,   # Increased length for more detailed responses
        num_beams=5,      # Increased number of beams for better generation quality
        early_stopping=True,
        temperature=0.7,  # Lower temperature for more focused and less random responses
        top_p=0.9,        # Nucleus sampling to balance between diversity and quality
        no_repeat_ngram_size=2  # Prevent repetition of n-grams for cleaner output
    )
    
    # Decode the generated output sequence
    generated_text = tokenizer.decode(output_sequences[0], skip_special_tokens=True).strip()
    
    # Create a well-formatted response
    response = f"As per Astro-GPT:{generated_text}"
    
    return response

