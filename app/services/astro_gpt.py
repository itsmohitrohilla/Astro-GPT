from app.config.celery_config import celery_app
from transformers import T5Tokenizer, T5ForConditionalGeneration
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

tokenizer = T5Tokenizer.from_pretrained('itsmohitrohilla/Astro-GPT')
model = T5ForConditionalGeneration.from_pretrained('itsmohitrohilla/Astro-GPT')

# Celery task
@celery_app.task
def astro_gpt_llm_task(pre_prompt, query):
    try:
        combined_input = f"""
        You are a highly knowledgeable and accurate assistant specialized in astrology. 
        Please use your expertise to provide the most accurate and insightful answer to the following query. 
        Base your answer on astrology principles and consider relevant planetary movements or astrological signs.

        Context: {pre_prompt}
        Question: {query}
        
        Provide a detailed and clear response.
        """
        
        inputs = tokenizer(combined_input, return_tensors='pt', padding=True, truncation=True)
        
        # Generate response 
        output_sequences = model.generate(
            input_ids=inputs['input_ids'],
            attention_mask=inputs['attention_mask'],
            max_length=200,   
            num_beams=7,     
            early_stopping=True,
            temperature=0.6,  
            top_p=0.85,       
            no_repeat_ngram_size=2  
        )
        
        # Decode
        generated_text = tokenizer.decode(output_sequences[0], skip_special_tokens=True).strip()
        response = f"As per the Astro-GPT: {generated_text}"
        
        return response

    except Exception as e:
        logger.error(f"Error in astro_gpt_llm_task: {str(e)}")
        
        return {"error": "An error occurred while processing the request. Please try again later."}



#celery -A app.config.celery_config.celery_app worker --loglevel=info
