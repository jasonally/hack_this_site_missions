# Mission 13
https://www.hackthissite.org/playlevel/13/

- [Overview](#overview)
- [Solution](#solution)
  * [Details from the Site Layout](#details-from-the-site-layout)
    + [Homepage](#homepage)
    + [News](#news)
    + [Debates, Members, and Economy](#debates--members--and-economy)
    + [Newsletter](#newsletter)
    + [Mailing List](#mailing-list)
    + [Speeches](#speeches)
    + [Press Releases](#press-releases)
  * [Taking Stock of Possible Vulnerabilities](#taking-stock-of-possible-vulnerabilities)
  * [Finding Hidden Parts of the Site](#finding-hidden-parts-of-the-site)
  * [Cracking Hashes](#cracking-hashes)
    + [Finding Hidden Parts of the Site, Part 2](#finding-hidden-parts-of-the-site--part-2)
  * [Key Concepts](#key-concepts)
  * [Key Ideas](#key-ideas)

## Overview
Elbonia's Elections are coming! Help delay these elections by taking down the main competitor's site! Be careful though, you get caught, you'll be wishing you had your soap on a rope...

From: Fr0zenB1t

Message: Hey, Josh Haze (a.k.a. Fr0zenB1t) here, I REALLY need some help. As you know, I'm in with the AOE (Anarchists of Elbonia). Our mission is to thwart the upcoming elections, and at least attempt to delay them for the time being. The way we've decided would work best is if one of the main competitor's site is taken down. Even if it is down for a small amount of time, things wont go smoothly for him, and things will be delayed...

## Solution
### Details from the Site Layout
Our goal is to find a way to break into the website, presumably to knock it offline. With that in mind, take a look at the site's pages and see what stands out.

#### Homepage
The homepage and subsequent pages on the site include images from the images/ subdirectory, and navigating to it reveals a directory which has directory listing enabled. There's nothing else of value, unfortunately, but this is of note.

#### News
The [News](https://www.hackthissite.org/missions/realistic/13/news.php?month=all) page has an update from September 10th which mentions part of the site being recoded. This seems useful. Tampering with the URL and removing a month parameter also yields this results:
```
MySQL Error Reported: row "" does not exist
Error in query: "SELECT post, date FROM newsTable WHERE month =""
```

#### Debates, Members, and Economy
The [Debates](https://www.hackthissite.org/missions/realistic/13/debates.php), [Members](https://www.hackthissite.org/missions/realistic/13/members.php), and [Economy](https://www.hackthissite.org/missions/realistic/13/economy.php) pages seem pretty static. Let's move on for now.

#### Newsletter
[This page](https://www.hackthissite.org/missions/realistic/13/newsletter.php) mentions starting anew with newsletters. There's a note that to order a newsletter you'll need to have a hidden login URL and password. This suggests there are hidden parts of the site which aren't meant for regular users to access.

#### Mailing List
The [Mailing List](https://www.hackthissite.org/missions/realistic/13/mailinglist.php) page has a form to sign up for upcoming events. Entering a valid-looking address like hello@hello.com and clicking add sends a POST request to https://www.hackthissite.org/missions/realistic/13/addmail.php, which yields this message:
```
"hello@hello.com" could not be added to "emails_table"
Please Contact Administrator
```

#### Speeches
[This page](https://www.hackthissite.org/missions/realistic/13/speeches.php) gives you the option of picking Speech option 1 and clicking View, which sends a POST request to https://www.hackthissite.org/missions/realistic/13/speeches2.php. But something funny happens when you navigate directly to speeches2.php. You get six warning messages with some weird stack trace messages. We'll come back to this.

#### Press Releases
The [Press Releases](https://www.hackthissite.org/missions/realistic/13/press.php) page has similar error handling as the Speeches page. The pulldown box lets you pick from three options which sends a POST request to https://www.hackthissite.org/missions/realistic/13/readpress.php. If you navigate to readpress.php directly, you get a similarly ugly error message after a MySQL error message referring to a press_table table.

### Taking Stock of Possible Vulnerabilities
Let's review what we've noticed about the site:
* A table called newsTable stores posts on the News page. It has two columns, post and date, as well as probably a third column with IDs.
* The Newsletter page mentions there are hidden parts of the site.
* The emails_table table contains email addresses from people signing up for the mailing list.
* The Speeches and Press Releases pages can trigger errors with lengthy stack traces.
* The Press Releases functionality also involves a table called press_table.

My initial thought was maybe it could be useful to get the email addresses in the emails_table. I tried using the News page to trigger a UNION attack on the emails_table, similar to what we did in [Realistic Mission 4](https://github.com/jasonally/hack_this_site_missions/blob/master/realistic/mission_04.md), but it didn't work. That pushed me to go back to the Speeches and Press Releases pages, trigger the errors, and look through the stack traces.

### Finding Hidden Parts of the Site
The error we get from navigating to https://www.hackthissite.org/missions/realistic/13/readpress.php includes this line:
```
$in = "GET /speeches/passwords/" . md5('Speeches') . "";
```

This implies there's a directory path at https://www.hackthissite.org/missions/realistic/13/speeches/passwords. If you navigate to that URL you get a page which says `Subdir`. We don't get a 404 error, so maybe we're onto something. But look again at the line above. /speeches/passwords wasn't the full path. There's a directory within passwords/ which is apparently the MD5 hash of 'Speeches'. The MD5 hash of Speeches is 7e40c181f9221f9c613adf8bb8136ea8. Try navigating to https://www.hackthissite.org/missions/realistic/13/speeches/passwords/7e40c181f9221f9c613adf8bb8136ea8/.

### Cracking Hashes
The directory we've just discovered has a file, passwords.fip, which contains what looks like a hashed username-password combo. We've just cracked one MD5 hash so perhaps these are MD5 hashes, too. Go to a password hash checker website like [CrackStation](https://crackstation.net/) or fire up your password cracking software of choice. You'll find the hash pair decrypts to moni1 as the username, admin as the password.

We've got our login credentials, but where do we use it?

### Finding Hidden Parts of the Site, Part 2
The homepage included a thank you message to the site admins, so maybe there's an admin page at https://www.hackthissite.org/missions/realistic/13/admin. If you go there, sure enough, there's a login page. Except our username and password credentials don't seem to work. Maybe there's another login page we should be looking for.

Go back to the stack trace at https://www.hackthissite.org/missions/realistic/13/speeches2.php and look at it in more detail. Two of the error messages include this line:
```
C:\Program Files\Apache Group\Apache2\ENRP\21232f297a57a5a743894a0e4a801fc3\speches.php
```

The 21232f297a57a5a743894a0e4a801fc3 string looks like another MD5 hash. It decrypts to admin. Maybe the real admin page is actually https://www.hackthissite.org/missions/realistic/13/21232f297a57a5a743894a0e4a801fc3. If we try navigating to that URL it indeed leads to another login page, our decrypted credentials work, and it completes the mission.

### Key Concepts
Directory traversal\
Password cracking

### Key Ideas
This mission referenced several ideas we've seen in other missions. We saw table names, making sense of error messages and source code, and intuition about a site's layout. But the detail which stood out to me the most was this site's attempt at [security through obscurity](https://en.wikipedia.org/wiki/Security_through_obscurity). The site admins thought obfuscating the location of sensitive directories would be enough to keep the site secure. They were wrong. Nobody should rely on that as their primary means of keeping a system safe.

[Elbonia](https://en.wikipedia.org/wiki/Dilbert#Elbonia) is also a reference to a fictional country from the Dilbert universe.

