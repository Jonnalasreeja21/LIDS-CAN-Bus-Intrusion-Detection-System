class DecisionFusion:
    def __init__(self, method='any'):
        self.method = method # 'any' or 'majority'

    def fuse(self, ibd: bool, fbd: bool, pbd: bool) -> bool:
        results = [ibd, fbd, pbd]
        
        if self.method == 'majority':
            # Returns True if 2 or more detectors are True
            return sum(results) >= 2
        
        # Default 'any': Returns True if at least one detector is True
        return any(results)