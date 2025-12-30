import random

class MusicAgent:
    def __init__(self, db):
        self.db = db
        self.vocal_profiles = {
            "Workout": {"emotion": "Aggressive", "pitch": "High", "style": "Rap/Drill"},
            "Focus": {"emotion": "Calm", "pitch": "Medium-Low", "style": "Ambient/Lo-fi"},
            "Sleep": {"emotion": "Ethereal", "pitch": "Soft", "style": "Pads/Slow"},
            "General": {"emotion": "Upbeat", "pitch": "Standard", "style": "Pop/Electronic"}
        }

    def generate_daily_track(self, context="General"):
        profile = self.vocal_profiles.get(context, self.vocal_profiles["General"])
        genre = profile["style"]
        
        # Musical Parameters
        keys = ["C", "G", "D", "A", "E", "F", "Bb", "Eb"]
        scales = ["Major", "Minor", "Pentatonic", "Melodic Minor"]
        synths = ["Sine", "Square", "Sawtooth", "Triangle"]
        
        bpm_map = {"Workout": 135, "Focus": 90, "Sleep": 60, "General": 110}
        tempo = bpm_map.get(context, 110) + random.randint(-5, 5)
        
        song_id = f"TRACK-{random.randint(1000, 9999)}"
        lyrics = self._generate_lyrics(genre, context)
        
        track = {
            "id": song_id,
            "title": f"{context} {genre} session",
            "genre": genre,
            "tempo": tempo,
            "key": random.choice(keys),
            "scale": random.choice(scales),
            "synth": random.choice(synths),
            "context": context,
            "vocal_config": {
                "emotion": profile["emotion"],
                "pitch": profile["pitch"],
                "language": "English",
                "vibrato": "Natural" if context != "Sleep" else "Soft"
            },
            "music_model": "Riffusion v2",
            "vocal_model": "Suno v3.5/Diff-Singer",
            "lyrics": lyrics,
            "prompt": f"AI {genre} track for {context}. VOCALS: {profile['emotion']}, {profile['pitch']} pitch. MUSIC: {tempo}BPM, high density.",
            "popularity": random.randint(10, 100),
            "timestamp": self.db.state["simulated_date"]
        }
        
        self.db.add_song(track)
        self.db.log_event("music_log", f"Generated Enhanced Track: {track['title']} ({track['vocal_config']['emotion']} vocals)")
        return track

    def _generate_lyrics(self, genre, context):
        themes = {
            "Focus": ["Flowing silence", "Deep concentration", "Steady rhythm of thought"],
            "Workout": ["Break the limit", "Infinite energy", "Rise and grind"],
            "Sleep": ["Drifting stars", "Quiet whispers", "Gentle ocean waves"],
            "General": ["Digital dreams", "Neon nights", "Signal in the noise"]
        }
        lines = random.sample(themes.get(context, themes["General"]), 2)
        return f"Chorus: {lines[0]}\nVerse: {lines[1]}"
