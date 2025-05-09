let LIST = [];
let dateOrder = true;
let numOrder = false;

function getResponseList(ip) {
    fetch(`../API/image.php`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
        .then(response => response.json())
        .then(r => {
            LIST = r;

            //  Json che voglio
            // {
            //     image: "data:image/png;base64,iVB...",
            //     prediction: 3,
            //     date: "22/05/2025 15:55",
            // }

            console.log(r); //stampo la risposta dell'🐝🐝
            printList(LIST);

        })
        .catch(e => {
            console.error(e);
        });
}


function printList(list) {
    const listContainer = document.getElementById('list-container');
    let cards = '';

    if (list)
        list.forEach(item => {
            cards = `
        <div class='card'>
            <img src='${item.image}' alt='number to guess' loading='lazy'>
            <div class='data'>
                <div class='date'>${item.date}</div>
                <div class='guess'>${item.prediction}</div>
            </div>
        </div>
        ` + cards;
        });

    listContainer.innerHTML = cards;
}


// Funzione per ottenere il valore numerico di una variabile (che puo essere sia numero che stringa di length 1)
const getValue = (x) => {
    if (typeof x.prediction === 'string') {
        // Se è una stringa, restituisci il codice del primo carattere
        return x.prediction.charCodeAt(0);
    } else {
        // Altrimenti usa direttamente il numero
        return x.prediction;
    }
};

function orderBy(param, list, callback) {
    switch (param) {
        case 'date':
            if (dateOrder)
                list.sort((a, b) => (new Date(b.date.split('/').reverse().join('-'))) - new Date(a.date.split('/').reverse().join('-')));
            else
                list.sort((a, b) => (new Date(a.date.split('/').reverse().join('-')) - new Date(b.date.split('/').reverse().join('-'))));
            dateOrder = !dateOrder;
            numOrder = false;
            break;
        case 'number':
            if (numOrder)
                list.sort((a, b) => { return getValue(a) - getValue(b); });
            else
                list.sort((a, b) => { return getValue(b) - getValue(a); });
            numOrder = !numOrder;
            dateOrder = false;
            break;
        default: break;
    }

    window.scrollTo({
        top: 0,
        left: 0,
        behavior: 'smooth'
    });

    callback(list);
}