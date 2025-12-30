import datetime
from .agent_base import AgentBase

class BillingAgent(AgentBase):
    def __init__(self):
        super().__init__("Billing Agent")
        
    def process_revenue(self):
        state = self.load_state()
        
        # Calculate Revenue based on Catalog Size + Random Variance
        # Simulation: Each track earns roughly $0.50 - $2.00 per 'tick'
        catalog_size = len(state.get("catalog", []))
        if catalog_size == 0: return

        revenue = catalog_size * 0.75 
        
        current_balance = state.get("balance", 0)
        new_balance = current_balance + revenue
        
        state["balance"] = new_balance
        
        # unexpected formatting, ensure billing_log exists
        if "billing_log" not in state: state["billing_log"] = []
        
        log_entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "message": f"Processed monthly billing. Revenue: ${revenue:.2f}"
        }
        state["billing_log"].append(log_entry)
        
        self.save_state(state)
        self.log(f"Added ${revenue:.2f} revenue. New Balance: ${new_balance:.2f}")
