const socket = io('http://localhost:5000');

document.addEventListener("DOMContentLoaded", () => {

    const params = new URLSearchParams(window.location.search);
    const title = params.get("title");
    const author = params.get("author");

    const titleInput = document.getElementById("title");
    const authorInput = document.getElementById("Author");

    if (titleInput && title) {
        titleInput.value = title;
    }

    if (authorInput && author) {
        authorInput.value = author;
    }

    const submit = document.getElementById("submit");

    if (submit) {
        submit.addEventListener('click', () => {
            const titleSubmit = document.getElementById("title").value;
            const authorSubmit = document.getElementById("Author").value;
            const nameSubmit = document.getElementById("name").value;
            const timeSubmit = document.getElementById("time").value;

            const array = [titleSubmit, authorSubmit, nameSubmit, timeSubmit]

            console.log(titleSubmit, authorSubmit, nameSubmit, timeSubmit);

            if (titleSubmit && authorSubmit && nameSubmit && timeSubmit) {
                socket.emit("check_out", array, (result, recipt) => {
                    console.log(result)
                    console.log(recipt)
                });
            }
        });
    }

});

