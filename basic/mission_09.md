# Mission 9
https://www.hackthissite.org/missions/basic/9/

- [Overview](#overview)
- [Solution](#solution)
- [Key Idea](#key-idea)

## Overview
Network Security Sam is going down with the ship - he's determined to keep
obscuring the password file, no matter how many times people manage to recover
it. This time the file is saved in
/var/www/hackthissite.org/html/missions/basic/9/.  

In the last level, however, in my attempt to limit people to using server side
includes to display the directory listing to level 8 only, I have mistakenly
screwed up somewhere.. there is a way to get the obscured level 9 password. See
if you can figure out how...  

This level seems a lot trickier then it actually is, and it helps to have an
understanding of how the script validates the user's input. The script finds the
first occurance of '<--', and looks to see what follows directly after it.  

## Solution
The mission description suggests the vulnerabiilty from Mission 8 is still in
play, even though there's no input box for this mission. So we still want to
list directory contents, but this time for directory /9/. So, let's go back to
Mission 8 and enter this into the script input box: `<!--#exec cmd="ls ../../9/"
-->`. This allows you to change directories over to /9/, revealing the name of
the PHP file allowing you to find the password similar to what you did in
Mission 8.  

## Key Idea
Mission 9 didn't have an input box, but like with Mission 5, the same
vulnerability was still in play because it wasn't fixed from Mission 8. The
twist was you just needed to know how to navigate the directory tree and change
your input.