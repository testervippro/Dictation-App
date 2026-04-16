import os
import json
import subprocess
import sys
import re
from pydub import AudioSegment


# ===== CLEAN TEXT =====
def clean_text(text):
    text = text.strip()
    text = re.sub(r'[\\/:*?"<>|]', '', text)
    text = re.sub(r'\s+', '_', text)
    return text[:50]  # tránh tên file quá dài


# ===== MAIN PROCESS =====
def process_audio(audio_file):
    base_name = os.path.splitext(audio_file)[0].lower()

    # ===== FOLDER OUTPUT =====
    output_folder = f"data_audio/{base_name}"
    os.makedirs(output_folder, exist_ok=True)

    # ===== 1. RUN WHISPER =====
    print(f"▶ Running whisper on {audio_file}...")
    subprocess.run([
        "whisper_timestamped",
        audio_file,
        "--model", "base",
        "--language", "en",
        "--output_format", "json",
        "--output_dir", "."
    ], check=True)

    # ===== 2. LOAD JSON =====
    json_file = f"{audio_file}.words.json"

    if not os.path.exists(json_file):
        print(f"❌ JSON not found: {json_file}")
        return

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # ===== 3. FILTER SEGMENTS =====
    segments = [
        {
            "id": i,
            "start": seg["start"],
            "end": seg["end"],
            "text": seg["text"].strip()
        }
        for i, seg in enumerate(data["segments"], 1)
    ]

    segments = sorted(segments, key=lambda x: x["start"])

    # ===== 4. SAVE CLEAN JSON =====
    json_output = os.path.join(output_folder, f"{base_name}_segments.json")

    with open(json_output, "w", encoding="utf-8") as f:
        json.dump(segments, f, ensure_ascii=False, indent=2)

    print(f"✅ Saved JSON: {json_output}")

    # ===== 5. CUT AUDIO =====
    audio = AudioSegment.from_file(audio_file)

    for seg in segments:
        start_ms = int(seg["start"] * 1000)
        end_ms = int(seg["end"] * 1000)

        chunk = audio[start_ms:end_ms]

        name = clean_text(seg["text"])
        audio_path = os.path.join(
            output_folder,
            f"{seg['id']}_{name}.mp3"
        )

        chunk.export(audio_path, format="mp3")

        print(f"🎧 Saved: {audio_path}")

    print("🚀 Done!")


# ===== RUN =====
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py audio.mp3")
    else:
        process_audio(sys.argv[1])