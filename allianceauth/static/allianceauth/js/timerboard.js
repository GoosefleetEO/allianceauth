$(document).ready(() => {
    'use strict';
    const inputAbsoluteTime = $('input#id_absolute_time');
    const inputCountdown = $('#id_days_left, #id_hours_left, #id_minutes_left');

    //inputAbsoluteTime.prop('disabled', true);
    inputAbsoluteTime.parent().hide()
    inputAbsoluteTime.parent().prev('label').hide()
    inputCountdown.prop('required', true);

    $('input#id_absolute_checkbox').change(function () {
        if ($(this).prop("checked")) {
            // check box enabled
            inputAbsoluteTime.parent().show()
            inputAbsoluteTime.parent().prev('label').show()
            inputCountdown.parent().hide()
            inputCountdown.parent().prev('label').hide()
            inputAbsoluteTime.prop('required', true);
            inputCountdown.prop('required', false);
        } else {
            // Checkbox is not checked
            inputAbsoluteTime.parent().hide()
            inputAbsoluteTime.parent().prev('label').hide()
            inputCountdown.parent().show()
            inputCountdown.parent().prev('label').show()
            inputAbsoluteTime.prop('required', false);
            inputCountdown.prop('required', true);
        }
    });
});
