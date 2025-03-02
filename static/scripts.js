document.addEventListener("keydown", function(event) {
    if (event.ctrlKey && event.key === "u") {
        alert("View Source is disabled!");
        event.preventDefault();
    }
});

function logout() {
    window.location.href = "/logout";
}

function sendMessage(event) {
    if (event.key === "Enter") {
        let message = document.getElementById("message").value;

        if (message.trim() !== "") {
            // Check if the device supports emojis
            let canvas = document.createElement("canvas");
            let ctx = canvas.getContext("2d");
            ctx.font = "16px Arial";
            ctx.fillText("😀", 0, 16);
            let supportsEmoji = ctx.getImageData(0, 0, 16, 16).data.some(channel => channel !== 0);

            if (!supportsEmoji) {
                message = message.replace(/[\u{1F600}-\u{1F64F}]/gu, ""); // Remove emojis if not supported
            }

            let chatBox = document.getElementById("chat-box");
            let newMessage = document.createElement("p");
            newMessage.textContent = "You: " + message;
            chatBox.appendChild(newMessage);
            document.getElementById("message").value = "";
        }
    }
}
