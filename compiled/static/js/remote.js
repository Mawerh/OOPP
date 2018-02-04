$(document).ready(function() {
    $('.modal').on('shown.bs.modal', function() {
        $('.modal_focus_input').trigger('focus');
    });

    /*$('.button_device').on('click', function() {
        var wrapper = $(this).closest('.device_dropdown');
        wrapper.find('.device_dropdown_content').slideToggle();
    });*/

    /*$('.button_device').blur(function() {
        var wrapper = $(this).closest('.device_dropdown');
        wrapper.find('.device_dropdown_content').slideUp();
    });*/

    $('button').on('click', function() {
        if (this.classList.contains('button_device')) {
            var wrapper = $(this).closest('.device_dropdown');
            var dropdown = wrapper.find('.device_dropdown_content');

            dropdown.slideToggle();
            $('.device_dropdown_content').not(dropdown).slideUp();
        }
        else if (!this.classList.contains('device_dropdown_button') && !this.classList.contains('close')) {
            $('.device_dropdown_content').slideUp();
        }
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

function setLocationBrandModal(type) {
    document.getElementById('modal_device_location_label').innerHTML = 'Select '+type+' location';
    document.getElementById('modal_device_brand_label').innerHTML = 'Select '+type+' brand';
    document.getElementById('span_device_type').innerHTML = type;
    document.getElementById('input_device_type').value = type;
}

function setDeviceLocationInput(location) {
    document.getElementById('input_device_location').value = location;
}

function showDeviceBrandModal() {
    var input = document.getElementById('input_device_other_location');

    if (input.checkValidity()) {
        $('#modal_location_name').modal('hide');

        var location = document.getElementById('input_device_other_location').value;
        setDeviceLocationInput(location);

        $('#modal_device_brand').modal('show');
    }
}

function showDeviceNameForm() {
    var input = document.getElementById('input_device_other_brand');

    if (input.checkValidity()) {
        $('#modal_brand_name').modal('hide');

        var brand = document.getElementById('input_device_other_brand').value;
        setDeviceNameForm(brand);

        $('#modal_device_name').modal('show');
    }
}

function setDeviceNameForm(brand) {
    document.getElementById('span_device_brand').innerHTML = brand;
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
    if (type !== 'TV' && type !== 'AC') {
        type = type.toLowerCase().replace(/\b[a-z]/g, function(letter) {
            return letter.toUpperCase();
        });
    }

    document.getElementById('device_info_type').innerHTML = type;
    document.getElementById('device_info_brand').innerHTML = brand;
    document.getElementById('device_info_name').innerHTML = name;
    document.getElementById('device_info_location').innerHTML = location;
}

function showAllDevices() {
    var devices = document.getElementsByClassName('device_dropdown');

    for (var i = 0; i < devices.length; i++) {
        devices[i].style.display = 'block';
    }
}

function showDevicesInRoom(data_location) {
    var devices = document.querySelectorAll('[data-device-location]');

    for (var i = 0; i < devices.length; i++) {
        if (devices[i].getAttribute('data-device-location') === data_location) {
            devices[i].style.display = 'block';
        }
        else {
            devices[i].style.display = 'none';
        }
    }
}
