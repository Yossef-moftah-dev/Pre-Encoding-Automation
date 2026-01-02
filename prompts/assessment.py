#############################################################
####           Rephrase and Clarify prompt template.
#############################################################


def get_rephrase_clarify_prompt(pdf_text: str) -> str:
    # Generate prompt for rephrasing and clarifying PDF content.
    # Args:
    #     pdf_text: Extracted text from PDF.
    # Returns:
    #     Complete prompt for Groq API.
    return f"""You are an expert educator. Analyze the following academic material and produce an Obsidian-compatible Markdown file that rephrases and clarifies the content.

**STRICT OUTPUT FORMAT:**

1. **Structure:** Use hierarchical headings (##, ###).
2. **Before each heading (##, ###):** Add a horizontal rule (---).
3. **Bullet lists:** Keep compact and scannable—maximum 3 bullets per concept. Use single spacing.
4. **Questions:** After the main content, add 5-7 questions labeled Q1, Q2, etc. that address Bloom's Taxonomy Level 1 (Remember) and Level 2 (Understand). Do NOT include answers.
5. **Markdown only:** Output ONLY valid Markdown. No meta-text, explanations, or preambles.

**SOURCE MATERIAL:**
{pdf_text}

**OUTPUT INSTRUCTIONS:**
- Rephrase complex concepts in simple, student-friendly language.
- Organize into clear sections using ##.
- Use ### for sub-concepts.
- Include a horizontal rule before each new section.
- End with Q1, Q2, ... Qn (Bloom L1-L2 questions without answers).
- Ensure all text is Markdown-valid for Obsidian.

BEGIN OUTPUT (Markdown only):"""


def get_schema_prompt(pdf_text: str) -> str:
    # Generate prompt for schema/overview generation.
    # Args:
    #     pdf_text: Extracted text from PDF. 
    # Returns:
    #     Complete prompt for Groq API.
    return f"""You are an expert educator. Analyze the following academic material and produce a comprehensive schema/overview document as Obsidian-compatible Markdown.

**STRICT OUTPUT FORMAT:**

1. **Executive Summary:** Start with a brief (200-300 words) executive summary of the material.
2. **Obsidian Callouts:** Use the following callout styles (each on its own section):
   - abstract: Key definitions
   - settings: Important assumptions or preconditions
   - globe: Real-world applications or examples
   - chart: Data, statistics, or numerical insights
   - zip: Summary of takeaways
3. **Mermaid Diagram:** Include a concept map using Mermaid's graph TD (top-down) format. Wrap it in a collapsible callout.
4. **Quick Revision:** 3-5 high-value questions (no answers) for self-testing.
5. **Markdown only:** Output ONLY valid Markdown. No explanations or meta-text.

**SOURCE MATERIAL:**
{pdf_text}

**OUTPUT INSTRUCTIONS:**
- Executive summary first (clear, concise, student-appropriate).
- Use proper Obsidian callout syntax: > [!callout_type] Title
- Mermaid diagram wrapped in > [!abstract] Concept Map (collapsible if needed).
- Quick Revision questions must be clear and testable.
- Ensure all text is Markdown-valid for Obsidian.

BEGIN OUTPUT (Markdown only):"""


def get_assessment_prompt(pdf_text: str, bloom_level: str) -> str:
    # Generate prompt for assessment question generation.
    # Args:
    #     pdf_text: Extracted text from PDF.
    #     bloom_level: Level of Bloom's Taxonomy ("Level 1", "Level 2", or "Level 3").
    # Returns:
    #     Complete prompt for Groq API.

    level_descriptions = {
        "Level 1": {
            "name": "Remember",
            "description": "Recall of facts, definitions, and simple concepts. Use verbs: define, list, identify, recall, state.",
            "example": "What is [key term]?"
        },
        "Level 2": {
            "name": "Understand",
            "description": "Comprehension and explanation of concepts. Use verbs: explain, describe, summarize, interpret, classify.",
            "example": "Why does [concept] occur? Explain [relationship]."
        },
        "Level 3": {
            "name": "Apply",
            "description": "Use of knowledge in new situations. Use verbs: apply, solve, demonstrate, construct, use.",
            "example": "How would you apply [concept] to [new scenario]?"
        }
    }
    
    level_info = level_descriptions.get(bloom_level, level_descriptions["Level 1"])
    
    return f"""You are an expert educator creating assessment questions for Obsidian study notes. Generate questions based on Bloom's Taxonomy {level_info['name']} (Level {bloom_level[-1]}).

**BLOOM'S TAXONOMY LEVEL: {level_info['name']}**
Description: {level_info['description']}
Example question type: {level_info['example']}

**STRICT OUTPUT FORMAT:**

1. **Title:** Start with a title like "## Assessment: {level_info['name']} Questions"
2. **Question Count:** Generate 8-10 questions.
3. **Questions Only:** Do NOT include answers, hints, or solution keys.
4. **Numbering:** Use numbered list format (1., 2., 3., etc.).
5. **Markdown only:** Output ONLY valid Markdown. No meta-text or explanations.

**SOURCE MATERIAL:**
{pdf_text}

**IMPORTANT:** Ensure all questions strictly target Bloom's Taxonomy {level_info['name']} (Level {bloom_level[-1]}). Do not mix levels.

BEGIN OUTPUT (Markdown only):"""
