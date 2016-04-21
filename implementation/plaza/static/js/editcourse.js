var my_username = ""
var course_number = -1
var course_semester = ''

function append_tag(name)
{
    $("#tag_table").prepend(
        '<tr id="tag_'+name+'_row">'+
            '<td>'+
                name+
            '</td>'+
            '<td>'+
                '<button class="btn btn-default"'+
                    'onclick=remove_tag("'+name+'")>'+
                    '<span class="glyphicon glyphicon-remove"></span></button>'+
            '</td>'+
        '</tr>'
    );
}

function append_assignment(title, number, team_min, team_max, end_time)
{
    $("#assignment_table").prepend(
        '<tr id="assignment_'+title+'_row">'+
            '<td>'+
                title+
            '</td>'+
            '<td>'+
                number+
            '</td>'+
            '<td>'+
                team_min+
            '</td>'+
            '<td>'+
                team_max+
            '</td>'+
            '<td>'+
                end_time+
            '</td>'+
            '<td>'+
                '<button class="btn btn-default"'+
                    'onclick=remove_assignment("'+title+'")>'+
                    '<span class="glyphicon glyphicon-remove"></span></button>'+
            '</td>'+
        '</tr>'
    );
}

function add_tag(dirty_name)
{
    var name=remove_special(dirty_name)
    $.ajax({

        url: "/add_tag_to_course/",

        data: {
            tag_name: name,
            course_number: course_number,
            course_semester: course_semester,
            csrfmiddlewaretoken: getCSRFToken()
        },

        type: "POST",

        dataType: "json",

        success: function (message) {
            display_success(message.message);
            // add the user to the new roles table
            append_tag(name);
        },

        error: function (xhr, status, errorThrown) {
            display_error(xhr.responseJSON.message);
            log_error(xhr, status, errorThrown);
        }
    });
}


function add_assignment(dirty_title, number, team_min, team_max, end_time)
{
    var title=remove_special(dirty_title)
    console.log(team_min);
    console.log(team_max);
    console.log(end_time);
    $.ajax({

        url: "/add_assignment_to_course/",

        data: {
            assignment_title: title,
            assignment_number: number,
            assignment_team_min_size: team_min,
            assignment_team_max_size: team_max,
            assignment_end_time: end_time,
            course_number: course_number,
            course_semester: course_semester,
            csrfmiddlewaretoken: getCSRFToken()
        },

        type: "POST",

        dataType: "json",

        success: function (message) {
            // add the user to the new roles table
            append_assignment(title, number, team_min, team_max, end_time);
            // append a tag as well if
            // one doesn't exist already
            if (!($("#tag_"+title+"_row").length))
                append_tag(title);
        },

        error: function (xhr, status, errorThrown) {
            display_error(xhr.responseJSON.message);
            log_error(xhr, status, errorThrown);
        }
    });
}



function add_instructor(a)
{
    add_person(a.text, "instructor");
}

function add_staff(a)
{
    add_person(a.text, "staff");
}

function add_student(a)
{
    add_person(a.text, "student");
}

function add_person(username, role)
{
    if (username == null)
    {
        return null
    }
    else
    {
        $.ajax({

            url: "/add_person_to_course/",

            data: {
                username: username,
                role: role,
                course_number: course_number,
                course_semester: course_semester,
                csrfmiddlewaretoken: getCSRFToken()
            },

            type: "POST",

            dataType: "json",

            success: function (userinf) {
                // remove the user from other roles
                // if it exists
                $("#"+username+"_row").remove();
                // add the user to the new roles table
                $("#"+role+"_table").prepend(
                    "<tr id='"+username+"_row'><td>" +
                    userinf.first_name + " " + userinf.last_name + "</td>"+
                    "<td>"+
                    "<button class='btn btn-default'" +
                    "onclick=remove_person('"+username+"','"+role+"')>"+
                    "<span class='glyphicon glyphicon-remove'></span></button>"+
                    "</td></td></tr>"
                    );
            },

            error: function (xhr, status, errorThrown) {
                display_error(xhr.responseJSON.message);
                log_error(xhr, status, errorThrown);
            }
        });
    }
}

