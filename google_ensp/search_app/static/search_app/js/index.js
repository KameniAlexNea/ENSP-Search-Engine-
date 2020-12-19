'use strict';

// paramètres du serveur
var PROTOCOL = 'http';
var HOST_NAME = 'localhost';
var PORT_NUMBER = '8000';

// Varialbles de requêtes cse
var cx = "012798039226510677058:enprrz7xr7p";
var key = "AIzaSyAz2EdlSyK-yKlB1xvYCOBgyYC-Ftcc2rE";
const CSE = {
    jour: {
        key: 'dateRestrict',
        value: 'd[1]'
    },
    semaine: {
        key: 'dateRestrict',
        value: 'w[1]'
    },
    mois: {
        key: 'dateRestrict',
        value: 'm[1]'
    },
    an: {
        key: 'dateRestrict',
        value: 'y[1]'
    },
    fr: {
        key: 'lr',
        value: 'lang_fr',
    },
    en: {
        key: 'lr',
        value: 'lang_en',
    }
}

// constantes du DOM
const OPACITY_MESSAGES = '0.3';

// variables du DOM
var form = document.querySelector("#search_form");
var conteneur = document.querySelector('.conteneur');

//variables javascrip
var filter_activate = true;
var response = null;
var index = 1;
var hist = [1];
var url = null;
var global_query = null;

function filter(query, start, filtered) {
    return new Promise((resolve, reject) => {
        url = new URL(`${PROTOCOL}://${HOST_NAME}:${PORT_NUMBER}`);
        url.pathname = filtered ? '/filter' : '/all'; 
        url.searchParams.set('q', query);
        url.searchParams.set('index', String(start));
        console.log(url);
        fetch(url.href, {
            method: "GET", // *GET, POST, PUT, DELETE, etc.
            mode: "cors", // no-cors, cors, *same-origin
        }).then(res => {
            res.json().then(data => {
                console.log(data);
                index = parseInt(data.meta.index) + 1;
                hist.push(index);
                resolve(data);
            });
        }).catch(err => {
            reject(err);
        });
    });
}

function printFilterredResult(data) {
    let meta = data.meta;
    let items = data.items;
    let urlItem = null;
    let link = '';
    let title = '';
    let displayLink = '';
    let origin = '';
    let imgSrc = '';
    let htmlSnippet = '';
    let scrapedSnipped = '';
    // let webscrapedSnipped = '';
    let conteneur = document.querySelector('#resultats');

    // affichage des métas données de la recherche
    conteneur.innerHTML = `
        <div class="meta-info">
            <span class="number gris" id="search-time">${meta.formattedSearchTime}</span>
            seconde${parseInt(meta.searchTime)>1?'s':''}
        </div>`;

    // affichage des résultats de la recherche
    for (let item of items) {
        link = item.link;
        title = item.title;
        scrapedSnipped = item.scrapedSnipped;
        displayLink = item.displayLink;
        htmlSnippet = item.htmlSnippet;
        urlItem = new URL(link)
        origin = urlItem.origin
        imgSrc = `${origin}/favicon.ico`;

        conteneur.innerHTML += `
            <div class="search-item">
                <div class="url-item">
                    <img src="${imgSrc}" alt="" width="16px">
                    <a href="${link}">${displayLink}</a>
                </div>
                <div class="title-item">
                    <a href="${link}" class="tooltip">${title}
                        <div class="right">
                            <h3>Résumé de contenu</h3>
                            <p>${scrapedSnipped}</p>
                            <i></i>
                        </div>
                    </a>
                </div>
                <div class="snipped-item">
                    ${htmlSnippet}
                </div>
            </div>`;
    }
}

form.addEventListener("submit", function(e) {
    let template = ``
    if(document.querySelector('#query').value == global_query) {
        e.preventDefault();
        console.log('pas besoin de soumettre le formulaire');
    }
});

