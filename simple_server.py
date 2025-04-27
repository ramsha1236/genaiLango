from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    lesson_id: int = 1

class ChatResponse(BaseModel):
    text: str
    audio_url: str = ""
    feedback: dict = {}

@app.get("/")
def read_root():
    return {"message": "Jen Lango Backend is running!"}

@app.post("/chat")
def chat(request: ChatRequest):
    message = request.message
    
    # Simple Hindi responses
    if message == "आप कैसे हो":
        response = "मैं बहुत अच्छा हूँ, धन्यवाद! आप कैसे हैं?"
        feedback = {
            "proficiency": "Intermediate",
            "pronunciation": "Good",
            "cultural_context": "This is a common greeting in Hindi"
        }
    else:
        response = f"You said: {message}"
        feedback = {
            "proficiency": "Beginner",
            "pronunciation": "Needs practice",
            "cultural_context": "Try using more Hindi phrases"
        }
    
    return ChatResponse(
        text=response,
        audio_url="",
        feedback=feedback
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
