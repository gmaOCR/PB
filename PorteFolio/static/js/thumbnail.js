 document.addEventListener('DOMContentLoaded', function() {
    var deleteButton = document.querySelector('.delete-thumbnail-button');
    deleteButton.addEventListener('click', function(event) {
      var confirmDelete = confirm("Voulez-vous vraiment effacer cette miniature ?");
      if (!confirmDelete) {
        event.preventDefault();  // Annule la soumission du formulaire
      }
    });
  });

