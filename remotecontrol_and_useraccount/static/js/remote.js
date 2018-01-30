$(document).ready(function() {
    $('.modal').on('shown.bs.modal', function() {
        $('.modal_focus_input').trigger('focus');
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

function setDeviceBrandModal(type) {
    document.getElementById('modal_device_brand_label').innerHTML = 'Select '+type+' brand';
    document.getElementById('header_device_type').innerHTML = type;
    document.getElementById('input_device_type').value = type;
}

function setDeviceNameForm(brand) {
    document.getElementById('header_device_brand').innerHTML = brand;
    document.getElementById('input_device_brand').value = brand;
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

function setDeviceInfo(type, brand, name, location) {
    if (type === 'device') {
        document.getElementById('device_info_type').innerHTML = 'Other';
    }
    else if (type === 'TV' || type === 'AC') {
        document.getElementById('device_info_type').innerHTML = type;
    }
    else {
        type = type.toLowerCase().replace(/\b[a-z]/g, function(letter) {
            return letter.toUpperCase();
        });

        document.getElementById('device_info_type').innerHTML = type;
    }

    document.getElementById('device_info_brand').innerHTML = brand;
    document.getElementById('device_info_name').innerHTML = name;
    document.getElementById('device_info_location').innerHTML = location;
}
