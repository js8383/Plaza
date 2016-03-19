Project Specification
=====================
### Description
For our project, we intend to launch an online platform (name-to-be-decided) that is focused around building healthy models of student engagement, mostly targeted at large programming courses. 

Our platform will support multiple courses throughout multiple semesters. Registered instructors will be able to create and manage their courses while students will be able register for courses. Students will be able to post questions and students and instructors will be able to collectively construct their own answers, build wikis or scribes per lecture, and quiz each other. Posts will have tuneable viewership rules (public / private / restricted to a group). 

	To prevent stagnation in the answering process we will implement a notification system where users will be “assigned” to answer certain questions, and these assignments will notify the designated users (imagine a ticket-management system for dealing with all pending course issues-- bugs, regrading, exceptions). We will implement tools that will allow instructors or students to be pushed to answer certain questions, effectively distributing the workload of answering questions across the staff adequately. A dashboard/home page informs users of pending actions and deadlines. Instructors can use a calendar frame on the dashboard to inform students about office hours, deadlines and expected resolution dates.
	
To prevent duplicate and low quality posts from students, we intend to implement a pluggable language analyzer that checks if variants of a post already exists, or if a post is not well constructed (e.g. a error log dump). We will start with a naive word-similarity-based-module, but we want the design to allow individual courses to specify their own module.

Finally to help instructors monitor a course, we plan to graph online activity (reading, posting, number of active users ...). We also plan to build directed graphs tracking students across courses (directed based on conversations). Remember, students in one course can be staff in another.

Other features include:
 * dealing with concurrent edits
 * rich text and images, file uploads in posts and comments
 * text search within all posts (Piazza, for one, struggles with this)


### Model
We have created the basic model on Django and generated an ER diagram based on it using graphviz from django-extensions (shown below)


![alt text](https://raw.githubusercontent.com/CMU-Web-Application-Development/team2/master/specification/plaza.png?token=AIuszZoRiBQN78Y2jFowuYsbLzHTHyCXks5W9fpAwA%3D%3D "ER diagram")


[Link](https://github.com/CMU-Web-Application-Development/team2/blob/master/specification/plaza.png)

The ERD is largely self-explantory. Users are free to define courses and automatically become instructors for that course. They cann add other instructors, TAs and students. All users can make posts with various degrees of anonymity. A course can have an associated schedule of assignments. 

Assignments can be individual or team-based. If there are teams, we allow skill-sharing and self-formation of teams by students.

Posts and replies can be assigned statuses and due dates similar to a bug tracking system like JIRA. Instructors can track TA and student activity, post popularity and TA promptness. Posts can be upvoted and downvoted to build karma. Students can win badges and there is also a scoreboard to encourage participation.

### Wireframes




### Backlog
[You can view the table with the backlog details here](https://github.com/CMU-Web-Application-Development/team2/blob/master/specification/Project%20Backlog.html)



### Code Uploaded
We have created a basic version of models.py, started with stubs for all the view methods that we need to implement in the first two sprints and created static HTML pages for the template.
