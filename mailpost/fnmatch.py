"""
A package that maps incoming email to HTTP requests
Mailpost version 0.0.1 alpha
(C) 2010 OTT Team
"""

"""
fnmatch.py - fork of original fnmatch
==================
.. _purpose:
Purpose of the fork
-----------------
Original fnmatch has an issue while matching escaped strings and not match
pattern in the string, just only complete match. To support in glob syntax 
same rules as we support in regex, we've decided to fork it and patch

.. _description:
Original descripition of fnmatch 
-----------------
Filename matching with shell patterns.

fnmatch(FILENAME, PATTERN) matches according to the local convention.
fnmatchcase(FILENAME, PATTERN) always takes case in account.

The functions operate by translating the pattern into a regular
expression.  They cache the compiled regular expressions for speed.

The function translate(PATTERN) returns a regular expression
corresponding to PATTERN.  (It does not compile it.)
"""
import re

__all__ = ["fnmatch","fnmatchcase","translate"]

_cache = {}

def fnmatch(name, pat):
    """
    Match name and pattern
    """
    import os
    name = os.path.normcase(name)
    pat = os.path.normcase(pat)
    return fnmatchcase(name, pat)

def fnmatchcase(name, pat):
    """
    Same to fnmatch, but with case
    """
    if not pat in _cache:
        res = translate(pat)
        _cache[pat] = re.compile(res)
    return _cache[pat].match(name) is not None

def translate(pat):
    """
    Translation of the pattern string to regex
    """
    i, n = 0, len(pat)
    res = ''
    while i < n:
        c = pat[i]
        i = i+1
        if c == '*':
            res = res + '.*'
        elif c == '?':
            res = res + '.'
        #fix to work with excaped string
        elif c == '\\' and i < n:
            c = pat[i]
            i = i+1
            res = res + re.escape(c)
        elif c == '[':
            j = i
            if j < n and pat[j] == '!':
                j = j+1
            if j < n and pat[j] == ']':
                j = j+1
            while j < n and pat[j] != ']':
                j = j+1
            if j >= n:
                res = res + '\\['
            else:
                stuff = pat[i:j].replace('\\','\\\\')
                i = j+1
                if stuff[0] == '!':
                    stuff = '^' + stuff[1:]
                elif stuff[0] == '^':
                    stuff = '\\' + stuff
                res = '%s[%s]' % (res, stuff)            
        else:
            res = res + re.escape(c)
    return res + '.*' + '\Z(?ms)'
