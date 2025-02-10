import requests
import json
from config import GROQ_API

class LORGenerator:
    def __init__(self):
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {GROQ_API}",
            "Content-Type": "application/json"
        }

    def generate_lor(self, user_text, lor_level):
        #  LOR length based 
        level_prompts = {
            "high": "Write a **highly detailed** and **strongly supportive** LOR with specific achievements, research contributions, and academic excellence. Ensure a formal, well-structured letter with **strong endorsement**.",
            "medium-high": "Write a **detailed and positive** LOR focusing on the student's strengths, coursework, and research skills. Keep it **engaging and supportive**, highlighting key skills.",
            "medium": "Write a **balanced** LOR that highlights key academic strengths while maintaining a neutral tone. Mention skills and contributions **without excessive emphasis**.",
            "medium-low": "Write a **concise and somewhat reserved** LOR, mentioning the student’s general strengths but **not strongly endorsing them**. Keep it short and formal.",
            "low": "Write a **brief and neutral** LOR with minimal details. Keep it **generic and polite**, without making strong recommendations."
        }

        #  instruction  on the LOR 
        lor_guidelines = level_prompts.get(lor_level, "Write a standard LOR.")

        prompt = f"""
You are a professor writing a formal academic Letter of Recommendation (LOR) for a student.  
The LOR should be aligned with the given student information and should reflect the appropriate level of recommendation.

### Student Details:
{user_text}

### LOR Guidelines:
- **{lor_guidelines}**
- Address it as: **"To the Admissions Committee"**.
- Highlight relevant academic strengths, achievements, research, and skills.
- **Do not include unnecessary introductory phrases like "Here is the LOR."**
- Keep the tone **formal and professional**.

Now, generate the complete LOR:
"""

        # tokens use based  level 
        max_tokens = {
            "high": 700,
            "medium-high": 500,
            "medium": 250,
            "medium-low": 200,
            "low": 180
        }

        payload = {
            "model": "llama3-70b-8192",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": max_tokens.get(lor_level, 400),
            "top_p": 0.9,
            "frequency_penalty": 0,
            "presence_penalty": 0
        }

        response = requests.post(self.api_url, headers=self.headers, json=payload)

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.json()}"

if __name__ == "__main__":
    generator = LORGenerator()
