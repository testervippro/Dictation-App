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
    m = re.match(r"(\d+)", filename)
    return int(m.group(1)) if m else 0

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
<title>Dictation</title>

<style>
body {{
    font-family: Inter, system-ui;
    background:#f7f7f8;
    display:flex;
    justify-content:center;
    padding:30px;
}}

.container {{
    width:520px;
    background:white;
    padding:24px;
    border-radius:16px;
    box-shadow:0 8px 30px rgba(0,0,0,0.05);
}}

h3 {{
    text-align:center;
    margin-bottom:5px;
}}

.note {{
    text-align:center;
    font-size:13px;
    color:#888;
    margin-bottom:15px;
}}

select {{
    width:100%;
    padding:10px;
    border-radius:10px;
    border:1px solid #ddd;
    margin-bottom:10px;
}}

.progress {{
    height:6px;
    background:#eee;
    border-radius:999px;
    overflow:hidden;
    margin-bottom:10px;
}}

.bar {{
    height:100%;
    background:#111;
    width:0%;
}}

#progressText {{
    text-align:center;
    font-size:13px;
    margin-bottom:10px;
}}

input {{
    width:100%;
    padding:14px;
    border-radius:10px;
    border:1px solid #ddd;
    text-align:center;
    margin-bottom:10px;
}}

.correct {{
    border-color:#2ecc71;
    background:#f6fff8;
}}

.controls {{
    display:flex;
    justify-content:space-between;
    font-size:13px;
    margin-bottom:10px;
}}

.buttons {{
    display:flex;
    gap:8px;
    margin-top:10px;
}}

button {{
    flex:1;
    padding:10px;
    border:none;
    border-radius:10px;
    background:#f2f2f2;
    cursor:pointer;
}}

button.primary {{
    background:#111;
    color:white;
}}

#result {{
    text-align:center;
    margin-top:10px;
    font-weight:500;
}}

.diff {{
    text-align:center;
    margin-top:10px;
    font-size:14px;
}}

.correct-word {{ color:#2ecc71; }}
.wrong-word {{ color:red; text-decoration:line-through; }}
.suggest-word {{ color:#111; font-weight:bold; }}

</style>
</head>

<body>

<div class="container">

<h3>🎧 Dictation</h3>

<div class="note">
Auto Next overrides Auto Repeat
</div>

<!-- ✅ PART SELECT -->
<select id="partSelect" onchange="changePart(this.value)">
    <option value="p1">Part 1</option>
    <option value="p2">Part 2</option>
    <option value="p3">Part 3</option>
    <option value="p4">Part 4</option>
</select>

<div id="progressText"></div>

<div class="progress">
<div id="bar" class="bar"></div>
</div>

<input id="jump" placeholder="Jump (e.g. 228)" onkeypress="if(event.key==='Enter') jumpTo()">

<input id="input" placeholder="Type what you hear..." autofocus>

<div id="result"></div>
<div id="diffBox" class="diff"></div>

<div class="controls">
<label><input type="checkbox" id="autoNext" checked> Auto Next</label>
<label><input type="checkbox" id="autoLoop"> Loop</label>
</div>

<div class="buttons">
<button onclick="preview()">←</button>
<button class="primary" onclick="play()">Play</button>
<button onclick="next()">→</button>
</div>

<div class="buttons">
<button onclick="checkAnswer()">Check</button>
<button onclick="showAnswer()">Answer</button>
</div>

</div>

<script>
const audioFiles = {json.dumps(audio_files)};
const folder = "{folder}";
const part = "{part}";

// set dropdown đúng part
document.getElementById("partSelect").value = part;

let index = parseInt(localStorage.getItem(part+"_idx")) || 0;

const player = new Audio();
const input = document.getElementById("input");

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
function compareText(user, correct) {{
    const u = user.split(" ");
    const c = correct.split(" ");

    let out = "";

    for(let i=0;i<Math.max(u.length,c.length);i++) {{
        if(u[i] === c[i]) {{
            out += `<span class="correct-word">${{c[i]||""}}</span> `;
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
        result.innerText = "Correct";
        input.classList.add("correct");

        if(autoNext.checked) setTimeout(next,500);
    }} else {{
        result.innerText = "Wrong";
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
    if(index>0) index--, load();
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
    result.innerText = getAnswer();
}}

function changePart(p) {{
    window.location.href = `/?part=${{p}}`;
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
    app.run(host="0.0.0.0", port=5001)