from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import pipeline

# Initialize FastAPI app
app = FastAPI()

# Load the GPT-J model pipeline for text generation
model_name = "EleutherAI/gpt-j-6B"
text_generator = pipeline("text-generation", model=model_name)

# Define request body schema
class TextRequest(BaseModel):
    text: str
    max_length: int = 50  # Default max_length for text generation
    pre_prompt: str = "Act like you are a tour guide"  # Optional pre-prompt to guide the model

# Define a route to generate text
@app.post("/generate-text")
async def generate_text(request: TextRequest):
    try:
        # Combine pre-prompt with the user input text
        full_prompt = f"{request.pre_prompt}\n\n{request.text}" if request.pre_prompt else request.text
        
        # Generate text using the GPT-J model pipeline
        results = text_generator(full_prompt, max_length=request.max_length)
        return {"generated_text": results[0]['generated_text']}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the application with `uvicorn` when the script is executed
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
