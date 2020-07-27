# Mission 10
https://www.hackthissite.org/missions/basic/10/

- [Overview](#overview)
- [Solution](#solution)
- [Key Idea](#key-idea)

## Overview
This time Sam used a more temporary and "hidden" approach to authenticating
users, but he didn't think about whether or not those users knew their way
around javascript...

## Solution
Take note of the hint about JavaScript. If you open Developer Tools, try
printing the value of document.cookie from the Console. For me it looked
something like `level10_authorized=no; PHPSESSID={session ID value}`. What if we
changed the value so `level10_authorized=yes`?  

You can do this in a variety of ways. The manual way would be to simply enter
`document.cookie="level10_authorized=yes";` into the Console and run it. You can
also use the JavaScript alert() function to view and modify the cookie contents,
as seen
[here](http://www.testingsecurity.com/how-to-test/injection-vulnerabilities/Javascript-Injection).

I also have the [Edit This Cookie](http://editthiscookie.com/) extension.
Regardless of your method, change the cookie value to yes, submit the form (no
need to enter a password), and you're done.  

## Key Idea
It's pretty well known by now to prevent users from tampering with cookies, but
if you find you can tamper with them, there's a lot you can do.