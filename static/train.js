const API_URL = 'http://127.0.0.1:8000';

$(document).ready(function () {
    $.ajax({
        url: API_URL + '/get_pipeline_status',
        success: function (result) {
            console.log(result)
            if(result.ActiveCount == 1) {
                $("#div_running").show();
                $("#div_idle").hide();
            }
            else {
                $("#div_idle").show();
                $("#div_running").hide();
            }
        }
    });

    $.ajax({
        url: API_URL + '/get_default_dataset',
        success: function (result) {
            $("#dataset_name").text(result.FileName);
        }
    });

    $.ajax({
        url: API_URL + '/get_pipeline_details',
        success: function (result) {
            for (let i = 0; i < result.length; i++) {
                var row = '<tr>' +
                    '<td>' + result[i].PipeLineName + '</td>' +
                    '<td>' + result[i].LastRunOn + '</td>' +
                    '<td>' +
                    '<div class="form-check">' +
                        '<button class="btn btn-success btn-sm" onclick="startTraining()" type="submit">Train</button>' +
                    '</div>' +
                    '</td>' +
                    '</tr>';
                $('#train_list').append(row);
            }
        }
    });

});

function startTraining() {
    $("#div_running").show();
    $("#div_idle").hide();
    $.ajax({
        url: API_URL + '/train_pipeline',
        success: function (result) {     
                 
        }
    });
}