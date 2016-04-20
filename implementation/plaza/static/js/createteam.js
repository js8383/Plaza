var course_number = -1;
var course_semester = -1;
var assignment_number = -1;

$("#person_search_field").keyup(function(event){
    if(event.keyCode == 13)
    {
        $("#add_person").click();
    }
    else
    {
        $.ajax({

                url: "/dynamic_obj_suggestion/",

                async: false,

                data: {
                    input_type: "username",
                    input_data: $("#person_search_field").val(),
                    course_number: course_number,
                    course_semester: course_semester,
                    csrfmiddlewaretoken: getCSRFToken()
                },

                type: "POST",

                dataType: "json",

                success: function (response) {
                    $("#student_list").empty();
                    console.log(response);
                    if (response != null)
                    {
                        for (var i = 0; i < response.length; i++)
                        {
                            var s = response[i];
                            $("#students_list").empty();
                            $("#students_list").append(
                            '<li>'+
                                '<a href="#">'+s.username+'</a></li>');
                        }
                        if (response.length != 0)
                        {
                            $("#students_list").show();
                        }
                        else
                        {
                            $("#students_list").empty();
                            $("#students_list").hide();
                        }
                    }
                    else
                    {
                        $("#students_list").empty();
                        $("#students_list").hide();
                    }
                },

                error: function (xhr, status, errorThrown) {
                    display_error(xhr, status, errorThrown);
                }
            });

    }
});

// submit the team
function submit_team()
{
    var team_name = $("#team_name_field").val();

    var members = get_all_tags_of_type("person");

    $.ajax({

            url: "/submit_team/",

            async: false,

            data: {
                course_number: course_number,
                course_semester: course_semester,
                assignment_number: assignment_number,
                team_name: team_name,
                team_members: JSON.stringify(members),
                csrfmiddlewaretoken: getCSRFToken()
            },

            type: "POST",

            dataType: "json",

            success: function (response) {
                console.log(response)
                append_success("Created team " + team_name + "!");
            },

            error: function (xhr, status, errorThrown) {
                display_error(xhr, status, errorThrown);
            }
        });


}

function remove_all_people()
{
    $("#added").empty();
}

function add_person(teammate)
{
    if (teammate.username == current_username)
    {
        append_error("Can't invite yourself to a team.");
    }
    else if ($.inArray(teammate.username, get_all_tags_of_type("person")) != -1)
    {
        console.log(get_all_tags_of_type("person"));
        append_error(teammate.username + " already added.");
    }
    else
    {
        $("#added").append(
                create_tag_html(
                    teammate.username,
                    "person",
                    teammate.username,
                    "profile/" + teammate.userid,
                    'default'));
    }
}

function get_person(username)
{
    if (username == null)
    {
        return null
    }
    else
    {
        $.ajax({

            url: "/search_student/",

            data: {
                username: username,
                csrfmiddlewaretoken: getCSRFToken()
            },

            type: "POST",

            dataType: "json",

            success: function (user) {
                add_person(user);
            },

            error: function (xhr, status, errorThrown) {
                display_error(xhr, status, errorThrown);
            }
        });
    }
}

$("#add_person").click(function(event){
    get_person($("#students_list").find('a').first().text());
    $("#students_list").empty();
    $("#students_list").hide();
    $("#person_search_field").val('');
});

$(document).ajaxStart(function () {
});

$(document).ajaxStop(function() {
});
