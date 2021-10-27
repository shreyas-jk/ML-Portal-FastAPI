const API_URL = 'http://127.0.0.1:8000';

$(document).ready(function () {
    $.ajax({
        url: API_URL + '/get_dataset_list',
        success: function (result) {
            for (let i = 0; i < result.length; i++) {
                var row = '<tr>' +
                    '<td>' + result[i].file_name + '</td>' +
                    '<td>' + result[i].created_on + '</td>' +
                    '<td>' + result[i].last_modified + '</td>' +
                    '<td>' +
                    '<div class="form-check">' +
                    '<input value="' + result[i].file_name + '" name="credit" type="radio" class="form-check-input" />' +
                    '</div>' +
                    '</td>' +
                    '</tr>';
                $('#dataset_list').append(row);
            }
            render_default_dataset();
        }
    });
});

function render_default_dataset() {
    $.ajax({
        url: API_URL + '/get_default_dataset',
        success: function (result) {
            $("#dataset_name").text(result.FileName);
        }
    });
}

function setDefaultDataset() {
    let selected_dataset = $('input[name="credit"]:checked').val();
    let body = {
        "file_name": selected_dataset,
        "created_on": "",
        "last_modified": ""
    }
    $.ajax({
        url: API_URL + '/update_default_dataset',
        type: "post",
        data: JSON.stringify(body),
        contentType: 'application/json',
        success: function(result) {
            render_default_dataset();
            // alert(selected_dataset + ' is set as default.');
        }
    });
}

