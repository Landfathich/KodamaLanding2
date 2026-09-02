function onWindowResize() {
    const button = document.getElementById("open-menu-btn");
    const mobile_menu = document.getElementById("mobile-menu");
    if (window.innerWidth >= 768) {
        button.style.display = "";
        mobile_menu.style.display = "";
    }
}

window.addEventListener("resize", onWindowResize);

document.getElementById('current-year').textContent = new Date().getFullYear();