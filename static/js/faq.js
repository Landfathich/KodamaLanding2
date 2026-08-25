function toggleAnswer(id) {
    const answer = document.getElementById(id);

    if (answer.classList.contains('open')) {
        answer.classList.remove('open');
    } else {
        answer.classList.add('open');
    }
}

const bubbles = document.querySelectorAll('.bubble');
bubbles.forEach(bubble => {
    const size = Math.floor(Math.random() * 10) + 2;
    bubble.style.width = size + 'vw';
    bubble.style.height = size + 'vh';
});