var course_number = -1;
var course_semester = -1;
var assignment_number = -1;



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
                display_error(xhr.responseJSON.message);
                log_error(xhr, status, errorThrown);
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
                display_error(xhr.responseJSON.message);
                log_error(xhr, status, errorThrown);
            }
        });
    }
}


init_people_suggestions(
        $("#person_search_field"),
        $("#add_person"),
        $("#students_list"),
        get_person);

$(document).ajaxStart(function () {
});

$(document).ajaxStop(function() {
});
