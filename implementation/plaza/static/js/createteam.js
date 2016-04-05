
$("#person_search_field").keyup(function(event){
    if(event.keyCode == 13)
    {
        $("#add_person").click();
    }
    else
    {
        
    }
});


$("#add_person").click(function(event){
    $("#added").append(
        $("<p/>", {
                text: $("#person_search_field").val()
        }));
});
