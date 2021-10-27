const API_URL = 'http://127.0.0.1:8000';

$(document).ready(function () {
    $("#loading").hide();
    render_predictions();

    $("#upload").click(function () {
        $("#loading").show();
        var fd = new FormData();
        var files = $('#file')[0].files;
        if (files.length > 0) {
            fd.append('data_file', files[0]);
            $.ajax({
                url: API_URL + '/upload_data',
                type: 'post',
                data: fd,
                contentType: false,
                processData: false,
                success: function (response) {
                    if(response.status == "OK") {
                        $("#loading").hide();
                        render_predictions();
                    }
                },
            });
        } else {
            alert("Please select a file.");
        }
    });

});

function render_predictions() {
    $.ajax({
        url: API_URL + '/get_prediction_files_list',
        success: function (result) {
            $("#predict_list").empty()
            for (let i = 0; i < result.length; i++) {
                var row = '<tr>' +
                    '<td>' + result[i].file_name + '</td>' +
                    '<td>' + result[i].created_on + '</td>' +
                    '<td><button class="btn btn-primary btn-sm" onclick="downloadFile(\'' + result[i].file_name + '\', 0)" type="submit">Download</button></td>' +
                    '</tr>';
                $("#predict_list").append(row);
            }
        }
    });
}

// function downloadFile(filename, source) {
//     let body = {
//         "file_name": filename,
//         "source": source
//     }
//     $.ajax({
//         url: API_URL + '/download_file',
//         type: "post",
//         data: JSON.stringify(body),
//         contentType: 'application/json',
//         success: function (result) {
//             console.log(result);
//             // result.download();
//         }
//     });
// }
