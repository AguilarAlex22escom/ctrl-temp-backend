let modoActivo = null;

let toggleMenu = () => {
  const navbarLinks = document.querySelector(".navbar-links");
  navbarLinks.classList.toggle("active");

  var menudes = document.getElementById("menudes");
  if (menudes.style.right === "0px") {
    menudes.style.right = "-400px";
  } else {
    menudes.style.right = "0px";
  }
};

let toggleModo = (modoId, element) => {
  const isActive = element.classList.contains("active");
  element.classList.toggle("active");
  if (modoActivo === null) {
    modoActivo = modoId;
    element.classList.add("active");
    showModal("El modo ha sido activado correctamente.");
  } else if (modoActivo === modoId) {
    modoActivo = null;
    element.classList.remove("active");
    showModal("El modo ha sido desactivado correctamente.");
  } else {
    showModal("Se debe desactivar el modo actual antes de seleccionar otro.");
  }
};

let showModal = (message) => {
  var modal = document.getElementById("modal");
  var modalMessage = document.getElementById("modalMessage");
  modalMessage.textContent = message;
  modal.style.display = "block";
}

var span = document.getElementsByClassName("close")[0];
span.onclick = function () {
  var modal = document.getElementById("modal");
  modal.style.display = "none";
};

window.onclick = function (event) {
  var modal = document.getElementById("modal");
  if (event.target == modal) {
    modal.style.display = "none";
  }
};

let updateChart = (month) => {
  // Simula obtener datos; reemplaza con tus datos reales
  fetch("/statistics")
    .then(response => response.json())
    .then(temperatureData => {
      temperatureChart.data.datasets[0].data = temperatureData
    })
  if (temperatureChart) {
    temperatureChart.destroy();
  }
  temperatureChart = new Chart(ctx, {
    type: "line",
    data: data,
    options: {
      scales: {
        y: {
          beginAtZero: false,
        },
      },
    },
  });
}

document.getElementById("monthSelector").addEventListener("change", (e) => {
  updateChart(e.target.value);
});

updateChart(4); // Inicializa la gráfica con datos de mayo 2024
