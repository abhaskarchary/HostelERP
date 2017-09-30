/*jslint browser: true*/
/*global $, jQuery, alert*/

$('#btn1').on('mouseenter mouseleave', function (e) {
    var image = e.type === 'mouseenter' ? 'emp.jpg' : 'stu.jpeg';
    $(this).parent().parent().css('background-image', 'url(' + image + ')');
});