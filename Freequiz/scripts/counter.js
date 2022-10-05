const targettt = document.getElementById("timerDown");
// let timer = 5;
function loopingTimer(timer) {
    setInterval(updateCount(timer), 1000);
}

function updateCount(timer) {
    const minutes = Math.floor(timer / 60);
    let seconds = timer % 60;
    seconds = seconds < 10 ? "0" + seconds : seconds;
    text = `${minutes}:${seconds}`;
    if (seconds > 0) {
        targettt.innerHTML = `${minutes}:${seconds}`;
        timer--;
    } else {
        targettt.innerHTML = `Время вышло!`;
    }
}