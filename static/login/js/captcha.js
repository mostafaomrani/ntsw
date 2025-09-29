$('#refresh-captcha').click(function () {
    refreshCaptcha();
});

setInterval(function () {
    var img = $('#img-captcha');
    var remind = img.data('remind');
    
    if (remind > 0) {
        img.data('remind', remind - 1);
    }
    else {
        refreshCaptcha();
    }
}, 1000);


function refreshCaptcha() {
    $.getJSON('/api/Captcha/Get', {},
        function (result) {
            var img = $('#img-captcha');
            var secretInputId = img.data('secret-input-id');

            $('#' + secretInputId).val(result.secret);
            img.data('remind', result.remindSecond);
            img.attr('src', result.captcha)
        });
} 