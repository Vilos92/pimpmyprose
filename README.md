# pimpMyProse
Repository for pimpMyProse, a website for posting any form of prose that you would like someone to improve.

# Haystack (Search Engine) Info
+ To add new Prose to the index:
	+ ```manage.py rebuild_index```
	+ This command needs to be used whenever altering the haystack search

# To-Do
## High-Priority
+ Test notifications list for bugs
	+ Notifications list was empty on first view, but then showed on refresh. But proses were empty.
	+ Tried again: 6 notifications, clicked. List was empty, notifications icon said 0. Refreshed and the notifications could be seen, but weren't marked as new.
		+ The list of 'new' notifications is not showing, the list of already viewed notifications is fine.
+ Finish organizing profile page in general
+ Restyle site
	+ Notification list has a very strange color scheme
	+ The list of Prose/Pimps should have alternating colors to distinguish them. The current layout of tables looks bland and uninviting
	+ Have some kind of graphic on the index page to direct users towards posting a new Prose, looking at Pimps, or just registering
	+ Items must be restyled in multiple places:
		+ pimp_list_item
		+ prose_list_item
		+ pimp_notification_list
		+ main.css
			+ Remove old CSS for tables afterwords
+ Determine the additions to the django configuration necessary for the server, to make uploading new versions of pimpMyProse more simple

## Medium-Priority
+ Filter to show posts from only people you are following
+ When a new Prose is posted, redirect user to the page of their Prose instead of the index
+ Proses longer than a certain length should be shortened on the index, with ellipse at end
	+ Must click on "see full Prose" or something to this effect, which takes use to that Prose page
+ A reddit share link exists, but maybe redesign (or make custom logo)
	+ Need to customize templates and views for share links. Facebook plugin needs correct url
+ Finish search page - style haystack search bar with bootstrap
+ Finish django tutorial, do some automated testing
	+ Reddit hot score algorithm seems to work, unit test it
	+ Confidence algorithm? http://amix.dk/blog/post/19588
+ Pagination on index, detail, profile, notifactions, etc.
+ Email validation (already figured it out for EnvoyNow)


## Low-Priority
+ Ability to string a series of Prose together
	+ Useful for users who want to separate a work into sections, all to be improved
+ Use angularJS to count characters left in text box
	+ Should also consider raising the text-input limit significantly
+ jQuery scripts for upvoting/downvoting have hardcoded URL, would be better if dynamic
	+ Use the {{ STATIC_URL }} tag and pass it into the JavaScript functions using django templates
+ Move ranking_functions.py to its own scripts folder?
	+ Python has specific way to load .py file from a different folder
+ Update admin page for your new models, customize to be more effective
+ Auto create userProfile if none exists for user (primarily for superusers/admins)
+ Following and unfollowing a user on their profile page should use ajax to retrieve new amount of followers
+ Do form validation for registration with jQuery/angularJS (frontend, backend is done)
+ Ability to follow users from a Prose/Pimp page, not just profile
	+ Users can follow each other, but need to expand follow_button to work for a list. Right now, takes in a context value of either "Followed" or "Not Followed" from the profile view. Sets it to a string that says "Null" if not logged in. The pimp_list would take a set.
+ Find way not to load main.js on every page
	+ In base.html, add a new block above all main content, where other pages can load their own JavaScript in that block

## Non-Priority
+ Make a pimp which is the origin of pimpMyProse. Let others upvote it
+ Tag other users to pimp your prose (users you are following?)
+ Categories - ask Byron
+ Allow signup through google/facebook?
+ Have a Prose of the day, to get responses from people

# Installing on Server
+ Need to install haystack and Whoosh (use pip)
	+ http://django-haystack.readthedocs.org/en/latest/tutorial.html
+ Use python2.7
