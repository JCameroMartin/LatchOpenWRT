var alias = document.getElementById("alias");
var mac = document.getElementById("mac");
var boton = document.getElementById("anadir");
var aliasReg = /^([A-Z]|[a-z]|[0-9])([A-Z]|[a-z]|\s|[0-9])+$/;
var macReg = /^([0-9A-Fa-f]{2}[:]){5}([0-9A-Fa-f]{2})$/;
var error1 = false;
var error2 = false;

function comprobarCampos(e){
    if(!aliasReg.test(alias.value)){
        alias.classList.add("vacio");
        alias.classList.remove("valido");
        error1 = true;
    }else{
        alias.classList.remove("vacio");
        alias.classList.add("valido");
        error1 = false;
    }
    if(!macReg.test(mac.value)){
        mac.classList.add("vacio");
        mac.classList.remove("valido");
        error2 = true;
        document.getElementById("msj").innerHTML = "MAC must be a valid format(a0:a0:a0:a0:a0:a0)";
    }else{
        mac.classList.remove("vacio");
        mac.classList.add("valido");
        error2 = false;
        document.getElementById("msj").innerHTML = "";
    }
    if(error1 || error2){
        e.preventDefault();
    }else{
        mensaje(e);
    }
}

function mensaje(e){
    if(!confirm("CAUTION: You are trying to link a permanent MAC. \n\nThis option will let the selected MAC connect without control from the mobile app Latch. \n\nThis option is based in a simple MAC filter and isn't as secure as manual control from Latch service.")){
        e.preventDefault();
    }
}

boton.addEventListener("click", comprobarCampos);