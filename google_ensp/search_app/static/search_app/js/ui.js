'use strict';
/**
 * @todo
 * à réaliser avec jQuery
 */
var typeResultats = 0;
(function() {
    let conteneur = document.querySelector('.conteneur');
    let entete3 = document.querySelector(".entete-3");
    let membres = document.querySelector('.membres');
    let footer = document.querySelector('.footer');
    let defaultW = (window.outerWidth-20);
    let defaultH = (window.outerHeight-200);

    conteneur.style.width = Math.max(window.innerWidth, defaultW) + 'px';
    conteneur.style.height = Math.max(window.innerHeight, defaultH) + 'px';
    let h = parseInt(conteneur.style.height);
    footer.style.top = Math.max(conteneur.scrollHeight-35, h-35) + 'px';

    document.querySelectorAll(".filtre").forEach(function(item) {
        item.addEventListener("click", function() {
            if (item.classList.contains("inactif")) {
                // let typeResultats = index;
                item.classList.remove("inactif");
                item.classList.add("actif");
                for (let elt of this.parentNode.childNodes) {
                    if (elt != this && (!elt.classList ? false : elt.classList.contains("actif"))) {
                        elt.classList.remove("actif");
                        elt.classList.add("inactif");
                        return;
                    }
                }
            }
        });
    });
    document.querySelector(".recherche-avance").addEventListener("click", function() {
        console.log("click !")
        let actif = this.classList.contains("actif");
        if (!actif) {
            this.classList.add("actif");
            entete3.style.display = "block";
        } else {
            this.classList.remove("actif");
            entete3.style.display = "none";
        }
    });
    document.querySelector('#display-membres').addEventListener('mouseover', () => {
        membres.style.opacity = '1';
    });
    document.querySelector('#display-membres').addEventListener('mouseout', () => {
        membres.style.opacity = '0';
    });
    window.onresize = () => {
        conteneur.style.width = Math.max(window.innerWidth, defaultW) + 'px';
        conteneur.style.height = Math.max(window.innerHeight, defaultH) + 'px';
        let h = parseInt(conteneur.style.height);
        footer.style.top = Math.max(conteneur.scrollHeight-35, h-35) + 'px';
        // showFooter();
    };
    // conteneur.addEventListener('scroll', showFooter);
})();
