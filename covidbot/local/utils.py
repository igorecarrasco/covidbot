"""
Utility functions
"""
from numpy import random


def distribution(n):
    """
    Returns a Pareto distribution of n length
    """
    d = random.pareto(1, n)
    distribution = list(d / d.sum(axis=0, keepdims=1)).sort(reverse=True)
    return distribution
