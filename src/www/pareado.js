var nombre = document.getElementById("nombre");
var codigo = document.getElementById("codigo");
var boton = document.getElementById("parear");
var error1 = false;
var error2 = false;
var error3 = false;

function comprobarCampos(e){
    if(nombre.value == "" || /^\s*$/.test(nombre.value)){
        nombre.classList.add("vacio");
        nombre.classList.remove("valido0");
        error1 = true;
    }else{
        nombre.classList.remove("vacio");
        nombre.classList.add("valido");
        error1 = false;
    }
    if(codigo.value == "" || codigo.value.length !== 6){
        codigo.classList.add("vacio");
        codigo.classList.remove("valido");
        error2 = true;
        if(codigo.value.length !== 6){
            document.getElementById("msj").innerHTML = "The pair code must be 6 character string";
        }
    }else{
        codigo.classList.remove("vacio");
        codigo.classList.add("valido");
        error2 = false;
    }
    if(error1 || error2 || error3){
        e.preventDefault();
    }else{
        mensaje();
    }
}

function mensaje(){
    alert("Please, wait while we try to pair your device. When the device is paired you can come to this page to unpair it. \n\nThe page will be reloaded after 30 seconds, if the device dont show a new service paired, try again.");
}

boton.addEventListener("click", comprobarCampos);