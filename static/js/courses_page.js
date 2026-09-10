const typeFilters = document.querySelectorAll('[data-type]');
const ageFilters = document.querySelectorAll('[data-age]');
const cards = document.querySelectorAll('.cp-card');
let activeType = 'all';
let activeAge = 'all';

function filterCards() {
    cards.forEach(card => {
        const minAge = parseInt(card.dataset.ageMin);
        const maxAge = parseInt(card.dataset.ageMax);
        const cardTypes = card.dataset.types.split(',');

        let matchesAge = true;
        if (activeAge !== 'all') {
            const [filterMin, filterMax] = activeAge.split('-').map(Number);
            matchesAge = (minAge <= filterMax && maxAge >= filterMin);
        }

        const matchesType = activeType === 'all' || cardTypes.includes(activeType);

        if (matchesType && matchesAge) {
            card.classList.remove('hidden');
        } else {
            card.classList.add('hidden');
        }
    });
}

const urlParams = new URLSearchParams(window.location.search);
const typeFromUrl = urlParams.get('type');

if (typeFromUrl) {
    const activeFilter = document.querySelector(`[data-type="${typeFromUrl}"]`);
    if (activeFilter) {
        typeFilters.forEach(f => f.classList.remove('active'));
        activeFilter.classList.add('active');
        activeType = typeFromUrl;
        filterCards();
    }
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