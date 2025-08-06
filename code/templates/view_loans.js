const socket = io('http://localhost:5000');

document.addEventListener("DOMContentLoaded", () => {

    socket.emit('view_out', (''), (result) => {

    const table = document.createElement('table');
    table.border = 1;
    table.style.marginTop = '20px';
    table.style.borderCollapse = 'collapse';
    table.style.width = '80%';
    table.className = 'center';

    const headerRow = document.createElement('tr');
    const headers = ['uuid', 'book id', 'date borrowed', 'due date', 'returned', 'overdue']

    for(let h of headers) {
        const th = document.createElement('th');
        th.textContent = h;
        th.style.padding = '8px';
        th.style.backgroundColor = '#f2f2f2';
        headerRow.appendChild(th);
    }
    table.appendChild(headerRow)

    for(let item of result) {
        console.log(item);

        const row = document.createElement('tr');

        const uuidCell = document.createElement('td');
        uuidCell.textContent = item[0];
        uuidCell.style.padding = '8px';

        const bookidCell = document.createElement('td');
        bookidCell.textContent = item[1];
        bookidCell.style.padding = '8px';

        const datebCell = document.createElement('td');
        datebCell.textContent = item[2];
        datebCell.style.padding = '8px';

        const duedateCell = document.createElement('td');
        duedateCell.textContent = item[3];
        duedateCell.style.padding = '8px';

        const returnedCell = document.createElement('td');
        returnedCell.textContent = item[4];
        returnedCell.style.padding = '8px';

        const overdueCell = document.createElement('td');
        overdueCell.textContent = item[5];
        overdueCell.style.padding = '8px';

        row.appendChild(uuidCell);
        row.appendChild(bookidCell);
        row.appendChild(datebCell);
        row.appendChild(duedateCell);
        row.appendChild(returnedCell);
        row.appendChild(overdueCell);

        table.appendChild(row);

    }

    document.getElementById('container-left').appendChild(table);

});

});


