function toggleMenu() {
    const navbarLinks = document.querySelector('.navbar-links');
    navbarLinks.classList.toggle('active');
}



function toggleMenu() {
    var menudes = document.getElementById("menudes");
    if (menudes.style.right === '0px') {
        menudes.style.right = '-400px';
    } else {
        menudes.style.right = '0px';
    }
}


function toggleModo(element) {
    const isActive = element.classList.contains('active');
    element.classList.toggle('active'); 
}


let modoActivo = null;

function toggleModo(modoId, element) {
    if (modoActivo === null) {
        modoActivo = modoId;
        element.classList.add('active');
        showModal('El modo ha sido activado correctamente.');
    } else if (modoActivo === modoId) {
        modoActivo = null;
        element.classList.remove('active');
        showModal('El modo ha sido desactivado correctamente.');
    } else {
        showModal('Se debe desactivar el modo actual antes de seleccionar otro.');
    }
}

function showModal(message) {
    var modal = document.getElementById("modal");
    var modalMessage = document.getElementById("modalMessage");
    modalMessage.textContent = message; 
    modal.style.display = "block";
}


var span = document.getElementsByClassName("close")[0];
span.onclick = () => {
    var modal = document.getElementById("modal");
    modal.style.display = "none";
}
window.onclick = (event) => {
    var modal = document.getElementById("modal");
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
