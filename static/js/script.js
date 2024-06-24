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


