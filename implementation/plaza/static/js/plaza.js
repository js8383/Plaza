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


function remove_tag(type, id)
{
    $("#" + id + "_" + type + "_tagcontainer").remove();
}

function get_all_tags_of_type(type)
{
    var all_text =[];
    $('[id$="'+type+'_tag"]').each(function() { all_text.push($(this).text()) });

    return all_text;
}

function create_tag_html(text, type, id, link, css_type)
{
    str = '<div class="btn-group" id="' + id + "_" + type + '_tagcontainer">' +
          '<button class="btn btn-' + css_type + ' tag" id="' + id + "_" + type + '_tag">' + text + '</button>' +
          '<button class="btn btn-default" onclick="' + "remove_tag('"+type+"','"+id+"')" + '">' +
            '<span>&times;</span>' +
          '</button>';
    return str;
}


$('#dpicker').datepicker({});