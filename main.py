import time
import random
from agents.music_agent import MusicAgent
from agents.marketing_agent import MarketingAgent
from agents.billing_agent import BillingAgent

def main():
    print("Initializing Nimbus AI Backend Agents...")
    
    music_agent = MusicAgent()
    marketing_agent = MarketingAgent()
    billing_agent = BillingAgent()
    
    # Tick Rate (simulation speed)
    print("Agents Active. Press Ctrl+C to stop.")
    
    while True:
        try:
            # Randomly trigger agents
            dice = random.random()
            
            if dice < 0.3: # 30% chance per tick
                music_agent.generate_track()
                
            if dice < 0.5: # 50% chance per tick
                marketing_agent.run_campaign()
                
            if dice < 0.1: # 10% chance per tick
                billing_agent.process_revenue()
                
            time.sleep(5) # Tick every 5 seconds
            
        except KeyboardInterrupt:
            print("Stopping Agents...")
            break
        except Exception as e:
            print(f"Error in loop: {e}")

if __name__ == "__main__":
    main()
