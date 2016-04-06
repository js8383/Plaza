var current_username = null;

// from posted example
function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0; i < cookies.length; i++) {
        if (cookies[i].startsWith("csrftoken=")) {
            return cookies[i].substring("csrftoken=".length, cookies[i].length);
        }
    }
    return "unknown";
}

function create_tag_html(text, id, link, type, onclick_event)
{
    str = '<div class="btn-group" id="' + id + '">' +
          '<button class="btn btn-' + type + '">' + text + '</button>' +
          '<button class="btn btn-default" onclick="' + onclick_event + '">' +
            '<span>&times;</span>' +
          '</button>';
    return str;
}
