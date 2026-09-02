const heroForm = document.getElementById('hero-form');
const modalOverlay = document.getElementById('modal-apply-overlay');
const modalClose = document.getElementById('modal-apply-close');
const ctaButton = document.querySelector('.cta-button');
const modalForm = document.getElementById('modal-apply-form');

function isValidName(name) {
    if (name.length < 2 || name.length > 50) return false;
    return /^[A-Za-zА-Яа-яЁё\s\-']+$/.test(name);
}

function isValidPhone(phone) {
    const digits = phone.replace(/\D/g, '');
    return digits.length >= 5 && digits.length <= 15;
}

function formatPhone(phone) {
    return phone.replace(/\D/g, '');
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email) && email.length <= 100;
}

function handleFormSubmit(form, submitButtonSelector, buttonText) {
    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const now = Date.now();
        if (now - (window.lastSubmitTime || 0) < 3000) {
            alert("Подождите 3 секунды перед повторной отправкой");
            return;
        }
        window.lastSubmitTime = now;

        const parentName = form.querySelector('input[name="parent_name"]').value.trim();
        const phone = form.querySelector('input[name="phone"]').value.trim();
        const email = form.querySelector('input[name="email"]').value.toLowerCase().trim();
        const childAge = form.querySelector('select[name="child_age"]').value;
        const agreePersonal = form.querySelector('input[name="agree_personal"]').checked;
        const csrfToken = form.querySelector('input[name="csrf_token"]').value.trim();

        if (!isValidName(parentName)) {
            alert("Имя: только буквы, пробелы, дефисы. От 2 до 50 символов.");
            return;
        }

        if (!isValidPhone(phone)) {
            alert("Телефон: от 5 до 15 цифр");
            return;
        }

        if (!isValidEmail(email)) {
            alert("Введите корректный email");
            return;
        }

        if (!childAge) {
            alert("Выберите возраст ребёнка");
            return;
        }

        if (!agreePersonal) {
            alert("Необходимо согласие с политикой конфиденциальности");
            return;
        }

        if (!csrfToken || csrfToken.length < 10) {
            alert("Ошибка безопасности. Обновите страницу.");
            return;
        }

        const submitButton = form.querySelector(submitButtonSelector);
        submitButton.disabled = true;
        submitButton.textContent = 'Отправка...';

        const formData = new FormData();
        formData.append("name", parentName);
        formData.append("tel", formatPhone(phone));
        formData.append("email", email);
        formData.append("child_age", childAge);
        formData.append("is_policy_accepted", "true");

        fetch('/request/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRF-Token': csrfToken
            }
        })
            .then(response => {
                return response.json().then(data => ({
                    ok: response.ok,
                    status: response.status,
                    data: data
                })).catch(() => ({
                    ok: response.ok,
                    status: response.status,
                    data: {detail: `Ошибка ${response.status}`}
                }));
            })
            .then(result => {
                if (result.ok) {
                    window.location.href = '/thank-you';
                } else {
                    alert("Ошибка: " + (result.data.detail || "Неверные данные"));
                }
            })
            .catch(error => {
                console.log("Сетевая ошибка:", error);
                alert("К сожалению, произошла ошибка. Свяжитесь с нами по телефону +7 (985) 260-33-74");
            })
            .finally(() => {
                submitButton.disabled = false;
                submitButton.textContent = buttonText;
            });
    });
}

handleFormSubmit(heroForm, '.hero-submit-btn', 'Записаться');
handleFormSubmit(modalForm, '.modal-apply-submit', 'Записаться');

ctaButton.addEventListener('click', function (e) {
    e.preventDefault();
    modalOverlay.classList.add('show');
});

modalClose.addEventListener('click', function () {
    modalOverlay.classList.remove('show');
});

modalOverlay.addEventListener('click', function (e) {
    if (e.target === modalOverlay) {
        modalOverlay.classList.remove('show');
    }
});

// popular_courses section
document.querySelectorAll('.pc-cta').forEach(btn => {
    btn.addEventListener('click', function() {
        const course = this.dataset.course;
        const modalOverlay = document.getElementById('modal-apply-overlay');

        // Можно добавить скрытое поле с названием курса в модалку
        const courseInput = document.getElementById('modal-course-input');
        if (courseInput) {
            courseInput.value = course;
        }

        modalOverlay.classList.add('show');
    });
});

// how_learning section
const hlCtaBtn = document.getElementById('hl-cta-btn');
if (hlCtaBtn) {
    hlCtaBtn.addEventListener('click', function() {
        const modalOverlay = document.getElementById('modal-apply-overlay');
        if (modalOverlay) {
            modalOverlay.classList.add('show');
        }
    });
}