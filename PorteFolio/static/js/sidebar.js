$(document).ready(function() {
  // Sélectionnez les flèches et les sidebars
  var arrowLeft = $('#arrow_left');
  var sidebarLeft = $('#sidebar_left');
  var arrowRight = $('#arrow_right');
  var sidebarRight = $('#sidebar_right');

  // Fonction pour ajouter la classe .active aux sidebars et aux flèches
  function activateSidebar(sidebar, arrow) {
    sidebar.addClass('active'); // Ajoute la classe .active à la sidebar
    arrow.addClass('active'); // Ajoute la classe .active à la flèche
  }

  // Fonction pour supprimer la classe .active des sidebars et des flèches
  function deactivateSidebar(sidebar, arrow) {
    sidebar.removeClass('active'); // Supprime la classe .active de la sidebar
    arrow.removeClass('active'); // Supprime la classe .active de la flèche
  }

  // Gestionnaire d'événements pour la sidebar gauche
  sidebarLeft.hover(
    function() {
      activateSidebar(sidebarLeft, arrowLeft);
    },
    function() {
      deactivateSidebar(sidebarLeft, arrowLeft);
    }
  );

  // Gestionnaire d'événements pour la flèche gauche
  arrowLeft.hover(
    function() {
      activateSidebar(sidebarLeft, arrowLeft);
    },
    function() {
      deactivateSidebar(sidebarLeft, arrowLeft);
    }
  );

  // Gestionnaire d'événements pour la sidebar droite
  sidebarRight.hover(
    function() {
      activateSidebar(sidebarRight, arrowRight);
    },
    function() {
      deactivateSidebar(sidebarRight, arrowRight);
    }
  );

  // Gestionnaire d'événements pour la flèche droite
  arrowRight.hover(
    function() {
      activateSidebar(sidebarRight, arrowRight);
    },
    function() {
      deactivateSidebar(sidebarRight, arrowRight);
    }
  );
});
