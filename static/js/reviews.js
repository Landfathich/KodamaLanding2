const track = document.getElementById('rv-track');
const prevBtn = document.getElementById('rv-prev');
const nextBtn = document.getElementById('rv-next');
const cards = document.querySelectorAll('.rv-card');
let currentIndex = 0;

function getCardsPerView() {
    if (window.innerWidth <= 768) return 1;
    return 2;
}

function updateCarousel() {
    const cardsPerView = getCardsPerView();
    const cardWidth = cards[0].offsetWidth + 20;
    track.style.transform = `translateX(-${currentIndex * cardWidth}px)`;

    prevBtn.disabled = currentIndex === 0;
    nextBtn.disabled = currentIndex >= cards.length - cardsPerView;
}

prevBtn.addEventListener('click', () => {
    if (currentIndex > 0) {
        currentIndex--;
        updateCarousel();
    }
});

nextBtn.addEventListener('click', () => {
    const cardsPerView = getCardsPerView();
    if (currentIndex < cards.length - cardsPerView) {
        currentIndex++;
        updateCarousel();
    }
});

window.addEventListener('resize', updateCarousel);
updateCarousel();