/**
 * Created by wangkai on 2018/1/2.
 */

// Highcharts.setOptions({
//     global: {
//         useUTC: false
//     },
//     credits: {
//         enabled: false
//     }
// });
// function activeLastPointToolip(chart) {
//     var points = chart.series[0].points;
//     chart.tooltip.refresh(points[points.length - 1]);
// }
// // 湿度历史记录
// $('#container_hum_his').highcharts({
//     chart: {
//         type: 'spline',
//         animation: Highcharts.svg, // don't animate in old IE
//         marginRight: 10,
//         rangeSelector: {
//             inputEnabled: $('#container').width() > 480,
//             selected: 1
//         },
//
//         events: {
//             load: function () {
//                 // set up the updating of the chart 2 seconds
//
//                 var series = this.series[0],
//                     chart = this;
//                 setInterval(function () {
//                     // ***
//                     $.ajax({
//                         type: 'GET',
//                         url: '/data/greenhouse/',
//                         dataType: 'json',
//                         timeout: 300,
//                         // context: $('body'),
//                         success: function (data) {
//                             var urlNow = String(window.location.pathname).split("/")[3];
//                             var x = (new Date(data["create_time"])).getTime(),
//                                 y = parseFloat(data["hum" + urlNow]);
//                             console.log("x:", x, ";y:", y);
//
//                             series.addPoint([x, y], true, true);
//                             activeLastPointToolip(chart)
//                         },
//                         error: function (xhr, type) {
//                             console.log('Ajax error!')
//                         }
//
//                     });
//                     // ***
//
//                 }, 2000);
//             }
//         }
//     },
//     title: {
//         text: '湿度实时数据(%)'
//     },
//     xAxis: {
//         type: 'datetime',
//         tickPixelInterval: 150
//     },
//     yAxis: {
//         title: {
//             text: '值'
//         },
//         plotLines: [{
//             value: 0,
//             width: 1,
//             color: '#808080'
//         }]
//     },
//     tooltip: {
//         formatter: function () {
//             return '<b>' + this.series.name + '</b><br/>' +
//                 Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
//                 Highcharts.numberFormat(this.y, 2);
//             return "test"
//         }
//     },
//     legend: {
//         enabled: false
//     },
//     exporting: {
//         enabled: false
//     },
//     series: [{
//         name: '湿度数据',
//         data: (function () {
//             // generate an array of random data
//             var data = [],
//                 time = (new Date()).getTime(),
//                 i;
//             for (i = -19; i <= 0; i += 1) {
//                 data.push({
//                     x: time + i * 1000,
//                     y: Math.random()
//                 });
//             }
//             return data;
//         }())
//     }]
// }, function (c) {
//     activeLastPointToolip(c);
// });
//
// // 温度历史记录
// $('#container_tem_his').highcharts({
//     chart: {
//         type: 'spline',
//         animation: Highcharts.svg, // don't animate in old IE
//         marginRight: 10,
//         events: {
//             load: function () {
//                 // set up the updating of the chart 2 seconds
//                 var series = this.series[0],
//                     chart = this;
//                 setInterval(function () {
//                     // ***
//                     $.ajax({
//                         type: 'GET',
//                         url: '/data/greenhouse/',
//                         dataType: 'json',
//                         timeout: 300,
//                         // context: $('body'),
//                         success: function (data) {
//                             // Supposing this JSON payload was received:
//
//                             // console.log("data:", data);
//                             var urlNow = String(window.location.pathname).split("/")[3];
//
//                             var x = (new Date(data["create_time"])).getTime(),
//                                 y = parseFloat(data["tem" + urlNow]);
//                             // console.log("x:",x,";y:",y);
//
//                             series.addPoint([x, y], true, true);
//                             activeLastPointToolip(chart)
//                         },
//                         error: function (xhr, type) {
//                             console.log('Ajax error!')
//                         }
//
//                     });
//                     // ***
//                 }, 2000);
//             }
//         }
//     },
//     title: {
//         text: '温度实时数据(℃)'
//     },
//     xAxis: {
//         type: 'datetime',
//         tickPixelInterval: 150
//     },
//     yAxis: {
//         title: {
//             text: '值'
//         },
//         plotLines: [{
//             value: 0,
//             width: 1,
//             color: '#808080'
//         }]
//     },
//     tooltip: {
//         formatter: function () {
//             return '<b>' + this.series.name + '</b><br/>' +
//                 Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' +
//                 Highcharts.numberFormat(this.y, 2);
//             return "test"
//         }
//     },
//     legend: {
//         enabled: false
//     },
//     exporting: {
//         enabled: false
//     },
//     series: [{
//         name: '温度数据',
//         data: (function () {
//             // generate an array of random data
//             var data = [],
//                 time = (new Date()).getTime(),
//                 i;
//             for (i = -19; i <= 0; i += 1) {
//                 data.push({
//                     x: time + i * 1000,
//                     y: Math.random()
//                 });
//             }
//             return data;
//         }())
//     }]
// }, function (c) {
//     activeLastPointToolip(c);
//
// });


Highcharts.setOptions({
    global: {
        useUTC: false
    }
});
// Create the chart
$('#container_hum_his').highcharts('StockChart', {
    chart: {
        events: {
            load: function () {
                // set up the updating of the chart each second
                var series = this.series[0];

                setInterval(function () {
                    // *****
                    $.ajax({
                        type: 'GET',
                        url: '/data/greenhouse/',
                        dataType: 'json',
                        timeout: 300,
                        // context: $('body'),
                        success: function (data) {
                            var x = (new Date(data["create_time"])).getTime();
                            var y = parseFloat(data["humIn"]);
                            console.log("new x y:", x, y);
                            series.addPoint([x, y], true, true);
                        },
                        error: function (xhr, type) {
                            console.log('Ajax error!')
                        }
                    });
                    // *****
                }, 1000);
            }
        }
    },
    rangeSelector: {
        buttons: [{
            count: 1,
            type: 'minute',
            text: '1M'
        }, {
            count: 5,
            type: 'minute',
            text: '5M'
        }, {
            type: 'all',
            text: 'All'
        }],
        inputEnabled: false,
        selected: 0
    },
    title: {
        text: '大棚内部湿度历史记录(%)'
    },
    tooltip: {
        split: false
    },
    exporting: {
        enabled: false
    },
    series: [{
        name: '随机数据',
        data: (function () {


            var data = [];
            // ***
            // $.ajax({
            //     type: 'POST',
            //     url: '/data/greenhouse/In',
            //     dataType: 'json',
            //     timeout: 500,
            //     // context: $('body'),
            //     success: function (datas) {
            //         // Supposing this JSON payload was received:
            //
            //         // console.log("data:", data);
            //         // var urlNow = String(window.location.pathname).split("/")[3];
            //         var listDatas = datas["contexts"];
            //
            //         for (var d in listDatas) {
            //             var time = (new Date(listDatas[d][2])).getTime();
            //             var hum = parseFloat(listDatas[d][0]);
            //             data.push([time, hum]);
            //             console.log("d time hum:", d, time, hum);
            //
            //         }
            //
            //
            //     },
            //     error: function (xhr, type) {
            //         console.log('Ajax error! container_hum_his')
            //     }
            //
            // });
            // ***

            // generate an array of random data
            var data = [], time = (new Date()).getTime(), i;
            for (i = -999; i <= 0; i += 1) {
                data.push([
                    time + i * 1000,
                    Math.round(Math.random() * 100)
                ]);
                console.log("time hum:", time + i * 1000, Math.round(Math.random() * 100));
            }
            return data;

        }())
    }]
});

