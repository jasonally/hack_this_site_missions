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

# Mission 1
https://www.hackthissite.org/missions/javascript/1/

## Overview
faith is learning Javascript, the only thing that is protecting her from hackers
is luck.

## Solution
Check the page source. For me, starting on Line 144 there's this code:  
```
function check(x)
{  
        if (x == "cookies")  
        {  
                        alert("win!");  
                        window.location += "?lvl_password="+x;  
        } else {  
                        alert("Fail D:");  
	}  
} 
```

Then on Line 162 there's this code:  
`<button onclick="javascript:check(document.getElementById('pass').value)">Check
Password</button>`

When a user enters a password and clicks Check Password, JavaScript calls the
check() function and passes the user input to it. check() then looks to see if
the input = "cookies", so that's your answer. Enter cookies as your password to
complete the challenge.

## Key Idea
Like with HTML, check all the pieces of JavaScript code on a page or site.
Sometimes what you're looking for is hiding in plain sight.

# Mission 2
https://www.hackthissite.org/missions/javascript/2/

## Overview
faith had made a redirect script and logout with javascript to keep hackers
away.

## Solution
Clicking the Take this challenge! link leads you to
https://www.hackthissite.org/missions/javascript/2/, which redirects to
https://www.hackthissite.org/missions/javascript/2/fail.php with a message: You
didn't disable javascript!

D'oh! The mission objective is you literally have to disable JavaScript. I
followed the instructions
[here](https://developers.google.com/web/tools/chrome-devtools/command-menu) to
use Chrome's DevTools Command Menu to disable JavaScript. Once it's disabled,
navigate back to https://www.hackthissite.org/missions/javascript/2/.

Now, no redirection occurs. And there's a link: Click here to win. Click it and
you've completed the mission.

## Key Idea
You don't always have to enter a specific input to get the behavior you're
looking for. Sometimes you might be able to just switch something off to get
unexpected results, in this case switching off JavaScript.

# Mission 3
https://www.hackthissite.org/missions/javascript/3/

## Overview
faith is going to test your math skills and your javascript operations.

## Solution
The premise of this mission is you enter an input and it gets passed to check(),
much like Mission 1. check() this time looks to see if the length of your input
== moo, moo being a variable defined in the JavaScript code.

If you look at how moo gets defined, it's based on variables bar and foo and
equals some value. This mission seems to require you to do some math to figure
out what moo equals, but I took an easier approach. I copied the JavaScript code
into Chrome's DevTools Console, hit enter, then checked the value of moo. moo =
14. So, enter any password input of 14 characters and you're done.

## Key Idea
If you hit some confusing code and you don't know how it works, try running it
somewhere, like your browser's developer tools console.