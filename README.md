# microblog
## Language: Python
## Framework: Flask
#### Description:
A microblogging site for users to post and comment on content. Each user has a unique profile page tailored to the post they have created. The site is designed to be responsive and mobile-friendly. The site is built with an MVC architecture. 

#### TODO:
- [ ] Create a user registration system
- [ ] Create a user login system
- [ ] Create a post system, where users can post content
- [ ] Create a comment system, where users can comment on posts
- [ ] Create a like system, where users can like posts and dislike posts

#### Notes:
- [ ] auth.py is the file that handles user authentication
  - [ ] Login function gets user input and checks if the user is in the database. If the user is in the database, the user is logged in. If the user is not in the database a flash message is displayed either saying that the user email is not in the database or that the password is incorrect.
  - [ ] Signup function gets user input and checks if the user is in the database. If the user is in the database, a flash message is displayed saying that the user email is already in the database. If the user is not in the database, the user is added to the database and a flash message is displayed saying that the user has created. Validations are also done on the user input; If email is already in use, or email is already in user or Password is not the same as Confirm Password. 
  - [ ] Logout function logs the user out and redirects to the login page.
- [ ] models.py is the file that handles the database
  - [ ] User class is the class that handles the user information and relationships to other classes like posts(one to many), comments (one to many) and likes (one to many).
  - [ ] Post class is the class that handles the post information and relationships to other classes like comments(one to many) and likes (one to many).
  - [ ] Comment class is the class that handles the comment information and relationships to other classes like author(many to one) and post(many to one)
  - [ ] Like class is the class that handles the like information and relationships to other classes like author(many to one) and post(many to one)
- [ ] views.py is the file that handles the user input and output and the rendering of the html templates
  - [ ] home function is the function that handles the home page. It renders the home.html template and passes the posts to the template.
  - [ ] create_post function is the function that handles the post creation page. It renders the create_post.html template and passes the posts to the template.
  - [ ] delete_post function is the function that handles the post deletion page using <post_id>. 
  - [ ] posts function is the function that handles the posts from a specific user. It renders the posts.html template and passes the posts to the template.
  - [ ] create_comment function is the function that handles the comment creation page using <post_id>. 
  - [ ] delete_comment function is the function that handles the comment deletion page using <comment_id>.
  - [ ] like function is the function that handles like and unlike using <post_id>. It returns json error messages and data which is used to update the likes.