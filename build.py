import os
import json
import re

AUDIO_BASE = "data_audio"

PART_FOLDERS = {
    "p1": "toeic_audio_p1ets2020",
    "p2": "toeic_audio_p2ets2020",
    "p3": "toeic_audio_p3ets2020",
    "p4": "toeic_audio_p4ets2020",
}

def natural_sort_key(filename):
    m = re.match(r"(\d+)", filename)
    return int(m.group(1)) if m else 0

data = {}

for part, folder in PART_FOLDERS.items():
    path = os.path.join(AUDIO_BASE, folder)

    if not os.path.exists(path):
        continue

    files = [
    f for f in os.listdir(path)
    if f.endswith(".mp3") and re.match(r"^\d+.*\.mp3$", f)
]

    files.sort(key=natural_sort_key)

    data[part] = {
        "folder": f"data_audio/{folder}",
        "files": files
    }

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# inject data
html = html.replace("__DATA__", json.dumps(data, ensure_ascii=False))

# ghi đè lại chính nó
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ Done")