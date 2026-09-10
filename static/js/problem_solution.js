const problemCards = document.querySelectorAll('.ps-problem-card');
const solutionTitle = document.getElementById('ps-solution-title');
const solutionPoints = document.getElementById('ps-solution-points');

const solutions = {
    1: {
        title: 'Превращаем интерес в полезный навык',
        points: [
            { icon: '✨', text: 'Ребёнок <strong>создаёт</strong>, а не просто потребляет' },
            { icon: '🎯', text: 'Подбираем направление по <strong>возрасту и интересам</strong>' },
            { icon: '🚀', text: 'Первый проект — <strong>уже на пробном уроке</strong>' },
            { icon: '👩‍🏫', text: 'Индивидуально с преподавателем, <strong>в комфортном темпе</strong>' }
        ]
    },
    2: {
        title: 'Направляем любовь к играм в обучение',
        points: [
            { icon: '🎮', text: 'Игры становятся <strong>основой для программирования</strong>' },
            { icon: '🎨', text: 'Развиваем <strong>творчество</strong> через дизайн и технологии' },
            { icon: '🧠', text: 'Тренируем <strong>логику и мышление</strong>, а не только играем' },
            { icon: '📈', text: 'Показываем <strong>результат</strong> через реальные проекты' }
        ]
    },
    3: {
        title: 'Помогаем выбрать направление',
        points: [
            { icon: '📞', text: 'Подбираем курс <strong>под интересы ребёнка</strong>' },
            { icon: '📋', text: 'Учитываем <strong>возраст и уровень</strong>' },
            { icon: '💡', text: 'Даём <strong>рекомендации</strong> по развитию' },
            { icon: '🔄', text: 'Можно <strong>поменять направление</strong> в любой момент' }
        ]
    },
    4: {
        title: 'Делаем первый шаг безопасным',
        points: [
            { icon: '🎁', text: 'Пробный урок — <strong>бесплатный</strong> и ни к чему не обязывает' },
            { icon: '👩‍🏫', text: '<strong>Чуткий преподаватель</strong>, который поддержит ребёнка' },
            { icon: '⏱️', text: 'Комфортный <strong>индивидуальный темп</strong>' },
            { icon: '👨‍👩‍👧', text: 'Родитель <strong>видит результат</strong> после первого урока' }
        ]
    }
};

problemCards.forEach(card => {
    card.addEventListener('click', function() {
        if (this.classList.contains('active')) return;

        problemCards.forEach(c => c.classList.remove('active'));
        this.classList.add('active');

        const solutionId = this.dataset.solution;
        const solution = solutions[solutionId];

        solutionTitle.style.transition = 'opacity 0.2s ease, transform 0.2s ease';
        solutionTitle.style.opacity = '0';
        solutionTitle.style.transform = 'translateY(-5px)';

        solutionPoints.style.transition = 'opacity 0.2s ease, transform 0.2s ease';
        solutionPoints.style.opacity = '0';
        solutionPoints.style.transform = 'translateY(-5px)';

        setTimeout(() => {
            solutionTitle.textContent = solution.title;
            solutionPoints.innerHTML = solution.points.map(point => `
                <div class="ps-point">
                    <span class="ps-point-icon">${point.icon}</span>
                    <p>${point.text}</p>
                </div>
            `).join('');

            solutionTitle.style.opacity = '1';
            solutionTitle.style.transform = 'translateY(0)';

            setTimeout(() => {
                solutionPoints.style.opacity = '1';
                solutionPoints.style.transform = 'translateY(0)';
            }, 50);
        }, 200);
    });
});