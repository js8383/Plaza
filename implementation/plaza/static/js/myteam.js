var my_username = "";
var course_semester = '';
var course_number = -1;
var team_id = -1;

function leave_team()
{
    console.log("username:"+my_username);
    console.log("team_id:"+team_id);
    $.ajax({

        url: "/remove_person_from_team/",

    data: {
        username: my_username,
        team_id: team_id,
        csrfmiddlewaretoken: getCSRFToken()
    },

    type: "POST",

    dataType: "json",

    success: function (obj) {
        window.location.replace(window.location.origin + '/home/' + obj.url)
    },

    error: function (xhr, status, errorThrown) {
               if (xhr.response != undefined)
                    display_error(xhr.responseJSON.message);
               log_error(xhr, status, errorThrown);
           }
    });

}

function add_person(a)
{
    var teammate = a.text;
    $.ajax({

        url: "/add_person_to_team/",

    data: {
        username: teammate,
        team_id: team_id,
        csrfmiddlewaretoken: getCSRFToken()
    },

    type: "POST",

    dataType: "json",

    success: function (user) {
        console.log(user);
        $('#member_table').prepend(
        '<tr>'+
            '<td>'+user.first_name+' '+user.last_name+'</td>'+
            '<td>'+user.username+'</td>'+
        '</tr>'
        );
    },

    error: function (xhr, status, errorThrown) {
               display_error(xhr.responseJSON.message);
               log_error(xhr, status, errorThrown);
           }
    });
}

function make_member_html(user)
{
    return '<a href="#">'+user.username+'</a>';
}

init_suggestions(
        "username",
        $("#student_search_field"),
        $("#add_member"),
        $("#students_list"),
        make_member_html,
        add_person,
        course_semester,
        course_number);


$("#alert_cancel").click(function(event){
    $("#alert_leave").modal("hide");
});
$("#alert_confirm").click(function(event){
    leave_team();
});

