#############################################################
#### Groq API client for LLM interactions with built-in rate limiting.
#############################################################

import os
import time
from groq import Groq
from typing import Tuple
from dotenv import load_dotenv

MAX_TOKENS_PER_MINUTE = 5500


class GroqClient:
    # Groq API client

    def __init__(self):
        load_dotenv()

        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY not in .env")

        self.model = os.getenv("GROQ_MODEL")
        if not self.model:
            raise ValueError("GROQ_MODEL not in .env")

        self.client = Groq(api_key=self.api_key)
        
        # Rate limiter state
        self.tokens_used = 0
        self.window_start = time.time()
    
    def _check_rate_limit(self, tokens: int) -> bool:
        # Check if tokens can be processed without exceeding limit.
        elapsed = time.time() - self.window_start
        if elapsed >= 60:
            self.tokens_used = 0
            self.window_start = time.time()
        return (self.tokens_used + tokens) <= MAX_TOKENS_PER_MINUTE
    
    def generate_text(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 4096
    ) -> Tuple[str, int]:
        # Generate text using Groq API.
        # Args:
        #     prompt: Input prompt
        #     temperature: Sampling temperature (0.0-1.0)
        #     max_tokens: Max tokens in response
        # Returns:
        #     (response_text, output_tokens_count)

        message = self.client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert educator creating structured Markdown content for Obsidian. Output only Markdown—no explanations or meta-text."
                },
                {"role": "user", "content": prompt}
            ],
            model=self.model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        
        response_text = message.choices[0].message.content.strip()
        output_tokens = message.usage.completion_tokens if hasattr(message, 'usage') else 0
        
        self.tokens_used += output_tokens
        
        return response_text, output_tokens

