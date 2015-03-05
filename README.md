# pimpMyProse
Repository for pimpMyProse

# Currently
+ Users can follow each other, but need to expand follow_button to work for 
a list. Right now, takes in a context value of either "Followed" or "Not Followed" from
the profile view. Sets it to a string that says "Null" if not logged in The pimp_list would take a set.

# About
+ A website where you can post a Prose, allowing the online community to Pimp it.

# To-Do
+ Search
+ Ability to edit profile, finish organizing profile page in general
+ Complete nav bar
+ Categories - ask Byron
+ Show submissions by date - need general filter, pagination
+ Finish django tutorial, do some automated testing
+ Pimp notifications - upvotes scaling
+ Authenticate submissions in view - cannot be exact same as other submissions
+ Update admin for models
+ No commenting on own post
+ Use for loop with context set to pass all user ids for follow alongside pimps, since cannot use a function inside the template must use beforehand %}
+ Auto create userProfile if none exists for user
+ Following and unfollowing needs to show number change on page from Ajax
+ Do form validation for registration with JQUERY (frontend, backend is done)