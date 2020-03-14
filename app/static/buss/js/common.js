$("#task_submit").click(function () {


    form = $("form#addtask_form");
    messenger = Messenger();

    $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: form.serialize(),
        success: function (data) {
            var response = JSON.parse(data);
            if (response.status == "success") {
                messenger.post({
                    message: response.content,
                    type: "success"
                });
                setTimeout(" window.location.href = '" + response.redirect + "'", 3000);


            }
            else if (response.status == "error")
                messenger.post({
                    message: response.content,
                    type: "error"
                })
        }
    });
    return false;
})

$("#setting_submit").click(function () {


    form = $("form#setting_form");
    messenger = Messenger();

    $.ajax({
        type: form.attr('method'),
        url: form.attr('action'),
        data: form.serialize(),
        success: function (data) {
            var response = JSON.parse(data);
            if (response.status == "success") {
                messenger.post({
                    message: response.content,
                    type: "success"
                });
                setTimeout(" window.location.href = '" + response.redirect + "'", 3000);


            }
            else if (response.status == "error")
                messenger.post({
                    message: response.content,
                    type: "error"
                })
        }
    });
    return false;
})


$(document).ready(function () {
    $("#diff_ports").hide();
    $('#diff_ips').hide();
});

$("button#delete_task").click(function () {

    var task_name = $(this).attr('name');

    swal({
            title: "确认删除？",
            text: "所有【" + task_name + "】的记录将被删除，请谨慎操作",
            type: "warning",
            showCancelButton: true,
            confirmButtonColor: "#DD6B55",
            confirmButtonText: "确定",
            cancelButtonText: "取消",
            closeOnConfirm: false
        },



        function () {


        $.ajax({
        type: "POST",
        url: "/delete_task",
        data: {task_name: task_name},
        success: function (data) {

            if (data === "success") {
                swal("已删除", '', "success");
                    $("button[name='" + task_name + "']").parent().parent().parent().remove();


            }
            else {
                swal("删除失败", '', "error");

            }
        }
    })




            // $.post('/delete_task', {task_name: task_name}, function (e) {
            //     if (e == 'success') {
            //         swal("已删除", '', "success");
            //         $("button[name='" + task_name + "']").parent().parent().parent().remove();
            //     }
            //     else {
            //         swal("删除失败", '', "error");
            //     }
            // })

        });
});


$("select[name='job_unit']").click(function () {
    if ($(this).val() == "no") {
        $("input[name='job_time']").attr("disabled", true);

    }
    else {
        $("input[name='job_time']").attr("disabled", false);
    }


});


$("a[name='history_scan']").on("click", function () {
    var task_id = $(this).attr('id');
    var ports_dataset = new Array();
    var ips_dataset = new Array();
    var ports_table = $('#ports_table').DataTable();
    var ips_table = $('#ips_table').DataTable();

    // $('#ips_row').empty();
    // $('#ports_row').empty()
// $('#ports_table').DataTable().clear();
    $.getJSON('/diff_result?task_id=' + task_id, function (data) {


        if (JSON.stringify(data) == '{}') {
            console.log("data is null!");
            $("#diff_ips").hide();
            $("#diff_ports").hide();
        } else {

            if (data.hasOwnProperty("add_ports")) {
                if ($("#diff_ports").is(':hidden')) {
                    $("#diff_ports").show();
                }
                $("#add_ports_title").text(data['title'] + "日与上次对比结果")
                ports_table.destroy();
                $('#ports_table').empty();
                $.each(data['add_ports'], function (i, info) {
                    ports_dataset.push([info['ip'], info['service'], info['version_info']])
                });

            }
            else {
                $("#diff_ports").hide();
            }

            if (data.hasOwnProperty("add_ips")) {
                if ($("#diff_ips").is(':hidden')) {
                    $("#diff_ips").show();
                }
                $("#add_ips_title").text(data['title'] + "日与上次对比结果")
                ips_table.destroy();
                $('#ips_table').empty();
                $.each(data['add_ips'], function (i, info) {
                    // $('#ips_row').append("<tr><td>" + info + "</td></tr>")
                    ips_dataset.push([info])
                });
            }
            else {
                $("#diff_ips").hide();

            }
            // $("#ports_table").DataTable({"destroy": true});
            // $('#ports_table').DataTable();
            ports_table = $('#ports_table').DataTable({
                columns: [
                    {title: "新增端口"},
                    {title: "服务"},
                    {title: "软件信息"}
                ],
                retrieve: true,
                data: ports_dataset
            });

            ports_table = $('#ips_table').DataTable({
                columns: [
                    {title: "新增IP"}
                ],
                retrieve: true,
                data: ips_dataset
            });

            // $('#ips_table').DataTable();
        }

    })
});
