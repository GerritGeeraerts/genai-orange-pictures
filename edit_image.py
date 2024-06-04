import os
from openai import OpenAI
from PIL import Image

# Load the image
image_path = "/home/gg/PycharmProjects/stable/img-57jHquJ93WFExLyDp6YvQl4G.png"
# Ensure the path exists
if not os.path.exists(image_path):
    raise FileNotFoundError(f"The image path '{image_path}' does not exist.")

image = Image.open(image_path)

# Convert the image to RGBA format if it's not already
if image.mode != 'RGBA':
    image = image.convert('RGBA')

# Save the converted image to a temporary file
temp_image_path = "/home/gg/PycharmProjects/stable/temp_img.png"
image.save(temp_image_path)

# Initialize the OpenAI client
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY_OPEN_WEB_UI"))

# Call the OpenAI API with the converted image
response = client.images.edit(
  image=open(temp_image_path, "rb"),
  prompt="Edit the image to change the orange jacket to a blue jacket",
  n=1,
  size="1024x1024"
)
print(response)

# Access the edited image from the response
edited_image_path = "/home/gg/PycharmProjects/stable/edited_image.png"
with open(edited_image_path, "wb") as f:
    f.write(response['data'][0]['image'])

print(f"Edited image saved to: {edited_image_path}")