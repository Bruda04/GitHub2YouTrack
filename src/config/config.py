# Configuration module to load environment variables for GitHub and YouTrack integration.
from dotenv import load_dotenv
import os
from . import consts
load_dotenv()

GITHUB_TOKEN = os.getenv(consts.GITHUB_TOKEN_ENV_NAME)
GITHUB_REPOSITORY_NAME = os.getenv(consts.GITHUB_REPOSITORY_NAME_ENV_NAME)
GITHUB_REPOSITORY_OWNER = os.getenv(consts.GITHUB_REPOSITORY_OWNER_ENV_NAME)
GITHUB_REPOSITORY_PATH = f"{GITHUB_REPOSITORY_OWNER}/{GITHUB_REPOSITORY_NAME}"

YOUTRACK_URL = os.getenv(consts.YOUTRACK_URL_ENV_NAME)
YOUTRACK_TOKEN = os.getenv(consts.YOUTRACK_TOKEN_ENV_NAME)
YOUTRACK_PROJECT_SHORT_NAME = os.getenv(consts.YOUTRACK_PROJECT_SHORT_NAME_ENV_NAME)