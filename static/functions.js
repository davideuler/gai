function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

$(document).ready(function(){

    var submit = $('#submit');
    var result = $('#result');
    var busy = $('#error-busy');
    var invalid = $('#error-invalid');
    var amount = $('#amount');

    result.hide();

    result.click(function(){
        $(this).select();
    })

    $('#shorten').submit(function(e){
        e.preventDefault();
        submit.val('Pruning...');
        submit.attr('disabled', true);
        $.ajax({
            url: "/a/shorten",
            data: {"origin": $("#id_origin").val()},
            method: "post",
            error: function(data, status){
                result.slideUp();
                $('#errors p').hide();
                if(status=="error"){
                    invalid.slideDown();
                }
                if(status=="timeout"){
                    busy.slideDown();
                }
                submit.attr('disabled', false);
                submit.val('Shorten');
            },
            success: function(data, status){
                $('#errors p').slideUp();
                if (data.is_new){
                    amount.text((parseInt(amount.text()) + 1).toString())
                }
                result.slideUp(function(){                
                    result.val(location.host + '/' + data.shorten);
                    result.slideDown(function(){
                        result.select();
                        submit.attr('disabled', false);
                        submit.val('Shorten');
                    });
                })
            }
        })
        
    })
})