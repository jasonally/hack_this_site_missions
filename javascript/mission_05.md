# Mission 5
https://www.hackthissite.org/missions/javascript/5/

- [Overview](#overview)
- [Solution](#solution)
- [Key Idea](#key-idea)

## Overview
Uhm, faith spelled runescape wrong?

## Solution
Look at the code and you'll see check() compares the user input to moo, moo
being a variable defined as `unescape('%69%6C%6F%76%65%6D%6F%6F')`. If you run
`unescape('%69%6C%6F%76%65%6D%6F%6F')` in your DevTools Console, you'll see it
resolves to ilovemoo, which is your answer.

## Key Idea
Websites sometimes convert URIs into hexadecimal notation to prevent errors with
handling ASCII and Unicode characters. JavaScript's
[unescape()](https://www.w3schools.com/jsref/jsref_unescape.asp) function takes
text in hexadecimal notation (as indicated by the % sign followed by two
characters), and converts it back into the characters the hexadecimal notation
represents. The [escape()](https://www.w3schools.com/jsref/jsref_escape.asp)
function is sort of the converse, as it takes in text and replaces certain
characters with hexadecimal escape sequences.

For more on what hexadecimal notation looks like for ASCII characters, [this
chart](https://www.ibm.com/support/knowledgecenter/en/ssw_aix_72/network/conversion_table.html)
is helpful. It's also worth noting unescape() and escape() have been deprecated
in JavaScript and developers should use functions like
[decodeURI()](https://www.w3schools.com/jsref/jsref_decodeuri.asp),
[decodeURIComponent()](https://www.w3schools.com/jsref/jsref_decodeuricomponent.asp),
[encodeURI()](https://www.w3schools.com/jsref/jsref_encodeuri.asp), or
[encodeURIComponent()](https://www.w3schools.com/jsref/jsref_encodeuricomponent.asp)
instead.

I also found [this Quora
answer](https://www.quora.com/What-is-the-difference-between-a-URL-and-a-URI) on
the differences between URLs and URIs helpful. All URLs are URIs, but not all
URIs are URLs.