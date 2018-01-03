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
                stripHtml: true
            }
        }, {
            extend: 'pdf',
            text: 'Save PDF',
            exportOptions: {
                stripNewlines: true
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

var regex = /^(0?[1-9]|[12][0-9]|3[01])[\/\-\.](0?[1-9]|1[012])[\/\-\.](\d{4})$/

$('#create').click(function (e) {
    if ($('#list').val() == false) {
        e.preventDefault()
        e.stopPropagation()
        alert('Выберите код болезни')
    }
    else if (regex.test($('#id_date_1').val()) == false || regex.test($('#id_date_2').val()) == false) {
        e.preventDefault()
        e.stopPropagation()
        alert('Введите корректную дату')
    }
})
$(document).ready(function () {
    if ($('.main_page').length >= 1) {
        $('.tree-multiselect').append("<img class='girl2' src='/static/img/girl2.png'>")
    }
    if ($('.update_page').length >= 1) {
        $('.tree-multiselect').append("<img class='girl3' src='/static/img/girl3.png'>")
    }

    if ($('#app').length >= 1) {
        $('.buttons-print').addClass('btn')
    }
    $('.link--del').click(function (e) {
        if ( !confirm('Вы действительно хотите удалить запись ?')) {
            e.preventDefault()
            e.stopPropagation()
        }

    })
})