function ajax_remove(username, role)
{
    $.ajax({

        url: "/remove_person_from_course/",

    data: {
        username: username,
        role: role,
        course_number: course_number,
        course_semester: course_semester,
        csrfmiddlewaretoken: getCSRFToken()
    },

    type: "POST",

    dataType: "json",

    success: function () {
        $("#"+username+"_row").remove();
    },

    error: function (xhr, status, errorThrown) {
               display_error(xhr.responseJSON.message);
               log_error(xhr, status, errorThrown);
           }
    });

}

function remove_person(username, role)
{
    if (username == my_username)
    {
        // add event handlers to the modal
        $("#alert_confirm").click(function(event){
            ajax_remove(username, role);
            $("#alert_self").modal("hide");
        });

        $("#alert_cancel").click(function(event){
            $("#alert_self").modal("hide");
        });

        // open up the modal
        $("#alert_self").modal();
    }
    else
    {
        ajax_remove(username, role);
    }
}

function remove_tag(name)
{
    $.ajax({

        url: "/remove_tag_from_course/",

    data: {
        tag_name: name,
        course_number: course_number,
        course_semester: course_semester,
        csrfmiddlewaretoken: getCSRFToken()
    },

    type: "POST",

    dataType: "json",

    success: function (obj) {
        $("#tag_"+name+"_row").remove();
    },

    error: function (xhr, status, errorThrown) {
               display_error(xhr.responseJSON.message);
               log_error(xhr, status, errorThrown);
           }
    });

}


function remove_assignment(title)
{
    $.ajax({

        url: "/remove_assignment_from_course/",

    data: {
        assignment_title: title,
        course_number: course_number,
        course_semester: course_semester,
        csrfmiddlewaretoken: getCSRFToken()
    },

    type: "POST",

    dataType: "json",

    success: function (obj) {
        $("#assignment_"+title+"_row").remove();
        $("#tag_"+title+"_row").remove();
    },

    error: function (xhr, status, errorThrown) {
               display_error(xhr.responseJSON.message);
               log_error(xhr, status, errorThrown);
           }
    });

}

/* Event handlers */

function make_member_html(user)
{
    return '<a href="#">'+user.username+'</a>';
}

init_suggestions(
        "username",
        $("#instructor_search_field"),
        $("#add_instructor"),
        $("#instructors_list"),
        make_member_html,
        add_instructor);

init_suggestions(
        "username",
        $("#staff_search_field"),
        $("#add_staff"),
        $("#staff_list"),
        make_member_html,
        add_staff);

init_suggestions(
        "username",
        $("#student_search_field"),
        $("#add_student"),
        $("#students_list"),
        make_member_html,
        add_student);

$("#tag_name_field").keyup(function(event){
    if(event.keyCode == 13)
    {
        $("#add_tag").click();
    }
});

$("#add_tag").click(function(event){
    add_tag($("#tag_name_field").val());
    $("#tag_name_field").val('');
});

$("#assignment_number_field").keyup(function(event){
    if(event.keyCode == 13)
    {
        $("#add_assignment").click();
    }
});

$("#add_assignment").click(function(event){
    add_assignment(
        $("#assignment_title_field").val(),
        $("#assignment_number_field").val(),
        $("#assignment_tm_mn_field").val(),
        $("#assignment_tm_mx_field").val(),
        $("#ass_dpicker").val());
    $("#assignment_title_field").val('');
    $("#assignment_number_field").val('');
});

// asynchronously submit the class preferences
$("#course_pref_form").submit(function(event) {
    var csrftoken = getCookie('csrftoken');
    console.log($("#course_pref_form").serialize());
    $.ajax(
        {
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },

        type: "POST",

        url: "/save_course_pref/"+course_semester+"/"+course_number+"/",

        data: $("#course_pref_form").serialize(),

        success: function(message) {
            display_success(message.message);
        },

        error: function (xhr, status, errorThrown) {
            display_error(xhr.responseJSON.message);
            log_error(xhr, status, errorThrown);
        }
    });

    event.preventDefault();
});


if ($( "#ass_dpicker" ).length) {
    $('#ass_dpicker').datepicker({});
}

