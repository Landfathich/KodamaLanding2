const menuButtons = document.querySelectorAll('.menu-item');
menuButtons.forEach(button => {
    button.classList.add('menu-button-no-scrolled');
});

window.addEventListener('scroll', function () {
    const header = document.querySelector('header');
    const logo = document.querySelector('.logo');
    const scrollPosition = window.scrollY;

    if (scrollPosition > 0) {
        header.classList.add('header-scrolled');
        logo.classList.add('logo-scrolled');

        menuButtons.forEach(button => {
            button.classList.remove('menu-button-no-scrolled');
        });

        menuButtons.forEach(button => {
            button.classList.add('menu-button-scrolled');
        });

    } else {
        header.classList.remove('header-scrolled');
        logo.classList.remove('logo-scrolled');

        menuButtons.forEach(button => {
            button.classList.remove('menu-button-scrolled');
        });

        menuButtons.forEach(button => {
            button.classList.add('menu-button-no-scrolled');
        });
    }
});