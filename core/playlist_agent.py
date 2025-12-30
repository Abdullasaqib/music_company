class PlaylistAgent:
    def __init__(self, db):
        self.db = db

    def build_playlists(self):
        catalog = self.db.state.get("catalog", [])
        if not catalog:
            return

        moods = ["Workout", "Focus", "Sleep"]
        playlists = {}

        for mood in moods:
            tracks = [t["title"] for t in catalog if t.get("context") == mood]
            if tracks:
                playlists[f"Ultimate {mood} Mix"] = random.sample(tracks, min(len(tracks), 5))

        self.db.state["playlists"] = playlists
        self.db.save()
        self.db.log_event("music_log", f"Updated playlists for {len(playlists)} moods")

import random
