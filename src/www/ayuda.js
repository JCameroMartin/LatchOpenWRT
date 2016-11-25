var botones = document.getElementsByClassName("tab");
var textos = document.getElementsByClassName("texto");

function mostrar(elemento){
    for(i=0;i<textos.length;i++){
        textos[i].classList.remove("view");
        textos[i].classList.add("none");
    }
    for(i=0;i<botones.length;i++){
        botones[i].classList.remove("cbi-tab");
        botones[i].classList.add("cbi-tab-disabled");
    }
    document.getElementById(elemento).parentNode.classList.remove("cbi-tab-disabled");
    document.getElementById(elemento).parentNode.classList.add("cbi-tab");
    if(elemento == "btnConfiguracion"){document.getElementById("configuration").classList.add("view");}
    if(elemento == "btnParear"){document.getElementById("pair").classList.add("view");}
    if(elemento == "btnDispositivos"){document.getElementById("devices").classList.add("view");}
    if(elemento == "btnAdministrar"){document.getElementById("administration").classList.add("view");}
}

for(i=0;i<botones.length;i++){
    botones[i].addEventListener("click", function(e){
        mostrar(e.target.id);
    });
}