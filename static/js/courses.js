const courseModal = document.getElementById("course-modal");
const closeButton = document.getElementsByClassName("close")[0];
const modalContent = document.querySelector(".modal-content");

const figmaTitle = "Графический дизайн"
const scratchTitle = "Создание 2D игр"
const compLitTitle = "Компьютер"
const robloxTitle = "Создание 3D игр"
const blenderTitle = "Моделирование"
const frontendTitle = "Создание сайтов"
const pythonTitle = "Основы программирования"
const unityTitle = "Создание игр на Unity"
const olympicProgrammingTitle = "Подготовка к олимпиадам"
const cppTitle = "Изучение языка C++"

const courseImage1 = document.getElementById('course-image1')
const courseImage2 = document.getElementById('course-image2')

function openCourseModal(course) {
    document.body.classList.add('no-scroll');

    const courseModalTitle = document.getElementById('course-modal-title')
    const courseModalSubtitle = document.getElementById('course-modal-subtitle')
    const courseModalDescription = document.getElementById('course-modal-description')
    const courseModalIcon = document.getElementById('course-modal-icon')

    const courseFact1 = document.getElementById('course-fact1')
    const courseFact2 = document.getElementById('course-fact2')
    const courseFact3 = document.getElementById('course-fact3')

    courseModalIcon.className = 'course-modal-icon';

    switch (course) {
        case 'figma':
            courseModalIcon.classList.add('course-modal-icon-smaller')

            courseModalTitle.textContent = figmaTitle;
            courseModalSubtitle.textContent = "в редакторе Figma";
            courseModalDescription.textContent = "Figma — это простая и удобная программа для создания дизайна. Здесь ребенок научится придумывать и рисовать макеты сайтов, приложений и других проектов. Программа работает прямо в браузере, что позволяет легко работать и делиться результатами.";
            courseModalIcon.src = getImagePath('figma_logo.webp');
            courseImage1.src = getImagePath('course_figma1.webp');
            courseImage2.src = getImagePath('course_figma2.webp');
            courseFact1.textContent = 'Идеально подойдет: детям с интересом к дизайну и творчеству.';
            courseFact2.textContent = 'Допустимый возраст: 7-16 лет.';
            courseFact3.textContent = 'Чему научится ребёнок: создавать макеты и прототипы, разрабатывать интерфейсы для веб и мобильных приложений, работать в команде над проектами.';
            break;
        case 'scratch':
            courseModalIcon.classList.add('course-modal-icon-larger')

            courseModalTitle.textContent = scratchTitle;
            courseModalSubtitle.textContent = "на языке Scratch";
            courseModalDescription.textContent = "Scratch — это визуальная платформа программирования для детей, где они могут создавать игры, мультфильмы и интерактивные истории. Курс помогает развить логическое мышление и креативность, погружая ребёнка в мир программирования в игровой форме.";
            courseModalIcon.src = getImagePath('scratch_logo.webp');
            courseImage1.src = getImagePath('course_scratch1.webp');
            courseImage2.src = getImagePath('course_scratch2.webp');
            courseFact1.textContent = 'Идеально для: детей, увлеченных играми и мультфильмами.';
            courseFact2.textContent = 'Возраст: 8-14 лет.';
            courseFact3.textContent = 'Навыки: логика, креативное мышление, основы программирования.';
            break;
        case 'computer-literacy':
            courseModalIcon.classList.add('course-modal-icon-larger')
            courseModalIcon.classList.add('course-modal-icon-center')

            courseModalTitle.textContent = compLitTitle;
            courseModalSubtitle.textContent = "с нуля";
            courseModalDescription.textContent = "Курс обучает детей основам работы с компьютером. Ребенок освоит использование офисных программ (Word, PowerPoint), научится пользоваться браузером, электронной почтой, а также узнает основные правила безопасного поведения в интернете. Этот курс поможет детям уверенно пользоваться компьютером в учебе и повседневной жизни.";
            courseModalIcon.src = getImagePath('comp_lit_logo.webp');
            courseImage1.src = getImagePath('course_comp_lit1.webp');
            courseImage2.src = getImagePath('course_comp_lit2.webp');
            courseFact1.textContent = 'Идеально для: начинающих пользователей, которым нужны базовые навыки работы с компьютером.';
            courseFact2.textContent = 'Возраст: 7-14 лет.';
            courseFact3.textContent = 'Навыки: работа с текстами и презентациями, интернет-серфинг, использование электронной почты.';
            break;
        case 'roblox':
            courseModalTitle.textContent = robloxTitle;
            courseModalSubtitle.textContent = "в Roblox";
            courseModalDescription.textContent = "Курс учит детей создавать свои собственные игры и миры в Roblox. Дети изучат основы программирования и дизайна, научатся использовать инструменты Roblox Studio для создания 3D-игр. Курс развивает творческие способности и логическое мышление, позволяя детям воплотить свои идеи в интерактивные проекты.";
            courseModalIcon.src = getImagePath('roblox_logo.webp');
            courseImage1.src = getImagePath('course_roblox1.webp');
            courseImage2.src = getImagePath('course_roblox2.webp');
            courseFact1.textContent = 'Идеально для: детей, интересующихся созданием игр и виртуальных миров.';
            courseFact2.textContent = 'Возраст: 8-14 лет.';
            courseFact3.textContent = 'Навыки: базовое программирование, работа с 3D-графикой, проектирование игровых уровней.';
            break;
        case 'blender':
            courseModalIcon.classList.add('course-modal-icon-larger')
            courseModalIcon.classList.add('course-modal-icon-center')

            courseModalTitle.textContent = blenderTitle;
            courseModalSubtitle.textContent = "в Blender";
            courseModalDescription.textContent = "Blender — это мощная и бесплатная программа для 3D-моделирования и анимации. На этом курсе ребенок научится создавать трехмерные модели, анимации и визуальные эффекты, развивая свои творческие способности и технические навыки.";
            courseModalIcon.src = getImagePath('blender_logo.webp');
            courseImage1.src = getImagePath('course_blender1.webp');
            courseImage2.src = getImagePath('course_blender2.webp');
            courseFact1.textContent = 'Идеально для: детей с интересом к 3D-дизайну и анимации.';
            courseFact2.textContent = 'Возраст: 10-16 лет.';
            courseFact3.textContent = 'Навыки: создание 3D-моделей, анимация объектов, работа с текстурами и освещением.';
            break;
        case 'web-development':
            courseModalIcon.classList.add('course-modal-icon-larger')
            courseModalIcon.classList.add('course-modal-icon-center')

            courseModalTitle.textContent = frontendTitle;
            courseModalSubtitle.textContent = "с нуля до публикации";
            courseModalDescription.textContent = "Курс по созданию сайтов познакомит детей с основами веб-разработки. Ребенок научится создавать красивые и функциональные сайты, используя HTML, CSS и JavaScript.";
            courseModalIcon.src = getImagePath('web_development_logo.webp');
            courseImage1.src = getImagePath('course_web_dev1.webp');
            courseImage2.src = getImagePath('course_web_dev2.webp');
            courseFact1.textContent = 'Идеально для: детей, интересующихся технологиями и дизайном.';
            courseFact2.textContent = 'Возраст: 9-15 лет.';
            courseFact3.textContent = 'Навыки: основы веб-разработки, работа с кодом, создание адаптивных интерфейсов.';
            break;
        case 'python':
            courseModalTitle.textContent = pythonTitle;
            courseModalSubtitle.textContent = "на языке Python";
            courseModalDescription.textContent = "Python — это один из самых популярных языков программирования, который идеально подходит для начинающих. На этом курсе ребенок освоит базовые концепции программирования и научится писать простые программы.";
            courseModalIcon.src = getImagePath('python_logo.webp');
            courseImage1.src = getImagePath('course_python1.webp');
            courseImage2.src = getImagePath('course_python2.webp');
            courseFact1.textContent = 'Идеально для: детей, желающих начать изучение программирования.';
            courseFact2.textContent = 'Возраст: 10-16 лет.';
            courseFact3.textContent = 'Навыки: основы синтаксиса Python, работа с переменными и функциями.';
            break;
        case 'unity':
            courseModalTitle.textContent = unityTitle;
            courseModalSubtitle.textContent = "от идеи до реализации";
            courseModalDescription.textContent = "Unity — это мощный игровой движок, который позволяет создавать 2D и 3D игры. На этом курсе ребенок научится разрабатывать свои собственные игры, изучая основы игрового дизайна и программирования.";
            courseModalIcon.src = getImagePath('unity_logo.webp');
            courseImage1.src = getImagePath('course_unity1.webp');
            courseImage2.src = getImagePath('course_unity2.webp');
            courseFact1.textContent = 'Идеально для: детей, увлеченных играми и технологиями.';
            courseFact2.textContent = 'Возраст: 11-16 лет.';
            courseFact3.textContent = 'Навыки: основы игрового дизайна, программирование на C#, создание игровых уровней.';
            break;
        case 'olympic-programming':
            courseModalTitle.textContent = olympicProgrammingTitle;
            courseModalSubtitle.textContent = "по программированию";
            courseModalDescription.textContent = "Курс по олимпиадному программированию поможет детям развить логическое мышление и навыки решения сложных задач. Ребенок познакомится с алгоритмами и структурами данных.";
            courseModalIcon.src = getImagePath('olympic_programming_logo.webp');
            courseImage1.src = getImagePath('course_olympic1.webp');
            courseImage2.src = getImagePath('course_olympic2.webp');
            courseFact1.textContent = 'Идеально для: детей, стремящихся участвовать в олимпиадах и конкурсах по программированию.';
            courseFact2.textContent = 'Возраст: 12-16 лет.';
            courseFact3.textContent = 'Навыки: алгоритмическое мышление, работа с данными, решение задач различной сложности.';
            break;
        case 'cpp':
            courseModalTitle.textContent = cppTitle;
            courseModalSubtitle.textContent = "для начинающих и продвинутых";
            courseModalDescription.textContent = "C++ — это мощный язык программирования, который используется в различных областях, от разработки игр до системного программирования. На этом курсе ребенок освоит основы C++ и научится писать эффективный код.";
            courseModalIcon.src = getImagePath('cpp_logo.webp');
            courseImage1.src = getImagePath('course_cpp1.webp');
            courseImage2.src = getImagePath('course_cpp2.webp');
            courseFact1.textContent = 'Идеально для: детей, желающих углубить свои знания в программировании.';
            courseFact2.textContent = 'Возраст: 11-16 лет.';
            courseFact3.textContent = 'Навыки: основы синтаксиса C++, работа с классами и объектами, разработка простых приложений.';
            break;
        default:
            courseModalTitle.textContent = "";
            courseModalSubtitle.textContent = "";
            courseModalDescription.textContent = "";
            courseModalIcon.src = null;
            courseImage1.src = '';
            courseImage2.src = '';
            courseFact1.textContent = '';
            courseFact2.textContent = '';
            courseFact3.textContent = '';
    }
    courseModal.style.display = "block";
    modalContent.scrollTop = 0;
}

