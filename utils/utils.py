import os

from dotenv import load_dotenv


def get_env_var(env_var_name, required=False):
    load_dotenv(".env")
    env_var_value = os.getenv(env_var_name, default=None)
    if not env_var_value and required:
        raise Exception(f"{env_var_name} environment variable not set, set it in the .env file")
    return env_var_value
