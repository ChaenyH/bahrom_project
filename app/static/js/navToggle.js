document.addEventListener("DOMContentLoaded", function () {
    const menuToggle = document.getElementById("menu-toggle");
    const navMenu = document.getElementById("nav-menu");
    const menuIcon = document.getElementById("menu-icon");

    const menuImage = menuIcon.dataset.menu;  // 메뉴 이미지 경로
    const closeImage = menuIcon.dataset.close; // 닫기 이미지 경로

    menuToggle.addEventListener("click", function () {
        navMenu.classList.toggle("active");

        // 이미지 변경
        if (navMenu.classList.contains("active")) {
            menuIcon.src = closeImage;  // 닫기 버튼 이미지
        } else {
            menuIcon.src = menuImage;  // 햄버거 버튼 이미지
        }
    });
});
