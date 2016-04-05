

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

function display_error(xhr, status, errorThrown)
{
    console.log( "Error: " + errorThrown );
    console.log( "Status: " + status );
    console.dir( xhr );
    $("#errors").append(
            '<div class="alert alert-danger">' +
            '<a href="#" class="close" data-dismiss="alert" aria-label="close">&times;</a>' +
            errorThrown +
            '</div>'
            );
}

function remove_all_people()
{
    $("#added").empty();
}

function remove_person(username)
{
    $("#" + username + "_tag").remove();
}

function add_person(user)
{
    $("#added").append(
            create_tag_html(
                user.username,
                user.username + "_tag",
                "profile/" + user.userid,
                'default',
                "remove_person('"+user.username+"')"));
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
