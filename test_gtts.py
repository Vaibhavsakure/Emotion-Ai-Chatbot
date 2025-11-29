from gtts import gTTS

tts = gTTS("Hello! This is a free TTS voice.", lang="en")
tts.save("voice.mp3")

print("Voice file generated: voice.mp3")
