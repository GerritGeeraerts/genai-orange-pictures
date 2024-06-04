import os

import openai
from PIL import Image
import base64
import io

# Provide your OpenAI API key
api_key = os.environ.get("OPENAI_API_KEY_OPEN_WEB_UI")


def encode_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def describe_image(image_path):
    # Load and encode the image
    with open(image_path, "rb") as img_file:
        image_binary = img_file.read()
        base64_encoded_image = base64.b64encode(image_binary).decode('utf-8')

    prompt = """
    Describe the original image in great detail:
    The main subject: What is the main object or entity the image revolves around?
    Setting or background: Where is the image set? What is in the background?
    Colours: What are the dominant colors in the image?
    Emotion: Does the image convey any particular emotion?
    Details: Are there unique or specific details that the image contains?
    """

    # Interact with OpenAI's API
    from openai import OpenAI
    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_encoded_image}"
                        }
                    },
                    {
                        "type": "text",
                        "text": "Describe the original image in great detail: The main subject: What is the main object or entity the image revolves around? Setting or background: Where is the image set? What is in the background? Colours: What are the dominant colors in the image? Emotion: Does the image convey any particular emotion? Details: Are there unique or specific details that the image contains?"
                    }
                ]
            },
        ],
        temperature=0.2,
        max_tokens=1087,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].message.content


# Get the current working directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(script_dir, "data/original")
output_file_path = os.path.join(script_dir, 'output.txt')

# Check if the directory exists
if os.path.exists(data_dir):
    with open(output_file_path, 'a') as output_file:  # Open the file in append mode
        for file in os.listdir(data_dir):
            file_path = os.path.join(data_dir, file)
            # Get the description
            description = describe_image(file_path)
            # Write the file path and description to the output file
            output_file.write(f"# {file}\n")
            output_file.write(f"{description}\n")
            output_file.write("--------------------------------------------------------------------\n")
            # Print to console (optional)
            print(file_path)
            print(description)
else:
    print(f"Directory '{data_dir}' does not exist.")
