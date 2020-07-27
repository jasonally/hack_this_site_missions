# Mission 7
https://www.hackthissite.org/missions/basic/7/

- [Overview](#overview)
- [Solution](#solution)
- [Key Idea](#key-idea)

## Overview
This time Network Security sam has saved the unencrypted level7 password in an
obscurely named file saved in this very directory. In other unrelated news, Sam
has set up a script that returns the output from the UNIX cal command. Here is
the script:\
Enter the year you wish to view and hit 'view'.  
[form box]  

## Solution
The mission description gives you two clues:
* The password is in an unencrypted file in the same directory as this mission
program. If we could figure out how to list the contents of the directory, we
should be able to find the obscurely-named file.
* We're given a hint that this mission involves UNIX commands, `ls` being one of
the most common commands you can use to list the contents of a directory.

Try opening Terminal and running the cal command. An input like `cal 2020` will
display the calendar for the year 2020. But UNIX commands can be chained
together using &&. So for instance, `cal 2020 && ls` will display the calendar
for 2020 and also list the contents of the current working directory.  

Try the same idea for this mission by typing a year followed by `&& ls`. You'll
see the calendar print out as expected, followed by the files in the directory.
I see something called `k1kh31b1n55h.php` in the directory contents. Navigate to
https://www.hackthissite.org/missions/basic/7/k1kh31b1n55h.php, and there's your
password.

## Key Idea
Many websites and computer systems are just Linux servers which can execute UNIX
commands similar to what you can do in Terminal on a personal computer. Chaining
together UNIX commands here can have similar results.