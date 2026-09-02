const menuButtons = document.querySelectorAll('.menu-item');
const header = document.querySelector('header');
const logo = document.querySelector('.logo');

menuButtons.forEach(button => button.classList.add('menu-button-no-scrolled'));

window.addEventListener('scroll', function () {
    const scrollPosition = window.scrollY;

    if (scrollPosition > 0) {
        header.classList.add('header-scrolled');
        logo.classList.add('logo-scrolled');
        menuButtons.forEach(button => {
            button.classList.remove('menu-button-no-scrolled');
            button.classList.add('menu-button-scrolled');
        });
    } else {
        header.classList.remove('header-scrolled');
        logo.classList.remove('logo-scrolled');
        menuButtons.forEach(button => {
            button.classList.remove('menu-button-scrolled');
            button.classList.add('menu-button-no-scrolled');
        });
    }
});