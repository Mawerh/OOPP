$(document).ready(function() {
    $('.weather_switch input').change(function() {
        var setting = $(this).attr('data-weather-setting');

        if (this.checked) {
            $.post('/WeatherSettings/setting', {
                'setting': setting,
                'switch': 'on'
            });
        }
        else {
            $.post('/WeatherSettings/setting', {
                'setting': setting,
                'switch': 'off'
            });
        }
    });
});
