import os
import sys
import subprocess
import threading
import logging

class AudioService:
    """Cross-platform audio cue player for host machine."""
    def __init__(self, project_root: str):
        self.project_root = project_root
        self.sound_dir = os.path.join(project_root, "res", "sound")
        self.sound_map = {
            "good_answer": "family-feud-good-answer.mp3",
            "strike": "strike.mp3",
            "win": "win-answer.mp3",
            "win_sound": "winSound.mp3",
            "face_off": "face-off.mp3",
            "intro": "family-feud-returning-from-commercial.mp3",
            "outro": "winSound.mp3",
            "fm_count": "FMSound1.mp3",
            "fm_correct": "FMCorrect.mp3",
            "fm_no_points": "FMNoPoints.mp3",
            "theme": "family-feud-theme.mp3",
            "buzzer": "family-feud-buzzer-sound-effect-2.mp3",
        }

    def play(self, cue_name: str):
        """Plays the mapped audio file asynchronously in a separate thread."""
        filename = self.sound_map.get(cue_name)
        if not filename:
            logging.warning(f"Unknown audio cue: {cue_name}")
            return
        
        sound_path = os.path.join(self.sound_dir, filename)
        if not os.path.exists(sound_path):
            logging.warning(f"Sound file not found: {sound_path}")
            return

        thread = threading.Thread(target=self._play_file, args=(sound_path,), daemon=True)
        thread.start()

    def _play_file(self, filepath: str):
        try:
            if sys.platform == "darwin":
                # macOS native audio player
                subprocess.run(["afplay", filepath], check=False)
            elif sys.platform == "win32":
                # Windows PowerShell audio playback
                cmd = f"(New-Object Media.SoundPlayer '{filepath}').PlaySync()"
                subprocess.run(["powershell", "-c", cmd], check=False)
            else:
                # Linux fallback
                subprocess.run(["aplay", filepath], check=False)
        except Exception as e:
            logging.error(f"Error playing sound {filepath}: {e}")
