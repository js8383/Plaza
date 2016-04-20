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

// Grabbed from Django site
// using jQuery
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

// Grabbed from django site
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

// remove special characters
function remove_special(str) {
     return str.replace(/([!@~#%^&*{}()_=+$`\[\]\|\\:;'<>\/? .,])+/g, '');
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

function append_error(errorThrown)
{
        $("#errors").append(
            '<div class="alert alert-danger">' +
            '<a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>' +
            errorThrown +
            '</div>'
            );
}

function append_success(success)
{
    $("#statuses").append(
            '<div class="alert alert-success">' +
            '<a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>' +
            success +
            '</div>'
            );
}

function display_success(success)
{
    $("#statuses").children().remove()
    append_success(success)
}


function display_error(error)
{
    if (error != undefined)
    {
        $("#errors").children().remove();
        append_error(error);
    }
}

function log_error(xhr, status, errorThrown)
{
    console.log( "Error: " + errorThrown );
    console.log( "Status: " + status );
    console.dir( xhr );
}


//$('#dpicker').datepicker({});

// $("#my-checkbox").bootstrapSwitch();

// $("#input-repl-1a").fileinput({
//     // uploadUrl: "#",
//     autoReplace: true,
//     overwriteInitial: true,
//     maxFileCount: 1,
//     initialPreview: [
//         "<img src='/profilepicture/4' alt='Profile Picture' class='img-rounded' height='100%' width='100%' />",
//     ],
//     initialPreviewShowDelete: false,
//     showDelete: true,
//     showCaption: false,
//     showClose: false,
//     showUpload: false,
//     allowedFileTypes: ["image"]
// });

$('#input-repl-1a').on('filecleared', function(event) {
    $('#input-repl-1a').fileinput('reset');
});


/*
 * USER SEARCH
 */

/* @brief install the appropriate handlers for the
 *        dynamic search box
 */
function init_suggestions(input_type,
                          input_box,
                          input_button,
                          dropdown_list,
                          dropdown_html_maker,
                          callback,
                          course_semester,
                          course_number)
{
    /* Event handlers */

    course_semester = course_semester || "";
    course_number = course_number || "";

    var list_i = 0;
    input_button.click(function(event){
        callback(dropdown_list.find("li.active").find("a")[0]);
        dropdown_list.hide();
        dropdown_list.empty();
        input_box.val('');
        event.preventDefault();
    });

    input_box.keyup(function(event){
        if(event.keyCode == 13)
        {
            input_button.click();
        }
        else if (event.keyCode == 40) // Down key
        {
            if (list_i < dropdown_list.children().length-1)
            {
                dropdown_list.children().eq(list_i+1).addClass("active");
                dropdown_list.children().eq(list_i).removeClass("active");
                list_i++;
            }
        }
        else if (event.keyCode == 38) // Up key
        {
            if (list_i > 0)
            {
                dropdown_list.children().eq(list_i-1).addClass("active");
                dropdown_list.children().eq(list_i).removeClass("active");
                list_i--;
            }
        }
        else
        {
            if (course_semester == "" && course_number == "")
            {
                var data = {
                        input_type: input_type,
                        input_data: input_box.val(),
                        csrfmiddlewaretoken: getCSRFToken()
                    };
            }
            else
            {
                var data = {
                        input_type: input_type,
                        input_data: input_box.val(),
                        course_semester: course_semester,
                        course_number: course_number,
                        csrfmiddlewaretoken: getCSRFToken()
                    };
            }
            console.log(data);
            $.ajax({

                    url: "/dynamic_obj_suggestion/",

                    async: false,

                    data: data,

                    type: "POST",

                    dataType: "json",

                    success: function (response) {
                        dropdown_list.empty();
                        console.log(response);
                        if (response != null)
                        {
                            list_i = 0;
                            for (var i = 0; i < response.length; i++)
                            {
                                var s = response[i];
                                var block = '';
                                if (i == 0)
                                    block='<li class="active">'+
                                        dropdown_html_maker(s)+
                                        '</li>';
                                else
                                    block='<li>'+dropdown_html_maker(s)+'</li>';
                                dropdown_list.append(block);
                            }
                            if (response.length != 0)
                            {
                                dropdown_list.show();
                            }
                            else
                            {
                                dropdown_list.hide();
                                dropdown_list.empty();
                            }
                        }
                        else
                        {
                            dropdown_list.hide();
                            dropdown_list.empty();
                        }
                    },

                    error: function (xhr, status, errorThrown) {
                        display_error(xhr.responseJSON.message);
                        log_error(xhr, status, errorThrown);
                    }
                });
        }
    });
}

/*
 * COURSE SEARCH
 */

function course_suggestion_html(c)
{
    return '<a href="/forum/'+c.fields.semester+'/'+c.fields.number+'">'+
                            +c.fields.number+' '+c.fields.semester+'</a>';
}

function on_course_suggestion_click(a)
{
    a.click();
}

init_suggestions(
        "course_number",
        $("#course_search_field"),
        $("#go_to_course"),
        $("#courses_list"),
        course_suggestion_html,
        on_course_suggestion_click);

// notification
function displaynotidropdown(id) {

    var req = new XMLHttpRequest();
    req.onreadystatechange = function() {
        if (req.readyState != 4) return;
        if (req.status != 200) return;
        var notifications = JSON.parse(req.responseText);
        var innerhtml_format = "";
        for (var i = 0; i < notifications.length; i++) {
            var notification = notifications[i]
            var sender = notification['sender']
            var sender_id = notification['sender_id']
            var action = notification['action']
            var extra_content = notification['extra_content']
            var created_at = notification['created_at']
            var destination = notification['destination']
            innerhtml_format += "<li> <a href='" + destination + "'> <div>" + sender + action +
                                   "<span class='pull-right text-muted small'>" + created_at + "</span></div></a>" +
                                   "</li> <li class='divider'></li>"
            // console.log(innerhtml_format);
            
        }
        $('#notidropdown li:not(:last)').remove();
        $('#notidropdown').prepend(innerhtml_format);
    
        
    }

    req.open("POST", "/getnotification/" + id, true);
    req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    req.send("csrfmiddlewaretoken="+getCSRFToken());
    
    $('#notidropdown').toggle();
}
