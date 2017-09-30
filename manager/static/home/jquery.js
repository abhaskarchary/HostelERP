jQuery(document).on('mouseover','a.hover',function(){
    jQuery('div#back').stop().fadeOut() ;
    jQuery('div#back2').stop().fadeIn() ;
}) ;

jQuery(document).on('mouseout','a.hover',function(){
    jQuery('div#back2').stop().fadeOut() ;
    jQuery('div#back').stop().fadeIn() ;
}) ;