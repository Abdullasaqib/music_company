import random
import uuid
import datetime
from .agent_base import AgentBase
from .wrappers.suno_api import SunoAPI
from .wrappers.riffusion_api import RiffusionAPI
from .wrappers.diff_singer import DiffSingerAPI

class MusicAgent(AgentBase):
    def __init__(self):
        super().__init__("Music Agent")
        self.suno = SunoAPI()
        self.riffusion = RiffusionAPI()
        self.diff_singer = DiffSingerAPI()
        
    def generate_track(self):
        moods = ["Focus", "Sleep", "Workout", "General"]
        selected_mood = random.choice(moods)
        
        # Select Model based on Context
        if selected_mood == "Focus":
            model_used = "Riffusion"
            api_data = self.riffusion.generate_spectrogram(f"Lo-fi beats for {selected_mood}")
        elif selected_mood == "Sleep":
            model_used = "Riffusion"
            api_data = self.riffusion.generate_spectrogram(f"Ambient pads for {selected_mood}")
        else:
            model_used = "Suno v3"
            api_data = self.suno.generate(f"High energy track for {selected_mood}", selected_mood)

        track_id = f"TRACK-{random.randint(1000, 9999)}"
        self.log(f"Generating new {model_used} track for {selected_mood}...")

        # Construct Track Object
        new_track = {
            "id": track_id,
            "title": f"{selected_mood} {api_data.get('style_modifier', 'Ambient')}/" 
                     f"{api_data.get('texture', 'Lo-fi')} session",
            "genre": f"{api_data.get('style_modifier', 'Ambient')}/{api_data.get('texture', 'Lo-fi')}",
            "tempo": random.randint(70, 140),
            "key": random.choice(["Cm", "Am", "F#", "Bb", "G"]),
            "scale": random.choice(["Pentatonic", "Minor", "Dorian"]),
            "synth": random.choice(["Sawtooth", "Sine", "Square", "Triangle"]),
            "context": selected_mood,
            "vocal_config": {
                "emotion": api_data.get("vocal_texture", "Calm"),
                "pitch": random.choice(["High", "Medium", "Low", "Medium-Low"]),
                "language": "English",
                "vibrato": "Natural"
            },
            "music_model": model_used,
            "vocal_model": "Suno v3.5/Diff-Singer",
            "lyrics": "Chorus: ...\nVerse: ...", 
            "prompt": f"AI {model_used} track for {selected_mood}. VOCALS: {api_data.get('vocal_texture', 'None')}. MUSIC: {api_data.get('clarity', 'Standard')}.",
            "popularity": random.randint(1, 100),
            "timestamp": datetime.datetime.now().isoformat()
        }

        # Update State
        state = self.load_state()
        state["catalog"].append(new_track)
        
        # Add Log
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "message": f"Generated new track: {new_track['title']} using {model_used}"
        }
        if "music_log" not in state: state["music_log"] = []
        state["music_log"].append(log_entry)
        
        self.save_state(state)
        self.log(f"Track {track_id} saved to catalog.")
