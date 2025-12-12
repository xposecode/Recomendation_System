"""
statistics_module.py - Simple statistics module
"""

import math
from collections import Counter

class StatisticsCalculator:
    @staticmethod
    def mean(values):
        if not values:
            return 0
        return sum(values) / len(values)
    
    @staticmethod
    def median(values):
        if not values:
            return 0
        sorted_vals = sorted(values)
        n = len(sorted_vals)
        if n % 2 == 0:
            return (sorted_vals[n//2 - 1] + sorted_vals[n//2]) / 2
        return sorted_vals[n//2]
    
    @staticmethod
    def mode(values):
        if not values:
            return 0
        counts = Counter(values)
        max_count = max(counts.values())
        modes = [val for val, count in counts.items() if count == max_count]
        return modes[0] if modes else 0
    
    @staticmethod
    def standard_deviation(values):
        if len(values) < 2:
            return 0
        mean_val = StatisticsCalculator.mean(values)
        variance = sum((x - mean_val) ** 2 for x in values) / len(values)
        return math.sqrt(variance)