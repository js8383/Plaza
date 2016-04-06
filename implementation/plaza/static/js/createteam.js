$("#person_search_field").keyup(function(event){
    if(event.keyCode == 13)
    {
        $("#add_person").click();
    }
    else
    {
        // TODO: search people and display suggestions
    }
});

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
    $("#errors").append(
            '<div class="alert alert-success">' +
            '<a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>' +
            success +
            '</div>'
            );
}

function display_error(xhr, status, errorThrown)
{
    console.log( "Error: " + errorThrown );
    console.log( "Status: " + status );
    console.dir( xhr );
    append_error(errorThrown);
}

function submit_team()
{
    var team_name = $("#team_name_field").val();
    //var members = $("#added: .btn")
    append_success("Created team " + team_name + "!");
}

function remove_all_people()
{
    $("#added").empty();
}

function remove_person(username)
{
    $("#" + username + "_tag").remove();
}

function add_person(teammate)
{
    console.log(current_username);
    if (teammate.username == current_username)
    {
        append_error("Can't invite yourself to a team.");
    }
    else
    {
        $("#added").append(
                create_tag_html(
                    teammate.username,
                    teammate.username + "_tag",
                    "profile/" + teammate.userid,
                    'default',
                    "remove_person('"+teammate.username+"')"));
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
    get_person($("#person_search_field").val());
});
