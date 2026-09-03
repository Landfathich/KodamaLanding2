const menuButtons = document.querySelectorAll('.menu-item');
const header = document.querySelector('header');
const logo = document.querySelector('.logo');
const openMenuBtn = document.getElementById('open-menu-btn');
const closeMenuBtn = document.getElementById('close-menu-btn');
const mobileMenu = document.getElementById('mobile-menu');
const mobileMenuOverlay = document.getElementById('mobile-menu-overlay');

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

document.querySelector('.cta-button').addEventListener('click', function (e) {
    e.preventDefault();
    const modalOverlay = document.getElementById('modal-apply-overlay');
    if (modalOverlay) {
        modalOverlay.classList.add('show');
    }
});

openMenuBtn.addEventListener('click', function () {
    mobileMenu.classList.add('show');
    mobileMenuOverlay.style.display = 'block';
    setTimeout(() => {
        mobileMenuOverlay.classList.add('show');
    }, 10);
    document.body.style.overflow = 'hidden';
});

closeMenuBtn.addEventListener('click', closeMobileMenu);
mobileMenuOverlay.addEventListener('click', closeMobileMenu);

function closeMobileMenu() {
    mobileMenu.classList.remove('show');
    mobileMenuOverlay.classList.remove('show');
    setTimeout(() => {
        mobileMenuOverlay.style.display = 'none';
    }, 350);
    document.body.style.overflow = '';
}

document.querySelectorAll('#nav-mobile-menu a').forEach(link => {
    link.addEventListener('click', closeMobileMenu);
});

const mobileCtaBtn = document.getElementById('mobile-cta-btn');
if (mobileCtaBtn) {
    mobileCtaBtn.addEventListener('click', function () {
        closeMobileMenu();
        const modalOverlay = document.getElementById('modal-apply-overlay');
        if (modalOverlay) {
            modalOverlay.classList.add('show');
        }
    });
}