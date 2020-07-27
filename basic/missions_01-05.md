- [Mission 1](#mission-1)
  * [Overview](#overview)
  * [Solution](#solution)
  * [Key Idea](#key-idea)
- [Mission 2](#mission-2)
  * [Overview](#overview-1)
  * [Solution](#solution-1)
  * [Key Idea](#key-idea-1)
- [Mission 3](#mission-3)
  * [Overview](#overview-2)
  * [Solution](#solution-2)
  * [Key Idea](#key-idea-2)
- [Mission 4](#mission-4)
  * [Overview](#overview-3)
  * [Solution](#solution-3)
  * [Key Idea](#key-idea-3)
- [Mission 5](#mission-5)
  * [Overview](#overview-4)
  * [Solution](#solution-4)
  * [Key Idea](#key-idea-4)

# Mission 1
https://www.hackthissite.org/missions/basic/1/

## Overview
This level is what we call "The Idiot Test", if you can't complete it, don't
give up on learning all you can, but, don't go begging to someone else for the
answer, thats one way to get you hated/made fun of. Enter the password and you
can continue.

## Solution
Check the page source. Above the password form I see this comment:  
`<!-- the first few levels are extremely easy: password is a13fe647 -->`  
The password might be different for you. But enter whatever text you see and
submit.

## Key Idea
Check the raw HTML and see what you can learn.

# Mission 2
https://www.hackthissite.org/missions/basic/2/

## Overview
Network Security Sam set up a password protection script. He made it load the
real password from an unencrypted text file and compare it to the password the
user enters. However, he neglected to upload the password file...

## Solution
If Sam didn't upload the password file, that means you just have to enter
nothing in the password form and submit. Sam using an unencrypted text file is
also a problem because anyone can read the password if they can find the file,
but for the purposes of this mission it's irrelevant if Sam didn't upload the
file.

## Key Idea
Try entering random inputs (or in this case, try entering no input). Entering
random inputs by itself won't necessarily help you find a solution, but it'll
help you better understand what's happening on the backend. That could then
allow you to craft a more precise input to get the result you're looking for.

# Mission 3
https://www.hackthissite.org/missions/basic/3/

## Overview
This time Network Security Sam remembered to upload the password file, but
there were deeper problems than that.

## Solution
Like Mission 1, start by checking the page source. The HTML for the password
form includes this line:  
`<input type="hidden" name="file" value="password.php" />`.  
Try navigating to https://www.hackthissite.org/missions/basic/3/password.php.
When I go there I see the password as a plain-text string. Go back to the
previous page, enter the password, and submit.

## Key Idea
This is exactly the issue highlighted in Mission 2, but in that mission it was
irrelevant because Sam didn't upload the password file. If you can discover
pusedo-hidden pages and files by checking the raw HTML, try accessing them and
see what you can learn.

# Mission 4
https://www.hackthissite.org/missions/basic/4/

## Overview
This time Sam hardcoded the password into the script. However, the password is
long and complex, and Sam is often forgetful. So he wrote a script that would
email his password to him automatically in case he forgot. Here is the script

[form box]

## Solution
If you click the 'Send password to Sam' button, you'll see it indeed sends a
password reminder email. Next, check the page source. There's this line in the
HTML:  
`<input type="hidden" name="to" value="sam@hackthissite.org" />`  
What if you change the email address to your own (or more specifically, the
email address you used to sign up for Hack this Site)? Edit the value
attribute using Developer Tools and click the password reset button. The
password should be emailed to you.

## Key Idea
Missions 1 and 3 were about what you can learn from checking the raw HTML, but
this mission goes one step further by encouraging you to try manipulating the
raw HTML. Sometimes it will actually work.

# Mission 5
https://www.hackthissite.org/missions/basic/5/

## Overview
Sam has gotten wise to all the people who wrote their own forms to get the
password. Rather than actually learn the password, he decided to make his
email program a little more secure.

## Solution
Trying to make the email program more secure instead of fixing the actual
problem on the site means the solution to Mission 4 also works in this
mission. Follow the same steps to edit the email address value using Developer
Tools and send yourself the password.

## Key Idea
This mission was a bit of a misdirection. If the fundamental vulnerability
hasn't been fixed, what worked in the past might still work now.