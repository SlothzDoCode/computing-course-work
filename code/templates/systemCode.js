document.addEventListener("DOMContentLoaded", () => {
    const addBooks_btn = document.getElementById('Add');
    const search_btn = document.getElementById('Search');
    const loanSearch_btn = document.getElementById('list-of-out');

    if (addBooks_btn) {
        addBooks_btn.addEventListener('click', () => {
            window.location.href = "C:/Users/harry/OneDrive - Nord Anglia Education/Desktop 1/computing coursework/templates/addBook.html";
        });
    } else {
        console.error("Add button not found.");
    }

    if (search_btn) {
        search_btn.addEventListener('click', () => {
            window.location.href = "C:/Users/harry/OneDrive - Nord Anglia Education/Desktop 1/computing coursework/templates/searchBook.html";
        });
    } else {
        console.error("Search button not found.");
    }

    if (loanSearch_btn) {
        loanSearch_btn.addEventListener('click', () => {
            window.location.href = "C:/Users/harry/OneDrive - Nord Anglia Education/Desktop 1/computing coursework/templates/view_loans.html";
        });
    } else {
        console.error("Loan search button not found.");
    }
});
