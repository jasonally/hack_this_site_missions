# Mission 14
https://www.hackthissite.org/playlevel/14/

- [Overview](#overview)
- [Solution](#solution)
  * [Properly Solving This Mission in the 2020s Isn't Possible](#properly-solving-this-mission-in-the-2020s-isnt-possible)
  * [Details from the Site Layout](#details-from-the-site-layout)
  * [Functionalities Vulnerable to SQL Injection](#functionalities-vulnerable-to-sql-injection)
  * [Using a Null Byte Input to List Directory Contents](#using-a-null-byte-input-to-list-directory-contents)
  * [Using a Null Byte Input to Read Files](#using-a-null-byte-input-to-read-files)
  * [Bypassing Security Privileges](#bypassing-security-privileges)
  * [Logging into the Admin Account](#logging-into-the-admin-account)
- [Key Concepts](#key-concepts)
- [Key Ideas](#key-ideas)
  * [Hints About Backend Scripts](#hints-about-backend-scripts)
  * [Null Byte Injection Workarounds](#null-byte-injection-workarounds)

## Overview
An internet start-up is rumoured to be selling user data and usage habits to advertisers while they claim the opposite. Hack in and get some proof.

From:

Message: You've probably heard of Yuppers Internet Solutions before. They started in 1997 and are now one of the top websites on the net. I was an intern at Yuppers for a time, but quit when I learned that the admins were selling user data and usage habits to advertisers while saying the opposite. Unfortunately, I couldn't get out of the building with any proof and don't have any high-level access. I do know, however, that much of the coding on their site was done by amateurs and is probably insecure. Can you hack in and get some proof?

## Solution
### Properly Solving This Mission in the 2020s Isn't Possible
This mission was meant to demonstrate the value of null byte attacks. The places, however, where you're supposed to use characters which resolve to null bytes don't seem to work anymore. It's possible the backend servers don't accept these characters anymore, but I also think there is now filtering in modern web browsers to prevent users from passing in null bytes. See [here](https://bugs.chromium.org/p/chromium/issues/detail?id=106991) for an example of a Chromium discussion and [here](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2013-0842) for a CVE report. Having said that, null byte attacks do seem to be theoretically possible still, as [this report](https://samcurry.net/filling-in-the-blanks-exploiting-null-byte-buffer-overflow-for-a-40000-bounty/) demonstrates.

For the purposes of this mission I'll continue to outline what I found to be the steps to finish the mission, but note that a big part of it isn't really reproducible anymore.

### Details from the Site Layout
The mission site has the look and feel of what Yahoo looked like in the late 1990s. I guess this mission was made before Google superseded Yahoo as the dominant search engine. If you click through the pages you'll see basic versions of what a search engine, even in the 2020s, offers: results for web search, news, and finance, and functionalities for email, webpage development, and connecting with other people. 

The mission solution likely involves some way of getting admin access, so I thought an initial step would be to make an account, similar to what we did in [Realistic Mission 8](https://github.com/jasonally/hack_this_site_missions/blob/master/realistic/mission_08.md). I couldn't get the feature to work and I wasn't able to make an account, so I figured I would look elsewhere.

### Functionalities Vulnerable to SQL Injection
Several functionalities have pages which take in URL parameters, including the pages for search, news, and finance. Trying SQL injection inputs is an obvious first step, similar to what we did in [Realistic Mission 9](https://github.com/jasonally/hack_this_site_missions/blob/master/realistic/mission_09.md). The news URLs eventually stand out, because URLs for nonexistent news articles like https://www.hackthissite.org/missions/realistic/14/news.cgi?story=20 return a strange error message: `Failed to load 20.news`.

The backend program takes the URL, grabs whatever value you provide for story, and looks for a file containing that value and a .news suffix. This isn't a definitive article not found error message we'd expect to see, and it's a hint this can be tampered with.

What's more, trying a URL with a story value of ., like [https://www.hackthissite.org/missions/realistic/14/news.cgi?story=.](https://www.hackthissite.org/missions/realistic/14/news.cgi?story=.), gives us an even more enticing error message: `Failed to load ..news`. In normal conditions this functionality is basically loading a file. What if we could tamper with the URL to essentially tell the backend to ignore the .news part? What would happen? That's where the null byte input comes in.

### Using a Null Byte Input to List Directory Contents
A [null byte injection](http://projects.webappsec.org/w/page/13246949/Null%20Byte%20Injection) involves a user providing an input which, once decoded, resolves to a null byte. On the backend, if unfiltered, this will cause the backend system to stop processing the string containing the user input. This abrupt termination can cause unusual and unexpected behavior in the application.

The URI encoding for a null byte value is %00. What if we added that to our [https://www.hackthissite.org/missions/realistic/14/news.cgi?story=.](https://www.hackthissite.org/missions/realistic/14/news.cgi?story=.) URL to get https://www.hackthissite.org/missions/realistic/14/news.cgi?story=.%00? We'd be telling the backend to stop processing the script immediately and ignore the .news part. Wonder what we would get.

When this part of the mission still worked, navigating to our URL containing the null byte would've given us a page containing a bunch of backend code not meant for the frontend. It would look like [this](https://www.aldeid.com/w/images/5/5f/Hackthissite-14-1.png). It's tough to decipher, but this output lists the site's directory tree. This is similar to what we were able to do using a SQL injection in [insert missions].

Two files stand out: administrator.cgi and moderator.cgi. If you try accessing https://www.hackthissite.org/missions/realistic/14/adminstrator.cgi, you'll get a 404 error saying this page doesn't exist and never did. It would be more convincing if this page wasn't clearly listed in the directory tree, so if there's really a page here, we can't access it right now. Accessing https://www.hackthissite.org/missions/realistic/14/moderator.cgi, meanwhile, takes us to a form which requires us to provide a moderator ID. This is promising, and clearly something ordinary Yuppers users shouldn't be able to access, but we don't know how to proceed. If only there was more we could learn about this moderator.cgi script.

### Using a Null Byte Input to Read Files
We already used a null byte input to manipulate https://www.hackthissite.org/missions/realistic/14/news.cgi?story= to list directory contents. Can we use it to display file contents? Yes – at least back when the mission worked properly.

All we had to do was try accessing https://www.hackthissite.org/missions/realistic/14/news.cgi?story=moderator.cgi%00. Given what we've discovered already about this site's vulnerability to null byte inputs, it's not hard to imagine what happened on the backend. In short, by using the null byte input to terminate the string processing, we're preventing the backend from affixing .news to the end of our moderator.cgi input. This would cause the backend to literally read the contents of moderator.cgi and print its contents to the frontend. The result would be something like [this](https://www.aldeid.com/w/images/8/84/Hackthissite-14-3.png) and [this](https://www.aldeid.com/wiki/File:Hackthissite-14-4.png).

### Bypassing Security Privileges
Like with [Realistic Mission 13](https://github.com/jasonally/hack_this_site_missions/blob/master/realistic/mission_13.md), we've would've had to do some parsing of code and error messages. There would be a block of code which really stood out:
```
if (isadmin($ret[0]))
{
print "Admin Account
";
}
```

isadmin is a value associated with admin accounts, one of which we're trying to identify and access. Maybe it's something we can spoof on the moderator lookup page. If we go back to https://www.hackthissite.org/missions/realistic/14/moderator.cgi, enter isadmin into the search box, and select log in, it takes us to Yuppers' moderator panel.

The moderator panel allows us to view account info for a given account username, or email traffic for a given email address. But it turns out there's a deceptively simple flaw with the account info lookup. Entering * is the equivalent of a SELECT * SQL statement on the backend, and will list info for all admin accounts. Enter * in the View Account Info box, click submit, and there's our admin username and password information we need.

### Logging into the Admin Account
The last part of this mission is easy. Navigate to the Yuppers login page at https://www.hackthissite.org/missions/realistic/14/login.html, log in using the username and password we've just obtained, and you're taken to https://www.hackthissite.org/missions/realistic/14/webpermit/login.cgi. The page now has a link to the administrator panel at https://www.hackthissite.org/missions/realistic/14/administrator.cgi, and going there completes the mission.

## Key Concepts
SQL injection, specifically null byte injection

## Key Ideas
### Hints About Backend Scripts
Like with several realistic missions, the first key to finding a vulnerable part of the site was getting an unexpectedly helpful error message. In this mission, it was finding out the news functionality loaded files with a .news suffix. This provided a clue as to how we might be able to get the site to behave outside of its intended purpose by bypassing this part of the backend code. We needed the right tool to do this, however, which in the past was using the null byte injection.

### Usefulness of Null Byte Injections
You can still find working null byte injection vulnerabilities in web applications, even if their existence has diminished throughout the 2010s. For instance, PHP 5.3.4 fixed [a major null byte injection bug](https://bugs.php.net/bug.php?id=39863), which was released in December 2010. 

But the idea of what the null byte injection in this mission helped us accomplish is worth pondering. In this mission, it helped us find an admin account and gain access to it. That idea still lives on though other types of attacks, some of which didn't even exist in the early 2000s. For instance, at the time of this writing, less than a week ago there was a major attack against Twitter. How attackers did what they did is still under investigation, but [SIM swapping](https://en.wikipedia.org/wiki/SIM_swap_scam) may [have been a factor](https://krebsonsecurity.com/2020/07/whos-behind-wednesdays-epic-twitter-hack/) to help the attackers get admin access. 
