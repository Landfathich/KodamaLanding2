function getImagePath(imageName) {
    return `${images}/${imageName}`;
}

function preloadImage(img_url) {
    let img = new Image();
    img.src = img_url;
}

function onWindowResize() {
    const button = document.getElementById("open-menu-btn");
    const mobile_menu = document.getElementById("mobile-menu");
    if (window.innerWidth >= 768) {
        button.style.display = "";
        mobile_menu.style.display = "";
    } else {

    }
}

window.addEventListener("resize", onWindowResize);

// header
preloadImage(getImagePath("logo.webp"))
preloadImage(getImagePath("logo_scrolled.webp"))

// preload only for mobile version
if (window.innerWidth < 768) {
    // mobile menu
    preloadImage(getImagePath("mobile_menu_bg.webp"))
    preloadImage(getImagePath("close_mobile_menu_btn.webp"))
    preloadImage(getImagePath("logo.webp"))
    preloadImage(getImagePath("about_icon.webp"))
    preloadImage(getImagePath("courses_icon.webp"))
    preloadImage(getImagePath("feedbacks_icon.webp"))
    preloadImage(getImagePath("contacts_icon.webp"))
}

// preload only for desktop version
if (window.innerWidth >= 768) {

}

// COURSES

// figma
preloadImage(getImagePath("figma_logo.webp"))
preloadImage(getImagePath("course_figma1.webp"))
preloadImage(getImagePath("course_figma2.webp"))

// scratch
preloadImage(getImagePath("scratch_logo.webp"))
preloadImage(getImagePath("course_scratch1.webp"))
preloadImage(getImagePath("course_scratch2.webp"))

// computer literacy
preloadImage(getImagePath("comp_lit_logo.webp"))
preloadImage(getImagePath("course_comp_lit1.webp"))
preloadImage(getImagePath("course_comp_lit2.webp"))

// roblox
preloadImage(getImagePath("roblox_logo.webp"))
preloadImage(getImagePath("course_roblox1.webp"))
preloadImage(getImagePath("course_roblox2.webp"))

// roblox
preloadImage(getImagePath("roblox_logo.webp"))
preloadImage(getImagePath("course_roblox1.webp"))
preloadImage(getImagePath("course_roblox2.webp"))

// blender
preloadImage(getImagePath("blender_logo.webp"))
preloadImage(getImagePath("course_blender1.webp"))
preloadImage(getImagePath("course_blender2.webp"))

// web development
preloadImage(getImagePath("web_development_logo.webp"))
preloadImage(getImagePath("course_web_dev1.webp"))
preloadImage(getImagePath("course_web_dev2.webp"))

// python
preloadImage(getImagePath("python_logo.webp"))
preloadImage(getImagePath("course_python1.webp"))
preloadImage(getImagePath("course_python2.webp"))

// unity
preloadImage(getImagePath("unity_logo.webp"))
preloadImage(getImagePath("course_unity1.webp"))
preloadImage(getImagePath("course_unity2.webp"))

// olympic programming
preloadImage(getImagePath("olympic_programming_logo.webp"))
preloadImage(getImagePath("course_olympic1.webp"))
preloadImage(getImagePath("course_olympic2.webp"))

// c++
preloadImage(getImagePath("cpp_logo.webp"))
preloadImage(getImagePath("course_cpp1.webp"))
preloadImage(getImagePath("course_cpp2.webp"))

// android
preloadImage(getImagePath("android_logo.webp"))

// unreal engine
preloadImage(getImagePath("unreal_engine_logo.webp"))


// SUBMIT APP
preloadImage(getImagePath("default_submit.webp"))
preloadImage(getImagePath("figma_submit.webp"))
preloadImage(getImagePath("roblox_submit.webp"))
preloadImage(getImagePath("comp_lit_submit.webp"))
preloadImage(getImagePath("scratch_submit.webp"))
preloadImage(getImagePath("blender_submit.webp"))
preloadImage(getImagePath("web_dev_submit.webp"))
preloadImage(getImagePath("python_submit.webp"))
preloadImage(getImagePath("olympic_submit.webp"))
preloadImage(getImagePath("unity_submit.webp"))
preloadImage(getImagePath("cpp_submit.webp"))

document.getElementById('current-year').textContent = new Date().getFullYear();
