###########################
# [ x ] Create a repo called 'Blogz'
# [ x ]  Create new MySQL Database
# [ x ] create new users with database.**
# Will need the following templates
# [ x ] index.thml
# [ x ] singup.html
# [ x ] login.html
# [ x ] singleUser.html WIll display only post by 1 given author,
#       it will be used when we dynamically generate a page using a GET request with a user query
#       parameter on the /blog route (similar to how we dynamically generated individual blog entry
#       pages in the last assignment).
# Route Handlers
# [ x ] singup
# [ x ] login
#       [ x ] If login sucess redirect to '/newpost' store username to session
#       [ x ] if wrong show error  message of why(wrong password/currently not registered) and redirected #               to '/login'
# [ x ] index
# [ x ] logout that will redirect user to '/blog'
# [ x ]  Create 'User'  Class