import math
from collections import Counter

class IntervalDetector:
    def __init__(self):
        self.last_timestamps = {}

    def update_and_detect(self, can_id, ts):
        if can_id not in self.last_timestamps:
            self.last_timestamps[can_id] = ts
            return False
        interval = ts - self.last_timestamps[can_id]
        self.last_timestamps[can_id] = ts
        # Logic: If interval is too small (e.g., < 0.001s), flag injection
        return interval < 0.001 

class FrequencyDetector:
    def __init__(self):
        self.counts = Counter()

    def train_baseline(self, can_id, count):
        self.counts[can_id] = count

    def detect(self, can_id, current_count):
        # Logic: If frequency exceeds baseline by 50%
        return current_count > (self.counts[can_id] * 1.5)

class PayloadDetector:
    def __init__(self):
        self.benign_entropy = {}

    def compute_entropy(self, data):
        if not data: return 0
        counts = Counter(data)
        probs = [c/len(data) for c in counts.values()]
        return -sum(p * math.log2(p) for p in probs)

    def detect(self, can_id, data):
        entropy = self.compute_entropy(data)
        # Simplified: If entropy jumps significantly, it's an anomaly
        return entropy > 3.5