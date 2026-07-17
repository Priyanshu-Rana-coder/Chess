const user = JSON.parse(sessionStorage.getItem("user"));

if (!user || !user.token)
    window.location.href = "../login_page/login_page.html";

const roomId = sessionStorage.getItem("room_id");

if (!roomId)
    window.location.href = "../room_page/room.html";

document.getElementById("room-id").textContent = `Room ID : ${roomId}`;

const socket = new WebSocket(`ws://127.0.0.1:8000/ws/${roomId}?token=${user.token}`);

const drawBtn = document.getElementById("draw-btn");
const resignBtn = document.getElementById("resign-btn");
const board = document.querySelector(".chess-board");
const flipBtn = document.getElementById("flip-btn");
const status = document.getElementById("game-status");

let drawRequested = false;
let flipped = false;
let selectedSquare = null;
let selectedElement = null;

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

    if (data.type === "draw_offer") {
        drawRequested = true;
        drawBtn.style.background = "linear-gradient(to right, #4caf50 50%, #ffcc00 50%)";
        status.textContent = "Opponent offered a draw";
        return;
    }

    if (data.type === "draw") {
        drawRequested = false;
        drawBtn.style.background = "";
        status.textContent = "Game Drawn by Agreement";
        return;
    }

    if (data.type === "resign") {
        drawRequested = false;
        drawBtn.style.background = "";
        status.textContent = data.winner === user.username ? "You Win by Resignation" : "You Lose by Resignation";
        return;
    }

    if (!data.success) {
        console.log("Illegal Move");
        return;
    }

    drawRequested = false;
    drawBtn.style.background = "";
    drawBoard(data.board);

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

drawBtn.addEventListener("click", function() {
    console.log("Draw clicked", socket.readyState);
    if (socket.readyState !== WebSocket.OPEN)
        return;
    console.log("Sending draw");
    socket.send(JSON.stringify({ draw: true }));
    drawBtn.style.background = "linear-gradient(to right, #4caf50 50%, #ffcc00 50%)";
});

resignBtn.addEventListener("click", function() {
    if (socket.readyState !== WebSocket.OPEN)
        return;

    if (confirm("Are you sure you want to resign?"))
        socket.send(JSON.stringify({ resign: true }));
});

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

        const move = { from: selectedSquare, to: [x, y] };

        console.log("Sending:", move);

        if (socket.readyState === WebSocket.OPEN)
            socket.send(JSON.stringify(move));

        selectedElement.style.backgroundColor = "";
        selectedSquare = null;
        selectedElement = null;
    });
});

flipBtn.addEventListener("click", function() {
    flipped = !flipped;

    if (flipped)
        board.classList.add("flipped");
    else
        board.classList.remove("flipped");
});