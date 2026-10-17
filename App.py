import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Flappy Bird", page_icon="🐦")
st.title("🐦 Flappy Bird")
st.caption("Nhấn Bắt đầu, sau đó nhấp chuột hoặc nhấn SPACE để bay.")

html = r"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body { margin:0; text-align:center; font-family:Arial; background:#87ceeb; }
canvas { display:block; width:100%; max-width:400px; height:auto;
         margin:auto; border:2px solid white; touch-action:manipulation; }
button { margin:12px; padding:12px 25px; font-size:18px;
         font-weight:bold; border:0; border-radius:10px;
         background:#ffd43b; cursor:pointer; }
</style>
</head>
<body>
<canvas id="c" width="400" height="550"></canvas>
<button id="start">Bắt đầu / Chơi lại</button>
<p>Nhấp vào game hoặc nhấn phím SPACE để bay lên.</p>

<script>
const c = document.getElementById("c");
const ctx = c.getContext("2d");
let bird, pipes, score, frame, started, alive;

function reset() {
  bird = {x:85, y:240, v:0, r:13};
  pipes = [];
  score = 0;
  frame = 0;
  started = true;
  alive = true;
}

function flap() {
  if (!started || !alive) return;
  bird.v = -6;
}

function control() {
  if (!started || !alive) reset();
  else flap();
}

document.getElementById("start").addEventListener("click", reset);
c.addEventListener("pointerdown", control);
document.addEventListener("keydown", e => {
  if (e.code === "Space" || e.code === "ArrowUp") {
    e.preventDefault();
    control();
  }
});

function drawBird() {
  ctx.fillStyle = "#ffdc35";
  ctx.beginPath();
  ctx.arc(bird.x, bird.y, bird.r, 0, Math.PI*2);
  ctx.fill();
  ctx.strokeStyle = "#9a6900";
  ctx.stroke();

  ctx.fillStyle = "white";
  ctx.beginPath();
  ctx.arc(bird.x+5, bird.y-4, 5, 0, Math.PI*2);
  ctx.fill();

  ctx.fillStyle = "black";
  ctx.beginPath();
  ctx.arc(bird.x+7, bird.y-4, 2, 0, Math.PI*2);
  ctx.fill();

  ctx.fillStyle = "orange";
  ctx.beginPath();
  ctx.moveTo(bird.x+11,bird.y);
  ctx.lineTo(bird.x+22,bird.y+4);
  ctx.lineTo(bird.x+11,bird.y+7);
  ctx.fill();
}

function drawPipe(p) {
  const bottom = p.top + p.gap;
  ctx.fillStyle = "#20ad48";
  ctx.fillRect(p.x,0,52,p.top);
  ctx.fillRect(p.x-4,p.top-18,60,18);
  ctx.fillRect(p.x,bottom,52,515-bottom);
  ctx.fillRect(p.x-4,bottom,60,18);
  ctx.strokeStyle = "#126b2c";
  ctx.strokeRect(p.x,0,52,p.top);
  ctx.strokeRect(p.x,bottom,52,515-bottom);
}

function loop() {
  ctx.clearRect(0,0,400,550);
  ctx.fillStyle = "#87ceeb";
  ctx.fillRect(0,0,400,550);

  // Mây
  ctx.fillStyle = "white";
  [[60,80],[270,115],[175,45]].forEach(([x,y]) => {
    ctx.beginPath();
    ctx.arc(x,y,17,0,Math.PI*2);
    ctx.arc(x+20,y-5,20,0,Math.PI*2);
    ctx.arc(x+40,y,15,0,Math.PI*2);
    ctx.fill();
  });

  if (started && alive) {
    frame++;
    bird.v += 0.3;
    bird.y += bird.v;

    if (frame % 100 === 0) {
      pipes.push({
        x:405,
        top:70+Math.random()*210,
        gap:165,
        passed:false
      });
    }

    for (const p of pipes) {
      p.x -= 2.5;

      const hitX = bird.x+bird.r > p.x &&
                   bird.x-bird.r < p.x+52;
      const hitY = bird.y-bird.r < p.top ||
                   bird.y+bird.r > p.top+p.gap;

      if (hitX && hitY) alive = false;

      if (!p.passed && p.x+52 < bird.x) {
        score++;
        p.passed = true;
      }
    }

    pipes = pipes.filter(p => p.x > -65);

    if (bird.y-bird.r < 0 || bird.y+bird.r > 515) {
      alive = false;
    }
  }

  for (const p of pipes) drawPipe(p);

  ctx.fillStyle = "#b6e36b";
  ctx.fillRect(0,515,400,35);
  ctx.fillStyle = "#78b83b";
  ctx.fillRect(0,515,400,6);

  drawBird();

  ctx.textAlign = "center";
  ctx.font = "bold 34px Arial";
  ctx.lineWidth = 3;
  ctx.strokeStyle = "#333";
  ctx.strokeText(score,200,48);
  ctx.fillStyle = "white";
  ctx.fillText(score,200,48);

  if (!started) {
    ctx.fillStyle = "#17324d";
    ctx.font = "bold 27px Arial";
    ctx.fillText("FLAPPY BIRD",200,235);
    ctx.font = "17px Arial";
    ctx.fillText("Nhan Bat dau de choi",200,270);
  }

  if (started && !alive) {
    ctx.fillStyle = "rgba(0,0,0,0.65)";
    ctx.fillRect(45,195,310,115);
    ctx.fillStyle = "#ffdf4d";
    ctx.font = "bold 28px Arial";
    ctx.fillText("GAME OVER",200,235);
    ctx.fillStyle = "white";
    ctx.font = "20px Arial";
    ctx.fillText("Diem: "+score,200,270);
    ctx.font = "14px Arial";
    ctx.fillText("Bam Choi lai ben duoi",200,293);
  }

  requestAnimationFrame(loop);
}

bird = {x:85,y:240,v:0,r:13};
pipes = [];
score = 0;
frame = 0;
started = false;
alive = false;
loop();
</script>
</body>
</html>
"""

components.html(html, height=680, scrolling=False)
