import base64
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Flappy Bird", page_icon="🐦")
st.title("🐦 Flappy Bird")
st.caption("SPACE hoặc chuột trái để bay. Nhấn R để chơi lại.")

# Đọc ảnh chim trong repository
bird_path = Path(__file__).parent / "bird.png"
bird_data = ""

if bird_path.exists():
    bird_data = base64.b64encode(bird_path.read_bytes()).decode("utf-8")

html = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {margin:0;background:#70d6f5;font-family:Arial;text-align:center}
canvas {width:100%;max-width:480px;height:auto;display:block;
        margin:auto;border:3px solid #fff;border-radius:8px;
        touch-action:manipulation}
button {padding:12px 28px;margin:10px;font-size:18px;font-weight:bold;
        background:#ffcf32;border:3px solid #69452f;border-radius:10px;
        cursor:pointer}
p {color:#173b54;font-weight:bold}
</style>
</head>
<body>
<canvas id="game" width="480" height="600"></canvas>
<br>
<button id="restart">BẮT ĐẦU / CHƠI LẠI</button>
<p>SPACE / ↑ / chuột trái: Bay lên &nbsp; | &nbsp; R: Chơi lại</p>

<script>
const canvas = document.getElementById("game");
const ctx = canvas.getContext("2d");
const W = 480, H = 600;

const birdImage = new Image();
birdImage.src = "data:image/png;base64,IMAGE_DATA";
const hasBirdImage = "IMAGE_DATA" !== "";

let bird, pipes, score, best = 0, started = false, over = false;
let frame = 0, audio = null;

function sound(freq, duration, type="sine", volume=0.045) {
  try {
    audio = audio || new (window.AudioContext || window.webkitAudioContext)();
    if (audio.state === "suspended") audio.resume();
    const osc = audio.createOscillator();
    const gain = audio.createGain();
    osc.type = type;
    osc.frequency.value = freq;
    gain.gain.setValueAtTime(volume, audio.currentTime);
    gain.gain.exponentialRampToValueAtTime(
      0.001, audio.currentTime + duration
    );
    osc.connect(gain);
    gain.connect(audio.destination);
    osc.start();
    osc.stop(audio.currentTime + duration);
  } catch(e) {}
}

function reset() {
  bird = {x:115, y:280, vy:0, size:38};
  pipes = [];
  score = 0;
  frame = 0;
  started = true;
  over = false;
  flap();
}

function flap() {
  if (!started || over) return;
  bird.vy = -5.1;
  sound(520, 0.07, "square", 0.025);
}

function control() {
  if (!started || over) reset();
  else flap();
}

document.getElementById("restart").onclick = reset;
canvas.addEventListener("pointerdown", control);
document.addEventListener("keydown", e => {
  if (["Space","ArrowUp","KeyR"].includes(e.code)) e.preventDefault();
  if (e.code === "KeyR") reset();
  else if (e.code === "Space" || e.code === "ArrowUp") control();
});

function drawBird() {
  ctx.save();
  ctx.translate(bird.x, bird.y);
  ctx.rotate(Math.max(-0.35, Math.min(0.65, bird.vy * 0.045)));

  if (hasBirdImage && birdImage.complete && birdImage.naturalWidth) {
    ctx.drawImage(birdImage, -25, -25, 50, 50);
  } else {
    // Chim dự phòng nếu chưa tải bird.png
    ctx.fillStyle = "#ffdc24";
    ctx.strokeStyle = "#513047";
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.arc(0,0,18,0,Math.PI*2);
    ctx.fill(); ctx.stroke();
    ctx.fillStyle = "white";
    ctx.beginPath(); ctx.arc(7,-6,7,0,Math.PI*2); ctx.fill();
    ctx.fillStyle = "black";
    ctx.beginPath(); ctx.arc(9,-6,3,0,Math.PI*2); ctx.fill();
    ctx.fillStyle = "#ff674b";
    ctx.fillRect(12,1,18,7);
  }
  ctx.restore();
}

function drawPipe(p) {
  const gap = p.gap;
  const bottom = p.top + gap;
  ctx.fillStyle = "#35c943";
  ctx.strokeStyle = "#12662b";
  ctx.lineWidth = 4;
  ctx.fillRect(p.x, 0, 65, p.top);
  ctx.strokeRect(p.x, -2, 65, p.top+2);
  ctx.fillRect(p.x-5, p.top-20, 75, 20);
  ctx.strokeRect(p.x-5, p.top-20, 75, 20);

  ctx.fillRect(p.x, bottom, 65, H-bottom-45);
  ctx.strokeRect(p.x, bottom, 65, H-bottom-45);
  ctx.fillRect(p.x-5, bottom, 75, 20);
  ctx.strokeRect(p.x-5, bottom, 75, 20);
}

function text(txt, y, size, color="white") {
  ctx.textAlign = "center";
  ctx.font = `bold ${size}px Arial`;
  ctx.lineWidth = 4;
  ctx.strokeStyle = "#473047";
  ctx.strokeText(txt, W/2, y);
  ctx.fillStyle = color;
  ctx.fillText(txt, W/2, y);
}

function loop() {
  frame++;
  ctx.clearRect(0,0,W,H);

  // Bầu trời
  ctx.fillStyle = "#70d6f5";
  ctx.fillRect(0,0,W,H);
  ctx.fillStyle = "#fff";
  [[65,95],[360,130],[270,65]].forEach(([x,y]) => {
    ctx.beginPath();
    ctx.arc(x,y,15,0,Math.PI*2);
    ctx.arc(x+18,y-8,20,0,Math.PI*2);
    ctx.arc(x+38,y,15,0,Math.PI*2);
    ctx.fill();
  });

  if (started && !over) {
    bird.vy += 0.22;
    bird.y += bird.vy;

    // Ống xuất hiện thưa hơn, khe rộng hơn để dễ chơi
    if (frame % 125 === 0) {
      pipes.push({
        x: W+10,
        top: 70 + Math.random()*200,
        gap: 205,
        passed: false
      });
    }

    for (const p of pipes) {
      p.x -= 2.0;

      const bx = bi
