import pandas as pd
import os
import shutil
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class ExcelProcessor:
    def __init__(self, file_path: str):
        """Initialize Excel processor with original file path"""
        self.original_path = Path(file_path)
        self.working_path = None
        self.excel_file = None
        self.sheet_names = []
        self.content_df = None
        self.instruction_df = None

    def create_working_copy(self) -> Path:
        """Create a working copy of the original Excel file"""
        try:
            # Create working file with _processed suffix
            working_path = self.original_path.parent / f"{self.original_path.stem}_processed{self.original_path.suffix}"
            shutil.copy2(self.original_path, working_path)
            self.working_path = working_path
            return working_path
        except Exception as e:
            logger.error(f"Error creating working copy: {e}")
            raise

    def load_excel(self) -> List[str]:
        """Load Excel file and return sheet names"""
        try:
            self.excel_file = pd.ExcelFile(self.working_path)
            self.sheet_names = self.excel_file.sheet_names
            return self.sheet_names
        except Exception as e:
            logger.error(f"Error loading Excel file: {e}")
            raise

    def load_sheets(self, instruction_sheet: str, content_sheet: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """Load specific sheets from Excel file"""
        try:
            self.instruction_df = pd.read_excel(self.working_path, sheet_name=instruction_sheet)
            self.content_df = pd.read_excel(self.working_path, sheet_name=content_sheet)
            return self.instruction_df, self.content_df
        except Exception as e:
            logger.error(f"Error loading sheets: {e}")
            raise

    def update_answers(self, answers: List[str], answer_column: str, start_row: int) -> None:
        """Update content sheet with generated answers"""
        try:
            if answer_column not in self.content_df.columns:
                self.content_df[answer_column] = ""
            
            current_row = start_row
            for answer in answers:
                if current_row < len(self.content_df):
                    self.content_df.at[current_row, answer_column] = answer
                    current_row += 1
        except Exception as e:
            logger.error(f"Error updating answers: {e}")
            raise

    def save_changes(self, content_sheet: str) -> None:
        """Save changes to the working copy"""
        try:
            with pd.ExcelWriter(self.working_path, engine='openpyxl', mode='a') as writer:
                # Remove the sheet if it exists
                if content_sheet in writer.book.sheetnames:
                    idx = writer.book.sheetnames.index(content_sheet)
                    writer.book.remove(writer.book.worksheets[idx])
                
                # Write the updated content sheet
                self.content_df.to_excel(writer, sheet_name=content_sheet, index=False)
        except Exception as e:
            logger.error(f"Error saving changes: {e}")
            raise

    def cleanup(self) -> None:
        """Clean up temporary files if needed"""
        try:
            if self.excel_file is not None:
                self.excel_file.close()
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")