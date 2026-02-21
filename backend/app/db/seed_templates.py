"""
Prompt Templates Seeding Script

This script populates the PromptTemplate table with initial templates
for system, image, and additional prompt types.
"""

import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from app.db.database import engine, get_db
from app.db.models import PromptTemplate


# System Prompt Templates
SYSTEM_TEMPLATES = [
    {
        "type": "system",
        "name": "Customer Support Bot",
        "description": "Professional customer service assistant for handling inquiries and resolving issues",
        "category": "customer-service",
        "tags": '["support", "professional", "helpful"]',
        "template_content": "You are a professional customer service assistant. Your role is to help customers with their inquiries, resolve their issues, and provide exceptional service. Always be polite, empathetic, and solution-oriented."
    },
    {
        "type": "system",
        "name": "Technical Assistant",
        "description": "Technical support specialist for complex problem-solving",
        "category": "technical",
        "tags": '["technical", "problem-solving", "detailed"]',
        "template_content": "You are a technical assistant specialized in problem-solving. Your role is to help users with technical issues, provide step-by-step solutions, and explain complex concepts clearly. Use precise language and include relevant technical details."
    },
    {
        "type": "system",
        "name": "Creative Writing Helper",
        "description": "Creative writing assistant for generating engaging content",
        "category": "creative",
        "tags": '["creative", "writing", "engaging"]',
        "template_content": "You are a creative writing assistant. Your role is to help users generate engaging, original, and well-structured content. Be imaginative, inspiring, and help users refine their ideas while maintaining their original intent."
    },
    {
        "type": "system",
        "name": "Data Analyst",
        "description": "Data analysis specialist for interpreting and presenting data insights",
        "category": "analytics",
        "tags": '["data", "analysis", "insights"]',
        "template_content": "You are a data analysis specialist. Your role is to help users interpret data, identify patterns, and present clear insights. Be methodical, thorough, and provide data-driven conclusions with appropriate visualizations or explanations."
    },
    {
        "type": "system",
        "name": "Code Reviewer",
        "description": "Code review specialist for providing constructive feedback on code quality",
        "category": "development",
        "tags": '["code", "review", "quality"]',
        "template_content": "You are a code review specialist. Your role is to provide constructive feedback on code quality, identify bugs, suggest improvements, and help developers write better code. Be thorough but supportive, focusing on best practices and maintainability."
    }
]

# Image Prompt Templates
IMAGE_TEMPLATES = [
    {
        "type": "image",
        "name": "Photorealistic Portrait",
        "description": "Generate lifelike portraits with professional photography quality",
        "category": "portrait",
        "tags": '["photorealistic", "portrait", "professional"]',
        "template_content": "Generate a photorealistic portrait of [SUBJECT], professional photography quality, studio lighting, sharp details, natural skin texture, 8K resolution, cinematic style."
    },
    {
        "type": "image",
        "name": "Fantasy Landscape",
        "description": "Create breathtaking fantasy landscapes with magical elements",
        "category": "landscape",
        "tags": '["fantasy", "landscape", "magical"]',
        "template_content": "Create a breathtaking fantasy landscape featuring [ELEMENTS], magical glowing particles, dramatic lighting, volumetric fog, epic scale, ultra-detailed, digital art style, trending on ArtStation, 4K resolution."
    },
    {
        "type": "image",
        "name": "Logo Design",
        "description": "Design modern, clean logos for brands and businesses",
        "category": "design",
        "tags": '["logo", "modern", "minimalist"]',
        "template_content": "Design a modern, clean logo for [BRAND/COMPANY], minimalist style, vector art, bold typography, professional aesthetic, centered composition, white background, high contrast."
    },
    {
        "type": "image",
        "name": "Product Photography",
        "description": "Professional product photography with studio lighting",
        "category": "product",
        "tags": '["product", "photography", "studio"]',
        "template_content": "Professional product photography of [PRODUCT], studio lighting, soft shadows, clean white background, high detail, commercial quality, 8K resolution, macro lens effect."
    },
    {
        "type": "image",
        "name": "Character Illustration",
        "description": "Stylized character illustrations with distinctive personality",
        "category": "character",
        "tags": '["character", "illustration", "stylized"]',
        "template_content": "Create a stylized character illustration of [CHARACTER DESCRIPTION], distinctive personality, vibrant colors, clean lines, flat design style, expressive pose, professional illustration quality, suitable for UI or print."
    }
]

# Additional Prompt Templates
ADDITIONAL_TEMPLATES = [
    {
        "type": "additional",
        "name": "Add More Detail",
        "description": "Enhance the prompt with additional details and specifics",
        "category": "enhancement",
        "tags": '["detail", "enhancement", "specificity"]',
        "template_content": "Please enhance the following prompt by adding more details, specifics, and comprehensive instructions: [ORIGINAL PROMPT]"
    },
    {
        "type": "additional",
        "name": "Simplify Language",
        "description": "Rewrite the prompt using simpler, more accessible language",
        "category": "simplification",
        "tags": '["simplify", "clarity", "accessibility"]',
        "template_content": "Please rewrite the following prompt using simpler, more accessible language while maintaining the original intent: [ORIGINAL PROMPT]"
    },
    {
        "type": "additional",
        "name": "Make More Professional",
        "description": "Refine the prompt to sound more professional and formal",
        "category": "professional",
        "tags": '["professional", "formal", "refinement"]',
        "template_content": "Please refine the following prompt to sound more professional, formal, and business-appropriate while maintaining the original intent: [ORIGINAL PROMPT]"
    },
    {
        "type": "additional",
        "name": "Add Examples",
        "description": "Enhance the prompt with relevant examples",
        "category": "examples",
        "tags": '["examples", "clarification", "few-shot"]',
        "template_content": "Please enhance the following prompt by adding relevant examples to clarify expectations: [ORIGINAL PROMPT]"
    },
    {
        "type": "additional",
        "name": "Improve Clarity",
        "description": "Rewrite the prompt to be clearer and more unambiguous",
        "category": "clarity",
        "tags": '["clarity", "unambiguous", "refinement"]',
        "template_content": "Please rewrite the following prompt to be clearer, more precise, and eliminate any ambiguity while maintaining the original intent: [ORIGINAL PROMPT]"
    }
]


def seed_templates():
    """Seed the database with initial templates."""
    db = next(get_db())

    try:
        # Check if templates already exist
        existing_count = db.query(PromptTemplate).count()

        if existing_count > 0:
            print(f"Database already contains {existing_count} templates. Skipping seeding.")
            return

        # Combine all templates
        all_templates = SYSTEM_TEMPLATES + IMAGE_TEMPLATES + ADDITIONAL_TEMPLATES

        # Add templates to database
        for template_data in all_templates:
            template = PromptTemplate(
                type=template_data["type"],
                name=template_data["name"],
                description=template_data["description"],
                template_content=template_data["template_content"],
                category=template_data["category"],
                tags=template_data["tags"],
                is_public=True,
                usage_count=0
            )
            db.add(template)

        db.commit()

        print(f"✅ Successfully seeded {len(all_templates)} templates:")
        print(f"   - {len(SYSTEM_TEMPLATES)} system prompt templates")
        print(f"   - {len(IMAGE_TEMPLATES)} image prompt templates")
        print(f"   - {len(ADDITIONAL_TEMPLATES)} additional prompt templates")

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding templates: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    print("Starting template seeding...")
    seed_templates()
    print("Seeding complete!")
