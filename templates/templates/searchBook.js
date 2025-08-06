const socket = io('http://localhost:5000');

document.addEventListener("DOMContentLoaded", () => {
    const submit = document.getElementById('search');

    if (submit) {
        submit.addEventListener('click', () => {
            title = document.getElementById('title').value;
            author = document.getElementById('Author').value;
            if (title === ""){

            } else{
                var searchTitle = title
            }
            if (author === ""){

            } else{
                var searchAuthor = author
            }

            const array = [searchTitle, searchAuthor]

            console.log(title, author);
            
            socket.emit("search", array, (result) => {

                const title = document.getElementById('title');
                const author = document.getElementById('Author');
                const btn = document.getElementById('search');

                if(title) title.remove();
                if(author) author.remove();
                if(btn) btn.remove();
                
                const table = document.createElement('table');
                table.border = 1;
                table.style.marginTop = '20px';
                table.style.borderCollapse = 'collapse';
                table.style.width = '80%';
                table.className = 'center';

                const headerRow = document.createElement('tr');
                const headers = ['Title', 'Author', 'In Stock', 'Sign Out']

                for (let h of headers) {
                    const th = document.createElement('th');
                    th.textContent = h;
                    th.style.padding = '8px';
                    th.style.backgroundColor = '#f2f2f2';
                    headerRow.appendChild(th);
                }
                table.appendChild(headerRow);

                for (let item of result) {
                    console.log(item);

                    const row = document.createElement('tr');

                    const titleCell = document.createElement('td');
                    titleCell.textContent = item[0];
                    titleCell.style.padding = '8px';

                    const authorCell = document.createElement('td');
                    authorCell.textContent = item[1];
                    authorCell.style.padding = '8px';

                    const stockCell = document.createElement('td');
                    stockCell.textContent = item[2] ? 'Yes' : 'No';
                    stockCell.style.padding = '8px';
                    
                    const signOut_btns = document.createElement('button');
                    signOut_btns.textContent = "Sign Out";
                    signOut_btns.style.padding = '8px';
                    signOut_btns.className = "sign-out-btn"

                    signOut_btns.addEventListener('click', () => {
                    const titleParam = encodeURIComponent(item[0]);   
                    const authorParam = encodeURIComponent(item[1]);
                    window.location.href = `checkOutForm.html?title=${titleParam}&author=${authorParam}`;
                    });
                    
                    row.appendChild(titleCell);
                    row.appendChild(authorCell);
                    row.appendChild(stockCell);
                    row.appendChild(signOut_btns);

                    table.appendChild(row);
                }

                document.getElementById('container-left').appendChild(table);
               
                const allSOBtn = document.querySelectorAll('.sign-out-btn');
                allSOBtn.forEach((btn) =>{

                    btn.addEventListener('click', () => {

                        const title = encodeURIComponent(item[0]);   
                        const author = encodeURIComponent(item[1]);
                        window.location.href = `checkOutForm.html?title=${title}&author=${author}`;

                    });

                });
            });
        });
    } else {
        console.error("Search button not found.");
    }
});