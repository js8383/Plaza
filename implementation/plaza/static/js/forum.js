function post(semester_id,course_id,parent_id)
{
  // Add validation
  document.getElementById('frame').src="/post/"+semester_id+"/"+course_id+"/"+parent_id
}

$('.clickable').click( function () {
  this.id
  document.getElementById('frame').src="/view_post/"+this.id.replace('post_','');
});
