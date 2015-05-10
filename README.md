# pimpMyProse
Repository for pimpMyProse

# About
+ A website where you can post a Prose, allowing the online community to Pimp it. Pimps can then be upvoted or downvoted.

## Current Activity
	+ Restyle site
		+ Notification list has a very strange color scheme
		+ The list of Prose/Pimps should have alternating colors to distinguish them. The current layout of tables looks bland and uninviting
		+ Have some kind of graphic on the index page to direct users towards posting a new Prose, looking at Pimps, or just registering
		
	+ Upload alpha to Webfactional

## Haystack
+ manage.py reindex
	+ Need to do whenever changing haystack search

## To-Do
+ Haystack search not working, maybe because URL for prose put at the root
+ Should be able to show posts of only followed people
+ JQUERY scripts for upvoting/downvoting have hardcoded URL, need to change to be somehow dynamic
	+ Use the {{ STATIC_URL }} tag and pass it into the JavaScript functions using django template
+ Test notifications list for bugs
	+ Notifications list was empty on first view, but then showed on refresh. But proses were empty.
	+ Tried again: 6 notifications, clicked. List was empty, notifications icon said 0. Refreshed and the notifications could be seen, but weren't marked as new.
		+ The list of 'new' notifications is not showing, the list of already viewed notifications is fine.
+ Redirect to prose just posted, if new prose successfully created
+ For longer Prose on the front page, show ellipse and more in the preview for it on index
+ Move ranking_functions.py to its own scripts folder?
	+ Python has specific way to load .py file from a different folder
+ Reddit share link added, add facebook link
	+ Need to customize templates and views for share links. Facebook plugin needs correct url
+ Finish search page - style haystack search bar with bootstrap
+ Finish organizing profile page in general
+ Finish django tutorial, do some automated testing
	+ Reddit hot score algorithm seems to work, unit test it
	+ Confidence algorithm? http://amix.dk/blog/post/19588
+ Update admin for models
+ Auto create userProfile if none exists for user
+ Following and unfollowing needs to show number change on page from Ajax
+ Do form validation for registration with JQUERY (frontend, backend is done)
+ Pagination on index, detail, profile, notifactions, etc.
+ Ability to follow users from a Prose/Pimp page, not just profile
	+ Users can follow each other, but need to expand follow_button to work for a list. Right now, takes in a context value of either "Followed" or "Not Followed" from the profile view. Sets it to a string that says "Null" if not logged in The pimp_list would take a set.
+ Find way not to load main.js on every page 
	+base.html block above all main content, where other pages can load their own JavaScript in that block
+ Email validation

## Other Possibilities
+ Make a pimp which is the origin of pimpMyProse. Let others upvote it
+ Tag other users to pimp your prose (users you are following?)
+ Categories - ask Byron
+ Allow signup through google/facebook?
+ Have a Prose of the day, to get responses from people

## For Server
+ Need to install haystack and Whoosh (use pip)
	+ http://django-haystack.readthedocs.org/en/latest/tutorial.html