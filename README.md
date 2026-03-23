# TOEIC Listening Transcription App

## Overview
This repository is a transcription app for TOEIC Listening (ETS 2020 set). Users can listen to audio segments and edit transcriptions (dictation correction) with provided text transcripts.

## Prerequisites
- Python 3.9+ (3.11 recommended)
- Virtual environment tool (venv)

## Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

## Usage
1. Inspect the dataset:
   - Audio: `data_audio/toeic_audio_p1ets2020`, `p2`, `p3`, `p4`
   - Text: `p1ets2020_clean.txt`, ...

2. Run your script (example):
```bash
python app.py
```

3. Add more notes or custom command usage in code or this README.

## Git
Repository is already initialized with a starting commit.

## Files
- `app.py`: main application logic (if any)
- `requirements.txt`: installed Python dependencies

