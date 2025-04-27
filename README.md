# Jen Lango

Jen Lango is an AI-powered language learning application that helps users learn Hindi through interactive lessons and conversational practice.

## Features

- **User Authentication**: Simple login system with Google authentication option
- **Multiple Languages**: UI prepared for Hindi, Arabic, French, and German (currently only Hindi is functional)
- **Learning Module**: 5 progressive lessons teaching basic Hindi phrases
- **Speaking Module**: AI-powered conversation practice with pronunciation feedback
- **Voice Recognition**: Practice pronunciation with real-time feedback
- **RAG Technology**: Retrieval-augmented generation for accurate language learning

## Tech Stack

### Frontend
- React with Vite
- React Router for navigation
- Tailwind CSS for styling
- Minimalist design with pink color theme

### Backend
- FastAPI for the API server
- RAG (Retrieval Augmented Generation) pipeline
- FAISS for vector search
- Sentence Transformers for embeddings
- Ollama for LLM integration

## Project Structure

```
jen-lango/
├── frontend/              # React frontend
│   ├── src/
│   │   ├── pages/         # Page components
│   │   ├── components/    # Reusable components
│   │   ├── services/      # API services
│   │   └── assets/        # Images and other assets
│   └── ...
├── backend/               # FastAPI backend
│   ├── app.py             # Main API server
│   ├── rag_pipeline.py    # RAG implementation
│   ├── retriever.py       # Vector search implementation
│   ├── voice_chat.py      # Voice chat implementation
│   └── lessons.json       # Lesson data
└── README.md              # This file
```

## Getting Started

### Prerequisites

- Node.js (v14+)
- Python (v3.8+)
- Ollama (for LLM)

### Installation

1. Clone the repository:
```
git clone <repository-url>
cd jen-lango
```

2. Install frontend dependencies:
```
cd frontend
npm install
```

3. Install backend dependencies:
```
cd ../backend
pip install fastapi uvicorn sentence-transformers faiss-cpu pydantic python-multipart
```

4. Install Ollama (if not already installed):
```
# Follow instructions at https://ollama.ai/
```

5. Pull the Llama3 model:
```
ollama pull llama3
```

### Running the Application

1. Start the backend server:
```
cd backend
python app.py
```

2. Start the frontend development server:
```
cd frontend
npm run dev
```

3. Open your browser and navigate to:
```
http://localhost:5173
```

## Usage

1. **Login**: Use any email/password combination for demo purposes, or click the Google button
2. **Select Language**: Choose Hindi from the language selection screen
3. **Learning Module**: Progress through the 5 lessons to learn basic Hindi phrases
4. **Speaking Module**: Practice your Hindi skills with the AI conversation partner

## Notes

- This is a demo version with only Hindi language support
- The backend uses local LLM (Llama3) through Ollama for AI responses
- User progress is stored in localStorage for demo purposes
