$(document).ready(function() {
  // Sélectionnez les flèches et les sidebars
  var arrowLeft = $('#arrow_left');
  var sidebarLeft = $('#sidebar_left');
  var arrowRight = $('#arrow_right');
  var sidebarRight = $('#sidebar_right');

  // Fonction pour afficher la sidebar gauche lorsque vous passez la souris sur la flèche
  arrowLeft.on('mouseenter', function() {
    sidebarLeft.addClass('active');
    arrowLeft.addClass('active');
  });

  // Fonction pour cacher la sidebar gauche lorsque vous déplacez la souris hors de la sidebar ou de la flèche
  sidebarLeft.on('mouseleave', function() {
    sidebarLeft.removeClass('active');
    arrowLeft.removeClass('active');
  });

  // Fonction pour afficher la sidebar droite lorsque vous passez la souris sur la flèche
  arrowRight.on('mouseenter', function() {
    sidebarRight.addClass('active');
    arrowRight.addClass('active');
  });

  // Fonction pour cacher la sidebar droite lorsque vous déplacez la souris hors de la sidebar ou de la flèche
  sidebarRight.on('mouseleave', function() {
    sidebarRight.removeClass('active');
    arrowRight.removeClass('active');
  });
});
