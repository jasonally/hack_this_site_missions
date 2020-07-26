# Mission 6
https://www.hackthissite.org/missions/javascript/6/

- [Overview](#overview)
- [Solution](#solution)
- [Key Idea](#key-idea)

## Overview
Fiftysixer decided to try his hand at javascript!\
All was going well until he realized that he forgot to remove the unused code, 
which resulted in a confusing mess.\
He didn't mind, in fact, he did his best to make it even MORE confusing!

## Solution
This mission has another misdirection, because you think the password checking
code involves something visible in the page source. But not quite. If you check
the button code, you'll see that onclick JavaScript calls checkpass(). But
there's no checkpass() in fiftysixer's code. Instead, there's a reference to a
completely separate JavaScript file, checkpass.js. For me this reference is on
Line 142.

Let's take a look at checkpass.js by navigating to
https://www.hackthissite.org/missions/javascript/6/checkpass.js. Here we see
checkpass() defined for real. The password check is defined by `pass == rawr+"
"+moo`. The variable rawr equals moo and the variable moo equals pwns. Putting
the pieces together, the solution is the string 'moo pwns'. Enter that as your
answer.

## Key Idea
Don't be led astray by extra code which isn't even used. It's also good practice
to define JavaScript code in a separate file, so be sure to check for any
additional scripts which are hosted elsewhere on the site (or elsewhere on the
web, for that matter).