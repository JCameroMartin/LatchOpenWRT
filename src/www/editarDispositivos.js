var alias = document.getElementById("alias");
var boton = document.getElementById("guardar");
var aliasReg = /^([A-Z]|[a-z]|[0-9])([A-Z]|[a-z]|\s|[0-9])*$/;

function comprobarCampos(e){
    if(alias.value == "" || !aliasReg.test(alias.value)){
        alias.classList.add("vacio");
        alias.classList.remove("valido");
        e.preventDefault();
    }else{
        alias.classList.remove("vacio");
        alias.classList.add("valido");
        if(document.getElementById("permanente").checked){
            		mensaje(e);
        }
    }
}

function mensaje(e){
    if(!confirm("CAUTION: You have the permanent MAC option selected. \n\nThis option will let the selected MAC connect without control from the mobile app Latch. \n\nThis option is based in a simple MAC filter and isn't as secure as manual control from Latch service.")){
        e.preventDefault();
    }
}

boton.addEventListener("click", comprobarCampos);