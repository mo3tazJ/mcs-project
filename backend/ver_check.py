
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


try:
    latest_file_path = BASE_DIR / 'latest.txt'
    # print(latest_file_path)
    with open(latest_file_path) as f:
        line = f.readline()
    latest_version = line
    # print(latest_version)
    latest_version_link = f"https://mcsproject.pythonanywhere.com/static/backend/apk/ITMS{latest_version}.apk"
except Exception as e:
    latest_version = "X"
    latest_version_link = f"https://mcsproject.pythonanywhere.com"
    print(e)
