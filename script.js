document.addEventListener("keydown", jump, true);

function jump(e) {
    if (e.key == " ") {
        document.getElementById('mario').classList.add("mario-jump");
        document.getElementById('mario').addEventListener("animationend", () => {
            document.getElementById('mario').classList.remove("mario-jump");
        })
    }
};

var points = 1;
var difficult = 0;
var post_data = 0;
setInterval( () => {
    const marioPosition = Number(window.getComputedStyle(document.getElementById('mario')).bottom.replace('px', ''));
    const pipe = document.getElementById('pipe');
    difficult += 0.0005;
    var duration = 3
    if(
            marioPosition <= 300
            &&
            pipe.offsetLeft <= 330
            &&
            pipe.offsetLeft >= 250
    ) {
        gameOver(Number(document.getElementById('score').textContent.replace('Score: ', '')));
    } else {
        if (duration >= 1.7) {
            var score = document.getElementById('score');
            points += 0.01;
            duration -= difficult
            score.innerText = 'Score: ' + (points ** 1.5).toFixed(0).toString().replace('.5', '');
            document.getElementById('pipe').style.animationDuration = `${duration}s`;
            document.getElementById('cloud').style.animationDuration = `${duration + 17}s`;
            document.getElementById('mario').style.animationDuration = `${0.8 - (points*0.001)}s`;
        } else {
            var score = document.getElementById('score');
            points += 0.01;
            score.innerText = 'Score: ' + (points ** 1.5).toFixed(0).toString().replace('.5', '');
            document.getElementById('mario').style.animationDuration = `0.6s`;
        }
    }
}, 10);

var posted = 0;
function gameOver(score) {
    const pipe = document.getElementById('pipe');
    pipe.style.left = `${pipe.offsetLeft}px`;
    pipe.style.animation = 'none';

    const mario = document.getElementById('mario');
    mario.style.left = mario.offsetLeft;
    mario.style.top = mario.offsetTop;
    mario.setAttribute('src', './assets/game-over.png');
    mario.style.animationDuration = '5s';
    mario.classList.add('game-over');
    document.removeEventListener('keydown', jump, true);

    mario.addEventListener("animationend", () => {
        mario.style.scale = '0.8'
    })

    if (posted == 0) {
        fetch(`http://127.0.0.1:5000/database/${score}`, { method: 'POST' })
        .then(T => T.json());
        console.log('Posted');
        posted = 1;
    }
}

(function fetchData() {
    fetch('http://127.0.0.1:5000/database', { method: 'GET' })
    .then(data => {
        return data.json();
    })
    .then(post => {
        document.getElementById('max-score').innerText = `Highest score: ${post[0]}`;
    });
})();
