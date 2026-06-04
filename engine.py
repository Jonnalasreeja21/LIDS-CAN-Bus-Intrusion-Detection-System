from .detectors import IntervalDetector, FrequencyDetector, PayloadDetector
from .fusion import DecisionFusion

class LIDSEngine:
    def __init__(self):
        self.interval = IntervalDetector()
        self.frequency = FrequencyDetector()
        self.payload = PayloadDetector()
        self.fusion = DecisionFusion(method='any')

    def process_message(self, frame):
        ibd = self.interval.update_and_detect(frame['id'], frame['ts'])
        fbd = self.frequency.detect(frame['id'], frame['count'])
        pbd = self.payload.detect(frame['id'], frame['data'])
        
        is_anomaly = self.fusion.fuse(ibd, fbd, pbd)
        return is_anomaly, {"interval": ibd, "freq": fbd, "payload": pbd}