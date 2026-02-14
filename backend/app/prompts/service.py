from typing import Optional
from app.prompts.templates import (
    CLARIFIER_TEMPLATE,
    GENERATOR_TEMPLATE,
    EVALUATOR_TEMPLATE,
    REFINER_TEMPLATE
)

class PromptService:
    @staticmethod
    def get_clarification_prompt(user_input: str, interaction_language: str = "Spanish") -> str:
        """
        Renders the system prompt for the Clarifier Agent.
        """
        return CLARIFIER_TEMPLATE.format(
            user_input=user_input,
            interaction_language=interaction_language
        )

    @staticmethod
    def get_generation_prompt(
        clarified_requirements: str,
        prompt_type: str = "normal",
        target_language: str = "Spanish"
    ) -> str:
        """
        Renders the system prompt for the Generator Agent.
        """
        return GENERATOR_TEMPLATE.format(
            clarified_requirements=clarified_requirements,
            prompt_type=prompt_type,
            target_language=target_language
        )

    @staticmethod
    def get_evaluation_prompt(
        candidate_prompt: str,
        original_requirements: str,
        interaction_language: str = "Spanish"
    ) -> str:
        """
        Renders the system prompt for the Evaluator Agent.
        """
        return EVALUATOR_TEMPLATE.format(
            candidate_prompt=candidate_prompt,
            original_requirements=original_requirements,
            interaction_language=interaction_language
        )

    @staticmethod
    def get_refinement_prompt(
        original_prompt: str,
        evaluator_feedback: str,
        suggestions: str,
        target_language: str = "Spanish"
    ) -> str:
        """
        Renders the system prompt for the Refiner Agent.
        """
        return REFINER_TEMPLATE.format(
            original_prompt=original_prompt,
            evaluator_feedback=evaluator_feedback,
            suggestions=suggestions,
            target_language=target_language
        )
