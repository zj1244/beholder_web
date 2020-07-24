$("#task_submit").click(function () {


    form = $("form#task_form");
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


            } else if (response.status == "error")
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


            } else if (response.status == "error")
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
    $("#monitor_div").hide();
});

$("button#delete_node").click(function () {

    var ip = $(this).attr('name');

    swal({
            title: "确认删除？",
            text: "将删除节点【" + ip + "】",
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
                url: "/delete_node",
                data: {ip: ip},
                success: function (data) {

                    if (data === "success") {
                        swal("已删除", '', "success");
                        $("button[name='" + ip + "']").parent().parent().parent().remove();


                    } else {
                        swal("删除失败", '', "error");

                    }
                }
            })


        });
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


                    } else {
                        swal("删除失败", '', "error");

                    }
                }
            })


        });
});


$("select[name='job_unit']").click(function () {
    if ($(this).val() == "no") {
        $("input[name='job_time']").attr("disabled", true);

    } else {
        $("input[name='job_time']").attr("disabled", false);
    }


});

