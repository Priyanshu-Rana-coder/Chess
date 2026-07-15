const user = JSON.parse(sessionStorage.getItem("user"));

if (!user || !user.token) {
    window.location.href = "../login_page/login_page.html";
}

const roomId = sessionStorage.getItem("room_id");

document.getElementById("room-id").textContent =
    `Room ID : ${roomId}`;
if (!roomId) {
    window.location.href = "../room_page/room.html";
}

const socket = new WebSocket(
    `ws://127.0.0.1:8000/ws/${roomId}?token=${user.token}`
);

socket.onopen = function () {
    console.log("Connected to websocket");
};

socket.onclose = function () {
    console.log("Disconnected");
};

socket.onerror = function (error) {
    console.log(error);
};

socket.onmessage = function (event) {

    const data = JSON.parse(event.data);

    if (data.type === "connected") {
        console.log("Server accepted connection");
        return;
    }

    console.log("Received:", data);

};

let selectedSquare = null;

const squares = document.querySelectorAll(".square");

squares.forEach(square => {

    square.addEventListener("click", function () {

        const [x, y] = square.id.split("-").map(Number);

        if (selectedSquare === null) {
            selectedSquare = [x, y];
            console.log("Selected:", selectedSquare);
            return;
        }

        const move = {
            from: selectedSquare,
            to: [x, y]
        };

        console.log("Sending:", move);

        if (socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify(move));
        }

        selectedSquare = null;

    });

});
const board = document.querySelector(".chess-board");
const flipBtn = document.getElementById("flip-btn");

let flipped = false;

flipBtn.addEventListener("click", function () {

    flipped = !flipped;

    if (flipped) {
        board.classList.add("flipped");
    } else {
        board.classList.remove("flipped");
    }

});