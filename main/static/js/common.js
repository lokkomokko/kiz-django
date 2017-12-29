if  ($('#app table').length >= 1) {
    $('#app table').DataTable({
        'language' : {
            'url': '//cdn.datatables.net/plug-ins/1.10.16/i18n/Russian.json'
        },
        "ordering": false

    });
}
