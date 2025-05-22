# Emotionally Aware Speech Assistant 🤖🗣️

Welcome to the **Emotionally Aware Speech Assistant**, a cutting-edge conversational AI that listens to your voice, detects your emotions, and responds empathetically with spoken responses. Powered by advanced speech recognition, emotion detection, and natural language processing, this assistant tailors its responses to your emotional state, creating a natural and engaging conversation.

# Project Overview 🌟

This project transforms spoken input into meaningful, emotionally intelligent responses. It uses Google Speech Recognition to capture your voice, a Hugging Face model to detect emotions, and the Mistral AI model to generate empathetic replies, delivered via text-to-speech. Whether you're feeling happy, sad, or angry, the assistant responds in a way that resonates with you.

## Key Features

- 🎙️ **Speech-to-Text**: Converts your spoken words to text using Google Speech Recognition.
- 😊 **Emotion Detection**: Identifies emotions (e.g., happy, sad, angry) with the `j-hartmann/emotion-english-distilroberta-base` model.
- 💬 **Empathetic Responses**: Crafts tailored replies using `mistralai/Mixtral-8x7B-Instruct-v0.1`, matching your emotional tone (e.g., comforting for sad, enthusiastic for happy).
- 🔊 **Text-to-Speech**: Delivers responses as audio using `pyttsx3` for a seamless conversational experience.
- 🛡️ **Robust Error Handling**: Gracefully manages microphone issues, API errors, and speech recognition failures.

# Technologies Used 🛠️

- **Python 3.8+**: The backbone of the project.
- **speech_recognition**: For real-time speech-to-text conversion.
- **pyttsx3**: For text-to-speech output.
- **Hugging Face Transformers**: Powers emotion detection.
- **Hugging Face Inference API**: Drives conversational responses.
- **LangChain**: Structures dynamic prompts.
- **python-dotenv**: Secures API key management.

# Getting Started 🚀

Follow these steps to set up and run the project locally.

## Prerequisites

- Python 3.8 or higher
- A working microphone and speakers
- Internet connection (for Google Speech Recognition and Hugging Face API)
- A Hugging Face API token

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/yourusername/emotionally-aware-speech-assistant.git
   cd emotionally-aware-speech-assistant
   ```

2. **Set Up a Virtual Environment**:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

   Sample `requirements.txt`:

   ```
   speechrecognition==3.10.0
   pyttsx3==2.90
   python-dotenv==1.0.0
   huggingface_hub==0.23.0
   transformers==4.41.0
   langchain==0.2.0
   ```

4. **Configure Environment Variables**: Create a `.env` file in the project root:

   ```plaintext
   HUGGINGFACEHUB_API_TOKEN=your_huggingface_api_key
   ```

# Usage 🎮

1. **Run the Assistant**:

   ```bash
   python main2.py
   ```

2. **Interact**:

   - The assistant greets you and waits for your voice input.
   - Speak clearly into your microphone. It adjusts for ambient noise automatically.
   - The system detects your emotion and responds with an empathetic spoken reply.
   - Say "goodbye," "bye," or "exit" to end the session.

3. **Example**:

   - **You (sad)**: "I'm feeling really down today."
   - **Assistant (comforting)**: "I'm so sorry to hear that. Want to talk about what's been going on?"
   - **You (happy)**: "I just aced my exam!"
   - **Assistant (excited)**: "That's awesome! Congrats on nailing it!"

# Project Structure 📂

```plaintext
emotionally-aware-speech-assistant/
├── main2.py                # Core application script
├── requirements.txt        # Project dependencies
├── .env                    # API keys (not tracked)
├── README.md               # This file
└── .gitignore              # Ignores venv, .env, etc.
```

# Troubleshooting 🐛

- **Microphone Issues**: Check that your microphone is connected and not muted.
- **API Errors**: Verify your Hugging Face API token and internet connection.
- **Speech Recognition**: Ensure a stable internet connection for Google Speech Recognition.
- **Model Loading**: Confirm sufficient memory and compatible library versions.

# Contributing 🤝

We welcome contributions! To get involved:

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).

# Open a pull request.

## Acknowledgments 🙌

- speech_recognition for audio input.
- pyttsx3 for text-to-speech.
- Hugging Face for emotion detection and conversational AI.
- LangChain for prompt engineering.
- Google Speech Recognition for reliable transcription.

# Contact 📬

Have questions or feedback? Reach out via rajakash607@gmail.com or open a GitHub issue.

---

⭐ **Enjoyed this project? Give it a star on GitHub!**
