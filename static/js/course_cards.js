document.querySelectorAll('.course-cta').forEach(btn => {
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