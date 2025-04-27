import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List
from pathlib import Path
import json

# 🔍 Get the path to lessons.json relative to this file
lessons_path = Path(__file__).parent / "lessons.json"

# Load the file
with open(lessons_path, "r", encoding="utf-8") as f:
    lessons = json.load(f)

# Load model once
model = SentenceTransformer("all-MiniLM-L6-v2")

class LessonRetriever:
    def __init__(self, lesson_number: int, json_path=lessons_path):
        self.lesson_number = lesson_number
        self.json_path = json_path
        self.phrases = []
        self.hindi_map = {}
        self.embeddings = None
        self.index = None
        self._load_lesson_data()
        self._build_index()

    def _load_lesson_data(self):
        with open(self.json_path, "r", encoding="utf-8") as f:
            all_lessons = json.load(f)

        lesson_data = next(
            (lesson for lesson in all_lessons if lesson["lesson_number"] == self.lesson_number),
            None
        )
        if not lesson_data:
            raise ValueError(f"Lesson {self.lesson_number} not found")

        self.phrases = [item["english"] for item in lesson_data["phrases"]]
        self.hindi_map = {item["english"]: item["hindi"] for item in lesson_data["phrases"]}

    def _build_index(self):
        self.embeddings = model.encode(self.phrases)
        dim = self.embeddings[0].shape[0]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(np.array(self.embeddings))

    def query(self, user_input: str, top_k=1):
        user_embedding = model.encode([user_input])
        D, I = self.index.search(np.array(user_embedding), top_k)
        results = []
        for i in I[0]:
            english_phrase = self.phrases[i]
            hindi_phrase = self.hindi_map[english_phrase]
            results.append({"english": english_phrase, "hindi": hindi_phrase})
        return results


# 🧪 Example usage
if __name__ == "__main__":
    lesson = LessonRetriever(lesson_number=1)
    while True:
        query = input("You: ")
        result = lesson.query(query)
        print("Closest Match:", result[0])
