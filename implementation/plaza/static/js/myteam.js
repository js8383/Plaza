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

function add_person(teammate)
{
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
               if (xhr.response != undefined)
                   display_error(xhr.responseJSON.message);
               log_error(xhr, status, errorThrown);
           }
    });
}

$("#student_search_field").keyup(function(event){
    if(event.keyCode == 13)
    {
        $("#add_member").click();
    }
    else
    {
       get_people_suggestions($("#student_search_field").val(),$("#students_list"));
    }
});

$("#add_member").click(function(event){
    add_person($("#students_list").find('a').first().text(), 'student');
    $("#students_list").empty();
    $("#students_list").hide();
    $("#student_search_field").val('');
});

$("#alert_cancel").click(function(event){
    $("#alert_leave").modal("hide");
});
$("#alert_confirm").click(function(event){
    leave_team();
});

