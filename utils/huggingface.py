import json
import os
import io
from dotenv import load_dotenv
import requests
from PIL import Image
from datetime import datetime
import time
from config import Config
from utils.utils import get_env_var


class HuggingFaceAPI:
    REAL_VIS_XL_V4 = "https://api-inference.huggingface.co/models/SG161222/RealVisXL_V4.0"
    REAL_VIS_XL_V4_RECOMMENDED_PARAMS = {
        "negative_prompt": "face asymmetry, eyes asymmetry, deformed eyes, open mouth",

        "generation_parameters": {
            "sampling_steps": 25,
            "sampling_method": "DPM++ 2M Karras",

            "hires_fix": {
                "enabled": True,
                "steps": 10,
                "upscaler": "4x-UltraSharp",
                "denoising_strength": 0.3,
                "upscale_by": 1.5
            }
        }
    }

    @classmethod
    def generate_image_and_save(cls, endpoint, prompt, negative_prompt=None, parameters=None, notes=""):
        # build headers
        headers = cls.__get_headers()

        # build payload
        payload = {"inputs": prompt, "wait_for_model": True}
        if parameters:
            payload['parameters'] = parameters
        if negative_prompt:
            payload['parameters']['negative_prompt'] = negative_prompt

        # make request with retry
        image_bytes = cls.__post_with_retry(endpoint, headers, payload)

        # build file names for image and settings
        suffix = endpoint.split("/")[-1]
        # only keep alphanumeric characters
        suffix = ''.join(e for e in suffix if e.isalnum())
        file_name = cls.__get_output_path(suffix=suffix)
        file_name_image = f"{file_name}.jpg"
        file_name_settings = f"{file_name}.json"

        # save image
        image = Image.open(io.BytesIO(image_bytes))
        image.save(file_name_image)
        print('image saved to:', file_name_image)

        # save prompt and settings
        with open(file_name_settings, 'w') as f:
            log = {"payload": json.dumps(payload, indent=4)}
            if notes:
                log['notes'] = notes
            f.write(json.dumps(log, indent=4))

    @staticmethod
    def __get_output_path(suffix=""):
        load_dotenv(".env")
        user = os.getenv('USER_OUTPUT_PATH')
        if not user:
            raise Exception("USER_OUTPUT_PATH environment variable not set, set it in the .env file")

        # create folder if it does not exist
        folder_path = os.path.join(Config.OUTPUT_FOLDER_IMAGES, user)
        os.makedirs(folder_path, exist_ok=True)

        # create file name with timestamp
        file_name = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        file_name = f"{file_name}-{suffix}" if suffix else file_name

        return os.path.join(folder_path, file_name)

    @staticmethod
    def __get_headers(api_key=None):
        api_key = api_key if api_key else get_env_var("HUGGINGFACE_API_KEY", required=True)
        headers = {"Authorization": f"Bearer {api_key}"}
        return headers

    @staticmethod
    def __post_with_retry(endpoint, headers, payload, retry_wait=None, max_retries=None):
        retry_wait = retry_wait if retry_wait else Config.HUGGINGFACE_RETRY_WAIT
        max_retries = max_retries if max_retries else Config.MAX_HUGGINGFACE_RETRIES
        retries = 0
        while retries < max_retries:
            response = requests.post(endpoint, headers=headers, json=payload)
            if response.status_code == 200:
                return response.content
            print(f"Prompt: {payload.get('inputs', '')[:50]} | Attempt {retries + 1} | Response code {response.status_code} | retry in {retry_wait}s")
            print(f"\terror: {response.text}")
            retries += 1
            time.sleep(retry_wait)
        raise Exception(f"Failed to get a valid response after {max_retries} retries.")