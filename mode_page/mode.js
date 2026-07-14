const user = JSON.parse(sessionStorage.getItem("user"));

if (!user || !user.token) {
    window.location.href = "../login_page/login_page.html";
}

document.getElementById("pvp-btn").addEventListener("click", function () {
    window.location.href = "../room_page/room.html";
});