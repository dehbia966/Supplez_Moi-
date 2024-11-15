document.addEventListener('DOMContentLoaded', function() {
    var deleteLinks = document.querySelectorAll('.delete-link');
    deleteLinks.forEach(function(link) {
        link.addEventListener('click', function(event) {
            event.preventDefault(); // Empêcher le lien de suivre son URL

            var confirmDelete = confirm('Êtes-vous sûr de vouloir supprimer cette demande ?');
            if (confirmDelete) {
                window.location.href = link.getAttribute('href'); // Rediriger vers l'URL de suppression si confirmé
            }
        });
    });
});