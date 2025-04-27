from retriever import LessonRetriever
import subprocess
import json

class RAGPipeline:
    def __init__(self, lesson_number: int):
        self.retriever = LessonRetriever(lesson_number)

    def generate_prompt(self, user_input: str):
        retrieved = self.retriever.query(user_input)[0]
        english = retrieved["english"]
        hindi = retrieved["hindi"]

        prompt = f"""""You are a friendly Hindi teacher for English-speaking beginners. "
    "Only use Hindi for the greetings and learned phrases. Explain everything in English. "
    "If a user says something like 'I learned नमस्ते today', praise them and maybe repeat the word together. "
    "Don’t over-correct unless the sentence is completely wrong — this is a beginner, be supportive!"
    "do not read the hindi transliteration in the bracket, just saying the word in hindi once is enough"
    "make it conversational, encourage the user to continue with the lesson."
They are currently in Lesson {self.retriever.lesson_number}, which covers phrases like:
English: "{english}" — Hindi: "{hindi}"

They just said: "{user_input}"

"""

        return prompt

    def ask_llama(self, prompt: str):
        result = subprocess.run(
            ["ollama", "run", "llama3", prompt],
            capture_output=True,
            text=True,
            encoding="utf-8",  
            errors="replace"   
        )
        return result.stdout.strip() if result.stdout else "⚠️ LLaMA didn't respond. Check ollama status."


    def chat(self, user_input: str):
        prompt = self.generate_prompt(user_input)
        response = self.ask_llama(prompt)
        return response


if __name__ == "__main__":
    rag = RAGPipeline(lesson_number=1)
    while True:
        user_input = input("You: ")
        print("AI:", rag.chat(user_input))
