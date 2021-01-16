/*
    This script refreshed the unread notification count in the top menu
    on a regular basis so to keep the user apprised about newly arrived
    notifications without having to reload the page.

    The refresh rate can be changes via the Django setting NOTIFICATIONS_REFRESH_TIME.
    See documentation for details.
*/

$(function () {
    var elem = document.getElementById("dataExport");
    var notificationsListViewUrl = elem.getAttribute("data-notificationsListViewUrl");
    var notificationsRefreshTime = elem.getAttribute("data-notificationsRefreshTime");
    var userNotificationsCountViewUrl = elem.getAttribute(
        "data-userNotificationsCountViewUrl"
    );

    // update the notification unread count in the top menu
    function update_notifications() {
        $.getJSON(userNotificationsCountViewUrl, function (data, status) {
            if (status == 'success') {
                var innerHtml = "";
                var unread_count = data.unread_count;
                if (unread_count > 0) {
                    innerHtml = (
                        `Notifications <span class="badge">${unread_count}</span>`
                    )
                }
                else {
                    innerHtml = '<i class="far fa-bell"></i>'
                }
                $("#menu_item_notifications").html(
                    `<a href="${notificationsListViewUrl}">${innerHtml}</a>`
                );
            }
            else {
                console.error(
                    `Failed to load HTMl to render notifications item. Error: `
                        `${xhr.status}': '${xhr.statusText}`
                );
            }
        });
    }

    var myInterval;

    // activate automatic refreshing every x seconds
    function activate_refreshing() {
        if (notificationsRefreshTime > 0) {
            myInterval = setInterval(
                update_notifications, notificationsRefreshTime * 1000
            );
        }
    }

    // deactivate automatic refreshing
    function deactivate_refreshing() {
        if ((notificationsRefreshTime > 0) && (typeof myInterval !== 'undefined')) {
            clearInterval(myInterval)
        }
    }

    // refreshing only happens on active browser tab
    $(document).on({
        'show': function () {
            activate_refreshing()
        },
        'hide': function () {
            deactivate_refreshing()
        }
    });

    // Initial start of refreshing on script loading
    activate_refreshing()
});
