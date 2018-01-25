$(document).ready(function() {
    $('.form_device_name').on('shown.bs.modal', function() {
        $('.device_name_input').trigger('focus');
    });

    $('.button_device').on('click', function() {
        var wrapper = $(this).closest('.device_dropdown');
        wrapper.find('.device_dropdown_content').slideToggle();
    });

    $('.button_device_power input').change(function() {
        var device_type = $(this).attr('data-device-switch-type');
        var device_name = $(this).attr('data-device-switch-name');

        if (this.checked) {
            $.post('/remote/power', {
                'type': device_type,
                'name': device_name,
                'power': 'on'
            });
        }
        else {
            $.post('/remote/power', {
                'type': device_type,
                'name': device_name,
                'power': 'off'
            });
        }
    });
});

function getDeviceName(type, brand) {
    brand_modal_id = 'add_device_'+type;
    $('#'+brand_modal_id).modal('hide');

    label_id = 'name_device_label_'+type+'_'+brand;
    document.getElementById(label_id).innerHTML = 'Name your '+brand+' '+type;

    form_modal_id = 'name_device_'+type+'_'+brand;
    $('#'+form_modal_id).modal('show');
}

function removeDevice(device_type, device_brand, device_name) {
    var remove = confirm("Are you sure you want to remove "+device_name+"? ("+device_brand+" "+device_type+")");

    if (remove === true) {
        $.post('/remote/remove', {
            'type': device_type,
            'name': device_name
        });

        window.location.replace('remote');
    }
}