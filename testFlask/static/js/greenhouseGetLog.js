/**
 * Created by wangkai on 2018/3/29.
 */

$(function () {
    $.ajax({
        type: 'POST',
        url: '/data/greenhouse/log/all',
        dataType: 'json',
        timeout: 300,
        // context: $('body'),
        success: function (data) {
            // var log = JSON.parse(data);
            var datas = data["contexts"];
            for(var i in datas){
                var trHtml = "<tr><td>"+datas[i]["SID"]+"</td><td>"+datas[i]["TID"]+"</td><td>"+msgChange(datas[i]['msg'])+"</td><td>"+datas[i]["time"]+"</td></tr>";
               $("#tableLog tr:eq(1)").before(trHtml);
            }


        },
        error: function (xhr, type) {
            console.log('Ajax error! greenhouse get Log')
        }
    });
});


setInterval(function () {
    $.ajax({
        type: 'POST',
        url: '/data/greenhouse/log/one',
        dataType: 'json',
        timeout: 300,
        // context: $('body'),
        success: function (data) {
            // var log = JSON.parse(data);
            // manageData(log);
            console.log("log one:",data["contexts"]);
            if(data["contexts"]== "None"){
                return;
            }
            var datas = data["contexts"][0];
            var trHtml = "<tr><td>"+datas["SID"]+"</td><td>"+datas["TID"]+"</td><td>"+msgChange(datas['msg'])+"</td><td>"+datas["time"]+"</td></tr>";
               $("#tableLog tr:eq(1)").before(trHtml);
        },
        error: function (xhr, type) {
            console.log('Ajax error!')
        }
    });
}, 3002);


function manageData(data) {
    var method = "空";
    var msg = data['message'];
    if(msg == "water1_1"){
        method = ""
    }

}

function msgChange(msg) {
    var re = "";
    if(msg == "water1Ctrl_0"){
        re = "关闭1号水阀";
    }
    else if(msg == "water1Ctrl_1"){
        re = "打开1号水阀";
    }

    else if(msg == "water2Ctrl_0"){
        re = "关闭2号水阀";
    }
    else if(msg == "water2Ctrl_1"){
        re = "打开2号水阀";
    }
    else if(msg == "windCtrl_1"){
        re = "打开通风";
    }
    else if(msg == "windCtrl_0"){
        re = "关闭通风";
    }
    else if(msg == "doorCtrl_1"){
        re = "开门";
    }
    else if(msg == "doorCtrl_0"){
        re = "关门";
    }
    else if(msg == "lightCtrl_1"){
        re = "开灯";
    }
    else if(msg == "lightCtrl_0"){
        re = "关灯";
    }
    else if(msg == "temCtrl_off"){
        re = "关闭自动调温";
    }
    else if(msg == "temCtrl_on"){
        re = "打开自动调温";
    }
    else if(!msg.indexOf("temCtrl")){
        re = "自动调温"+msg.split('_')[1]+"℃";
    }
    else{
        re = "error";
    }
    return re;

}