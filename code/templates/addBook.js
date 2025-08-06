const socket = io('http://localhost:5000');

document.addEventListener("DOMContentLoaded", () => {
    const submit = document.getElementById('add');

    if (submit) {
        submit.addEventListener('click', () => {
            title = document.getElementById('title').value;
            author = document.getElementById('Author').value;
            copies = document.getElementById('copies').value;

            const array = [title, author, copies]

            console.log(title, author, copies);

            if (title && author && copies) {
                socket.emit("add_book", array, (result) => {
                    console.log(result)
                    window.location.href = "C:/Users/harry/OneDrive - Nord Anglia Education/Desktop 1/computing coursework/templates/systemScreen.html";
                });
            }
        });
    } else {
        console.error("Add button not found.");
    }
});