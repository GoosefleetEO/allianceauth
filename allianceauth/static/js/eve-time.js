$(document).ready(function () {
    'use strict';

    /**
     * check time
     * @param i
     * @returns {string}
     */
    let checkTime = function (i) {
        if (i < 10) {
            i = '0' + i;
        }

        return i;
    };

    /**
     * render a JS clock for Eve Time
     * @param element
     * @param utcOffset
     */
    let renderClock = function (element, utcOffset) {
        let today = new Date();
        let h = today.getUTCHours();
        let m = today.getUTCMinutes();

        h = h + utcOffset;

        if (h > 24) {
            h = h - 24;
        }

        if (h < 0) {
            h = h + 24;
        }

        h = checkTime(h);
        m = checkTime(m);

        element.html(h + ':' + m);

        setTimeout(function () {
            renderClock(element, 0);
        }, 500);
    };

    /**
     * functions that need to be executed on load
     */
    let init = function () {
        renderClock($('.eve-time-wrapper .eve-time-clock'), 0);
    };

    /**
     * start the show
     */
    init();
});
