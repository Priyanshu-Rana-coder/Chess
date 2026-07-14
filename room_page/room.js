const user = JSON.parse(sessionStorage.getItem("user"));

if (!user || !user.token) {
    window.location.href = "../login_page/login_page.html";
}

document.getElementById("username").textContent = `♔ ${user.username}`;
document.getElementById("wins").textContent = `🏆 ${user.wins}`;
document.getElementById("losses").textContent = `❌ ${user.losses}`;
document.getElementById("draws").textContent = `🤝 ${user.draws}`;