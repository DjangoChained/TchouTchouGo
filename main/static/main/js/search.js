function showLoader(text) {
    hideLoader();
    $(".global").append('<div class="loader loader-default is-active" data-half data-blink data-text="' + (text ? text : 'Chargement') + '"></div>');
}

function hideLoader() {
    $(".loader").remove();
}

function createAutoComp(data) {
    $('#startStation, #endStation').autocomplete({
        source: function(request, response) {
            var results = $.ui.autocomplete.filter(data, request.term);
    
            response(results.slice(0, 10));
        },
        minLength: 3,
        
    });
}

$(function() {
    $.getJSON("/train/stations.json", createAutoComp);
    $("#date").datepicker({
        altField: "#date",
        closeText: 'Fermer',
        prevText: 'Précédent',
        nextText: 'Suivant',
        currentText: 'Aujourd\'hui',
        monthNames: ['Janvier', 'Février', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre'],
        monthNamesShort: ['Janv.', 'Févr.', 'Mars', 'Avril', 'Mai', 'Juin', 'Juil.', 'Août', 'Sept.', 'Oct.', 'Nov.', 'Déc.'],
        dayNames: ['Dimanche', 'Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi', 'Samedi'],
        dayNamesShort: ['Dim.', 'Lun.', 'Mar.', 'Mer.', 'Jeu.', 'Ven.', 'Sam.'],
        dayNamesMin: ['D', 'L', 'M', 'M', 'J', 'V', 'S'],
        weekHeader: 'Sem.',
        dateFormat: 'dd/mm/yy'
    });
    $("input[name=passengers]").first().prop('checked', true);
    $("form").submit(function() {
        showLoader("Calcul des trajets...");
    });
});
