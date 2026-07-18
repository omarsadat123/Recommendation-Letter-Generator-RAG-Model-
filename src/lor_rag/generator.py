"""LOR generation using the Groq chat completion API."""

from __future__ import annotations

import logging
from typing import Dict

import requests

from .config import get_settings

LOGGER = logging.getLogger(__name__)


class LORGenerator:
    """Generate recommendation letters from student details."""

    def __init__(self) -> None:
        settings = get_settings()
        self.api_url = settings.groq_api_url
        self.api_key = settings.groq_api_key
        self.model_name = settings.model_name

    def generate_lor(self, user_text: str, lor_level: str) -> str:
        """Generate an LOR for the provided text and recommendation level."""

        if not self.api_key:
            LOGGER.error("Missing GROQ_API_KEY environment variable.")
            return "Error: Missing GROQ_API_KEY environment variable."

        level_prompts: Dict[str, str] = {
            "high": (
                "Write a highly detailed and strongly supportive LOR with specific "
                "achievements, research contributions, and academic excellence."
            ),
            "medium-high": (
                "Write a detailed and positive LOR focusing on strengths, coursework, "
                "and research skills."
            ),
            "medium": "Write a balanced LOR with a neutral and professional tone.",
            "medium-low": (
                "Write a concise and somewhat reserved LOR without strong endorsement."
            ),
            "low": "Write a brief and neutral LOR with minimal details.",
        }

        lor_guidelines = level_prompts.get(lor_level, "Write a standard LOR.")

        prompt = f"""
You are a professor writing a formal academic Letter of Recommendation (LOR) for a student.

### Student Details:
{user_text}

### LOR Guidelines:
- {lor_guidelines}
- Address it as: "To the Admissions Committee".
- Highlight relevant academic strengths, achievements, research, and skills.
- Keep the tone formal and professional.

Now, generate the complete LOR:
"""

        max_tokens = {
            "high": 700,
            "medium-high": 500,
            "medium": 250,
            "medium-low": 200,
            "low": 180,
        }

        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": max_tokens.get(lor_level, 400),
            "top_p": 0.9,
            "frequency_penalty": 0,
            "presence_penalty": 0,
        }

        headers = {
            "Authorization": f"******",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            body = response.json()
            return body["choices"][0]["message"]["content"]
        except requests.RequestException as exc:
            LOGGER.exception("LOR generation request failed")
            return f"Error: API request failed ({exc})."
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            LOGGER.exception("Unexpected API response format")
            return f"Error: Unexpected API response format ({exc})."
