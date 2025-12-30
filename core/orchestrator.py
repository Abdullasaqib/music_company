import argparse
from datetime import datetime, timedelta
from database import CompanyDatabase
from music_agent import MusicAgent
from billing_agent import BillingAgent
from marketing_agent import MarketingAgent
from playlist_agent import PlaylistAgent

class Orchestrator:
    def __init__(self):
        self.db = CompanyDatabase()
        self.music_agent = MusicAgent(self.db)
        self.billing_agent = BillingAgent(self.db)
        self.marketing_agent = MarketingAgent(self.db)
        self.playlist_agent = PlaylistAgent(self.db)

    def run_daily_cycle(self, context="General"):
        print(f"--- Cycle Start: {self.db.state['simulated_date']} ---")
        
        # 1. Generate Music
        self.music_agent.generate_daily_track(context)
        
        # 2. Promote
        self.marketing_agent.promote_latest_release()
        
        # 3. Update Playlists
        self.playlist_agent.build_playlists()
        # For simplicity, we trigger a billing event every few cycles in sim
        
    def simulate_period(self, days):
        for i in range(days):
            # Advance simulation clock
            dt = datetime.fromisoformat(self.db.state["simulated_date"]) + timedelta(days=1)
            self.db.state["simulated_date"] = dt.isoformat()
            
            # Context-based bonus feature: alternate contexts
            context = random.choice(["Focus", "Workout", "Sleep", "General"])
            self.run_daily_cycle(context)
            
            # Trigger billing every 30 days
            if (i + 1) % 30 == 0:
                self.billing_agent.process_billing_cycle()
                self.playlist_agent.build_playlists()
        
        print(f"\nSimulation Complete. {days} days processed.")
        print(f"Final Balance: ${self.db.state['balance']}")
        print(f"Tracks in Catalog: {len(self.db.state['catalog'])}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["daily", "simulation"], default="daily")
    parser.add_argument("--days", type=int, default=7)
    args = parser.parse_args()
    
    import random # needed for context choice in sim
    
    orch = Orchestrator()
    if args.mode == "daily":
        orch.run_daily_cycle()
    else:
        orch.simulate_period(args.days)
