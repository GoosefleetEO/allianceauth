/*
    Javascript for the base template
*/

$(function() {
    var elem = document.getElementById("dataExport");
    var notificationsRenderUrl = elem.getAttribute("data-notificationsRenderUrl");
    
    // render the notifications item in the top menu
    function render_notifications(){
        $("#menu_item_notifications").load(
            notificationsRenderUrl, 
            function(responseTxt, statusTxt, xhr){
                if(statusTxt == "error")
                    console.log(
                        "Failed to load HTMl to render notifications item. Error: " 
                        + xhr.status 
                        + ": " 
                        + xhr.statusText
                    );
        });
    }
    render_notifications()
    
    // re-render notifications every x seconds
    setInterval(render_notifications, 5000);
});
