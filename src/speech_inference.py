import whisper

class SpeechToText:
    def __init__(self, file_path):
        self.file_path = file_path

    def transcribe_audio(self, model):
        print(self.file_path)
        transcript = model.transcribe(self.file_path)
        return transcript["text"]