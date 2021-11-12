import os
from os import getenv
from dotenv import load_dotenv

if os.path.exists("local.env"):
    load_dotenv("local.env")

load_dotenv()
admins = {}
SESSION_NAME = getenv("SESSION_NAME", "session")
BOT_TOKEN = getenv("BOT_TOKEN")
BOT_NAME = getenv("BOT_NAME", "Video Stream")
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
OWNER_NAME = getenv("OWNER_NAME", "dlwrml")
ALIVE_NAME = getenv("ALIVE_NAME", "Levina")
BOT_USERNAME = getenv("BOT_USERNAME", "veezvideobot")
ASSISTANT_NAME = getenv("ASSISTANT_NAME", "cleo_invida")
GROUP_SUPPORT = getenv("GROUP_SUPPORT", "VeezSupportGroup")
UPDATES_CHANNEL = getenv("UPDATES_CHANNEL", "levinachannel")
SUDO_USERS = list(map(int, getenv("SUDO_USERS").split()))
COMMAND_PREFIXES = list(getenv("COMMAND_PREFIXES", "/ ! .").split())
ALIVE_IMG = getenv("ALIVE_IMG", "https://telegra.ph/file/8aeb92cd7cfb176a403e0.jpg")
DURATION_LIMIT = int(getenv("DURATION_LIMIT", "60"))
IMG_1 = getenv("IMG_1", "https://telegra.ph/file/67b2184e9ab3dbd8c3b27.jpg")
IMG_2 = getenv("IMG_2", "https://telegra.ph/file/0999c47b06173cf040137.jpg")
IMG_3 = getenv("IMG_3", "https://telegra.ph/file/017c27e00f1484491072f.jpg")
IMG_4 = getenv("IMG_4", "https://telegra.ph/file/27be9a2b467e5a91ac818.jpg")
