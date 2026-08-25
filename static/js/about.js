document.addEventListener("DOMContentLoaded", () => {
    const image = document.querySelector(".hover-image");
    let currentStep = 0; // Хранит текущий шаг анимации

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    window.addEventListener("scroll", handleScroll);
                } else {
                    window.removeEventListener("scroll", handleScroll);
                }
            });
        },
        {threshold: [0.2, 0.4, 0.6, 0.8, 1]}
    );

    function handleScroll() {
        const rect = image.getBoundingClientRect();
        const viewportHeight = window.innerHeight;

        let newStep = 0;
        if (rect.top > viewportHeight * 0.8) {
            newStep = 1;
        } else if (rect.top > viewportHeight * 0.6) {
            newStep = 2;
        } else if (rect.top > viewportHeight * 0.4) {
            newStep = 3;
        } else if (rect.top > viewportHeight * 0.2) {
            newStep = 4;
        } else {
            newStep = 5;
        }

        // Обновляем состояние, только если оно изменилось
        if (newStep !== currentStep) {
            setStep(newStep);
            currentStep = newStep;
        }
    }

    function setStep(step) {
        image.classList.remove("step-1", "step-2", "step-3", "step-4", "step-5");
        image.classList.add(`step-${step}`);
    }

    observer.observe(image);
});
