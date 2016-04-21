function post(semester_id,course_id,parent_id)
{
  // Add validation
  document.getElementById('frame').src="/post/"+semester_id+"/"+course_id+"/"+parent_id
}

$('.clickable').click( function () {
  document.getElementById('frame').src="/view_post/"+this.id.replace('post_','');
});

function edit_text(post_id)
{
  d = document.getElementById('edit_post_div_'+post_id);
  d.style.display = 'block';
  d.style.width = '100%';
}
