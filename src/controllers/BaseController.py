from doctest import debug
from helpers.config import get_settings, Settings
import os
import random
import string
class BaseController:

    def __init__(self):
        self.app_settings: Settings = get_settings()

        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.file_dir = self.base_dir + "/" + "assets/files"

        #or 
        # self.file_dir = os.path.join(self.base_dir, "assets", "files")

    def handle_request(self, request):
        raise NotImplementedError("Subclasses should implement this method.")



    def generate_random_string(self, length: int = 12) -> str:
        letters_and_digits = string.ascii_letters + string.digits
        random_string = ''.join(random.choice(letters_and_digits) for _ in range(length))
        return random_string