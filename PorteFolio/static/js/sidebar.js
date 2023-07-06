$(document).ready(function() {
    // Sélectionnez la flèche et la sidebar
    var arrow = $('#arrow');
    var sidebar = $('#sidebar');

    // Événement de survol de la flèche
    arrow.hover(
        function() {
            sidebar.addClass('active'); // Ajoute la classe .active à la sidebar
            arrow.addClass('active'); // Ajoute la classe .active à la flèche
        },
        function() {
            sidebar.removeClass('active'); // Supprime la classe .active de la sidebar
            arrow.removeClass('active'); // Supprime la classe .active de la flèche
        }
    );

    // Événement de survol de la sidebar
    sidebar.hover(
        function() {
            sidebar.addClass('active'); // Ajoute la classe .active à la sidebar
            arrow.addClass('active'); // Ajoute la classe .active à la flèche
        },
        function() {
            sidebar.removeClass('active'); // Supprime la classe .active de la sidebar
            arrow.removeClass('active'); // Supprime la classe .active de la flèche
        }
    );
});
