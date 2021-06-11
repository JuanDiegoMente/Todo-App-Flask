// 8/7/21

/** Archivo creado para la verificacion
 * de que la contraseña sea lo suficientemente "segura"
 * y asgurarse de que cuando se le de al btn para crear usuario
 * todos los campos esten listos!
 * */
let campoPassword = document.getElementById('password');
let quetansegura = document.getElementById('que-tan-segura');
let btnSubmit = document.getElementById('listo')

// Desactivamos el boton hasta que la password no sea segura
btnSubmit.disabled = true;


function seguridadCaracteres(str_) {
    // Devuelve N coincidencias y dependiendo a eso decimos que tan segura es la password
    // es inventado ya que no nos basamos en algo especifico
    let regex = /[!?-_.]/g
    let matches = [...str_.matchAll(regex)];
    console.log(str_, "->", matches.length)
    return matches.length;
}

campoPassword.addEventListener('change', (e) => {
    const textValue = e.target.value;

    if (textValue.length <= 10 || seguridadCaracteres(textValue) === 0) {
        quetansegura.innerText = "Intenta que sea mas larga e incluya caracteres seguros!";
        campoPassword.style.border = "1px solid red";
        btnSubmit.disabled = true;

        let email = document.getElementById('email');
        console.log(email.textContent)
    }
    if (textValue.length >= 10 && seguridadCaracteres(textValue) >= 1) {
        quetansegura.innerText = "Perfecta!";
        campoPassword.style.border = "1px solid lightgrey";
        btnSubmit.disabled = false;
    }

});


const vEmail = (email_) => {
    let regexEmail = /^[a-zA-Z0-9_.+-]+@[a-z]+.com$/;
    return regexEmail.test(email_);
}

const vNameUser = (userName) => {
    let regex1 = /^[a-zA-Z0-0\_\-]{6,16}$/;
    return regex1.test(userName);
}


btnSubmit.addEventListener('click', () => {
    let username = document.getElementById('username');
    let email = document.getElementById('email');

    // No verificamos la password  ya que si se activo el boton es porque la password esta bien
    if (!vEmail(email.value) || !vNameUser(username.value)) {
        swal("Ups...", "Verifica los campos, de seguro de falta algo!", "error");
    }

})


/***
 *
 *
 */



