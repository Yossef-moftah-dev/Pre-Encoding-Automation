#############################################################
####       Markdown file generation and management module.
#############################################################
import os
from datetime import datetime


class MarkdownWriter:
    # Handles Markdown file generation and saving.
    
    def __init__(self, output_dir: str = "app/outputs"):
        # Initialize Markdown writer.
        # Args:
        #     output_dir: Directory to save generated files.

        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def save_file(self, filename: str, content: str) -> str:
        # Save Markdown content to file.
        # Args:
        #     filename: Name for the output file.
        #     content: Markdown content to write.   
        # Returns:
        #     Full path to saved file.
        
        # Sanitize filename
        filename = filename.replace(" ", "_")
        if not filename.endswith(".md"):
            filename += ".md"
        
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        return filepath
    
    def get_file_list(self) -> list:
        # Get list of generated files.
        # Returns:
        #     List of file paths in output directory.

        if not os.path.exists(self.output_dir):
            return []
        
        return [
            os.path.join(self.output_dir, f)
            for f in os.listdir(self.output_dir)
            if f.endswith(".md")
        ]
    
    def clear_outputs(self) -> None:
        # Clear all output files from the output directory.
        for filepath in self.get_file_list():
            try:
                os.remove(filepath)
            except Exception as e:
                print(f"Failed to delete {filepath}: {e}")
