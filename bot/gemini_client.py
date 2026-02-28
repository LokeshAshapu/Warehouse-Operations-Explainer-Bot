"""
Gemini Flash Client for Warehouse Explainer Bot.
Handles model initialization and text generation with system instruction.
"""

import os
import google.generativeai as genai
from bot.prompt_templates import SYSTEM_PROMPT


class GeminiClient:
    """Wrapper around Gemini Flash model with warehouse-specific system prompt."""

    def __init__(self, api_key: str, model_name: str = "gemini-2.0-flash"):
        genai.configure(api_key=api_key)

        self.model = genai.GenerativeModel(
            model_name=model_name,
            system_instruction=SYSTEM_PROMPT,
            generation_config=genai.GenerationConfig(
                temperature=0.3,
                top_p=0.85,
                max_output_tokens=2048,
            )
        )
        self.model_name = model_name
        print(f"[Gemini Client] Initialized with model: {model_name}")

    def generate(self, prompt: str) -> str:
        """
        Generate a response from Gemini Flash.
        Falls back to gemini-2.5-flash if the primary model returns quota errors.
        """
        import google.generativeai as genai_module

        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            err = str(e)
            # Try fallback model on quota or not-found errors
            if "429" in err or "quota" in err.lower() or "404" in err:
                try:
                    fallback_model = genai_module.GenerativeModel(
                        model_name="gemini-2.5-flash",
                        system_instruction=SYSTEM_PROMPT,
                        generation_config=genai_module.GenerationConfig(
                            temperature=0.3,
                            max_output_tokens=2048,
                        )
                    )
                    response = fallback_model.generate_content(prompt)
                    return response.text
                except Exception as e2:
                    return (
                        f"⚠️ **API Quota Exhausted**\n\n"
                        f"The free-tier daily quota for Gemini has been exceeded. "
                        f"This resets automatically — please try again in a few minutes or hours.\n\n"
                        f"**Note:** The RAG retrieval above is working correctly. "
                        f"The retrieved source documents show the relevant warehouse knowledge. "
                        f"The LLM generation step is temporarily paused due to quota limits.\n\n"
                        f"*Technical detail: {str(e2)[:200]}*"
                    )
            return f"⚠️ An error occurred: {err[:300]}\n\nPlease check your API key and try again."
