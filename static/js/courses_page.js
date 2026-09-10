const typeFilters = document.querySelectorAll('[data-type]');
const ageFilters = document.querySelectorAll('[data-age]');
const cards = document.querySelectorAll('.cp-card');
let activeType = 'all';
let activeAge = 'all';

function filterCards() {
    cards.forEach(card => {
        const minAge = parseInt(card.dataset.ageMin);
        const maxAge = parseInt(card.dataset.ageMax);

        let matchesAge = true;
        if (activeAge !== 'all') {
            const [filterMin, filterMax] = activeAge.split('-').map(Number);
            matchesAge = (minAge <= filterMax && maxAge >= filterMin);
        }

        const matchesType = activeType === 'all' || card.dataset.type === activeType;

        if (matchesType && matchesAge) {
            card.classList.remove('hidden');
        } else {
            card.classList.add('hidden');
        }
    });
}

typeFilters.forEach(filter => {
    filter.addEventListener('click', function () {
        typeFilters.forEach(f => f.classList.remove('active'));
        this.classList.add('active');
        activeType = this.dataset.type;
        filterCards();
    });
});

ageFilters.forEach(filter => {
    filter.addEventListener('click', function () {
        ageFilters.forEach(f => f.classList.remove('active'));
        this.classList.add('active');
        activeAge = this.dataset.age;
        filterCards();
    });
});

document.querySelectorAll('.cp-cta').forEach(btn => {
    btn.addEventListener('click', function () {
        const course = this.dataset.course;
        const modalOverlay = document.getElementById('modal-apply-overlay');
        const courseInput = document.getElementById('modal-course-input');
        if (courseInput) {
            courseInput.value = course;
        }
        if (modalOverlay) {
            modalOverlay.classList.add('show');
        }
    });
});

const fcBtnSecondary = document.querySelector('.fc-btn-secondary');
if (fcBtnSecondary) {
    fcBtnSecondary.style.display = 'none';
}