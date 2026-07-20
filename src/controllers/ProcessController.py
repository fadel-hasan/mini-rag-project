import os

from .BaseController import BaseController
from .ProjectController import ProjectController

from langchain_community.document_loaders import TextLoader, PyMuPDFLoader

from models import ProcessingEnum
from langchain_text_splitters import RecursiveCharacterTextSplitter

class ProcessController(BaseController):
    
    def __init__(self,project_id : str):
        super().__init__()
        
        self.project_id = project_id
        self.project_path = ProjectController().get_project_path(project_id)
        
        
        
    def get_file_extension(self, file_id: str) -> str:
        """
        Get the file extension of a file based on its ID.

        Args:
            file_id (str): The ID of the file.

        Returns:
            str: The file extension (e.g., '.txt', '.csv').
        """
        # Assuming the file_id is the filename with extension
        _, file_extension = os.path.splitext(file_id)
        return file_extension
    
    
    def get_file_loader(self, file_id: str):
        """
        Get the appropriate file loader based on the file extension.

        Args:
            file_id (str): The ID of the file.

        Returns:
            BaseLoader: An instance of the appropriate file loader.
        """
        file_extension = self.get_file_extension(file_id)
        
        if file_extension == ProcessingEnum.TEXT.value:
            return TextLoader(os.path.join(self.project_path, file_id),encoding='utf-8')
        
  
        if file_extension == ProcessingEnum.PDF.value:
            return PyMuPDFLoader(os.path.join(self.project_path, file_id))

        return None
    
    def get_file_content(self, file_id: str) -> str:
        """
        Get the content of a file based on its ID.

        Args:
            file_id (str): The ID of the file.

        Returns:
            str: The content of the file as a string.
        """
        loader = self.get_file_loader(file_id)
        
        if loader is None:
            raise ValueError(f"Unsupported file extension for file: {file_id}")
        
        documents = loader.load()
        
        # Assuming you want to concatenate all document contents into a single string
        # content = "\n".join([doc.page_content for doc in documents])
        
        return documents
    
    
    def process_file_content(self, file_id: str, file_content: str, chunk_size: int = 100, chunk_overlap: int = 20) -> list:
        """
        Process the content of a file based on its ID.

        Args:
            file_id (str): The ID of the file.
            chunk_size (int): The size of each chunk.
            chunk_overlap (int): The overlap between chunks.

        Returns:
            list: A list of processed content chunks.
        """
        # content = self.get_file_content(file_id)
        
        # Use RecursiveCharacterTextSplitter to split the content into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len
        )
        
        file_content_texts = [
            doc.page_content for doc in file_content
        ]
        
        file_content_metadata = [
            doc.metadata for doc in file_content
        ]
        
        chunks = text_splitter.create_documents(file_content_texts, metadatas=file_content_metadata)
        
        return chunks