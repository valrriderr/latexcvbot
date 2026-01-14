from anthropic import Anthropic
from typing import Dict, Any

from app.core.config import settings
from app.schemas.resume import ResumeContent


class AITranslationService:
    def __init__(self):
        self.client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)

    async def translate_resume(
        self,
        content: ResumeContent,
        target_language: str,
        mode: str = "standard"  # standard or professional
    ) -> Dict[str, Any]:
        prompt = self._build_translation_prompt(content, target_language, mode)

        message = self.client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        # Parse the response and return structured JSON
        # TODO: Implement proper JSON parsing from response
        return message.content[0].text

    def _build_translation_prompt(
        self,
        content: ResumeContent,
        target_language: str,
        mode: str
    ) -> str:
        language_names = {
            "en": "English",
            "ru": "Russian",
            "fr": "French"
        }

        mode_instruction = ""
        if mode == "professional":
            mode_instruction = """
            Use professional HR terminology and optimize the language for job applications.
            Make achievements sound more impactful while maintaining accuracy.
            """

        return f"""
        Translate the following resume JSON to {language_names.get(target_language, target_language)}.
        {mode_instruction}

        Maintain the exact JSON structure. Only translate the text values, not the keys.
        Return only valid JSON, no additional text.

        Resume JSON:
        {content.model_dump_json(indent=2)}
        """


ai_translation_service = AITranslationService()
