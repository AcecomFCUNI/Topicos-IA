//========================================================================
// Manejo de imágenes de arrastrar y soltar
//========================================================================

var fileDrag = document.getElementById("file-drag");
var fileSelect = document.getElementById("file-upload");

// Agregar oyentes de eventos
fileDrag.addEventListener("dragover", fileDragHover, false);
fileDrag.addEventListener("dragleave", fileDragHover, false);
fileDrag.addEventListener("drop", fileSelectHandler, false);
fileSelect.addEventListener("change", fileSelectHandler, false);

function fileDragHover(e) {
  // prevenir el comportamiento predeterminado
  e.preventDefault();
  e.stopPropagation();

  fileDrag.className = e.type === "dragover" ? "upload-box dragover" : "upload-box";
}

function fileSelectHandler(e) {
  // manejar la selección de archivos
  var files = e.target.files || e.dataTransfer.files;
  fileDragHover(e);
  for (var i = 0, f; (f = files[i]); i++) {
    previewFile(f);
  }
}

//========================================================================
// Elementos de la página web para funciones a utilizar
//========================================================================

var imagePreview = document.getElementById("image-preview");
var imageDisplay = document.getElementById("image-display");
var uploadCaption = document.getElementById("upload-caption");
var predResult = document.getElementById("pred-result");
var loader = document.getElementById("loader");

//========================================================================
// Eventos de los botones principales
//========================================================================

function submitImage() {
  // acción para el botón enviar
  console.log("enviar");

  if (!imageDisplay.src || !imageDisplay.src.startsWith("data")) {
    window.alert("Por favor seleccione una imagen antes de enviar.");
    return;
  }

  loader.classList.remove("hidden");
  imageDisplay.classList.add("loading");

  // llamamos a la función de predicción en el backend
  predictImage(imageDisplay.src);
}

function clearImage() {
  // reseteamos los archivos seleccionados
  fileSelect.value = "";

  // Eliminar las fuentes de la imagen y la ocultamos
  imagePreview.src = "";
  imageDisplay.src = "";
  predResult.innerHTML = "";

  hide(imagePreview);
  hide(imageDisplay);
  hide(loader);
  hide(predResult);
  show(uploadCaption);

  imageDisplay.classList.remove("loading");
}

function previewFile(file) {
  // un preview de la imagen
  console.log(file.name);
  var fileName = encodeURI(file.name);

  var reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onloadend = () => {
    imagePreview.src = URL.createObjectURL(file);

    show(imagePreview);
    hide(uploadCaption);

    // reseteando
    predResult.innerHTML = "";
    imageDisplay.classList.remove("loading");

    displayImage(reader.result, "image-display");
  };
}

//========================================================================
// Funciones de ayuda
//========================================================================

function predictImage(image) {
  fetch("/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(image)
  })
    .then(resp => {
      if (resp.ok)
        resp.json().then(data => {
          displayResult(data);
        });
    })
    .catch(err => {
      console.log("Ocurrió un error", err.message);
      window.alert("Oops! Ocurre algún error.");
    });
}

function displayImage(image, id) {
  // mostrar la imagen con el elemento id <img> dado
  let display = document.getElementById(id);
  display.src = image;
  show(display);
}

function displayResult(data) {
  // Mostramos el resultado
  // imageDisplay.classList.remove("loading");
  hide(loader);
  predResult.innerHTML = data.result;
  show(predResult);
}

function hide(el) {
  // ocultamos un elemento
  el.classList.add("hidden");
}

function show(el) {
  // Mostramos un elemento
  el.classList.remove("hidden");
}