import os
import re
from pydub import AudioSegment

# --- Configuration ---
input_txt = 'p1ets2020_clean.txt'
input_audio = 'P1.mp3'
output_folder = 'toeic_audio_p1ets2020'

# Create directory if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Load the original audio file
print(f"Loading {input_audio}...")
audio = AudioSegment.from_file(input_audio)

# Regex to extract [start - end] and text
pattern = re.compile(r"\[\s*([\d.]+)s\s*-\s*([\d.]+)s\]\s*(.*)")

def clean_filename(text):
    """Remove special characters to create safe filenames"""
    # Replace spaces with underscores, remove periods, commas, question marks
    clean = re.sub(r'[^\w\s-]', '', text).strip().replace(" ", "_")
    return clean

with open(input_txt, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        match = pattern.search(line)
        if match:
            start_s = float(match.group(1))
            end_s = float(match.group(2))
            original_text = match.group(3).strip()

            # Convert to milliseconds and add 100ms buffer
            start_ms = max(0, (start_s - 0.1) * 1000)
            end_ms = (end_s + 0.1) * 1000

            # Create filename: STT_Content.mp3 (example: 003_A_woman_is_painting.mp3)
            name_part = clean_filename(original_text)
            filename = f"{i+1:03d}_{name_part}.mp3"
            filepath = os.path.join(output_folder, filename)

            # Cut and export file
            segment = audio[start_ms:end_ms]
            segment.export(filepath, format="mp3")
            
            print(f"Saved: {filename}")

print(f"\n--- DONE! All audio files are in the folder: {output_folder} ---")