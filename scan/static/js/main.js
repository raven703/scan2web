$(document).ready(function(){
    $("#objects").children("li").each(function(){
        $(this).mouseover(function() {
            $(this).addClass("liteback");
             $("#types").children("li[data-ship='" + $(this).attr('data-ship') + "']").each(function(){
                $(this).addClass("liteback");
            });
        });

        $(this).mouseout(function () {
            $(this).removeClass("liteback");
            $("#types").children("li[data-ship='" + $(this).attr('data-ship') + "']").each(function() {
                $(this).removeClass("liteback");
            });
        });
    });

    $("#types").children("li").each(function(){
        $(this).mouseover(function() {
            $(this).addClass("liteback");
            $("#objects").children("li[data-ship='" + $(this).attr('data-ship') + "']").each(function(){
                $(this).addClass("liteback");
            });

        });
        $(this).mouseout(function () {
            $(this).removeClass("liteback");
            $("#objects").children("li[data-ship='" + $(this).attr('data-ship') + "']").each(function(){
                $(this).removeClass("liteback");
            });
        });
    });


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





