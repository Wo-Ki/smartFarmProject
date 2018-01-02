$(function () {
    // 公共配置
    Highcharts.setOptions({
        chart: {
            type: 'solidgauge'
        },
        title: null,
        pane: {
            center: ['50%', '85%'],
            size: '140%',
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
                y: -70
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
// 湿度仪表
    var chart1 = Highcharts.chart('container-hum', {
        yAxis: {
            min: 0,
            max: 100,
            title: {
                text: '湿度'
            }
        },
        credits: {
            enabled: false
        },
        series: [{
            name: '湿度',
            data: [80],
            dataLabels: {
                format: '<div style="text-align:center"><span style="font-size:25px;color:' +
                ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y}</span><br/>' +
                '<span style="font-size:12px;color:silver">%</span></div>'
            },
            tooltip: {
                valueSuffix: ' %'
            }
        }]
    });
// 温度仪表
    var chart2 = Highcharts.chart('container-tem', {
        yAxis: {
            min: 0,
            max: 100,
            title: {
                text: '温度'
            }
        },
        credits: {
            enabled: false
        },
        series: [{
            name: '温度',
            data: [1],
            dataLabels: {
                format: '<div style="text-align:center"><span style="font-size:25px;color:' +
                ((Highcharts.theme && Highcharts.theme.contrastTextColor) || 'black') + '">{y:.1f}</span><br/>' +
                '<span style="font-size:12px;color:silver">℃</span></div>'
            },
            tooltip: {
                valueSuffix: ' ℃'
            }
        }]
    });
// 定时刷新数据
    setInterval(function () {

        $.ajax({
            type: 'GET',
            url: '/data/1001/',
            // data to be added to query string:
            // data: {name: 'Zepto.js'},
            // type of data we are expecting in return:
            dataType: 'json',
            timeout: 300,
            // context: $('body'),
            success: function (data) {
                // Supposing this JSON payload was received:
                //   {"project": {"id": 42, "html": "<div>..." }}
                // append the HTML to context object.
                // this.append(data.project.html)

                // console.log(data);
                managerData(data);
            },
            error: function (xhr, type) {
                // alert('Ajax error!')
                console.log('Ajax error!')
            }
        });
        function managerData(data) {
            var point,
                newVal,
                inc;
            if (chart1) {
                point = chart1.series[0].points[0];
                // inc = Math.round((Math.random() - 0.5) * 100);
                // inc = data["Hum"];
                // newVal = point.y + inc;
                // if (newVal < 0 || newVal > 200) {
                //     newVal = point.y - inc;
                // }
                newVal = data["Hum"];
                console.log("Hum newVal:" + String(newVal));
                point.update(newVal);
            }
            if (chart2) {
                point = chart2.series[0].points[0];
                // inc = Math.random() - 0.5;
                inc = data["Tem"];
                // newVal = point.y + inc;
                // if (newVal < 0 || newVal > 5) {
                //     newVal = point.y - inc;
                // }
                console.log("Temm newVal:" + String(newVal));
                newVal = data["Tem"];
                point.update(newVal);
            }
        }

    }, 2000);

    $("#btnOn").click(function () {
        // $.get("http://192.168.100.3:8989/1001/4/on", function (data, status) {
        //     alert("Data: " + data + "\nStatus: " + status);
        // });
        var jsonData = {device_id: "1001", ctrl: "on"};
        $.post("http://192.168.100.3:8989", jsonData, function (data, status) {
            alert("Data: " + data + "\nStatus: " + status);
        });
    });
    $("#btnOff").click(function () {
        // $.get("http://192.168.100.3:8989/1001/4/off", function (data, status) {
        //     alert("Data: " + data + "\nStatus: " + status);
        // });
        var jsonData = {"device_id": "1001", "ctrl": "off"};
        $.post("http://192.168.100.3:8989", jsonData, function (data, status) {
            alert("Data: " + data + "\nStatus: " + status);
        });
    });
   // 温控滑块
    var $box_tem = $('.box_tem');
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
            console.log("box_tem_parent_pos_w:"+String($box_tem_parent.width()));
            console.log(ui.position.left);
            var v = parseInt(ui.position.left / $box_tem_parent.width() * 50);
            $("#tem_set_value").text(v);
        }
    });
    // 通风按钮
    $cb2 = $("#cb2");
    $cb2.click(function () {
        if ($cb2.is(':checked')) {
            $("#wind_msg").html("已经开始通风");
        }
        else {
            $("#wind_msg").html("已关闭通风");
        }
    });


});
