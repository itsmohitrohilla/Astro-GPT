from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import GPT2LMHeadModel, GPT2Tokenizer

app = FastAPI()

# Load pre-trained model and tokenizer for DistilGPT-2
model_name = 'distilgpt2'  # DistilGPT-2 model
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)

class Query(BaseModel):
    text: str

@app.post("/generate/")
async def generate_response(query: Query):
    try:
        # Tokenize the input text
        inputs = tokenizer.encode(query.text, return_tensors='pt')

        # Generate text from the model
        outputs = model.generate(inputs, max_length=100, num_return_sequences=1, no_repeat_ngram_size=2)
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return {"generated_text": generated_text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
