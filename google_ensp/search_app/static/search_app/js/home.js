const RANDOM_BACKDGROUND = true;
const NB_BACKGROUND = 22;
const FREQUENCE_CHANGE = 1; // 1 heure

window.onload = function() {
    let imageSrc = '';
    let membres = document.querySelector('.membres');
    let footer = document.querySelector('.footer');
    let form = document.querySelector('search');

    footer.style.width = window.outerWidth + 'px';

    if (RANDOM_BACKDGROUND) {
        let randInt = parseInt(1+Math.random()*NB_BACKGROUND);
        let randString = randInt<10?'0'+randInt:''+randInt;
        imageSrc = `../static/search_app/assets/backgrounds/${randString}.jpg`
    } else {
        imageSrc = `../static/search_app/assets/backgrounds/09.jpg`
    }

    document.querySelector('body').setAttribute('background', imageSrc);
    document.querySelector('#display-membres').addEventListener('mouseover', () => {
        membres.style.opacity = '1';
    });
    document.querySelector('#display-membres').addEventListener('mouseout', () => {
        membres.style.opacity = '0';
    });
    window.addEventListener('resize', () => {
        footer.style.width = window.outerWidth + 'px';
    });
}
