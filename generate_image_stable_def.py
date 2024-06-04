import os
import requests
import time
import io
from PIL import Image

API_URL = "https://api-inference.huggingface.co/models/SG161222/RealVisXL_V4.0"
headers = {"Authorization": f"Bearer {os.environ.get('HUGGING')}"}


def query(payload, max_retries=5, time_delta=2):
    retries = 0
    while retries < max_retries:
        response = requests.post(API_URL, headers=headers, json=payload)
        print(f"Attempt {retries + 1}: Response code {response.status_code}")
        if response.status_code == 200:
            return response.content
        retries += 1
        time.sleep(time_delta)
    raise Exception(f"Failed to get a valid response after {max_retries} retries.")


def generate_and_save_image(prompt, save_path, max_retries=5, time_delta=2):
    payload = {"inputs": prompt, "wait_for_model": True}
    try:
        image_bytes = query(payload, max_retries=max_retries, time_delta=time_delta)
        image = Image.open(io.BytesIO(image_bytes))
        image.save(save_path)
        print(f"Image saved to {save_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
generate_and_save_image("""The main subject:
The main subject of the image is a young man who appears to be in his twenties or thirties. He is standing outdoors, leaning against a building, and is smiling broadly. He is holding a smartphone in his right hand and has a backpack slung over his left shoulder. He is also wearing wireless earbuds.

Setting or background:
The image is set in an urban environment, likely on a city street. The background includes a sidewalk, a row of parked cars, and several buildings. There are also some people walking in the background, and the street appears to be bustling with activity. The buildings have a mix of architectural styles, and there is a clear blue sky visible above.

Colours:
The dominant colors in the image are warm and neutral tones. The young man is wearing a mustard yellow jacket over a white shirt, and his backpack is a dark color, possibly black or navy blue. The buildings and cars in the background are in various shades of white, gray, and beige. The sky is a bright blue, adding a touch of vibrancy to the scene.

Emotion:
The image conveys a positive and cheerful emotion. The young man’s broad smile and relaxed posture suggest that he is happy and possibly enjoying a pleasant moment or conversation on his phone.

Details:
- The young man has a neatly trimmed beard and short curly hair.
- He is wearing a mustard yellow jacket with a button-up front.
- His smartphone appears to be a modern model, possibly an iPhone, given its sleek design.
- The wireless earbuds are white, which is a common color for popular brands like Apple AirPods.
- The backpack has a simple design with a single strap visible over his shoulder.
- The street is lined with parked cars, and there are a few people walking in the background, adding to the urban atmosphere.
- The building he is leaning against has large windows, and the sidewalk is clean and well-maintained.
""", 'output_image.png')
