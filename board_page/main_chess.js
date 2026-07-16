const user = JSON.parse(sessionStorage.getItem("user"));

if (!user || !user.token)
    window.location.href = "../login_page/login_page.html";

const roomId = sessionStorage.getItem("room_id");

if (!roomId)
    window.location.href = "../room_page/room.html";

document.getElementById("room-id").textContent = `Room ID : ${roomId}`;

const socket = new WebSocket(`ws://127.0.0.1:8000/ws/${roomId}?token=${user.token}`);

function drawBoard(board) {
    for (let i = 0; i < 8; i++)
        for (let j = 0; j < 8; j++)
            document.getElementById(`${i}-${j}`).textContent = board[i][j];
}

socket.onopen = function() {
    console.log("Connected to websocket");
};

socket.onclose = function() {
    console.log("Disconnected");
};

socket.onerror = function(error) {
    console.log(error);
};

socket.onmessage = function(event) {
    const data = JSON.parse(event.data);

    if (data.type === "connected") {
        console.log("Server accepted connection");
        return;
    }

    if (!data.success) {
        console.log("Illegal Move");
        return;
    }

    drawBoard(data.board);

    const status = document.getElementById("game-status");

    if (data.checkmate)
        status.textContent = data.white_move ? "Black Wins by Checkmate" : "White Wins by Checkmate";
    else if (data.stalemate)
        status.textContent = "Game Drawn (Stalemate)";
    else if (data.check)
        status.textContent = data.white_move ? "White is in Check" : "Black is in Check";
    else
        status.textContent = data.white_move ? "White to Move" : "Black to Move";

    console.log(data);
};

let selectedSquare = null;
let selectedElement = null;

const squares = document.querySelectorAll(".square");

squares.forEach(square => {
    square.addEventListener("click", function() {
        const [x, y] = square.id.split("-").map(Number);

        if (selectedSquare === null) {
            selectedSquare = [x, y];
            selectedElement = square;
            square.style.backgroundColor = "red";
            return;
        }

        const move = {
            from: selectedSquare,
            to: [x, y]
        };

        console.log("Sending:", move);

        if (socket.readyState === WebSocket.OPEN)
            socket.send(JSON.stringify(move));

        selectedElement.style.backgroundColor = "";
        selectedSquare = null;
        selectedElement = null;
    });
});

const board = document.querySelector(".chess-board");
const flipBtn = document.getElementById("flip-btn");

let flipped = false;

flipBtn.addEventListener("click", function() {
    flipped = !flipped;

    if (flipped)
        board.classList.add("flipped");
    else
        board.classList.remove("flipped");
});