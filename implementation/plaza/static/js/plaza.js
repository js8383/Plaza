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



function display_error(xhr, status, errorThrown)
{
    console.log( "Error: " + errorThrown );
    console.log( "Status: " + status );
    console.dir( xhr );
    $("#errors").children().remove()
    append_error(errorThrown);
}


$('#dpicker').datepicker({});

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
function get_people_suggestions(input, dropdown_list)
{
    $.ajax({

            url: "/dynamic_obj_suggestion/",

            async: false,

            data: {
                input_type: "username",
                input_data: input,
                csrfmiddlewaretoken: getCSRFToken()
            },

            type: "POST",

            dataType: "json",

            success: function (response) {
                dropdown_list.empty();
                console.log(response);
                if (response != null)
                {
                    for (var i = 0; i < response.length; i++)
                    {
                        var s = response[i];
                        dropdown_list.append(
                        '<li>'+
                            '<a href="#">'+s.username+'</a></li>');
                    }
                    if (response.length != 0)
                    {
                        dropdown_list.show();
                    }
                    else
                    {
                        dropdown_list.hide();
                    }
                }
                else
                {
                    dropdown_list.hide();
                }
            },

            error: function (xhr, status, errorThrown) {
                display_error(xhr, status, errorThrown);
            }
        });
}

function get_people_suggestions_with_profile(input, dropdown_list)
{
    $.ajax({

            url: "/dynamic_obj_suggestion/",

            async: false,

            data: {
                input_type: "username",
                input_data: input,
                csrfmiddlewaretoken: getCSRFToken()
            },

            type: "POST",

            dataType: "json",

            success: function (response) {
                dropdown_list.empty();
                console.log(response);
                if (response != null)
                {
                    for (var i = 0; i < response.length; i++)
                    {
                        var s = response[i];
                        dropdown_list.append(
                        '<li>'+
                            '<a href="/profile/'+s.user_id+'">'+s.username+'</a></li>');
                    }
                    if (response.length != 0)
                    {
                        dropdown_list.show();
                    }
                    else
                    {
                        dropdown_list.hide();
                    }
                }
                else
                {
                    dropdown_list.hide();
                }
            },

            error: function (xhr, status, errorThrown) {
                display_error(xhr, status, errorThrown);
            }
        });
}

/* Event handlers */

$("#user_search_field").keyup(function(event){
    if(event.keyCode == 13)
    {
        $("#go_to_user").click();
    }
    else
    {
        get_people_suggestions_with_profile($("#user_search_field").val(), $("#users_list"))
    }
});

$("#go_to_user").click(function(event){
    $("#users_list").find("a")[0].click();
    event.preventDefault();
});


/*
 * COURSE SEARCH
 */



$("#course_search_field").keyup(function(event){
    if(event.keyCode == 13)
    {
        $("#go_to_course").click();
    }
    else
    {
        $.ajax({

                url: "/dynamic_obj_suggestion/",

                async: false,

                data: {
                    input_type: "course_number",
                    input_data: $("#course_search_field").val(),
                    csrfmiddlewaretoken: getCSRFToken()
                },

                type: "POST",

                dataType: "json",

                success: function (response) {
                    $("#courses_list").empty();
                        if (response != null)
                        {
                            for (var i = 0; i < response.length; i++)
                            {
                                var c = response[i].fields;
                                $("#courses_list").append(
                                '<li>'+
                                    '<a href="/forum/'+c.semester+'/'+c.number+'">'
                                     +c.number+' '+c.semester+'</a></li>');
                            }
                            if (response.length != 0)
                            {
                                $("#courses_list").show();
                            }
                            else
                            {
                                $("#courses_list").hide();
                            }
                        }
                        else
                        {
                            $("#courses_list").hide();
                        }
                },

                error: function (xhr, status, errorThrown) {
                    display_error(xhr, status, errorThrown);
                }
            });
    }
});

$("#go_to_course").click(function(event){
    $("#courses_list").find("a")[0].click();
    event.preventDefault();
});



