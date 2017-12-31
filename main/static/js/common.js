if  ($('#app table').length >= 1) {
    $('#app table').DataTable({
        'language' : {
            'url': '//cdn.datatables.net/plug-ins/1.10.16/i18n/Russian.json'
        },
        "ordering": false,
        dom: 'Blfrtip',
'buttons': [{
    extend: 'print',
    text: 'Распечатать',
    exportOptions: {
        stripHtml: false
    }
}, {
    extend: 'pdf',
    text: 'Save PDF',
    exportOptions: {
        stripNewlines: false
    }
}
],
    });
}
            $("#list").treeMultiselect({
                searchable: true,
                maxSelections: 1,
                startCollapsed: true
            });
            $('.search').attr('placeholder', 'Поиск')

$('#create').click(function (e) {
    if($('#list').val() == false) {
        e.preventDefault()
        e.stopPropagation()
        alert('Выберите код болезни')
    }
})
// $(document).ready(function () {
//     $('.buttons-print span').text('Распечатать')
// })
