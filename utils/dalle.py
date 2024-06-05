import os

from dotenv import load_dotenv
from openai import OpenAI

from utils.utils import get_env_var


class DallE:
    @classmethod
    def generate_image_and_save(cls, prompt, parameters=None):
        api_key = get_env_var("OPENAI_API_KEY", required=True)
        client = OpenAI(api_key)

        kwargs = {
            "model": "dall-e-3",
            "prompt": """Main subject: A person sitting at a modern desk setup, intensely focused on a laptop.""",
            "n": 1,  # number of images to generate
            "size": "1792x1024",  # 1024x1024, 1792x1024, 1024x1792
            "quality": "standard",  # "standard" or "hd"
            "response_format": "url",
            "style": "natural",  # "natural" or "vivid"
        }

        response = client.images.generate(**kwargs)

