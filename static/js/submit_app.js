const courseSelect = document.getElementById('course-select');
const submitForm = document.getElementById('submit-app-content');
const formInputs = document.querySelectorAll('#submit-app-block input');
const submitAppTitle = document.getElementById('submit-app-title')
const submitAppPhoto = document.getElementById('submit-app-photo')

// Добавляем обработчик события change
courseSelect.addEventListener('change', changeBackground);

// Функция для изменения фона в зависимости от выбранного варианта
function changeBackground() {
    const selectedCourse = courseSelect.value;

    // Определяем цвет фона в зависимости от выбранного курса
    let backgroundColor;
    let inputBackgroundColor;
    let backgroundColorTransparent;
    let titleColor;

    switch (selectedCourse) {
        case 'roblox':
            backgroundColor = '#FFC75C'; // Желтый цвет для Figma
            inputBackgroundColor = '#FFFFE0'; // Более блеклый цвет для областей ввода информации
            backgroundColorTransparent = 'rgba(255, 199, 92, 0.5)';
            titleColor = '#410E6A';
            submitAppPhoto.src = getImagePath('roblox_submit.webp');
            break;
        case 'computer-literacy':
            backgroundColor = '#41EAD4'; // Зеленый цвет для Компьютерной грамотности
            inputBackgroundColor = '#E0FFF3'; // Более блеклый цвет для областей ввода информации
            backgroundColorTransparent = 'rgba(65, 234, 212, 0.5)';
            titleColor = '#410E6A';
            submitAppPhoto.src = getImagePath('comp_lit_submit.webp');
            break;
        case 'scratch':
            backgroundColor = '#6E65FF'; // Фиолетовый цвет для Scratch
            inputBackgroundColor = '#F0E7FF'; // Более блеклый цвет для областей ввода информации
            backgroundColorTransparent = 'rgba(110, 101, 255, 0.5)';
            titleColor = '#FFC75C';
            submitAppPhoto.src = getImagePath('scratch_submit.webp');
            break;
        case 'figma':
            backgroundColor = '#FF6E6E'; // Красный цвет для Roblox
            inputBackgroundColor = '#FFE0E0'; // Более блеклый цвет для областей ввода информации
            backgroundColorTransparent = 'rgba(255, 110, 110, 0.5)';
            titleColor = '#410E6A';
            submitAppPhoto.src = getImagePath('figma_submit.webp');
            break;
        case 'blender':
            backgroundColor = '#FFB74D'; // Оранжевый цвет для Blender
            inputBackgroundColor = '#FFE0B2'; // Более блеклый цвет для областей ввода информации
            backgroundColorTransparent = 'rgba(255, 183, 77, 0.5)';
            titleColor = '#f6683b';
            submitAppPhoto.src = getImagePath('blender_submit.webp');
            break;
        case 'web-development':
            backgroundColor = '#4CAF50'; // Зеленый цвет для создания сайтов
            inputBackgroundColor = '#C8E6C9'; // Более блеклый цвет для областей ввода информации
            backgroundColorTransparent = 'rgba(76, 175, 80, 0.5)';
            titleColor = '#14bc20';
            submitAppPhoto.src = getImagePath('web_dev_submit.webp');
            break;
        case 'python':
            backgroundColor = '#FFD54F'; // Желтый цвет для Python
            inputBackgroundColor = '#FFF9C4'; // Более блеклый цвет для областей ввода информации
            backgroundColorTransparent = 'rgba(255, 213, 79, 0.5)';
            titleColor = '#F57F20';
            submitAppPhoto.src = getImagePath('python_submit.webp');
            break;
        case 'olympic-programming':
            backgroundColor = '#fa6030'; // Ярко-оранжевый цвет для олимпиадного программирования
            inputBackgroundColor = '#FFAB40'; // Более блеклый цвет для областей ввода информации
            backgroundColorTransparent = 'rgba(255, 61, 0, 0.5)';
            titleColor = '#fd764d'; // Темный оттенок оранжевого
            submitAppPhoto.src = getImagePath('olympic_submit.webp');
            break;
        case 'unity':
            backgroundColor = '#1DE9B6'; // Яркий бирюзовый цвет для Unity
            inputBackgroundColor = '#B2EBF2'; // Более блеклый цвет для областей ввода информации
            backgroundColorTransparent = 'rgba(29, 233, 182, 0.5)';
            titleColor = '#004D40'; // Темный оттенок бирюзового
            submitAppPhoto.src = getImagePath('unity_submit.webp');
            break;
        case 'cpp':
            backgroundColor = '#2196F3'; // Яркий синий цвет для C++
            inputBackgroundColor = '#BBDEFB'; // Более блеклый цвет для областей ввода информации
            backgroundColorTransparent = 'rgba(33, 150, 243, 0.5)';
            titleColor = '#448dfd'; // Темный оттенок синего
            submitAppPhoto.src = getImagePath('cpp_submit.webp');
            break;
        default:
            backgroundColor = '#ffffff'; // Белый цвет по умолчанию
            inputBackgroundColor = '#f8f9fa'; // Светло-серый цвет для областей ввода информации
            backgroundColorTransparent = '#2E3038';
            titleColor = '#A4FFDE';
            submitAppPhoto.src = getImagePath('default_submit.webp');
    }

    // Устанавливаем цвет фона для элемента выбора курса
    courseSelect.style.backgroundColor = backgroundColor;

    // Устанавливаем цвет фона для всей формы с изменением прозрачности
    submitForm.style.backgroundColor = backgroundColorTransparent;

    // Устанавливаем цвет фона для областей ввода информации
    formInputs.forEach(input => {
        input.style.backgroundColor = inputBackgroundColor;
    });

    submitAppTitle.style.color = titleColor;
}

