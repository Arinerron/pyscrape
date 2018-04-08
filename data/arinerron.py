'''
    This file is an example scraper for arinerron.com. It will simply scrape a
    list of blog posts titles.
'''

# import the pyscrape library
import utils

# perform HTTP GET request to get the HTML content from the blog
html = utils.http.get('https://arinerron.com/blog/')

# So here's an example snippet of the contents of `html`:
#   <div id="post">
#     <div id="name"><a href="/blog/posts/2">The Title of the Blog Post</a></div>
#     <div id="date" style="user-select: none;">November 33, 2070</div><br>
#     <div id="snippet">The description is here.</div>
#   </div>
# As you can see, the name is stored inside of the div with the id "name".
# The id "name" id is defined for each blog post, so let's iterate each
# instance of it to get the name of each post

# loop code for each case of the string '<div id="name">'
for case in utils.iterate(html, '<div id="name">', skip_first = True):
    # At this point, the variable `case` will contain something similar to
    # the following for each instance of the delimiter:
    #   <a href="/blog/posts/2">The Title of the Blog Post</a></div>
    # As you can see, the blog post title is wrapped in an <a> element.
    # The problem is that the blog post URL (/blog/posts/X) appears to
    # change for each post. However, the string '">' is always preceding the
    # blog post title, therefore, all we need to do is get the string after
    # the string '">'.

    # redefine case: set it to the string after first instance of the delimiter '">'
    case = utils.after(case, '">', first = True)

    # Okay. Now, the variable `case` will contain something similar to this:
    #   The Title of the Blog Post</a></div>
    # That's great. Now we just need to remove the last part of the string
    # so that we are left with the title:
    #   The Title of the Blog Post
    # To do that, we will remove the first instance of the string '</a>'.

    # redefine case: set it to the string before the last instance of the delimiter '</a>'
    case = utils.before(case, '</a>', first = True)

    # Woopee, now `case` is equal to "The Title of the Blog Post", which is
    # exactly what we want.

    # If this were a real script, you may want to add this title to the
    # database or something, but because this is just an example, we will
    # simply print it out.

    # print out title of blog post
    print('Found blog post title: ' + case)
