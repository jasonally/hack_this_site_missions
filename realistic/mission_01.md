# Mission 1
https://www.hackthissite.org/playlevel/1/

- [Overview](#overview)
- [Solution](#solution)
- [Key Concept](#key-concept)
- [Key Idea](#key-idea)

## Overview
Your friend is being cheated out of hundreds of dollars. Help him make things
even again!

From: HeavyMetalRyan

Message: Hey man, I need a big favour from you. Remember that website I showed
you once before? Uncle Arnold's Band Review Page? Well, a long time ago I made a
$500 bet with a friend that my band would be at the top of the list by the end
of the year. Well, as you already know, two of my band members have died in a
horrendous car accident... but this ass hole still insists that the bet is on!  
I know you're good with computers and stuff, so I was wondering, is there any
way for you to hack this website and make my band on the top of the list? My
band is Raging Inferno. Thanks a lot, man!

## Solution
The underlying problem in this mission is: we need a way to dramatically improve
the rating for Raging Inferno. If you click into the mission page, you'll see
each band has a form consisting of a dropdown menu with options, each option
being a rating from 1 to 5. This is what we need to game to boost Raging
Inferno's rating.

We can manipulate the form by literally editing the values of the options. Using
your browser's developer tools, inspect the form for voting for Raging Inferno.
I see something like this:
```
<form action="v.php" method="get">
	<input type="hidden" name="PHPSESSID" value="abcaeadfc31a5c43b2534bf995c0553f" />
	<input type="hidden" name="id" value="3" />
	<select name="vote">
		<option value="1">1</option>
		<option value="2">2</option>
		<option value="3">3</option>
		<option value="4">4</option>
		<option value="5">5</option>
	</select>
	<input type="submit" value="vote!" />
</form>
```

Still in developer tools, try editing the raw HTML of one of the options. I
changed `<option value="5">5</option>` to `<option value="1000">1000</option>`
or some other high number (note that you only need to change the option value
attribute, but I chose to edit the display text, too).

Exit out of developer tools, give Raging Inferno a rating of 1000, and you're
done.

## Key Concept
HTML manipulation

## Key Idea
Directly editing HTML can let you get away with some nasty effects if there's no
backend validation. This seems like a basic thing for web developers to prevent,
however, which is probably why this mission was rated as easy.