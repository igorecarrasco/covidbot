"""
Random image getter. Will allow tweeting out guidance from the WHO. 
"""
from pathlib import Path
import random


class Image:
    def random_image(self):
        files = Path("/user_code/local/images").glob("*.*")
        self.random_filename = random.choice([f for f in files])
        self.media_id = self.upload_image(self.random_filename)
        return {"image": True}
