'''
    This file is a library for the scrapers. It is made to make string
    manipulation as easy as possible. Some functions may be redundant for
    consistency.
'''

from urllib import request, parse

############################### STRING FUNCTIONS ###############################

'''
    Converts the string to upper case
'''
def uppercase(s):
    return str(s).upper()

'''
    Converts the string to lower case
'''
def lowercase(s):
    return str(s).lower()

'''
    Returns whether or not the first string contains the second string
'''
def contains(s1, s2):
    return (s1 in s2)

'''
    Returns the string before the first or last instance of the given delimiter
'''
def before(s, delimiter, first = None, last = None):
    # first is the default
    if last is None:
        return s[:s.index(delimiter)]

    # if last is set to anything, return that instead
    return s[:s.rindex(delimiter)]

'''
    Returns the string after the first or last instance of the given delimiter
'''
def after(s, delimiter, first = None, last = None):
    # first is the default
    if last is None:
        return s[s.index(delimiter) + len(delimiter):]

    # if last is set to anything, return that instead
    return s[s.rindex(delimiter) + 1:]

'''
    Splits string into a list at the delimiter, with an optional maximum number of splits
'''
def iterate(s, delimiter, number = -1, skip_first = False):
    split = s.split(delimiter, number)
    if skip_first:
        split.pop(0)
    return split

################################ HTTP FUNCTIONS ################################

class http:
    '''
        Sends an HTTP GET request to a URL, returns the response
    '''
    def get(url):
        return request.urlopen(url).read().decode('utf-8')

    '''
        Sends an HTTP POST request to a URL with given data, returns the response
    '''
    def post(url, data = {}):
        return request.urlopen(request.Request(data)).read().decode('utf-8')

    '''
        Converts URL parameter syntax to data
    '''
    def parse_url_params(s):
        return {k: v[0] for k, v in parse.parse_qs(s).items()}
