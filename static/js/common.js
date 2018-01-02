if ($('#app table').length >= 1) {
    $('#app table').DataTable({
        'language': {
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
    if ($('#list').val() == false) {
        e.preventDefault()
        e.stopPropagation()
        alert('Выберите код болезни')
    }
})
$(document).ready(function () {
    if($('.add').length >= 1) {
        $('.tree-multiselect').append("<img class='girl2' src='http://orig10.deviantart.net/9f5c/f/2015/192/3/c/girl_and_blade_anime_render_by_schorch2812_d7j5mha_by_harunanami-d90wcmt.png'>")
    }

    if ($('#app').length >= 1) {
        $('.buttons-print').addClass('btn')
    }
})
