import speech_recognition as sr
import threading

class VoiceCommandListener:
    def __init__(self, controller):
        self.controller = controller
        self.recognizer = sr.Recognizer()
        try:
            self.microphone = sr.Microphone()
        except OSError:
            self.microphone = None
        self.running = False
        self._build_name_map()

    def _build_name_map(self):
        self.name_map = {}
        for strat in self.controller.get_stratagems().values():
            self.name_map[strat.name.lower()] = strat

    def start(self):
        if self.microphone is None:
            return
        self.running = True
        thread = threading.Thread(target=self._listen_loop, daemon=True)
        thread.start()

    def stop(self):
        self.running = False

    def _listen_loop(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while self.running:
                try:
                    audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=2)
                    command = self.recognizer.recognize_google(audio).lower()
                    self._handle_command(command)
                except sr.WaitTimeoutError:
                    continue
                except sr.UnknownValueError:
                    continue
                except sr.RequestError:
                    continue

    def _handle_command(self, command: str):
        command = command.strip().lower()
        if command in self.name_map:
            self.controller.trigger_macro(self.name_map[command])
