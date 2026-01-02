#############################################################
####  Main entry point for PDF-to-Obsidian Notes Generator.
#############################################################
#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Add app directory to path
sys.path.insert(0, str(Path(__file__).parent))

from dotenv import load_dotenv
from ui.gradio_ui import create_ui


def main():
    # Launch the Gradio application.
    
    # Load environment variables from .env file
    load_dotenv()
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not in .env")
        sys.exit(1)
    else :
        print("📍 Groq API key loaded successfully.")

    model = os.getenv("GROQ_MODEL")
    if not model:
        raise ValueError("GROQ_MODEL not in .env")
        sys.exit(1)
    else :
        print("📍 Groq model loaded successfully.")

    
    # Create and launch UI
    demo = create_ui()
    demo.launch(
        share=False,
        server_name="127.0.0.1",
        server_port=7860,
        show_error=True
    )


if __name__ == "__main__":
    main()
