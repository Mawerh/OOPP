$(document).ready(function() {
    $('.form_device_name').on('shown.bs.modal', function () {
        $('.device_name_input').trigger('focus');
    });

    $('.button_device').on('click', function() {
        var wrapper = $(this).closest('.device_dropdown');
        wrapper.find('.device_dropdown_content').slideToggle();
    });

    $('.button_device_power input').change(function() {
        var device = $(this).attr('data-device-switch');

        if (this.checked) {
            $.post('/remote/power', {
                'name': device,
                'power': 'on'
            });
        }
        else {
            $.post('/remote/power', {
                'name': device,
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

function devicePower(power) {
    if (power.innerHTML === 'OFF') {
        power.innerHTML = 'ON';
        power.classList.add('btn-success');
        power.classList.remove('btn-danger')
    }
    else {
        power.innerHTML = 'OFF';
        power.classList.add('btn-danger');
        power.classList.remove('btn-success')
    }
}

function removeDevice(device) {
    var remove = confirm(device+" will be removed. Are you sure?");

    if (remove === true) {
        $.post('/remote/remove', {
            'name': device
        });

        window.location.replace('remote');
    }
}