function previewImage(input) {
  var preview = document.getElementById("image-preview");
  var file = input.files[0];
  var reader = new FileReader();

  reader.onloadend = function() {
    preview.src = reader.result;

    var desiredWidth = 800; // Largeur souhaitée en pixels
    var scaleFactor = desiredWidth / preview.naturalWidth; // Calcul du facteur d'échelle

    // Réinitialise la transformation d'échelle précédente uniquement si le fichier a été modifié
    if (input.value) {
      preview.style.transform = '';
    }

    // Applique la nouvelle transformation d'échelle
    preview.style.transform = `scale(${scaleFactor})`;

    var dataForm = document.querySelector('.data-form');
    var formElements = dataForm.querySelectorAll('input, textarea, select');
    var maxWidth = 0;
    formElements.forEach(function(element) {
      maxWidth = Math.max(maxWidth, element.scrollWidth);
    });
    dataForm.style.width = maxWidth + 'px';

    var parentWidth = preview.parentNode.clientWidth; // Obtenir la largeur du parent
    preview.style.maxWidth = parentWidth + "px"; // Définir la largeur maximale de l'élément preview
  };

  if (file) {
    reader.readAsDataURL(file);
  } else {
    preview.src = "";
    preview.style.transform = ""; // Réinitialise la transformation de l'image si aucun fichier n'est sélectionné

    var dataForm = document.querySelector('.data-form');
    dataForm.style.width = ""; // Réinitialise la largeur du conteneur si aucun fichier n'est sélectionné
  }
}

window.addEventListener('load', function() {
  var dataForm = document.querySelector('.data-form');
  var formElements = dataForm.querySelectorAll('input, textarea, select');

  function adjustDataFormSize() {
    var maxWidth = 0;
    formElements.forEach(function(element) {
      maxWidth = Math.max(maxWidth, element.scrollWidth);
    });

    dataForm.style.width = maxWidth + 'px';
  }

  adjustDataFormSize();

  window.addEventListener('resize', adjustDataFormSize);
});