function closeCourseModal() {
    courseModal.style.display = "none";
    document.body.classList.remove('no-scroll');
    courseImage1.src = ''; // Очищаем src
    courseImage1.removeAttribute('src'); // Удаляем атрибут src

    courseImage2.src = '';
    courseImage2.removeAttribute('src');
}

closeButton.onclick = function () {
    closeCourseModal()
}

document.addEventListener('click', function (e) {
    // Проверяем, был ли клик на модальном окне или его содержимом
    if (e.target === courseModal) {
        closeCourseModal();
    }
});

// Объект для сопоставления заголовков и значений селектора
const courseMapping = {
    [figmaTitle]: "figma",
    [scratchTitle]: "scratch",
    [compLitTitle]: "computer-literacy",
    [robloxTitle]: "roblox",
    [blenderTitle]: "blender",
    [frontendTitle]: "web-development",
    [pythonTitle]: "python",
    [unityTitle]: "unity",
    [olympicProgrammingTitle]: "olympic-programming",
    [cppTitle]: "cpp",
};

// Обработчик клика по кнопке "Записаться"
document.querySelector('.apply-button').addEventListener('click', function () {
    // Закрываем модальное окно
    closeCourseModal()

    // Получаем выбранный курс
    const selectedCourseTitle = document.getElementById('course-modal-title').innerText;

    // Прокручиваем страницу к форме
    document.getElementById('apply').scrollIntoView({behavior: 'smooth'});

    // Получаем значение селектора на основе заголовка
    const courseSelect = document.getElementById('course-select');
    // Если нет совпадений, устанавливаем пустую строку
    courseSelect.value = courseMapping[selectedCourseTitle] || '';
    changeBackground();

    // Включаем фокус на первом поле ввода
    document.getElementById('name').focus();
});