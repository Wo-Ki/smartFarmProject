/**
 * Created by wangkai on 2018/1/8.
 */


$(function () {
    $.ajax({
        type: 'POST',
        url: '/data/greenhouse/status',
        dataType: 'json',
        timeout: 300,
        // context: $('body'),
        success: function (data) {

            var deviceStatus = parseInt(data["contexts"][0]);
            if (deviceStatus == 0) {
                $("#deviceStatus").html("离线");
            } else {
                $("#deviceStatus").html("在线");
            }
            var sensorStatusLists = JSON.parse(data["contexts"][1]);
            for (var i in sensorStatusLists) {
                var li = sensorStatusLists[i].split(":");
                var key = li[0];
                var value = li[1];
                if (!key.indexOf("light")) {
                    if (value == "1") {
                        $("#lightCtrlBtn").attr('checked', true);
                        $("#light_msg").html("已开灯");
                    } else {
                        $("#lightCtrlBtn").attr('checked', false);
                        $("#light_msg").html("已关灯");
                    }
                } else if (!key.indexOf("door")) {
                    if (value == "1") {
                        $("#doorCtrlBtn").attr('checked', true);
                        $("#door_msg").html("已经开门");
                    } else {
                        $("#doorCtrlBtn").attr('checked', false);
                        $("#door_msg").html("已关门");
                    }
                } else if (!key.indexOf("water1")) {
                    if (value == "1") {
                        $("#water1CtrlBtn").attr('checked', true);
                        $("#water1_msg").html("已开始浇水");
                    } else {
                        $("#water1CtrlBtn").attr('checked', false);
                        $("#water1_msg").html("已停止浇水");
                    }
                } else if (!key.indexOf("water2")) {
                    if (value == "1") {
                        $("#water2CtrlBtn").attr('checked', true);
                        $("#water2_msg").html("已开始浇水");
                    } else {
                        $("#water2CtrlBtn").attr('checked', false);
                        $("#water2_msg").html("已停止浇水");
                    }
                } else if (!key.indexOf("wind")) {
                    if (value == "1") {
                        $("#windCtrlBtn").attr('checked', true);
                        $("#wind_msg").html("已开始通风");
                    } else {
                        $("#windCtrlBtn").attr('checked', false);
                        $("#wind_msg").html("已停止通风");
                    }
                } else if (!key.indexOf("tem")) {
                    if (value == "off") {
                        $("#preTemValue").html("无");
                        $("#temSlider").draggable("option", "disabled", true );
                        $("#temSlider").css({background:"gray"});
                        $("#autoTemBtn").attr('checked', false);
                    }else if(value == "on"){
                        $("#preTemValue").html("请调温");
                        $("#temSlider").draggable("option", "disabled", false );
                        $("#temSlider").css({background:"green"});
                        $("#autoTemBtn").attr('checked', true);
                    }
                    else {
                        $("#preTemValue").html(value + "℃");
                        $("#temSlider").draggable("option", "disabled", false );
                        $("#temSlider").css({background:"green"});
                        $("#autoTemBtn").attr('checked', true);
                    }
                }

            }
            console.log("sensorStatusLists:", sensorStatusLists);
        },
        error: function (xhr, type) {
            console.log('Ajax error!')
        }
    });
})


setInterval(function () {
    $.ajax({
        type: 'POST',
        url: '/data/greenhouse/status',
        dataType: 'json',
        timeout: 300,
        // context: $('body'),
        success: function (data) {

            var deviceStatus = parseInt(data["contexts"][0]);
            if (deviceStatus == 0) {
                $("#deviceStatus").html("离线");
            } else {
                $("#deviceStatus").html("在线");
            }
            var sensorStatusLists = JSON.parse(data["contexts"][1]);
            for (var i in sensorStatusLists) {
                var li = sensorStatusLists[i].split(":");
                var key = li[0];
                var value = li[1];
                if (!key.indexOf("light")) {
                    if (value == "1") {
                        // $("#lightCtrlBtn").attr('checked', true);
                        $("#light_msg").html("已开灯");
                    } else {
                        // $("#lightCtrlBtn").attr('checked', false);
                        $("#light_msg").html("已关灯");
                    }
                } else if (!key.indexOf("door")) {
                    if (value == "1") {
                        // $("#doorCtrlBtn").attr('checked', true);
                        $("#door_msg").html("已经开门");
                    } else {
                        // $("#doorCtrlBtn").attr('checked', false);
                        $("#door_msg").html("已关门");
                    }
                } else if (!key.indexOf("water1")) {
                    if (value == "1") {
                        // $("#water1CtrlBtn").attr('checked', true);
                        $("#water1_msg").html("已开始浇水");
                    } else {
                        // $("#water1CtrlBtn").attr('checked', false);
                        $("#water1_msg").html("已停止浇水");
                    }
                } else if (!key.indexOf("water2")) {
                    if (value == "1") {
                        // $("#water2CtrlBtn").attr('checked', true);
                        $("#water2_msg").html("已开始浇水");
                    } else {
                        // $("#water2CtrlBtn").attr('checked', false);
                        $("#water2_msg").html("已停止浇水");
                    }
                } else if (!key.indexOf("wind")) {
                    if (value == "1") {
                        // $("#windCtrlBtn").attr('checked', true);
                        $("#wind_msg").html("已开始通风");
                    } else {
                        // $("#windCtrlBtn").attr('checked', false);
                        $("#wind_msg").html("已停止通风");
                    }
                } else if (!key.indexOf("tem")) {
                   if (value == "off") {
                        $("#preTemValue").html("无");
                        $("#temSlider").draggable("option", "disabled", true );
                        $("#temSlider").css({background:"gray"});
                    }else if(value == "on"){
                        $("#preTemValue").html("请调温");
                        $("#temSlider").draggable("option", "disabled", false );
                        $("#temSlider").css({background:"green"});
                    }
                    else {
                        $("#preTemValue").html(value + "℃");
                        $("#temSlider").draggable("option", "disabled", false );
                        $("#temSlider").css({background:"green"});
                    }
                }

                // $SendorID = $("#"+String(sensorStatusLists[i][0]));
                // sendorValue = sensorStatusLists[i][1];
                // if(sendorValue == "0"){
                //     $SendorID.html("已经关闭");
                // }else if(sendorValue == "1"){
                //     $SendorID.html("已经打开")
                // }else{
                //     alert("greenhouse Get Status Error!");
                // }
            }
            console.log("sensorStatusLists:", sensorStatusLists);
        },
        error: function (xhr, type) {
            console.log('Ajax error!')
        }
    });
}, 3000);

