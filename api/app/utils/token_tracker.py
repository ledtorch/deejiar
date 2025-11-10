from datetime import datetime
from typing import Dict, List
from collections import defaultdict

class TokenTracker:
    """Track refresh token usage to debug 'Already Used' errors"""
    
    def __init__(self):
        # token -> list of usage records
        self._usage_log: Dict[str, List[dict]] = defaultdict(list)
        
    def log_usage(self, token: str, action: str, result: str = "unknown", details: str = ""):
        """Log a token usage event"""
        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "result": result,
            "details": details
        }
        
        self._usage_log[token].append(record)
        
        # Keep only last 100 entries per token to prevent memory bloat
        if len(self._usage_log[token]) > 100:
            self._usage_log[token] = self._usage_log[token][-100:]
    
    def get_token_history(self, token: str) -> List[dict]:
        """Get all usage records for a token"""
        return self._usage_log.get(token, [])
    
    def check_for_reuse(self, token: str) -> tuple[bool, int]:
        """Check if token has been used before
        
        Returns:
            (is_reused, usage_count)
        """
        history = self._usage_log.get(token, [])
        usage_count = len([r for r in history if r["action"] == "REFRESH_ATTEMPT"])
        return (usage_count > 0, usage_count)
    
    def print_token_history(self, token: str):
        """Print formatted history for a token"""
        history = self.get_token_history(token)
        
        if not history:
            print(f"[TokenTracker] No history for token: {token}")
            return
        
        print(f"[TokenTracker] History for token: {token}")
        print(f"[TokenTracker] Total events: {len(history)}")
        print("[TokenTracker] ════════════════════════════════════")
        
        for i, record in enumerate(history, 1):
            print(f"[TokenTracker] {i}. {record['timestamp']}")
            print(f"[TokenTracker]    Action: {record['action']}")
            print(f"[TokenTracker]    Result: {record['result']}")
            if record['details']:
                print(f"[TokenTracker]    Details: {record['details']}")
        
        print("[TokenTracker] ════════════════════════════════════")

# Global singleton instance
token_tracker = TokenTracker()