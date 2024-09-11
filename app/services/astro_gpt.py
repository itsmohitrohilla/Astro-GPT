from transformers import T5Tokenizer, T5ForConditionalGeneration

tokenizer = T5Tokenizer.from_pretrained('itsmohitrohilla/Astro-GPT')
model = T5ForConditionalGeneration.from_pretrained('itsmohitrohilla/Astro-GPT')

def astro_gpt_llm(pre_prompt, query):
    
    combined_input = f"{pre_prompt}\n\nQuestion: {query}"
    
    # input
    inputs = tokenizer(combined_input, return_tensors='pt', padding=True, truncation=True)
    
    #output
    output_sequences = model.generate(
        input_ids=inputs['input_ids'],
        attention_mask=inputs['attention_mask'],
        max_length=150,   
        num_beams=5,      
        early_stopping=True,
        temperature=0.7,  
        top_p=0.9,        
        no_repeat_ngram_size=2  
    )
    
    
    generated_text = tokenizer.decode(output_sequences[0], skip_special_tokens=True).strip()
    
   
    response = f"As per Astro-GPT:{generated_text}"
    
    return response

