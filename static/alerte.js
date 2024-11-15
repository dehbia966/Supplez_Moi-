function verifierOptionCours(code){
    let url = 'http://127.0.0.1:8000/make_query/'+code;
    console.log(url);
    fetch(url, {
        method: 'GET', // ou 'GET' selon votre configuration
        headers: {
            'Content-Type': 'application/json',
        },
        //body: JSON.stringify({ codeCours: code }), // Envoyer la valeur de l'option
    })
    .then(response => response.json())
    .then(data => {
        // Traiter la réponse de la vue Django
        if (data.error) {
            // Afficher un message d'erreur si nécessaire
            alert(data.message);
        } else {
            if (data.option =='Oui'){
                alert('le cours ne sera organisé si et seulement si au moins 3 étudiant ( à vérifier avec le vice-Doyen) sont inscrits au cours');
            }
           
            
        }
    })
    .catch(error => {
        // Gérer les erreurs
        console.error('Error:', error);
    });
}

const selectElement = document.getElementById("id_cours");

selectElement.addEventListener("change", () => {   
    const optionSelectionnee = selectElement.options[selectElement.selectedIndex];   // Affiche le texte de l'option sélectionnée  
    console.log(optionSelectionnee.textContent);   // Affiche la valeur de l'option sélectionnée  
    console.log(optionSelectionnee.value); 
    verifierOptionCours(optionSelectionnee.value)

});