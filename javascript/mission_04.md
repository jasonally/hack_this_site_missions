# Mission 4
https://www.hackthissite.org/missions/javascript/4/

- [Overview](#overview)
- [Solution](#solution)
- [Key Idea](#key-idea)

## Overview
Faith is trying to trick you... she knows that you're tired after all the math
works...

## Solution
This confused me for longer than it probably should have. Check the page source
and look at the JavaScript:
```
RawrRawr = "moo";
function check(x)
{
        "+RawrRawr+" == "hack_this_site"
	if (x == ""+RawrRawr+"")
        {
		alert("Rawr! win!");
                window.location = "../../../missions/javascript/4/?lvl_password="+x;
        } else {
		alert("Rawr, nope, try again!");
	}
}
```

The code is similar to other missions where the form input gets passed to
check() and an evaluation occurs. Copy it into your developer tools console and
run some of the lines if it's tough to visualize.

The key is `"+RawrRawr+" == "hack_this_site"` is a misdirection. It's a Boolean
comparison which evaluates to False, but it doesn't interact with the code in
any other way. So, you can ignore it. You're then left with `RawrRawr = "moo"`
and the comparison `x == ""+RawrRawr+""`.

`""+RawrRawr+""` literally means concatenate "" (an empty string) to RawrRawr
and "" (another empty string). The comparison simplifies down to just RawrRawr,
which we know equals moo, so that's our answer.

## Key Idea
Don't overthink math! Sometimes the answer isn't as tricky as it looks.