$(function() {
    $("a.travel-modal").click(function() {
        $.get($(this).data('url'), function(data) {
            $("body").prepend('<div class="modal" id="mapModal" role="dialog" tabindex="-1"><div class="modal-dialog" role="document"><div class="modal-content"><div class="modal-header"><h5 class="modal-title">Carte du trajet</h5><button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button></div><div class="modal-body">' + data + '</div><div class="modal-footer"><button type="button" class="btn btn-primary" data-dismiss="modal">Fermer</button></div></div></div></div></div>');
            $("#mapModal").modal('show');
            $("#mapModal").on('hidden.bs.modal', function(e) { $("#mapModal").remove(); });
        });
    });
});
