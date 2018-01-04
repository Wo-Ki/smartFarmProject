/**
 * Created by wangkai on 2018/1/4.
 */

$(function () {
   // $(".collapse ul li ").click(function () {
   //     $(this).addClass("active");
   //     // $(".collapse ul li ").not($(this)).removeClass("active");
   //
   // });
   //  $(".collapse ul li .dropdown ul li a").click(function () {
   //     $(this).parent().parent().addClass("active");
   //     $(".collapse ul li ").not($(this)).removeClass("active");
   //
   // })
    $(window).scroll(function () {
        if($(window).scrollTop() <= 200){
            $(".toTop").hide();
        }
        else{
            $(".toTop").show();
        }
    });
    $(".toTop").click(function () {
        $(window).scrollTop(0);
    })
});