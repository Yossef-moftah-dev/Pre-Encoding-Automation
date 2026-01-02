#############################################################
#### Text chunking for serial processing.
#############################################################
from typing import List, Tuple, Callable, Dict, Any


class TextChunker:    
    TOKENS_PER_CHUNK = 5000
    CHARS_PER_TOKEN = 4
    CHARS_PER_CHUNK = TOKENS_PER_CHUNK * CHARS_PER_TOKEN
    
    def estimate_tokens(text: str) -> int:
        return len(text) // TextChunker.CHARS_PER_TOKEN
    
    def split(text: str) -> List[str]:
        if len(text) <= TextChunker.CHARS_PER_CHUNK:
            return [text]
        
        chunks = []
        current = ""
        paragraphs = text.split("\n\n")
        
        for para in paragraphs:
            if len(current) + len(para) <= TextChunker.CHARS_PER_CHUNK:
                current += para + "\n\n"
            else:
                if current:
                    chunks.append(current.strip())
                
                if len(para) > TextChunker.CHARS_PER_CHUNK:
                    sentences = para.split(". ")
                    chunk_text = ""
                    for sent in sentences:
                        sent = sent + ". " if not sent.endswith(". ") else sent
                        if len(chunk_text) + len(sent) <= TextChunker.CHARS_PER_CHUNK:
                            chunk_text += sent
                        else:
                            if chunk_text:
                                chunks.append(chunk_text.strip())
                            chunk_text = sent
                    if chunk_text:
                        chunks.append(chunk_text.strip())
                else:
                    current = para + "\n\n"
        
        if current:
            chunks.append(current.strip())
        
        return chunks if chunks else [text]
    
    @staticmethod
    def process_serial(
        text: str,
        process_fn: Callable[[str, int], Tuple[str, int]],
        show_progress: bool = True
    ) -> Tuple[str, Dict[str, Any]]:
        
        chunks = TextChunker.split(text)
        total_tokens = len(text) / TextChunker.CHARS_PER_TOKEN
        results = []
        total_output_tokens = 0
        failed = 0
        
        if show_progress:
            print(f"\n📊 Processing {total_tokens:,} tokens in {len(chunks)} chunk(s)")
        
        for i, chunk in enumerate(chunks, 1):
            chunk_tokens = len(chunk) / TextChunker.CHARS_PER_TOKEN
            
            try:
                if show_progress:
                    print(f"  ⏳ Chunk {i}/{len(chunks)} ({chunk_tokens:,} tokens)...", end=" ")
                
                result, output_tokens = process_fn(chunk, i)
                results.append(result)
                total_output_tokens += output_tokens
                
                if show_progress:
                    print(f"✓ ({output_tokens:,} tokens)")
                    
            except Exception as e:
                failed += 1
                if show_progress:
                    print(f"❌ {str(e)[:50]}")
        
        stats = {
            "total_input_tokens": total_tokens,
            "total_output_tokens": total_output_tokens,
            "chunks_processed": len(chunks) - failed,
            "chunks_failed": failed,
            "total_chunks": len(chunks)
        }
        
        if show_progress:
            print(f"✅ Complete")
        
        return "".join(results), stats
