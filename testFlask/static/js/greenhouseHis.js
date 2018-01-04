/**
 * Created by wangkai on 2018/1/2.
 */
// alert(String(window.location.pathname).split("/")[3]);
Highcharts.setOptions({
    global: {
        useUTC: false
    },
    credits: {
        enabled: false
    }
});
function activeLastPointToolip(chart) {
    var points = chart.series[0].points;
    chart.tooltip.refresh(points[points.length - 1]);
}
// 湿度历史记录
$('#container_hum_his').highcharts({
    chart: {
        type: 'spline',
        animation: Highcharts.svg, // don't animate in old IE
        marginRight: 10,
        events: {
            load: function () {
                // set up the updating of the chart 2 seconds

                var series = this.series[0],
                    chart = this;
                setInterval(function () {
                    // ***
                    $.ajax({
                        type: 'GET',
                        url: '/data/greenhouse/',
                        dataType: 'json',
                        timeout: 300,
                        // context: $('body'),
                        success: function (data) {
                            var urlNow = String(window.location.pathname).split("/")[3];
                            var x = (new Date(data["create_time"])).getTime(),
                                y = parseFloat(data["hum" + urlNow]);
                            console.log("x:", x, ";y:", y);

                            series.addPoint([x, y], true, true);
                            activeLastPointToolip(chart)
                        },
                        error: function (xhr, type) {
                            console.log('Ajax error!')
                        }

                    });
                    // ***

                }, 2000);
            }
        }
    },
    title: {
        text: '湿度实时数据(%)'
    },
    xAxis: {
        type: 'datetime',
        tickPixelInterval: 150
    },
    yAxis: {
        title: {
            text: '值'
        },
        plotLines: [{
            value: 0,
            width: 1,
            color: '#808080'
        }]
    },
    tooltip: {
        formatter: function () {
            return '<b>' + this.series.name + '</b><br/>' +
                Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
                Highcharts.numberFormat(this.y, 2);
            return "test"
        }
    },
    legend: {
        enabled: false
    },
    exporting: {
        enabled: false
    },
    series: [{
        name: '湿度数据',
        data: (function () {
            // generate an array of random data
            var data = [],
                time = (new Date()).getTime(),
                i;
            for (i = -19; i <= 0; i += 1) {
                data.push({
                    x: time + i * 1000,
                    y: Math.random()
                });
            }
            return data;
        }())
    }]
}, function (c) {
    activeLastPointToolip(c);
});
//
// function managerData() {
//
//     var renturnData = {};
//     // ***
//     $.ajax({
//         type: 'GET',
//         url: '/data/greenhouse/',
//         dataType: 'json',
//         timeout: 300,
//         // context: $('body'),
//         success: function (data) {
//             // Supposing this JSON payload was received:
//             //   {"project": {"id": 42, "html": "<div>..." }}
//             // append the HTML to context object.
//             // this.append(data.project.html)
//
//             console.log("data:", data);
//             renturnData = data;
//         },
//         error: function (xhr, type) {
//             // alert('Ajax error!')
//             console.log('Ajax error!')
//         }
//
//     });
//     // ***
//     return renturnData;
// }

// 温度历史记录
$('#container_tem_his').highcharts({
    chart: {
        type: 'spline',
        animation: Highcharts.svg, // don't animate in old IE
        marginRight: 10,
        events: {
            load: function () {
                // set up the updating of the chart 2 seconds
                var series = this.series[0],
                    chart = this;
                setInterval(function () {
                    // ***
                    $.ajax({
                        type: 'GET',
                        url: '/data/greenhouse/',
                        dataType: 'json',
                        timeout: 300,
                        // context: $('body'),
                        success: function (data) {
                            // Supposing this JSON payload was received:

                            // console.log("data:", data);
                            var urlNow = String(window.location.pathname).split("/")[3];

                            var x = (new Date(data["create_time"])).getTime(),
                                y = parseFloat(data["hum"+urlNow]);
                            // console.log("x:",x,";y:",y);

                            series.addPoint([x, y], true, true);
                            activeLastPointToolip(chart)
                        },
                        error: function (xhr, type) {
                            console.log('Ajax error!')
                        }

                    });
                    // ***
                }, 2000);
            }
        }
    },
    title: {
        text: '温度实时数据(℃)'
    },
    xAxis: {
        type: 'datetime',
        tickPixelInterval: 150
    },
    yAxis: {
        title: {
            text: '值'
        },
        plotLines: [{
            value: 0,
            width: 1,
            color: '#808080'
        }]
    },
    tooltip: {
        formatter: function () {
            return '<b>' + this.series.name + '</b><br/>' +
                Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
                Highcharts.numberFormat(this.y, 2);
            return "test"
        }
    },
    legend: {
        enabled: false
    },
    exporting: {
        enabled: false
    },
    series: [{
        name: '温度数据',
        data: (function () {
            // generate an array of random data
            var data = [],
                time = (new Date()).getTime(),
                i;
            for (i = -19; i <= 0; i += 1) {
                data.push({
                    x: time + i * 1000,
                    y: Math.random()
                });
            }
            return data;
        }())
    }]
}, function (c) {
    activeLastPointToolip(c);

});