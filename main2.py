import speech_recognition as sr
import pyttsx3
import time
import os
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from huggingface_hub import InferenceClient
from transformers import pipeline as hf_pipeline

# Load environment variables
if not os.path.exists('.env'):
    print("Error: .env file not found. Please create one with HUGGINGFACEHUB_API_TOKEN.")
    exit(1)
load_dotenv()
huggingface_api_token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
if not huggingface_api_token:
    print("Error: HUGGINGFACEHUB_API_TOKEN not set in .env file.")
    exit(1)

# Initialize TTS Engine
try:
    tts_engine = pyttsx3.init()
    voices = tts_engine.getProperty('voices')
    if voices:
        tts_engine.setProperty('voice', voices[0].id)
        tts_engine.setProperty('rate', 160)
except Exception as e:
    print(f"Error initializing TTS engine: {e}")
    exit(1)

def speak(text):
    """Converts text to speech."""
    print(f"Bot: {text}")
    tts_engine.say(text)
    tts_engine.runAndWait()

def listen_for_speech(timeout=10, phrase_time_limit=10):
    """Listens for user speech and converts it to text."""
    recognizer = sr.Recognizer()
    try:
        microphone = sr.Microphone()
    except Exception as e:
        print(f"Error initializing microphone: {e}")
        speak("I couldn't access the microphone. Please check your audio setup.")
        return None

    with microphone as source:
        print("\nAdjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
        except sr.WaitTimeoutError:
            print("No speech detected within timeout.")
            return None
        except Exception as e:
            print(f"Error during listening: {e}")
            return None

    try:
        print("Recognizing...")
        text = recognizer.recognize_google(audio)
        print(f"You: {text}")
        return text.lower()
    except sr.UnknownValueError:
        speak("Sorry, I could not understand what you said.")
        return None
    except sr.RequestError as e:
        print(f"Google Speech Recognition error: {e}")
        if "connection" in str(e).lower():
            speak("I couldn't connect to the speech recognition service. Please check your internet.")
        else:
            speak(f"Speech recognition service error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error during speech recognition: {e}")
        return None

# Initialize Emotion Detection
try:
    print("Loading emotion detection model...")
    emotion_classifier = hf_pipeline(
        "text-classification",
        model="j-hartmann/emotion-english-distilroberta-base",
        return_all_scores=False,
        device=-1
    )
    print("Emotion detection model loaded.")
except Exception as e:
    print(f"Error loading emotion model: {e}")
    emotion_classifier = None
    speak("Emotion detection is unavailable. Using neutral emotion.")

def detect_emotion(text):
    """Detects emotion from text using a Hugging Face model."""
    if not emotion_classifier or not text:
        return "neutral"
    try:
        result = emotion_classifier(text)
        return result[0]['label'].lower() if result else "neutral"
    except Exception as e:
        print(f"Emotion detection error: {e}")
        return "neutral"

# Initialize Hugging Face Inference API for Mistral
inference_client = None
prompt_template = None

def initialize_inference_client():
    """Initializes the Hugging Face Inference API client with Mistral model."""
    global inference_client, prompt_template
    print("Initializing Hugging Face Inference API client...")
    try:
        repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
        inference_client = InferenceClient(model=repo_id, token=huggingface_api_token)
        # System prompt for conversational task
        template = """You are a conversational AI assistant. Your goal is to respond empathetically and appropriately based on the user's emotion. Consider these guidelines:
- If the user is sad, be comforting.
- If the user is happy, share enthusiasm.
- If the user is angry, be understanding or calming.
- If the user is surprised, react with appropriate curiosity or acknowledgement.
- If the user is fearful, be reassuring.
- If the user is disgusted, acknowledge it without being repulsed yourself.
- For a neutral emotion, have a normal conversation and answer questions directly.

User's current emotion: {emotion}
User's statement: {user_input}"""
        prompt_template = PromptTemplate(template=template, input_variables=["emotion", "user_input"])
        print(f"Hugging Face Inference API client initialized for {repo_id}")
        return True
    except Exception as e:
        print(f"Error initializing Inference API client: {e}")
        speak("I couldn't connect to the language model. Please check the console.")
        return False

def get_chatbot_response_with_emotion(user_text, emotion):
    """Generates a response using the Mistral model’s conversational task."""
    global inference_client, prompt_template
    if not inference_client or not prompt_template:
        return "My language model is not ready due to an API issue."
    try:
        formatted_prompt = prompt_template.format(emotion=emotion, user_input=user_text)
        # Use conversational task with message structure
        messages = [
            {"role": "system", "content": "You are an empathetic conversational AI assistant. Follow the guidelines provided in the user prompt."},
            {"role": "user", "content": formatted_prompt}
        ]
        response = inference_client.chat_completion(
            messages=messages,
            max_tokens=500,
            temperature=0.7,
            top_p=0.9,
        )
        # Extract the generated text from the conversational response
        bot_response = response.choices[0].message.content.strip()
        return bot_response if bot_response else "I'm not sure how to respond to that."
    except Exception as e:
        print(f"API error: {e}")
        if "503" in str(e) or "overloaded" in str(e).lower():
            return "The language model is busy. Please try again soon."
        elif "401" in str(e) or "unauthorized" in str(e).lower():
            return "Authentication failed. Please check your API token."
        elif "not supported" in str(e).lower():
            return "The model does not support this task. Please check the console for details."
        return "An error occurred while generating a response. Please try again."

def main_conversation_loop():
    """Main loop for the emotionally aware speech assistant."""
    if not initialize_inference_client():
        return
    speak("Hello! I am your emotionally aware speech assistant, powered by Mistral AI. How can I help you today?")
    while True:
        user_input_text = listen_for_speech()
        if not user_input_text:
            speak("I didn't hear anything. Please try speaking again.")
            continue
        if "goodbye" in user_input_text or "bye" in user_input_text or "exit" in user_input_text:
            speak("Goodbye! It was nice talking to you.")
            break
        detected_emotion = detect_emotion(user_input_text)
        print(f"Detected emotion: {detected_emotion}")
        time.sleep(0.5)
        bot_response = get_chatbot_response_with_emotion(user_input_text, detected_emotion)
        if bot_response and "error" not in bot_response.lower():
            speak(bot_response)
        elif bot_response:
            speak(bot_response)
        else:
            speak("I couldn't generate a response. Please try again.")
        time.sleep(0.1)

if __name__ == "__main__":
    try:
        main_conversation_loop()
    except KeyboardInterrupt:
        print("\nExiting chatbot...")
    finally:
        if 'tts_engine' in globals() and tts_engine:
            try:
                tts_engine.stop()
            except Exception as e:
                print(f"Error stopping TTS engine: {e}")
        print("Chatbot shutdown complete.")