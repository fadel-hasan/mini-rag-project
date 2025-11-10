import os
from fastapi import UploadFile
from .BaseController import BaseController
from models import ResponseSignal
from .ProjectController import ProjectController
import re


class DataController(BaseController):


    def __init__(self):
        super().__init__()
        self.size_scale = 1024 * 1024  # 1 MB

    
    def validate_upload_file(self,file: UploadFile):

        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False,ResponseSignal.FILE_TYPE_NOT_SUPPORTED.value
        

        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False,ResponseSignal.FILE_SIZE_EXCEEDED.value
        

        return True,ResponseSignal.FILE_VALIDATED_SUCCESS.value
    

    

    def generate_unique_filename(self,orign_file_name:str,project_id:str):
        
        random_filename = self.generate_random_string(8)
        project_path = ProjectController().get_project_path(project_id)
        clean_name = self.get_clean_file_name(orign_file_name)

        unique_file_name = f"{random_filename}_{clean_name}"
        new_file_path = os.path.join(project_path,
                                      unique_file_name)
        
        while os.path.exists(new_file_path):
            random_filename = self.generate_random_string(8)
            unique_file_name = f"{random_filename}_{clean_name}"
            new_file_path = os.path.join(project_path,
                                      unique_file_name)
            
        return new_file_path
        

    def get_clean_file_name(self,orign_file_name:str):
        # Remove special characters and spaces
        clean_name = re.sub(r'[^a-zA-Z0-9_.-]', '_', orign_file_name.strip())
        return clean_name