from core.file_reader import FileReader
from core.file_writer import FileWriter
from core.data_transformer import DataTransformer
import os

class AppController:
    """AppController is the controller in an MVC architecture. It mediates between the AppGUI and the core classes"""

    FILE_EXTENSION = "txt"
    FILE_NAME = "sheet.txt"

    def __init__(self):
        self.reader = FileReader()
        self.transformer = DataTransformer()
        self.writer = FileWriter()
    
    def read_file_content(self, file_path: str) -> list:
        """Read the given file and return content as a list of strings"""
        # Save the file name and extension
        #path = os.path.normpath(file_path)  # normalize different OSes
        #file, ext = path.split(os.sep)
        folder, self.FILE_NAME = os.path.split(file_path)
        path, dotted_extension = os.path.splitext(file_path)
        self.FILE_EXTENSION =  dotted_extension[1:]
        # Read the file and return its raw content as a list
        try:
            data = self.reader.read_file(file_path)
            return data  # Assuming `read_file` returns the raw content directly
        except Exception as e:
            raise ValueError(f"Error reading file: {e}")
        
    def evaluate(self, source_lines: list):
        """Parse the source lines into the ironcalc model and evaluate it."""
        self.transformer.parse_source(self.FILE_EXTENSION, source_lines)

        # When parsing is complete, evaluate the spreadsheet (recalculate all cells)
        worksheet = self.transformer.get_worksheet()
        spreadsheet = worksheet['sheet']
        spreadsheet.evaluate()
        
        return worksheet
