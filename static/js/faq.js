function toggleFaq(item) {
    const answer = item.nextElementSibling;
    const isOpen = answer.classList.contains('open');

    document.querySelectorAll('.faq-answer').forEach(a => {
        a.classList.remove('open');
        a.style.maxHeight = '0';
    });

    document.querySelectorAll('.faq-item').forEach(i => {
        i.classList.remove('active');
    });

    if (!isOpen) {
        answer.classList.add('open');
        answer.style.maxHeight = answer.scrollHeight + 200 + 'px';
        item.classList.add('active');
    }
}

const bubbles = document.querySelectorAll('.faq-bubble');
bubbles.forEach((bubble) => {
    const size = Math.floor(Math.random() * 10) + 2;
    const randomDelay = Math.random() * 5;
    bubble.style.width = size + 'vw';
    bubble.style.height = size + 'vh';
    bubble.style.animationDelay = randomDelay + 's';
    bubble.style.opacity = '0';
});