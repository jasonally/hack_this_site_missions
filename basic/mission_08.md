# Mission 8
https://www.hackthissite.org/missions/basic/8/

- [Overview](#overview)
- [Solution](#solution)
- [Key Idea](#key-idea)

## Overview
Sam remains confident that an obscured password file is still the best idea, but
he screwed up with the calendar program. Sam has saved the unencrypted password
file in /var/www/hackthissite.org/html/missions/basic/8/

However, Sam's young daughter Stephanie has just learned to program in PHP.
She's talented for her age, but she knows nothing about security. She recently
learned about saving files, and she wrote a script to demonstrate her ability.  

## Solution
Like with Mission 7, we're given two clues:
* The password is still in a file in the directory. The solution seems to still
involve being able to list the directory contents to find the name of the file.
* The solution involves PHP commands.  

Before this challenge I wasn't familiar with ways to abuse PHP. I tried inputs
similar to what I used to solve Mission 7, but those didn't work. I had a hunch,
however, the solution still involved something close to Mission 7's solution.
Google led me
[here](https://owasp.org/www-community/attacks/Server-Side_Includes_(SSI)_Injection),
where I learned server side includes are scripts which normally help with
rendering an HTML page containing dynamic content. The article mentions testing
characters like these in an input box to see if an SSI injection might work: `<
! # = / . " - > and [a-zA-Z0-9]`.

I tried <> in the input box and I was told my name contains eight characters.
That's not right, so I knew I was onto something. I researched more about how to
script SSI commands and found
[this](https://www.w3.org/Jigsaw/Doc/User/SSI.html#exec). `<!--#exec cmd="ls
-lsa" -->` didn't quite work either, but I got a message telling me I was on the
right track.  

`<!--#exec cmd="ls" -->` listed a bunch of .shtml files in the output. More
progress! But I realized the resulting URL was for
https://www.hackthissite.org/missions/basic/8/tmp/ugpsnhtj.shtml. I was one
directory up, since I wanted to be in
https://www.hackthissite.org/missions/basic/8/ per the mission instructions. So,
`<!--#exec cmd="ls ../" -->` moved me back up a level in the directory tree and
listed the contents there, revealing the name of a PHP file – in my case it was
au12ha39vc.php. Navigating to
https://www.hackthissite.org/missions/basic/8/au12ha39vc.php gave me my answer. 


## Key Idea
This mission builds on Mission 7 with executing UNIX commands. But knowing the
server-side programming language and how you can use it to execute UNIX commands
is important. For a server using PHP, SSIs are what you want to know more about.