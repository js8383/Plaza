function post(semester_id,course_id,parent_id)
{
  // Add validation
  document.getElementById('frame').src="/post/"+semester_id+"/"+course_id+"/"+parent_id
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
  d = document.getElementById('edit_post_div_'+post_id);
  d.style.display = 'block';
  d.style.width = '100%';
}

// Sends a new request to update the post list
function getPosts() 
{
    var req = new XMLHttpRequest();
    req.onreadystatechange = function() {
        if (req.readyState != 4) return;
        if (req.status != 200) return;
        var posts = JSON.parse(req.responseText);
        updatePosts(posts);
    }
    last_post = $("li").filter(".post")[0].id.split("_")[2]

    req.open("GET", "/post_list_ajax/" + last_post , true);
    req.send();
}

// http://stackoverflow.com/questions/847185/convert-a-unix-timestamp-to-time-in-javascript
function timeConverter(UNIX_timestamp)
{
  var a = new Date(UNIX_timestamp * 1000);
  var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  var year = a.getFullYear();
  var month = months[a.getMonth()];
  var date = a.getDate();
  var hour = a.getHours();
  var min = a.getMinutes();
  var time = date + ' ' + month + ' ' + year + ', ' + hour + ':' + min;
  return time;
}

// window.setInterval(getPosts, 5000);

