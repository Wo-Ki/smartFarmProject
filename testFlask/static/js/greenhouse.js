$(function () {

    var backgroundIP = "http://192.168.100.3:8989";
    // 公共配置
    Highcharts.setOptions({
        chart: {
            type: 'solidgauge'
        },
        title: null,
        pane: {
            center: ['50%', '70%'],
            size: '100%',
            startAngle: -90,
            endAngle: 90,
            background: {
                backgroundColor: (Highcharts.theme && Highcharts.theme.background2) || '#EEE',
                innerRadius: '60%',
                outerRadius: '100%',
                shape: 'arc'
            }
        },
        tooltip: {
            enabled: false
        },
        yAxis: {
            stops: [
                [0.1, '#55BF3B'], // green
                [0.5, '#DDDF0D'], // yellow
                [0.9, '#DF5353'] // red
            ],
            lineWidth: 0,
            minorTickInterval: null,
            tickPixelInterval: 400,
            tickWidth: 0,
            title: {
                y: -60
            },
            labels: {
                y: 16
            }
        },
        plotOptions: {
            solidgauge: {
                dataLabels: {
                    y: 5,
                    borderWidth: 0,
                    useHTML: true
                }
            }
        }
    });
// 大棚内湿度仪表
    var chartHumIn = Highcharts.chart('container-humIn', {
        yAxis: {
            min: 0,
            max: 100,
            title: {
                text: '大棚内湿度'
            }
        },
        credits: {
            enabled: false
        },
        series: [{
            name: '大棚内湿度',
            data: [80],
            dataLabels: {
                format: '<div style="text-align:center"><span style="font-size:20px;color:' +
                ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y}</span><br/>' +
                '<span style="font-size:12px;color:silver">%</span></div>'
            },
            tooltip: {
                valueSuffix: ' %'
            }
        }]
    });
// 大棚内温度仪表
    var chartTemIn = Highcharts.chart('container-temIn', {
        yAxis: {
            min: 0,
            max: 100,
            title: {
                text: '大棚内温度'
            }
        },
        credits: {
            enabled: false
        },
        series: [{
            name: '大棚内温度',
            data: [1],
            dataLabels: {
                format: '<div style="text-align:center"><span style="font-size:20px;color:' +
                ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y:.1f}</span><br/>' +
                '<span style="font-size:12px;color:silver">℃</span></div>'
            },
            tooltip: {
                valueSuffix: ' ℃'
            }
        }]
    });
    // 大棚外湿度仪表
    var chartTemOut = Highcharts.chart('container-humOut', {
        yAxis: {
            min: 0,
            max: 100,
            title: {
                text: '大棚外湿度'
            }
        },
        credits: {
            enabled: false
        },
        series: [{
            name: '大棚外湿度',
            data: [1],
            dataLabels: {
                format: '<div style="text-align:center"><span style="font-size:20px;color:' +
                ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y:.1f}</span><br/>' +
                '<span style="font-size:12px;color:silver">%</span></div>'
            },
            tooltip: {
                valueSuffix: ' %'
            }
        }]
    });
    // 大棚外温度仪表
    var chartTemOut = Highcharts.chart('container-temOut', {
        yAxis: {
            min: 0,
            max: 100,
            title: {
                text: '大棚外温度'
            }
        },
        credits: {
            enabled: false
        },
        series: [{
            name: '大棚外温度',
            data: [1],
            dataLabels: {
                format: '<div style="text-align:center"><span style="font-size:20px;color:' +
                ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y:.1f}</span><br/>' +
                '<span style="font-size:12px;color:silver">℃</span></div>'
            },
            tooltip: {
                valueSuffix: ' ℃'
            }
        }]
    });

    // 土壤1温度仪表
    var chartTemSoil1 = Highcharts.chart('container-temSoil1', {
        yAxis: {
            min: 0,
            max: 100,
            title: {
                text: '土壤1温度'
            }
        },
        credits: {
            enabled: false
        },
        series: [{
            name: '土壤1温度',
            data: [1],
            dataLabels: {
                format: '<div style="text-align:center"><span style="font-size:20px;color:' +
                ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y:.1f}</span><br/>' +
                '<span style="font-size:12px;color:silver">℃</span></div>'
            },
            tooltip: {
                valueSuffix: ' ℃'
            }
        }]
    });
    // 土壤1湿度仪表
    var chartTHumSoil1 = Highcharts.chart('container-humSoil1', {
        yAxis: {
            min: 0,
            max: 100,
            title: {
                text: '土壤1湿度'
            }
        },
        credits: {
            enabled: false
        },
        series: [{
            name: '土壤1湿度',
            data: [1],
            dataLabels: {
                format: '<div style="text-align:center"><span style="font-size:20px;color:' +
                ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y:.1f}</span><br/>' +
                '<span style="font-size:12px;color:silver">%</span></div>'
            },
            tooltip: {
                valueSuffix: ' %'
            }
        }]
    });
    // 土壤2温度仪表
    var chartTemSoil1 = Highcharts.chart('container-temSoil2', {
        yAxis: {
            min: 0,
            max: 100,
            title: {
                text: '土壤2温度'
            }
        },
        credits: {
            enabled: false
        },
        series: [{
            name: '土壤2温度',
            data: [1],
            dataLabels: {
                format: '<div style="text-align:center"><span style="font-size:20px;color:' +
                ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y:.1f}</span><br/>' +
                '<span style="font-size:12px;color:silver">℃</span></div>'
            },
            tooltip: {
                valueSuffix: ' ℃'
            }
        }]
    });

    // 土壤2湿度仪表
    var chartTHumSoil2 = Highcharts.chart('container-humSoil2', {
        yAxis: {
            min: 0,
            max: 100,
            title: {
                text: '土壤2湿度'
            }
        },
        credits: {
            enabled: false
        },
        series: [{
            name: '土壤2湿度',
            data: [1],
            dataLabels: {
                format: '<div style="text-align:center"><span style="font-size:20px;color:' +
                ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y:.1f}</span><br/>' +
                '<span style="font-size:12px;color:silver">%</span></div>'
            },
            tooltip: {
                valueSuffix: ' %'
            }
        }]
    });

