const mobileLogo = document.getElementById('mobile-logo-link');

document.addEventListener('DOMContentLoaded', function () {
    const menuToggle = document.getElementById('open-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    const closeButton = document.getElementById('close-menu-btn');
    const menuButton = document.getElementById('open-menu-btn');
    const navLinks = document.querySelectorAll('#nav-mobile-menu a');

    function closeMenu() {
        mobileMenu.style.display = 'none';
        menuButton.style.display = 'block';
        document.body.classList.remove('no-scroll');
    }

    function openMenu() {
        mobileMenu.style.display = 'block';
        menuButton.style.display = 'none';
        document.body.classList.add('no-scroll');
    }

    menuToggle.addEventListener('click', function () {
        openMenu();
    });

    closeButton.addEventListener('click', function () {
        closeMenu();
    });

    mobileLogo.addEventListener('click', function () {
        closeMenu();
    })

    navLinks.forEach(function (link) {
        link.addEventListener('click', function () {
            closeMenu();
        });
    });
});