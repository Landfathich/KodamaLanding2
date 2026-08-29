const problemCards = document.querySelectorAll('.ps-problem-card');
const solutionTitle = document.getElementById('ps-solution-title');
const solutionPoints = document.getElementById('ps-solution-points');
const solutionContent = document.querySelector('.ps-solution-content');

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
        title: 'Направляем интерес в развитие',
        points: [
            { icon: '🎮', text: 'Связываем игры с <strong>программированием и логикой</strong>' },
            { icon: '🎨', text: 'Учим <strong>дизайну и творчеству</strong> через технологии' },
            { icon: '🧠', text: 'Развиваем <strong>мышление и навыки</strong>, а не только развлечение' },
            { icon: '📈', text: 'Показываем <strong>результат</strong> через проекты' }
        ]
    },
    3: {
        title: 'Помогаем выбрать направление',
        points: [
            { icon: '🔍', text: 'На пробном уроке <strong>определяем интересы</strong> ребёнка' },
            { icon: '📋', text: 'Подбираем курс по <strong>возрасту и уровню</strong>' },
            { icon: '💡', text: 'Даём <strong>рекомендации</strong> по развитию' },
            { icon: '🔄', text: 'Можно <strong>поменять направление</strong> в любой момент' }
        ]
    },
    4: {
        title: 'Делаем первый шаг безопасным',
        points: [
            { icon: '🎁', text: 'Пробный урок — <strong>бесплатный</strong> и ни к чему не обязывает' },
            { icon: '👩‍🏫', text: '<strong>Мягкий преподаватель</strong>, который поддержит ребёнка' },
            { icon: '⏱️', text: 'Комфортный <strong>индивидуальный темп</strong>' },
            { icon: '👨‍👩‍👧', text: 'Родитель <strong>видит результат</strong> после первого урока' }
        ]
    }
};

problemCards.forEach(card => {
    card.addEventListener('click', function() {
        problemCards.forEach(c => c.classList.remove('active'));
        this.classList.add('active');

        const solutionId = this.dataset.solution;
        const solution = solutions[solutionId];

        solutionContent.style.transition = 'opacity 0.1s ease';
        solutionContent.style.opacity = '0';

        setTimeout(() => {
            solutionTitle.textContent = solution.title;
            solutionPoints.innerHTML = solution.points.map(point => `
                <div class="ps-point">
                    <span class="ps-point-icon">${point.icon}</span>
                    <p>${point.text}</p>
                </div>
            `).join('');

            solutionContent.style.opacity = '1';
        }, 100);
    });
});