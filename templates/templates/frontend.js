const signUpButton = document.getElementById('signUp');
const signInButton = document.getElementById('signIn');
const container = document.getElementById('container');


signUpButton.addEventListener('click', () => {
    container.classList.add("right-panel-active");
});

signInButton.addEventListener('click', () => {
    container.classList.remove("right-panel-active");
});

const socket = io('http://localhost:5000');

document.addEventListener("DOMContentLoaded", () => {

    const signupSubmit = document.getElementById('get-signUp');
    const signInSubmit = document.getElementById('get-signIn');


    if (signInSubmit) {
        signInSubmit.addEventListener('click', () => {

            uName_input = document.getElementById('uname').value;
            password_input = document.getElementById('password').value;

            console.log(uName_input);
            console.log(password_input);

            const array = [uName_input,password_input]

            if (uName_input && password_input) {
                socket.emit("login_check", array, (result) => {
                    if (result === true) {
                        window.location.href = "C:/Users/harry/OneDrive - Nord Anglia Education/Desktop 1/computing coursework/templates/systemScreen.html";
                    } else{alert("Invalid username or password")}

                });
            }
        });
    }


    if (signupSubmit) {
        signupSubmit.addEventListener('click', () => {


            nameInput = document.getElementById('name').value;
            emailInput = document.getElementById('email').value;
            passwordInput = document.getElementById('pass').value;
            confpasswordInput = document.getElementById('confpass').value;

            const array = [nameInput,emailInput,passwordInput]

            console.log(array)

            if (passwordInput === confpasswordInput) {

                socket.emit("create_user", array, (response) => {
                    console.log(response)
                    window.location.href = "C:/Users/harry/OneDrive - Nord Anglia Education/Desktop 1/computing coursework/templates/frontend.html"
                });

            }

        });
    }

});
