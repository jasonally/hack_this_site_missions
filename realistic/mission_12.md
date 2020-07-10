# Mission 12
https://www.hackthissite.org/playlevel/12/

- [Overview](#overview)
- [Solution](#solution)
  * [Details from the Site Layout](#details-from-the-site-layout)
  * [Finding the Admin Panel](#finding-the-admin-panel)
  * [Local File Intrusion Via the Guestbook](#local-file-intrusion-via-the-guestbook)
  * [Clearing the Proxy Filter](#clearing-the-proxy-filter)
- [Key Concepts](#key-concepts)
- [Key Ideas](#key-ideas)
  * [Server Operating Systems](#server-operating-systems)
  * [toastytech and Browser Market Share](#toastytech-and-browser-market-share)
  * [CGI](#cgi)
  * [URI Schemes](#uri-schemes)

## Overview
Schools are supposed to prepare students for the outside world, but how can they do this if students are kept from everything by overly-protective administrators? Clear the blocked site list and help fight censorship in public schools.

From: OutThere

Message: Hey it's OutThere from hackthissite.org. I've run into a problem that I can't seem to solve. As you may know, I go to Heartland High School, and our school put everything on the internet a few years ago. This was great at first, but then this really uptight guy, Jason Bardus, got a job as a computer teacher. He set up this overly restrictive web proxy and made it so that school computers could only connect to the district site. He hates people who know more than him, so he blocked all these hacker sites, open source websites, and he even blocked google! He is really paranoid about security, but I don't think he really knows what he is doing. The district site is here, and it runs on some crappy Windows 95 machine, if that helps. Can you clear the list of blocked pages by getting admin access? Please help me out, because information should be for everyone.

## Solution
### Details from the Site Layout
The mission overview provides us with two useful details. First, we know the name of the computer teacher who set up the web proxy we're trying to clear. Second, we're dealing with a web server running Windows 95.

After clicking into the site, the first thing I tried was the address bar in the top left corner of the page. I tried to go to https://www.google.com and sure enough, you'll get a message saying the page is blocked. That proxy really does work.

Go back to the homepage and check the other pages on the site. There's nothing particularly interesting in the Testing Scores page, but Mr. Bardus' (remember that he's the computer teacher who created the web proxy) and Mr. Englebert's pages in the Teacher Pages section lead us to the Student Work section. Joey Simons' page is the only one with a functionality which could be of interest. There's a link to sign his guestbook, which then leads to a page with a form. If we inspect the raw HTML of this form, it looks something like this:
```
<form action="../cgi-bin/guest.pl">
	<input type="hidden" name="action" value="write">
	Message: 
	<input type="text" name="text" size="50">
	<input type="submit" value="submit">
</form>
```

Type something like 'hello world' into the message box but before clicking submit, open Developer Tools and go into the Network menu.
When we click submit, you'll see our message gets passed to a URL like this:
https://www.hackthissite.org/missions/realistic/12/cgi-bin/guest.pl?action=write&text=hello+world

And then there's a redirection to a URL like this:
https://www.hackthissite.org/missions/realistic/12/cgi-bin/guest.pl?action=read&file=guestbook.txt

guest.pl, the Perl script which handles the guestbook functionality, appears to have both read and write permissions on files on the server (it seems the file for the guestbook, guestbook.txt, doesn't exist, but that's not relevant to our mission objective. This is...of note.

### Finding the Admin Panel
For now, let's go back to the address bar and tinker with it some more. Remember that from the mission overview we're explicitly told we're dealing with a server running Windows 95, not Linux. We need to learn more about Windows 95 server paths. A Google search for [windows 95 server path] gave me a result  [like this from toastytech](http://toastytech.com/guis/win952.html) which includes this:
```
You can also access shares directly by entering a "UNC" name. Click Start then Run, and type a path like "\\server\share\folder". And there are your files! Similarly when opening or saving a file from an application you can type in a file name like "\\server\share\folder\mydoc1", and there it is!
```

Maybe we can use the address bar to directly access files and folders on the server's hard drive. What's more, there's a URI scheme for [file](https://en.wikipedia.org/wiki/File_URI_scheme), which allows us to retrieve files from someone's own computer. This is how, for instance, you can open some text and PDF documents using your web browser. So, if the file URI scheme can help us retrieve files, and we know Windows 95 by default can allow us to access a machine's files and folders, we might have a way in.

Try using the address bar to navigate to the server's hard drive, file://C:\. It works, and now we can see the directory tree inside the server's hard drive. The one caveat is we have to keep using the address bar to navigate. The links in the directory tree itself don't seem to work.

Navigate to file://C:\WEB. We're blocked from accessing the Perl and cgi-bin directories, but we can access \HTML by navigating to file://C:\WEB\HTML. Inside are files for the homepage and images we saw on the homepage, as well as a file called heartlandadminpanel.html. We already know the .html homepage file and the images are saved directly off the root directory, so it stands to reason heartlandadminpanel.html is saved there, too. Try navigating to https://www.hackthissite.org/missions/realistic/12/heartlandadminpanel.html in your browser.

The page loads and we've got ourselves a login page. It’s likely the username is jbardus, jasonbardus, bardus, or some variant of the computer teacher's name. But we don't know the password. Common passwords don't work, either.

If you check the raw HTML of this page, the login form submits a GET request to a script located at cgi-bin/heartlandadminpanel.pl. That this form triggers a GET request is a major security problem in its own right, as Compare GET vs. POST on [this page](https://www.w3schools.com/tags/ref_httpmethods.asp) describes. When you enter in a username and password and click submit, the strings you entered in are clearly visible in plain text in the URL you get redirected to. Your browser will save this URL in its history, meaning anyone with access to your computer or browser could check the history and get your account credentials. But this isn't even the detail which is most helpful to us. That distinction goes to the detail that this form performs a check against a script located at cgi-bin/heartlandadminpanel.pl. We previously found a spot on the site where there seems to be read and write privileges to server files. Let's go back to that.

### Local File Intrusion Via the Guestbook
When we were examining Joey Simons' guestbook functionality, we found this URL by following the network activity:
https://www.hackthissite.org/missions/realistic/12/cgi-bin/guest.pl?action=read&file=guestbook.txt

Change the URL so instead of reading from guestbook.txt, we're reading from the new script we've discovered, heartlandadminpanel.pl:
https://www.hackthissite.org/missions/realistic/12/cgi-bin/guest.pl?action=read&file=heartlandadminpanel.pl

The page loads and we get a weird UI which seems broken because of the hacky way we're accessing it. View the raw HTML of this page, however, and the contents of this Perl script become much clearer. Of note is this snippet which is referenced twice in an if-elsif statement:\
`/^username=jbardus&password=heartlandnetworkadministrator&blocked=/`

That's our username and password. Go back to the admin panel at https://www.hackthissite.org/missions/realistic/12/heartlandadminpanel.html and log in using those credentials.

### Clearing the Proxy Filter
Once you get here, the rest of the mission is easy. The admin panel loads properly and we can see the list of keywords which feeds into the proxy filter. Click clear all to delete the list and you're done.

## Key Concepts
URI schemes\
Directory traversal\
Local file intrusion\

## Key Ideas
### Server Operating Systems
Missions until now mostly involved Unix-based servers. This was the first mission which explicitly involved us working with a Windows server. According to w3techs.com, to the extent we can track website operating systems it's believed [Unix-based operating systems comprise about 70% of the web](https://w3techs.com/technologies/overview/operating_system), with Windows comprising almost all of the rest. Even though Windows servers appear to comprise a minority of servers connected to the internet today, it's important to know the basics of how to navigate their file systems. Even though this example of using Windows 95 is woefully out of date now, more modern Windows systems [continue to use the same file path syntax](https://docs.microsoft.com/en-us/dotnet/standard/io/file-path-formats).

### toastytech and Browser Market Share
Researching Windows server file paths led me to [toastytech](http://toastytech.com/), a corner of the web known for its gallery of GUIs from the operating systems of yesteryear. There's also a section dedicated to how Internet Explorer is evil. This took me down the rabbit hole of when Chrome became the most popular web browser. The transition [happened around August 2012](https://www.w3counter.com/globalstats.php?year=2012&month=8), no doubt in part because of the rise of Android in the mobile market. As of June 2020 Chrome has [63% market share](https://www.w3counter.com/globalstats.php?year=2020&month=6).

### CGI
I've seen cgi-bin in the URL structure of sites plenty of times but never knew much about the underlying technology until now. [This blog post](https://medium.com/adobetech/2017-will-be-the-year-of-the-cgi-bin-err-serverless-f5d99671bc99) provides context. Common Gateway Interface, or CGI, was an early web tech which helped get the web tech industry up and running. But over time issues with performance, security, and scalability pushed developers to build new technologies. Indeed, the security issues with CGI were a part of how we solved this mission. The local file intrusion vulnerability allowed us to abuse one functionality to access a completely unrelated script, thereby helping us break into the admin panel and clear the web proxy filter list.

### URI Schemes
http and https are likely the most widely known URI schemes on the web, but there are others out there. This mission introduced us to the file URI scheme. Other common URI schemes include [ftp](https://tools.ietf.org/html/rfc7151) for transferring files between a client and server, [mailto](https://tools.ietf.org/html/rfc6068) for email addresses, [tel:](https://tools.ietf.org/html/rfc5341) for phone numbers, and [view-source](https://tools.ietf.org/html/draft-yevstifeyev-view-source-uri-01) for viewing the source code of a URI. There's even a satirical URI scheme, [coffee](https://tools.ietf.org/html/rfc7168), which was an April Fool's Day joke from 1998 and 2014. There's even an associated HTTP response code, 418.
