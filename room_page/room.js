const user = JSON.parse(sessionStorage.getItem("user"));
if (!user || !user.token) {
    window.location.href = "../login_page/login_page.html";
}
document.getElementById("username").textContent = `♔ ${user.username}`;
document.getElementById("wins").textContent = `🏆 ${user.wins}`;
document.getElementById("losses").textContent = `❌ ${user.losses}`;
document.getElementById("draws").textContent = `🤝 ${user.draws}`;


const createRoomBtn = document.getElementById("create-room-btn");
createRoomBtn.addEventListener("click", async function () {
    const response = await fetch("https://chess-production-7d07.up.railway.app/room/create", {
        method: "POST",
        headers: {
            "Authorization": `Bearer ${user.token}`
        }
    });
    const data = await response.json();
    document.getElementById("created-room").value = data.room_id;
    sessionStorage.setItem("room_id", data.room_id);
    window.location.href = "../board_page/main_chess.html";
});

const joinRoomBtn = document.getElementById("join-room-btn");
joinRoomBtn.addEventListener("click", async function () {
    const roomId = document.getElementById("join-room").value.trim();
    const response = await fetch("https://chess-production-7d07.up.railway.app/room/join", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${user.token}`
        },
        body: JSON.stringify({
            room_id: roomId
        })
    });
    const data = await response.json();
    sessionStorage.setItem("room_id", roomId);
    window.location.href = "../board_page/main_chess.html";
});