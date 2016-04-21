function post(parent_id)
{
  // Add validation
  document.getElementById('frame').src="/post/"+semester_id+"/"+course_id+"/"+parent_id;
}

$('.clickable').click( function ()
{
  if (typeof oldPostId !== 'undefined')
  {
    $(document.getElementById(oldPostId)).removeClass('panel-primary').addClass('panel-default');
  }
  $(document.getElementById(this.id)).removeClass('panel-default').addClass('panel-primary');
  oldPostId = this.id
  document.getElementById('frame').src="/view_post/"+this.id.replace('post_','');
});

function edit_text(post_id)
{
  document.getElementById('edit_post_div_'+post_id).style.display = 'block';
  document.getElementById('to_hide_'+post_id).style.display = 'none';
}


// Sends a new request to update the post list
function getPosts()
{
    var req = new XMLHttpRequest();
    req.onreadystatechange = function()
    {
        if (req.readyState != 4) return;
        if (req.status != 200) return;
        var posts = JSON.parse(req.responseText);
        updatePosts(posts);
    }
    if($("div").filter(".clickable").length > 0) last_post = $("div").filter(".clickable")[0].id.split("_")[1]
    else last_post = 0;

    req.open("GET", "/get_new_posts_json/"+semester_id+"/"+course_id+"/" + last_post + '?q=' + $('#q')[0].value , true);
    req.send();
}



function updatePosts(posts)
{
  for(var i=0; i<posts.length;++i)
  {
  new_post_html = '<div class="list-group-item panel panel-default clickable visborder" id="post_'
   + posts[i]["post_id"]
   + '"><div class="panel-heading"><div class="row"><div class="col-md-8 pull-left"><p>'
   + posts[i]["title"]
   + '</p></div><div class="col-md-4 pull-right"><p><small>'
   + posts[i]["timestamp"]
   + '</small></p></div></div></div><div class="panel-body"><p>'
   + posts[i]["text"]
   + '</p></div></div>';

    $("#posts-list").prepend(new_post_html);
  }
}



function updownvote(post_id,vote_type)
{
    var req = new XMLHttpRequest();
    req.onreadystatechange = function()
    {
        if (req.readyState != 4) return;
        if (req.status == 404)
        {
          var msg = JSON.parse(req.responseText);
          display_error(msg.message);
        }
        if (req.status != 200) return;
        display_success("Voted successfully");

        console.log("debug: ");
        console.log($("#post_"+post_id));
        console.log($("#post_"+post_id).find("col-sm-4"));
        console.log($("#post_"+post_id).find("col-sm-4")[0]);
        console.log($("#post_"+post_id).find("col-sm-4")[0].find("span"));
        console.log($("#post_"+post_id).find("col-sm-4")[0].find("span")[0]);
        console.log($("#post_"+post_id).find("col-sm-4")[0].find("span")[0].val());
        if (vote_type == "upvote")
        {
            cnt = $("#post_"+post_id).find("col-sm-4")[0].find("span")[0].val();
            cnt++;
            $("#post_"+post_id).find("col-sm-4")[0].find("span")[0].val(cnt);
        }
        else
        {
            cnt = $("#post_"+post_id).find("col-sm-4")[0].find("span")[1].val();
            cnt--;
            $("#post_"+post_id).find("col-sm-4")[0].find("span")[1].val(cnt);
        }

        var msg = JSON.parse(req.responseText);
    }
    req.open("GET", "/"+vote_type+"/" + post_id ,true);
    req.send();


}

