#############################################################
####            Gradio-based web UI for PDF processing.
#############################################################
import gradio as gr
import os
from pathlib import Path

from core.pdf_loader import extract_text_from_pdf
from core.groq_client import GroqClient
from core.markdown_writer import MarkdownWriter
from core.chunked_processor import TextChunker
from prompts.assessment import (
    get_rephrase_clarify_prompt,
    get_schema_prompt,
    get_assessment_prompt
)


class PdfProcessorUI:
    # Gradio UI for PDF-to-Obsidian note generation.
    
    def __init__(self):
        self.groq = GroqClient()
        self.writer = MarkdownWriter()
        self.current_pdf_text = None
        self.current_filename = None
    
    def process_pdf(self, pdf_file):
        # Extract text from uploaded PDF.
        # Args:
        #     pdf_file: Uploaded PDF file from Gradio.
        # Returns:
        #     Status message.

        try:
            if pdf_file is None:
                return "No PDF uploaded. Please select a file."
            
            self.current_pdf_text = extract_text_from_pdf(pdf_file.name)
            self.current_filename = Path(pdf_file.name).stem
            
            text_preview = self.current_pdf_text[:500] + "..." if len(self.current_pdf_text) > 500 else self.current_pdf_text
            tokens = TextChunker.estimate_tokens(self.current_pdf_text)
            return f"✅ PDF processed!\n\nFilename: {self.current_filename}\nTokens: {tokens:,}\n\nPreview:\n{text_preview}"
        except Exception as e:
            return f"❌ Error processing PDF: {str(e)}"
    
    def rephrase_and_clarify(self):
        # Generate rephrased notes and schema.
        if not self.current_pdf_text:
            return "❌ Please upload and process a PDF first.", None, None
        
        try:
            def process_chunk(chunk: str, chunk_num: int) -> tuple:
                # Process one chunk.
                prompt = get_rephrase_clarify_prompt(chunk)
                result, tokens = self.groq.generate_text(prompt)
                return result, tokens
            
            # Process in chunks serially
            notes_content, stats = TextChunker.process_serial(
                self.current_pdf_text, 
                process_chunk,
                show_progress=True
            )
            
            # Save notes
            notes_filename = f"{self.current_filename}_notes"
            notes_path = self.writer.save_file(notes_filename, notes_content)
            
            # Generate schema on full text (smaller)
            schema_prompt = get_schema_prompt(self.current_pdf_text[:8000])
            schema_content, _ = self.groq.generate_text(schema_prompt)
            
            # Save schema
            schema_filename = f"{self.current_filename}_schema"
            schema_path = self.writer.save_file(schema_filename, schema_content)
            
            status_msg = f"✅ Generated:\n- {os.path.basename(notes_path)}\n- {os.path.basename(schema_path)}"
            return status_msg, notes_content, schema_content
        
        except Exception as e:
            return f"❌ Error: {str(e)}", None, None
    
    def generate_assessment(self, bloom_level):
        # Generate assessment questions based on Bloom's level.
        if bloom_level == "None":
            return "ℹ️ Assessment disabled. Select a Bloom's Taxonomy level.", None
        
        if not self.current_pdf_text:
            return "❌ Please upload and process a PDF first.", None
        
        try:
            def process_chunk(chunk: str, chunk_num: int) -> tuple:
                # Process one chunk.
                prompt = get_assessment_prompt(chunk, bloom_level)
                result, tokens = self.groq.generate_text(prompt)
                return result, tokens
            
            # Process in chunks serially with rate limiting
            assessment_content, stats = TextChunker.process_serial(
                self.current_pdf_text,
                process_chunk,
                show_progress=True
            )
            
            # Save assessment
            assessment_filename = f"{self.current_filename}_assessment_{bloom_level.replace(' ', '_').lower()}"
            assessment_path = self.writer.save_file(assessment_filename, assessment_content)
            
            status_msg = f"✅ Generated: {os.path.basename(assessment_path)}"
            return status_msg, assessment_content
        
        except Exception as e:
            return f"❌ Error: {str(e)}", None
    
    def clear_workspace(self):
        self.writer.clear_outputs()
        self.current_pdf_text = None
        self.current_filename = None
        return "✅ Workspace cleared."


def create_ui():
    # Create and return the Gradio interface.
    # Returns:
    #     Gradio Blocks interface.

    processor = PdfProcessorUI()
    
    with gr.Blocks(title="PDF → Obsidian Notes Generator") as demo:
        gr.Markdown("# 📚 PDF → Obsidian Notes Generator")
        gr.Markdown("Convert academic PDFs into structured Obsidian-compatible markdown notes.")
        
        # PDF Upload
        with gr.Row():
            with gr.Column(scale=2):
                pdf_input = gr.File(label="📄 Upload PDF", file_types=[".pdf"])
                process_btn = gr.Button("📥 Process PDF", variant="primary")
            
            with gr.Column(scale=1):
                pdf_status = gr.Textbox(label="Status", interactive=False, lines=5)
        
        # Process PDF callback
        process_btn.click(
            fn=processor.process_pdf,
            inputs=[pdf_input],
            outputs=[pdf_status]
        )
        
        # Notes & Schema Generation
        with gr.Row():
            notes_btn = gr.Button("✍️ Rephrase & Clarify", variant="primary", size="lg")
        
        with gr.Row():
            with gr.Column():
                gr.Markdown("### 📝 Rephrased Notes")
                notes_output = gr.Markdown(label="Notes Content")
            
            with gr.Column():
                gr.Markdown("### 📊 Schema")
                schema_output = gr.Markdown(label="Schema Content")
        
        # Generate notes callback
        notes_btn.click(
            fn=processor.rephrase_and_clarify,
            inputs=[],
            outputs=[pdf_status, notes_output, schema_output]
        )
        
        # Assessment Questions
        with gr.Row():
            with gr.Column(scale=1):
                bloom_level = gr.Radio(
                    choices=["None", "Level 1 (Remember)", "Level 2 (Understand)", "Level 3 (Apply)"],
                    value="None",
                    label="📋 Bloom's Taxonomy Level"
                )
            
            with gr.Column(scale=1):
                assessment_btn = gr.Button("🎓 Generate Assessment", variant="primary", size="lg")
        
        with gr.Row():
            gr.Markdown("### 📋 Assessment Questions")
            assessment_output = gr.Markdown(label="Assessment Content")
        
        # Generate assessment callback
        assessment_btn.click(
            fn=processor.generate_assessment,
            inputs=[bloom_level],
            outputs=[pdf_status, assessment_output]
        )
        
        # Configuration display
        with gr.Row():
            with gr.Column():
                gr.Markdown(f"""
### ⚙️ Configuration
- **Rate Limiting:** 5500 tokens/minute
- **Output Directory:** `{processor.writer.output_dir}/`
- **API Status:** Ready
                """)
        
        # Control buttons
        with gr.Row():
            clear_btn = gr.Button("🗑️ Clear Workspace", variant="secondary")
        
        # Clear workspace callback
        clear_btn.click(
            fn=processor.clear_workspace,
            inputs=[],
            outputs=[pdf_status]
        )
    
    return demo


def main():
    print("🚀 Starting PDF → Obsidian Notes Generator...")
    
    
    # Create and launch UI
    demo = create_ui()
    demo.launch(share=False, server_name="127.0.0.1", server_port=7860)


if __name__ == "__main__":
    main()
