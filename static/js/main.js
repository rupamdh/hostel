$(document).ready(function () {
    $('.menu > li').click(function (e) { 
        e.preventDefault();
        $(this).find('ul').slideToggle();
        $(this).toggleClass('show');  // Toggle active class for the clicked menu item
        $(this).siblings().find('ul').slideUp(); // Remove active class from other menu items
        $(this).siblings().removeClass('show'); // Close any open submenus of other menu items
    });

});