window.onload = () => {
    conteneur.style.opacity = '1';
    let url = new URL(location.href);
    let url_query = url.searchParams;
    let query = url_query.get('q');  
    let searchInput = document.querySelector('#query');
    let cont = document.querySelector('.conteneur').style.height;
    let loader = document.querySelector('.results-loader');
    let filtered = false;

    updateIndex(url_query);

    searchInput.value = query;
    global_query = query;
    loader.style.height = cont;
    if (parseInt(url_query.get('filtered')) == 0) { // les resultats sont non filtrés
        filtered = false;
        let sf = document.querySelector('#sans-filtre');
        let af = document.querySelector('#avec-filtre')
        sf.classList.remove('inactif');
        sf.classList.add('actif');
        af.classList.remove('actif');
        af.classList.add('inactif');
    } else { // les resultats sont filtrés par défaut
        filtered = true;
    }
    url_query.delete('filtered');
    filter(query, index, filtered).then(data => {
        loader.style.opacity = '0';
        setTimeout(() => {
            loader.style.display = 'none';
        }, 400);
        printFilterredResult(data);
        window.onresize();
        updateHist();
        updateDomFromHist();

        // définition du compornement webscraping
        changeTypePage();
    }).catch(err => {
        document.querySelector('#loader-text').style.display = 'none';
        document.querySelector('#loader-image').style.display = 'none';
        document.querySelector('#error-text').style.display = 'block';
        setTimeout(() => {
            document.querySelector('#error-text').style.opacity = OPACITY_MESSAGES;
        }, 100);
        console.error(err);
    });
}

function changeTypePage() {
    let sansFiltre = document.querySelector('#sans-filtre');
    let avecFiltre = document.querySelector('#avec-filtre');

    avecFiltre.addEventListener('click', () => {
        let url = new URL(location.href);
        let searchParams = url.searchParams;
        searchParams.delete('filtered');
        location.assign(url.href);
    });

    sansFiltre.addEventListener('click', () => {
        let url = new URL(location.href);
        let searchParams = url.searchParams;
        searchParams.append('filtered', '0');
        location.assign(url.href);
    });
}

function updateHist() {
    let url = new URL(location.href);
    let currentActive = parseInt(url.searchParams.get('page'));
    if (!currentActive) {
        currentActive = 1;
    }
    if (currentActive == 1) {
        let navig = document.querySelector('.navigation');
        let firstChild = navig.firstElementChild;
        firstChild.style.display = 'none';
    } else {
        let navig = document.querySelector('.navigation');
        let firstChild = navig.firstElementChild;
        firstChild.style.display = 'block';
    }
    if (hist.length > 1 && index < 100) {
        let navig = document.querySelector('.navigation');
        let lastChild = navig.lastElementChild;
        lastChild.style.display = 'block';
    } else {
        let navig = document.querySelector('.navigation');
        let lastChild = navig.lastElementChild;
        lastChild.style.display = 'none';
    }
}

function updateIndex(query) {
    if(query.get('page')) {
        hist = query.get('hist').split(',');
        hist.map(function(value) {
            return parseInt(value);
        });
        index = hist[parseInt(query.get('page')) - 1];
        query.delete('page');
        query.delete('hist');
    }
}

function updateDomFromHist() {
    let tmpNode;
    let parentNode = document.querySelector('.navigation');
    let lastElementChild = parentNode.lastElementChild;
    let url = new URL(location.href);
    let currentIndex = parseInt(url.searchParams.get('page'));
    if (!currentIndex) {
        currentIndex = 1;
    }
    for (let i in hist) {
        tmpNode = document.createElement('button');
        tmpNode.classList.add('nav-number');
        if (i == currentIndex - 1) {
            tmpNode.classList.add('actif');
            tmpNode.setAttribute('id', 'id-page');
        }
        tmpNode.innerHTML = String(parseInt(i) + 1);
        parentNode.insertBefore(tmpNode, lastElementChild);
        tmpNode.addEventListener('click', (e) => {
            let url = new URL(location.href);
            url.searchParams.set('page', e.target.innerText);
            url.searchParams.set('hist', hist.join(','));
            location.assign(url.href);
        });
    }
    parentNode.firstElementChild.addEventListener('click', () => {
        let url = new URL(location.href);
        let currentActive = document.querySelector('.navigation').querySelector('.actif');
        if (parseInt(currentActive.innerHTML) > 1) {
            url.searchParams.set('page', (parseInt(currentActive.innerHTML) - 1) + '');
            url.searchParams.set('hist', hist.join(','));
            location.assign(url.href);
        }
    });
    parentNode.lastElementChild.addEventListener('click', () => {
        let url = new URL(location.href);
        let currentActive = document.querySelector('.navigation').querySelector('.actif');
        if (parseInt(currentActive.innerHTML) < hist.length) {
            url.searchParams.set('page', (parseInt(currentActive.innerHTML) + 1) + '');
            url.searchParams.set('hist', hist.join(','));
            location.assign(url.href);
        }
    });
}

function enrichQuery(extend) {
    let url = new URL(location.href);
    url.searchParams.append(CSE[extend].key, CSE[extend].value);
    location.assign(url.href);
}
