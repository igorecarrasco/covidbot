"""
Random image getter. Will allow tweeting out guidance from the WHO. 
"""
from pathlib import Path
import random


class Image:
    def random_image(self):
        files = Path("local/images").glob("*.*")
        self.random_filename = random.choice([f for f in files])
        return True
