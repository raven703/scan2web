$(document).ready(function(){


  $("#alliances").children("li").each(function(){
        $(this).mouseover(function() {
            $(this).addClass("liteback");
            $("#corps").children("li[data-alliance='" + $(this).attr('data-alliance') + "']").each(function(){
                $(this).addClass("liteback");
            });
        });
        $(this).mouseout(function () {
            $(this).removeClass("liteback");
            $("#corps").children("li[data-alliance='" + $(this).attr('data-alliance') + "']").each(function(){
                $(this).removeClass("liteback");
            });
        });
    });

  $("#corps").children("li").each(function(){
        $(this).mouseover(function() {
            $(this).addClass("liteback");
            $("#alliances").children("li[data-alliance='" + $(this).attr('data-alliance') + "']").each(function(){
                $(this).addClass("liteback");
            });
        });
        $(this).mouseout(function () {
            $(this).removeClass("liteback");
            $("#alliances").children("li[data-alliance='" + $(this).attr('data-alliance') + "']").each(function(){
                $(this).removeClass("liteback");
            });
        });
    });




});



