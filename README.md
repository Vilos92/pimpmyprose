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
+ Reddit hot score algorithm seems to work, unit test it
+ Confidence algorithm? http://amix.dk/blog/post/19588
+ Move ranking_functions.py to its own folder?
+ Make a pimp which is the origin of pimpMyProse. Let others upvote it
+ Reddit share link added, add facebook link
	+ Need to customize templates and views for share links. Facebook plugin needs correct url
+ Finish styling
	+ Notification color scheme is very bad
	+ Try alternating posts like twitter, rather than blankd tables
+ Finish search page - style haystack search bar with bootstrap
+ Finish organizing profile page in general
+ Categories - ask Byron
+ Finish django tutorial, do some automated testing
	+ Create batch files for testing
+ Update admin for models
+ Auto create userProfile if none exists for user
+ Following and unfollowing needs to show number change on page from Ajax
+ Do form validation for registration with JQUERY (frontend, backend is done)
+ Have a Prose of the day, to get responses from people
+ Tag other users to pimp your prose (users you are following?)
+ Pagination on index, detail, profile, notifactions, etc.
+ Need to be able to click follow on user for all Pimps/Proses. Need to be able to pass in list of 
user names to accomplish this.
+ Find way not to load main.js on every page
+ Email validation

# For Server
+ Need to install haystack and Whoosh (use pip)
	+ http://django-haystack.readthedocs.org/en/latest/tutorial.html