import speech_recognition as sr
import pygame
import os
import json
from google.cloud import texttospeech
from rag_pipeline import RAGPipeline
import uuid
import re

# ✅ Set up Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:\\Users\\hp\\OneDrive\\Desktop\\genLango\\backend\\rag\\gcloud-key.json"

# 🔁 Set up pygame for audio playback
pygame.init()

# 🎤 Setup recognizer
recognizer = sr.Recognizer()

# 🧠 Load your AI pipeline (Ollama-backed)
rag = RAGPipeline(lesson_number=1)

# 🔊 Google Text-to-Speech speaking function
def speak(text):
    print(f"\U0001F9E0 AI: {text}")

    # Setup the Text-to-Speech client
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="hi-IN",
        name="hi-IN-Wavenet-C",
        ssml_gender=texttospeech.SsmlVoiceGender.FEMALE
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Synthesize speech and save to file
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    filename = f"output_{uuid.uuid4().hex}.mp3"
    with open(filename, "wb") as out:
        out.write(response.audio_content)

    pygame.mixer.init()
    pygame.mixer.music.load(filename)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.quit()
    os.remove(filename)

# 🎙️ Listen function to capture speech and process it
def listen():
    with sr.Microphone() as source:
        print("🎙️ Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            # First, try recognizing as English
            text_en = recognizer.recognize_google(audio, language="en-IN")
            print(f"👤 You (EN): {text_en}")
            return text_en, "english"
        except sr.UnknownValueError:
            pass

        try:
            # If English fails, try recognizing as Hindi
            text_hi = recognizer.recognize_google(audio, language="hi-IN")
            print(f"👤 You (HI): {text_hi}")
            return text_hi, "hindi"
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand. Could you please repeat?")
        except sr.RequestError:
            speak("Server se connect nahi ho pa raha hai. (Unable to connect to the server.)")

    return "", "unknown"


# 📚 Introduce Lesson Function
def lesson_intro(lesson_num, lesson_data):
    phrases = lesson_data.get("phrases", [])
    if not phrases:
        return "There are no phrases found for this lesson."
    english_words = [phrase["english"] for phrase in phrases]
    lesson_words = ", ".join(english_words)
    return (
        f"Welcome to Lesson {lesson_num}! Today we will revise what you learned: {lesson_words}. "
        f"Can you tell me one word or phrase you remember?"
    )

def handle_user_response(user_input, lesson_data, language):
    user_input_lower = user_input.lower()

    if language == "english":
        # User asked something in English, treat as a question
        if "good morning" in user_input_lower:
            return "In Hindi, we say 'सुप्रभात' (Suprabhat) for Good Morning!"
        elif "hello" in user_input_lower:
            return "In Hindi, we say 'नमस्ते' (Namaste) for Hello!"
        elif "good night" in user_input_lower:
            return "In Hindi, we say 'शुभ रात्रि' (Shubh Raatri) for Good Night!"
        elif "how are you" in user_input_lower:
            return "In Hindi, we say 'कैसे हो?' (Kaise ho?) for How are you?"
        elif "nice to meet you" in user_input_lower:
            return "In Hindi, we say 'आपसे मिलकर खुशी हुई' (Aapse milkar khushi hui) for Nice to meet you!"
        else:
            return rag.chat(user_input)
    elif language == "hindi":
        # User is speaking Hindi
        for phrase in lesson_data.get("phrases", []):
            if phrase["hindi"] in user_input_lower:
                return f"Yes! '{phrase['english']}' means '{phrase['hindi']}' in Hindi. Great job!"
        return rag.chat(user_input)
    else:
        return "I'm sorry, I couldn't understand the language you spoke."


# 🚀 Main conversation loop
if __name__ == "__main__":
    lesson_number = 1
    base_dir = os.path.dirname(__file__)
    lessons_path = os.path.join(base_dir, "lessons.json")

    with open(lessons_path, "r", encoding="utf-8") as f:
        lessons = json.load(f)
        current_lesson_data = next((lesson for lesson in lessons if lesson["lesson_number"] == lesson_number), None)

    if current_lesson_data:
        intro_text = lesson_intro(lesson_number, current_lesson_data)
        speak(intro_text)
    else:
        speak("Sorry, I couldn't find your lesson data.")

    while True:
        user_input, language = listen()
        if user_input:
            response = handle_user_response(user_input, current_lesson_data, language)
            speak(response)
