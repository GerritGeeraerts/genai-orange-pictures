from pprint import pprint

from utils.huggingface import HuggingFaceAPI

# Simple
HuggingFaceAPI.generate_image_and_save(
    HuggingFaceAPI.REAL_VIS_XL_V4,
    "Generate a realistic image of a futuristic city at night.",
    parameters=HuggingFaceAPI.REAL_VIS_XL_V4_RECOMMENDED_PARAMS
)

# Complex
HuggingFaceAPI.generate_image_and_save(
    HuggingFaceAPI.REAL_VIS_XL_V4,
    "Generate a realistic image a spaceship flying through a nebula.",
    parameters={
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
)

# Loop
prompts = ['image of an orange', 'image of a banana']
for prompt in prompts:
    HuggingFaceAPI.generate_image_and_save(
        HuggingFaceAPI.REAL_VIS_XL_V4,
        prompt,
        parameters=HuggingFaceAPI.REAL_VIS_XL_V4_RECOMMENDED_PARAMS
    )


# with open("./data/output/original_images_description.md", "r") as output_file:
#     contents = output_file.read()
#     descriptions = contents.split('#')
#     for desc in descriptions:
#         lines = desc.split('\n')
#         desc = '\n'.join(lines[1:-2])
#         HuggingFaceAPI.generate_image_and_save(
#             HuggingFaceAPI.REAL_VIS_XL_V4,
#             desc,
#             parameters=HuggingFaceAPI.REAL_VIS_XL_V4_RECOMMENDED_PARAMS,
#             notes="original orange picture descriptions"
#         )
