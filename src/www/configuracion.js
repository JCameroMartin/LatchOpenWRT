var aplicacionID = document.getElementById("applicationId");
var password = document.getElementById("password");
var tiempo = document.getElementById("tiempoComprobacion");
var error = document.getElementById("error");
var msj = document.getElementById("msj");
var boton = document.getElementById("guardar");
var error1 = false;
var error2 = false;
var error3 = false;

function comprobarCampos(e){
    if(aplicacionID.value == "" || /^\s*$/.test(aplicacionID.value)){
        aplicacionID.classList.add("vacio");
        aplicacionID.classList.remove("valido");
        error1 = true;
    }else{
        aplicacionID.classList.remove("vacio");
        aplicacionID.classList.add("valido");
        error1 = false;
    }
    if(password.value == "" || /^\s*$/.test(password.value)){
        password.classList.remove("valido");
        password.classList.add("vacio");
        error2 = true;
    }else{
        password.classList.remove("vacio");
        password.classList.add("valido");
        error2 = false;
    }
    if(tiempo.value == "" || /^\s*$/.test(tiempo.value) || !/^\d*$/.test(tiempo.value) || tiempo.value < 15){
	if(tiempo.value < 15){
		error.setAttribute("style", "");
		msj.setAttribute("style", "display:none;");
	}
        tiempo.classList.remove("valido");
        tiempo.classList.add("vacio");
        error3 = true;
    }else{
	tiempo.classList.remove("vacio");
        tiempo.classList.add("valido");
        error3 = false;
    }
    if(error1 || error2 || error3){
        e.preventDefault();
    }
}

boton.addEventListener("click", comprobarCampos);