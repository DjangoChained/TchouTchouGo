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
    $('form').submit(function(event) {
	$(".alert").remove();
        labels = data.map(s => s.label.toLowerCase());
        if(!labels.includes($("#startStation").val().trim().toLowerCase())) {
            $('.input-stack').before('<div class="alert alert-danger alert-dismissible fade show" role="alert">Cette station de départ n\'existe pas.<button type="button" class="close" data-dismiss="alert" aria-label="Fermer"><span aria-hidden="true">&times;</span></button></div>');
            event.preventDefault();
        } else if(!labels.includes($("#endStation").val().trim().toLowerCase())) {
            $('.input-stack').before('<div class="alert alert-danger alert-dismissible fade show" role="alert">Cette station d\'arrivée n\'existe pas.<button type="button" class="close" data-dismiss="alert" aria-label="Fermer"><span aria-hidden="true">&times;</span></button></div>');
            event.preventDefault();
        } else {
        	showLoader("Calcul des trajets...");
	}
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
});
