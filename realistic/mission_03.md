# Mission 3
https://www.hackthissite.org/playlevel/3/

## Overview
A little girl made a website to post poetry related to peace and understanding. American fascists have hacked this website replacing it with Hitler-esque propaganda. Can you repair the website?

From: PeacePoetry

Message: I run this website where people can read and submit peace-related poetry. I am doing this out of good will towards others, and I don't see why I would be making enemies out of this, but some real ass hole hacked my website posting a bunch of ignorant aggressive propaganda on the front page. And I made that website a while ago, and I no longer have access to it. Do you think you can hack in and change it back? Please? Oh, and bonus points if you message me the name of the bastard who did this!

## Solution
Think about the objective of this mission: we want to restore the site to its state before getting hacked. This means:
* We need to find what the site looked like before getting hacked. In other words, we need the HTML, because web pages are in HTML.
* Once we find the HTML of what the site looked like, we'll need to find a mechanism to get that HTML back onto the site.
* It likely follows that if we can find a way to change the code on part of the site, that's probably the same mechanism the hackers used to deface the site in the first place.

Click into the mission site and we're taken to the defaced page (the mid-2000s bent to the hacked content seems so...idyllic, looking back on it now, in 2020). Check the raw HTML to see if there's anything we can learn, and sure enough, at the very bottom (you need to scroll all the way to the bottom), there's this comment:  
`<!--Note to the webmasterThis website has been hacked, but not totally destroyed. The old website is still up. I simply copied the old index.html file to oldindex.html and remade this one. Sorry about the inconvenience.-->`

This tells us:
* The old index page is still up. That's where we can get the code of what the site looked like before getting hacked.
* The hacker copied the original index.html file to oldindex.html and then put the defaced content on index.html. Seems like whatever vulnerability is at play allowed the hacker to manipulate multiple files, not just index.html.

Searching queries like [website edit files vulnerability] led me to references of path traversal and directory traversal. This led me [here](https://portswigger.net/web-security/file-path-traversal) and then [here](https://owasp.org/www-community/attacks/Path_Traversal). This seems important to the end solution. This type of attack involves being able to access files and directories across a site, similar to what we see happening in this mission.

Go back to the other detail we discovered, that the old index page is available at oldindex.html. Try accessing it by going to https://www.hackthissite.org/missions/realistic/3/oldindex.html. This is the main page of the site before it was hacked, complete with the raw HTML we want to put back on the real index.html page. We can simply copy the raw HTML if needed.

The old index page has two links, one to an area to read submitted poems (https://www.hackthissite.org/missions/realistic/3/readpoems.php) and one to submit a new poem (https://www.hackthissite.org/missions/realistic/3/submitpoems.php). If you click any of the poems from https://www.hackthissite.org/missions/realistic/3/readpoems.php, like https://www.hackthissite.org/missions/realistic/3/readpoem.php?name=Hacker, you'll see the resulting URL contains a query parameter (the name=Hacker) part. This seems to plug directly into the site's file system API, exactly the sort of thing the PortSwigger article cautions against.

Finally, from https://www.hackthissite.org/missions/realistic/3/submitpoems.php you'll see there's a way for anyone to submit a poem to the site. There's also this message:  
`Note: Poems will be stored online immediately but will not be listed on the main poetry page until it has a chance to be looked at.`
Again, this sort of immediate storage implies there isn't any validation happening first.

Putting it all together, we have our framework for a solution:
* We have the code we need to restore the old HTML on the index.html page.
* The site has open entry points into the file system API, based on what we see in URLs like https://www.hackthissite.org/missions/realistic/3/readpoem.php?name=Hacker.
* Per the note on https://www.hackthissite.org/missions/realistic/3/submitpoems.php, the site stores user inputs immediately, without any validation check.

Now, visit https://www.hackthissite.org/missions/realistic/3/submitpoems.php. Enter `../index.html` as the Name of poem, which I picked up from the PortSwigger article about path traversal. Paste the raw HTML from https://www.hackthissite.org/missions/realistic/3/oldindex.html in the Poem box. Press add poem, and you're done. You’ll have successfully rewritten the index.html file with the original contents, and as you can see, this is exactly what the hackers did to deface the site in the first place. Now, if only we could help PeacePoetry get access to the site to fix this underlying problem.

## Key Concept
Path traversal

## Key Ideas
Path traversal is probably how a lot of hackers deface legitimate websites as well as [access files](https://hackernoon.com/the-power-of-directory-traversal-93e8dfd608ef) webmasters otherwise intend to keep hidden. The easiest way to prevent this type of attack is to prevent users from directly accessing the file system API, like in the way we just did. But if you can't cut off this access entirely, PortSwigger suggested at least two different types of validation, such as limiting the types of characters users can enter in input areas (e.g., limit to alphanumeric characters), or making sure backend commands stay within a specific set of allowable paths.
