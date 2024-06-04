import os

from openai import OpenAI
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY_OPEN_WEB_UI"))

response = client.images.generate(
  model="dall-e-3",
  prompt="""Main subject: A person sitting at a modern desk setup, intensely focused on a laptop.

Setting or background: The image is set in a bright and modern home office. The desk is organized with minimal clutter, featuring a sleek laptop, a cup of coffee, and perhaps a tablet beside it. The background includes a large window with sunlight streaming in, enhancing the vibrant atmosphere.

Colours: The dominant colors are neutral and bright tones—white, beige, and light grey, with the laptop and coffee cup adding subtle shades of metallic and warm brown.

Emotion: The image conveys a sense of productivity and efficiency, with the person's expression indicating focused concentration as large files are quickly downloaded.
  """,
  n=1,
  size="1024x1024"
)
breakpoint()
