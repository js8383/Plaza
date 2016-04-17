var course_number = -1
var course_semester = ''

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
                $("#"+role+"_table").prepend(
                    "<tr><td>" + userinf.first_name + " " + userinf.last_name + "</td></tr>"
                    );
            },

            error: function (xhr, status, errorThrown) {
                display_error(xhr, status, errorThrown);
            }
        });
    }
}


/* Event handlers */

$("#instructor_search_field").keyup(function(event){
    if(event.keyCode == 13)
    {
        $("#add_instructor").click();
    }
    else
    {
    }
});

$("#staff_search_field").keyup(function(event){
    if(event.keyCode == 13)
    {
        $("#add_staff").click();
    }
    else
    {
    }
});

$("#student_search_field").keyup(function(event){
    if(event.keyCode == 13)
    {
        $("#add_student").click();
    }
    else
    {
    }
});

$("#add_instructor").click(function(event){
    add_person($("#instructor_search_field").val(), 'instructor');
    $("#instructor_search_field").val('');
});

$("#add_staff").click(function(event){
    add_person($("#staff_search_field").val(), 'staff');
    $("#staff_search_field").val('');
});


$("#add_student").click(function(event){
    add_person($("#student_search_field").val(), 'student');
    $("#student_search_field").val('');
});





