# pimpMyProse
Repository for pimpMyProse

# Currently
+ Users can follow each other, but need to expand follow_button to work for 
a list. Right now, takes in a context value of either "Followed" or "Not Followed" from
the profile view. Sets it to a string that says "Null" if not logged in The pimp_list would take a set.
+ manage.py reindex
	+ Need to do whenever changing haystack search

# About
+ A website where you can post a Prose, allowing the online community to Pimp it.

# To-Do
+ Added filtering on index page for proses
	+ Need to do the same for the detail page (pimps)
+ Reddit share link added, add facebook link
	+ Need to customize templates and views for share links. Facebook plugin needs correct url
+ Finish styling
+ Finish search page - style haystack search bar with bootstrap
+ Finish organizing profile page in general
+ Categories - ask Byron
+ Show submissions by date - need general filter, pagination
+ Finish django tutorial, do some automated testing
+ Update admin for models
+ Use for loop with context set to pass all user ids for follow alongside pimps, since cannot use a function inside the template must use beforehand %}
+ Auto create userProfile if none exists for user
+ Following and unfollowing needs to show number change on page from Ajax
+ Do form validation for registration with JQUERY (frontend, backend is done)
+ Have a Prose of the day, to get responses from people
+ Tag other users to pimp your prose (users you are following?)

# For Server
+ Need to install haystack and Whoosh (use pip)
	+ http://django-haystack.readthedocs.org/en/latest/tutorial.html