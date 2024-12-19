from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv(".env")


def get(name: str):
    return os.getenv(name)
