const form = document.getElementById("login-form");
const message = document.getElementById("message");
const loginButton = document.getElementById("login-btn");
form.addEventListener("submit", async function (event) {
    event.preventDefault();
    message.textContent = "";
    loginButton.disabled = true;
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;
    try {
        const response = await fetch("https://chess-production-7d07.up.railway.app/user/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });
        const data = await response.json();
        if (!response.ok) {
            message.textContent = data.detail;
            loginButton.disabled = false;
            return;
        }
        // Store user information
        sessionStorage.setItem("user", JSON.stringify(data));
        // Go to next page
        window.location.href = "../mode_page/mode.html";
    } catch (error) {
        console.error(error);
        message.textContent = "Unable to connect to server.";
        loginButton.disabled = false;
    }
});