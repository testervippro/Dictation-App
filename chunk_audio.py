from flask import Flask, send_from_directory, request
import os, json, re

app = Flask(__name__)

AUDIO_BASE = "data_audio"

PART_FOLDERS = {
    "p1": "toeic_audio_p1ets2020",
    "p2": "toeic_audio_p2ets2020",
    "p3": "toeic_audio_p3ets2020",
    "p4": "toeic_audio_p4ets2020",
}

def natural_sort_key(filename):
    match = re.match(r"(\d+)", filename)
    return int(match.group(1)) if match else 0

def get_audio_files(part):
    folder = PART_FOLDERS.get(part, PART_FOLDERS["p1"])
    path = os.path.join(AUDIO_BASE, folder)

    if not os.path.exists(path):
        return [], folder

    files = [f for f in os.listdir(path) if f.endswith(".mp3")]
    files.sort(key=natural_sort_key)
    return files, folder


@app.route("/")
def index():
    part = request.args.get("part", "p1")
    audio_files, folder = get_audio_files(part)

    return f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>TOEIC Dictation Pro</title>

<style>
body {{
    font-family: system-ui;
    background:#f0f2f5;
    display:flex;
    justify-content:center;
    padding:20px;
}}

.container {{
    width:650px;
    background:white;
    padding:25px;
    border-radius:12px;
}}

.note {{
    background:#f8f9fa;
    border-left:4px solid #1877f2;
    padding:10px;
    margin-bottom:10px;
}}

.bar {{
    height:10px;
    background:#1877f2;
    margin-bottom:10px;
}}

input {{
    width:100%;
    padding:12px;
    margin:10px 0;
    text-align:center;
}}

.correct {{
    background:#eaffea;
}}

.diff {{
    text-align:center;
    margin-top:10px;
    font-size:16px;
}}

.correct-word {{ color:green; font-weight:bold; }}
.wrong-word {{ color:red; text-decoration:line-through; }}
.suggest-word {{ color:#1877f2; font-weight:bold; }}

button {{
    margin:5px;
    padding:10px;
}}
</style>
</head>

<body>
<div class="container">

<h3>🎧 TOEIC Dictation</h3>

<div class="note">
🚀 Auto Next takes priority over Auto Repeat
</div>

<div id="progressText"></div>
<div id="bar" class="bar"></div>

<input id="jump" placeholder="Jump (vd: 228)" onkeypress="if(event.key==='Enter') jumpTo()">

<div>
<label><input type="checkbox" id="autoNext" checked> Auto Next</label>
<label><input type="checkbox" id="autoLoop"> Auto Repeat</label>
<label><input type="checkbox" id="manualCheck"> Check Mode</label>
</div>

<audio id="player"></audio>

<input id="input" placeholder="Type what you hear...">

<div id="result"></div>
<div id="diffBox" class="diff"></div>

<div>
<button onclick="preview()">Preview</button>
<button onclick="play()">Play</button>
<button onclick="next()">Next</button>
<button onclick="checkAnswer()">Check</button>
<button onclick="showAnswer()">Answer</button>
</div>

</div>

<script>
const audioFiles = {json.dumps(audio_files)};
const folder = "{folder}";
const part = "{part}";

let index = parseInt(localStorage.getItem(part+"_idx")) || 0;

const player = document.getElementById("player");
const input = document.getElementById("input");

// =========================
// ANSWER lấy từ filename
// =========================
function getAnswer() {{
    return audioFiles[index]
        .substring(4)
        .replace(".mp3","")
        .replace(/_/g," ");
}}

function normalize(t) {{
    return t.toLowerCase().replace(/[^\\w\\s]/g,"").trim();
}}

// =========================
function load() {{
    if(index >= audioFiles.length) index = 0;

    localStorage.setItem(part+"_idx", index);

    progressText.innerText = `Câu ${{index+1}} / ${{audioFiles.length}}`;
    bar.style.width = `${{(index+1)/audioFiles.length*100}}%`;

    player.src = `/data_audio/${{folder}}/${{audioFiles[index]}}`;

    input.value = "";
    input.classList.remove("correct");
    result.innerText = "";
    diffBox.innerHTML = "";

    player.play();
}}

// =========================
// 🔥 SO SÁNH ANSWER
// =========================
function compareText(user, correct) {{
    const u = user.split(" ");
    const c = correct.split(" ");

    let out = "";

    for(let i=0;i<Math.max(u.length, c.length);i++) {{
        if(u[i] === c[i]) {{
            out += `<span class="correct-word">${{c[i] || ""}}</span> `;
        }} else {{
            if(u[i]) out += `<span class="wrong-word">${{u[i]}}</span> `;
            if(c[i]) out += `<span class="suggest-word">${{c[i]}}</span> `;
        }}
    }}

    return out;
}}

// =========================
function checkAnswer() {{
    const user = normalize(input.value);
    const correct = normalize(getAnswer());

    diffBox.innerHTML = compareText(user, correct);

    if(user === correct) {{
        result.innerText = "✅ Correct";
        input.classList.add("correct");

        if(autoNext.checked) setTimeout(next,500);
    }} else {{
        result.innerText = "❌ Wrong";
    }}
}}

// =========================
input.addEventListener("input", () => {{

    if(manualCheck.checked) return;

    if(normalize(input.value) === normalize(getAnswer())) {{
        input.classList.add("correct");

        if(autoNext.checked) setTimeout(next,400);
    }}
}});

// =========================
player.onended = () => {{
    if(autoNext.checked) return setTimeout(next,700);
    if(autoLoop.checked) player.play();
}};

// =========================
function jumpTo() {{
    const v = parseInt(jump.value);
    if(!v || v<1 || v>audioFiles.length) return;

    index = v-1;
    load();
}}

function preview() {{
    if(index>0) {{ index--; load(); }}
}}

function next() {{
    index++;
    load();
}}

function play() {{
    player.currentTime = 0;
    player.play();
}}

function showAnswer() {{
    result.innerText = "Answer: " + getAnswer();
}}

window.onload = load;
</script>

</body>
</html>
"""

@app.route("/data_audio/<path:folder>/<path:filename>")
def serve_audio(folder, filename):
    return send_from_directory(os.path.join(os.getcwd(), AUDIO_BASE, folder), filename)

if __name__ == "__main__":
    app.run(debug=True, port=5001)