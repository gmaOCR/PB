document.getElementById("edit-img").addEventListener("change", function(event) {
  var output = document.getElementById("image-output");
  output.innerHTML = ""; // Réinitialise l'aperçu de l'image

  var files = event.target.files;
  if (files && files.length > 0) {
    var file = files[0];
    if (file.type.match(/^image\//)) {
      var reader = new FileReader();
      reader.onload = function(e) {
        var img = document.createElement("img");
        img.src = e.target.result;
        img.classList.add("preview-image");
        output.appendChild(img);
      };
      reader.readAsDataURL(file);
    }
  }
});