// ========================
// 1. ВАЛИДАЦИЯ ДАННЫХ
// ========================
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

// ========================
// 2. РАБОТА С МОДАЛЬНЫМ ОКНОМ
// ========================
function showSubmitAppModal(message, isSuccess = true) {
    const modal = document.getElementById('submit-app-modal');
    const title = document.getElementById('submit-app-modal-title');
    const messageElement = document.getElementById('submit-app-modal-message');

    title.textContent = isSuccess
        ? 'Спасибо за заявку!'
        : 'Проверьте данные';

    // Устанавливаем сообщение
    messageElement.textContent = message;

    // Показываем модалку
    modal.style.display = 'flex';

    // Добавляем класс для анимации
    setTimeout(() => {
        modal.classList.add('show');
    }, 10);
}

function closeSubmitAppModal() {
    const modal = document.getElementById('submit-app-modal');

    // Убираем класс анимации
    modal.classList.remove('show');

    // Скрываем через небольшой таймаут для плавности
    setTimeout(() => {
        modal.style.display = 'none';
    }, 300);
}

// ========================
// 3. ОСНОВНАЯ ЛОГИКА ФОРМЫ
// ========================
function validateFormData(data) {
    const {name, tel, email, courseSelect, privacyCheckbox, csrfToken} = data;

    if (!isValidName(name)) {
        return "Имя: только буквы, пробелы, дефисы. От 2 до 50 символов.";
    }

    if (!isValidPhone(tel)) {
        return "Телефон: от 5 до 15 цифр";
    }

    if (!isValidEmail(email)) {
        return "Введите корректный email (например: example@mail.ru)";
    }

    if (!courseSelect.value) {
        return "Пожалуйста, выберите курс";
    }

    if (!privacyCheckbox.checked) {
        return "Необходимо согласие с политикой конфиденциальности";
    }

    if (!csrfToken || csrfToken.length < 10) {
        return "Ошибка безопасности. Обновите страницу и попробуйте снова.";
    }

    return null; // Ошибок нет
}

function prepareFormData(formValues) {
    const {name, tel, email, courseSelect, privacyCheckbox} = formValues;
    const formData = new FormData();

    const formattedTel = formatPhone(tel);

    formData.append("name", name);
    formData.append("tel", formattedTel);
    formData.append("email", email);
    formData.append("course", courseSelect.options[courseSelect.selectedIndex].textContent);
    formData.append("is_policy_accepted", privacyCheckbox.checked);

    return formData;
}

function handleFormResponse(result, name) {
    if (result.ok) {
        showSubmitAppModal(result.data.message, true);
    } else {
        showSubmitAppModal("Ошибка: " + (result.data.detail || "Неверные данные"), false);
    }
}

function handleFormError(name) {
    const errorMessage = `Уважаемый(ая) ${name},\nК сожалению, при обработке вашей заявки на обучение произошла ошибка. Мы приносим извинения за доставленные неудобства.\nСвяжитесь пожалуйста с нами по телефону +7 (985) 260-33-74 или по электронной почте kodama.edu@gmail.com. Мы постараемся помочь вам как можно скорее.\n\nС уважением,\nKodama`;
    showSubmitAppModal(errorMessage, false);
}

// ========================
// 4. ОБРАБОТЧИК ФОРМЫ
// ========================
document.getElementById('submit-app-form').addEventListener('submit', function (e) {
    e.preventDefault();

    // Защита от быстрых повторных отправок
    const now = Date.now();
    if (now - (window.lastSubmitTime || 0) < 3000) {
        showSubmitAppModal("Подождите 3 секунды перед повторной отправкой", false);
        return;
    }
    window.lastSubmitTime = now;

    // Сбор данных формы
    const formValues = {
        name: document.getElementById("name").value.trim(),
        tel: document.getElementById("phone").value.trim(),
        email: document.getElementById("email").value.toLowerCase().trim(),
        courseSelect: document.getElementById("course-select"),
        privacyCheckbox: document.getElementById("privacy-policy-checkbox"),
        csrfToken: document.querySelector('input[name="csrf_token"]').value.trim()
    };

    // Валидация
    const validationError = validateFormData(formValues);
    if (validationError) {
        showSubmitAppModal(validationError, false);
        return;
    }

    // Блокировка кнопки
    const submitButton = document.getElementById('submit-btn');
    submitButton.disabled = true;
    submitButton.textContent = 'Отправка...';

    // Подготовка и отправка данных
    const formData = prepareFormData(formValues);

    fetch('/request', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRF-Token': formValues.csrfToken
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
            handleFormResponse(result, formValues.name);
        })
        .catch(error => {
            console.log("Сетевая ошибка:", error);
            handleFormError(formValues.name);
        })
        .finally(() => {
            submitButton.disabled = false;
            submitButton.textContent = 'Отправить';
        });
});