// 定时刷新数据
    setInterval(function () {

        $.ajax({
            type: 'POST',
            url: '/data/greenhouse/all',
            dataType: 'json',
            timeout: 300,
            // context: $('body'),
            success: function (data) {
                managerData(data["contexts"]);
            },
            error: function (xhr, types) {
                console.log('Ajax error!')
            }
        });
        function managerData(data) {
            console.log("data:", data);
            var dataJson = JSON.stringify(data);
            sessionStorage.setItem("greenhouseTemHumData", dataJson);
            var point,
                newVal,
                inc;
            if (chartHumIn) {
                point = chartHumIn.series[0].points[0];
                newVal = parseFloat(data["humIn"]);
                console.log("HumIn newVal:" + String(newVal));
                point.update(newVal);
            }
            if (chartTemIn) {
                point = chartTemIn.series[0].points[0];
                newVal = parseFloat(data["temIn"]);
                console.log("TemOut newVal:" + String(newVal));

                point.update(newVal);
            }
        }

    }, 2000);

    $("#btnOn").click(function () {
        var jsonData = {device_id: "1001", ctrl: "on"};
        $.post(backgroundIP, jsonData, function (data, status) {
            alert("Data: " + data + "\nStatus: " + status);
        });
    });
    $("#btnOff").click(function () {

        var jsonData = {"device_id": "1001", "ctrl": "off"};
        $.post(backgroundIP, jsonData, function (data, status) {
            alert("Data: " + data + "\nStatus: " + status);
        });
    });
    // 温控滑块
    var $box_tem = $('#temSlider');
    var box_tem_pos = $box_tem.offset();
    var box_tem_pos_w = $box_tem.width();
    var box_tem_pos_h = $box_tem.height();
    var $box_tem_parent = $(".con_tem");
    var box_tem_parent_pos = $box_tem_parent.offset();
    var box_tem_parent_pos_w = $box_tem_parent.width();
    var box_tem_parent_pos_h = $box_tem_parent.height();
    $box_tem.css({left: box_tem_parent_pos_w / 2 - box_tem_pos_w / 2});
    $box_tem.draggable({
        containment: 'parent',  // 约束其只能在父级内拖动
        axis: 'x', // 只能在x轴
        opacity: 0.5,  // 拖动时透明度
        drag: function (ev, ui) {
            // console.log(ui);
            // console.log(ev);
            // ev.preventDefault();
            // ev.setDefaults();
            console.log("box_tem_parent_pos_w:" + String($box_tem_parent.width()));
            console.log(ui.position.left);
            var v = parseInt(ui.position.left / $box_tem_parent.width() * 50);
            $("#tem_set_value").text(v + "℃");
        },
        // 当停止滑动滑块时，发送滑块数据，即温度值
        stop: function (ev, ui) {
            var v = parseInt(ui.position.left / $box_tem_parent.width() * 50);
            var jsonData = {"M": "say", "ID": "1001", "C": "temCtrl_ " + String(v), T: (new Date()).getTime()};
            $.post(backgroundIP, jsonData, function (data, status) {
            });
        }

    });
    // 温控自动按钮
    var $autoTemBtn = $("#autoTemBtn");
    $autoTemBtn.click(function () {
        if ($autoTemBtn.is(":checked")) {
            var jsonData = {"M": "say", "ID": "1001", "C": "temCtrl_on", T: (new Date()).getTime()};
            $.post(backgroundIP, jsonData, function (data, status) {
                console.log(jsonData);
            });
        } else {
            var jsonData = {"M": "say", "ID": "1001", "C": "temCtrl_off", T: (new Date()).getTime()};
            $.post(backgroundIP, jsonData, function (data, status) {
                console.log(jsonData);
            });
        }

    });
    // 通风按钮
    var $winCtrlBtn = $("#windCtrlBtn");
    $winCtrlBtn.click(function () {
        if ($winCtrlBtn.is(':checked')) {
            var jsonData = {"M": "say", "ID": "1001", "C": "windCtrl_1", T: (new Date()).getTime()};
            $.post(backgroundIP, jsonData, function (data, status) {
                console.log(jsonData);
            });
            // $("#wind_msg").html("已开始通风");
        }
        else {
            var jsonData = {"M": "say", "ID": "1001", "C": "windCtrl_0", T: (new Date()).getTime()};
            $.post(backgroundIP, jsonData, function (data, status) {
                console.log(jsonData);
            });
            // $("#wind_msg").html("已关闭通风");
        }
    });
    // 开门按钮
    var $doorCtrlBtn = $("#doorCtrlBtn");
    $doorCtrlBtn.click(function () {
        if ($doorCtrlBtn.is(':checked')) {
            var jsonData = {"M": "say", "ID": "1001", "C": "doorCtrl_1", T: (new Date()).getTime()};
            $.post(backgroundIP, jsonData, function (data, status) {
                console.log(jsonData);
            });
            // $("#door_msg").html("已经开门");
        }
        else {
            var jsonData = {"M": "say", "ID": "1001", "C": "doorCtrl_0", T: (new Date()).getTime()};
            $.post(backgroundIP, jsonData, function (data, status) {
                console.log(jsonData);
            });
            // $("#door_msg").html("已关门");
        }
    });
    // 开灯按钮
    var $lightCtrlBtn = $("#lightCtrlBtn");
    $lightCtrlBtn.click(function () {
        if ($lightCtrlBtn.is(':checked')) {
            var jsonData = {"M": "say", "ID": "1001", "C": "lightCtrl_1", T: (new Date()).getTime()};
            $.post(backgroundIP, jsonData, function (data, status) {
                console.log(jsonData);
            });
            // $("#light_msg").html("已经开灯");

        }
        else {
            var jsonData = {"M": "say", "ID": "1001", "C": "lightCtrl_0", T: (new Date()).getTime()};
            $.post(backgroundIP, jsonData, function (data, status) {
                console.log(jsonData);
            });
            // $("#light_msg").html("已关灯");

        }
    });

    // 喷灌1
    var $water1CtrlBtn = $("#water1CtrlBtn");
    $water1CtrlBtn.click(function () {
        if ($water1CtrlBtn.is(':checked')) {
            var jsonData = {"M": "say", "ID": "1001", "C": "water1Ctrl_1", T: (new Date()).getTime()};
            $.post(backgroundIP, jsonData, function (data, status) {
                console.log(jsonData);
            });
            // $("#water1_msg").html("已开始喷灌");
        }
        else {
            var jsonData = {"M": "say", "ID": "1001", "C": "water1Ctrl_0", T: (new Date()).getTime()};
            $.post(backgroundIP, jsonData, function (data, status) {
                console.log(jsonData);
            });
            // $("#water1_msg").html("已关闭喷灌");
        }
    });
    // 喷灌2
    var $water2CtrlBtn = $("#water2CtrlBtn");
    $water2CtrlBtn.click(function () {
        if ($water2CtrlBtn.is(':checked')) {
            var jsonData = {"M": "say", "ID": "1001", "C": "water2Ctrl_1", T: (new Date()).getTime()};
            $.post(backgroundIP, jsonData, function (data, status) {
                console.log(jsonData);
            });
            // $("#water2_msg").html("已开始喷灌");
        }
        else {
            var jsonData = {"M": "say", "ID": "1001", "C": "water2Ctrl_0", T: (new Date()).getTime()};
            $.post(backgroundIP, jsonData, function (data, status) {
                console.log(jsonData);
            });
            // $("#water2_msg").html("已关闭喷灌");
        }
    });


});
