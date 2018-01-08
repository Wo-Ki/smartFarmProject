$(function () {
    var mySwiper = new Swiper('.swiper-container', {
        initialSlide: 2,
        speed: 2000,
        direction: 'horizontal',
        loop: true,
        autoplay: {
            delay: 2000,
        },
        // autoplay: true,//可选选项，自动滑动
        grabCursor: true, //鼠标覆盖Swiper时指针会变成手掌形状
        width: window.innerWidth, //全屏
        height: window.innerHeight,
        roundLengths: true, //防止某些分辨率的屏幕上文字或边界(border)模糊。

        preventClicks : false,// 当swiper在触摸时阻止默认事件（preventDefault），用于防止触摸时触发链接跳转
        preventLinksPropagation : false, // 阻止click冒泡。拖动Swiper时阻止click事件。
        // 如果需要分页器
        pagination: {
            el: '.swiper-pagination'
        },

        // 如果需要前进后退按钮
        navigation: {
            nextEl: '.swiper-button-next',
            prevEl: '.swiper-button-prev'
        },

        // 如果需要滚动条
        // scrollbar: {
        //     el: '.swiper-scrollbar',
        // },
    });
    // 注册事件
    mySwiper.on('slideChange', function () {

    });
});