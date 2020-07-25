# Mission 15
https://www.hackthissite.org/playlevel/15/

- [Overview](#overview)
- [Solution](#solution)
  * [Details from the Site Layout](#details-from-the-site-layout)
  * [Accessing the Backup File](#accessing-the-backup-file)
    + [Downloading the File](#downloading-the-file)
    + [Peeking Inside](#peeking-inside)
    + [Cracking the Backup Using PkCrack](#cracking-the-backup-using-pkcrack)
      - [Saving a Copy of index.htm with wget](#saving-a-copy-of-indexhtm-with-wget)
      - [Downloading and Installing PkCrack](#downloading-and-installing-pkcrack)
      - [Running PkCrack](#running-pkcrack)
  * [Accessing the Internal Messages System](#accessing-the-internal-messages-system)
    + [Working Through msgshow.php and msgauth.php's Logic](#working-through-msgshowphp-and-msgauthphps-logic)
    + [Giving Ourselves admin Access](#giving-ourselves-admin-access)
  * [Accessing admin_area/](#accessing-admin-area-)
  * [Navigating the Shell](#navigating-the-shell)
  * [Buffer Overflow Attack](#buffer-overflow-attack)
- [Key Concepts](#key-concepts)
- [Key Ideas](#key-ideas)
  * [Meta Tags](#meta-tags)
  * [Getting the Source Code of Files](#getting-the-source-code-of-files)
  * [Hash Cracking](#hash-cracking)
  * [Web Shells](#web-shells)

## Overview
900 billion dollars were spent on guns this year! Now rumours are spreading that
seculas Ltd. is developing an awful laser aided weapon, and that they already
have patents pending. Please try to find out what their latest patents are
about.

From: html

Message: Hi, please help me if you are against war like me. Rumours are saying
that the seculas Ltd. company is developing an awful new laser aided weapon, and
that they already have patents pending. Please try to find out what their latest
patents are about. People say you know your shit and that you are an amazingly
good hacker. It should not be a prob for someone with your skills. What I know
is that seculas Ltd. hired a new programmer who is responsible for the server,
and he passworded everything and always with different passwords. I heard about
him, he is one the kind who locks the front door twice and leaves the back-door
open.

If you think like me please help me and fight those people that make money with
war.

## Solution
This mission is hard both because of the multiple steps and because of the
necessary tools and intuition. It requires knowledge of shell commands, the
ability to download programs and files to your own machine, and reading your way
through someone else's code. Don't forget the end goal, either: we're looking
for a way to access patent information in seculas' systems.

### Details from the Site Layout
Start with the usual recon of exploring the site. If you're observant, you'll
see at least two things in this initial set of pages:
* The [index page](https://www.hackthissite.org/missions/realistic/15/index.htm)
has [meta tags](https://www.w3schools.com/tags/tag_meta.asp). These don't
appear on the page in a browser but they're machine parsable. I think this is 
the first time meta tags like these have appeared in a realistic mission and 
the Author tag includes the name and email address for a webadmin.
* Images are saved in an images/ directory which has directory listing enabled.
The directory by itself doesn't have anything of use to us, but it's a hint,
like with other missions, additional directories we encounter might have this
feature enabled.

The real key to pushing us ahead in this mission is from the
[Jobs](https://www.hackthissite.org/missions/realistic/15/jobs.php) page.
Clicking the link to send a job application takes you to [an additional
page](https://www.hackthissite.org/missions/realistic/15/application_form.php)
and submitting the form takes you to [yet another
page](https://www.hackthissite.org/missions/realistic/15/storeapplication.php).
If you've continued to check the source for each of these pages, you'll notice
the storeapplication.php page loads a green checkbox image saved at
\_backups\_/images/ok.gif. \_backups\_ – that's a new directory to check out.

### Accessing the Backup File
#### Downloading the File
Navigate over to this new directory in your browser. There's an images/
directory containing files like the green checkbox we just saw on the
storeapplication.php page as well as a backup.zip file. Download it to your
machine and try to open it. Darn, it's password protected.

#### Peeking Inside
One thing we can do as an initial step is use command line trickery to peek
inside the archive and get a sense of what's inside. From the Terminal, change
directory over to wherever you've saved backup.zip (I saved my version of the
archive to the desktop), and run `unzip -l backup.zip`. 

You should get something like this:
```
  Length      Date    Time    Name
---------  ---------- -----   ----
        0  12-08-2004 12:55   internal_messages/
      336  12-08-2004 12:44   internal_messages/msgshow.php
      965  12-11-2004 07:02   internal_messages/msgauth.php
        0  12-05-2004 09:51   misc (files from different folders)/
     4423  12-04-2004 09:41   misc (files from different folders)/index.htm
    16860  12-05-2004 09:51   misc (files from different folders)/shell.php
---------                     -------
    22584                     6 files
```

To state the obvious: assuming this is a backup of part of the site, what we've
got inside this archive are copies of files on the site right now. It suggests
there's a directory called internal_messages/, so let's see if it's there on the
live site.

Unfortunately,
https://www.hackthissite.org/missions/realistic/15/internal_messages/ loads a
Page Not Found message. But check the network activity in your browser's
developer tools to see if that's actually what happens. When I check the
activity, this page actually returns a 403 Forbidden status. So this directory
really is there, we just can't access it via our browser. Similarly, if we try
to access
https://www.hackthissite.org/missions/realistic/15/internal_messages/msgshow.php
and
https://www.hackthissite.org/missions/realistic/15/internal_messages/msgauth.php
via our browser, we get 200 OK status codes but nothing loads on the page.

So, these files are indeed present on the site, we just can't see anything of
use through our browser. To view their source code we'll need to crack the
backup.zip file, and to do that we'll need a specific program.

#### Cracking the Backup Using PkCrack
The theory behind compressed files like backup.zip is: compression uses a
predictable algorithm to reduce the size of the files you're trying to compress.
Compression needs to be predictable so you can decompress the files (note how
this is in contrast to something like hashing, which uses a one-way algorithm
which isn't meant to be reversed). But this predictability with compressed files
makes it theoretically possible to crack open a password-protected compressed
archive. [PkCrack](https://www.unix-ag.uni-kl.de/~conrad/krypto/pkcrack.html) is
a tool to do just this, but it requires two more elemente: an uncompressed,
identical version of one file which is part of the compressed archive, plus a
compressed version of this file.

Luckily for us, we can look at the contents of backup.zip and make an important
observation: the index.htm file in the archive might be the same as the
index.htm file on the live site. We'll need to save a copy of index.htm from the
live site. But I found trying to do this in a 2020s-era browser like Chrome v.83
didn't save the file exactly the way it needs to be to work with this mission
(Chrome puts the images from index.htm in a separate folder and that's not what
we want). We can see from running `unzip -l backup.zip` that index.htm is 4423
bytes. We need the version we'll pull from the live site to be 4423 bytes, too.

##### Saving a Copy of index.htm with wget
I found [wget](https://formulae.brew.sh/formula/wget) was a useful tool to
accomplish this task (I noted in [Realistic Mission
5](https://github.com/jasonally/hack_this_site_missions/blob/master/realistic/mission_05.md)
I use [Homebrew](https://brew.sh/) on my Mac to manage packages). Once I
installed wget, I ran `wget
https://www.hackthissite.org/missions/realistic/15/index.htm` in Terminal to
download and save a copy of index.htm from the live site. If you run `ls -l` in
whatever directory you saved index.htm to, you should hopefully see this version
of the file is also 4423 bytes.

Once the download is complete, create a compressed version of the index.htm file
you just pulled from the live site.

##### Downloading and Installing PkCrack
PkCrack dates back to the early 2000s and there's a problem: the build tools the
original program uses don't play nicely with modern machines. The good news is
[there's a Github repo](https://github.com/keyunluo/pkcrack) to build PkCrack
with the modern build tool [cmake](https://formulae.brew.sh/formula/cmake).
Install cmake if you don't already have it on your machine. I also got a message
telling me to add /usr/local/opt/make/libexec/gnubin to my shell PATH for cmake
to work properly, so I did that (see
[here](https://medium.com/@jalendport/what-exactly-is-your-shell-path-2f076f02deb4)
for a primer on how to update your shell PATH).

Next, clone the Github repo onto your machine (install
[git](https://formulae.brew.sh/formula/git) too if you don't have it already).
Follow PkCrack's [build
instructions](https://github.com/keyunluo/pkcrack#build), and once that's done
we're ready to follow the [usage
instructions](https://github.com/keyunluo/pkcrack#usage) and crack our archive.

##### Running PkCrack
The command you need to run PkCrack varies depending on your current working
directory and where the other files are in relation to your current working
directory. I ran PkCrack from the Desktop/pkcrack/bin directory, meanwhile my
backup.zip, index.htm, and index.zip files were on the desktop. The command
therefore looked like: ```./pkcrack -C ../../backup.zip -c "misc (files from
different folders)/index.htm" -P ../../index.zip -p index.htm -d
../../result.zip -i -a```

It'll take a few minutes to crack the archive. I also ran into a weird situation
where my more modern 2019 laptop couldn't properly read backup.zip, and
therefore PkCrack kept failing. I'm not sure if it was specific to my machine or
what, but running PkCrack with all the prerequisites on my 2012 laptop worked as
intended.

Once the file is decrypted, go to the newly-created archive file. I saved mine
to my desktop and called it result.zip. Unzip this file, marvel at how there
isn't any password protection, and open it up.

### Accessing the Internal Messages System
#### Working Through msgshow.php and msgauth.php's Logic
All that work yielded us a folder containing two folders and four files. We
already know one of those files is index.htm but now we can view msgauth.php and
msgshow.php.

Before going further, there's an important thing to keep in mind: these files
contain the source code of the files we'll encounter on the live site. The code
can literally tell us what loopholes might exist in these files.

msgshow.php gives us a clue from the first comment: there's another page
available to us on the live site at internal_messages/internal_messages.php.
Navigate to
https://www.hackthissite.org/missions/realistic/15/internal_messages/internal_messages.php
and a message system loads. The admin username jumped out to me but no obvious
password string like admin or password works. Maybe we need to find the admin
password or figure out a way to crack it.

Go back to the msgauth.php and msgshow.php files and look for more clues. The
include statements help us see internal_messages.php calls msgshow.php, which
then calls msgauth.php. The three files are supposed to work together in normal
conditions.

Line 17 of msgauth.php has an fopen statement referring to a directory at files/
and a variable, filename. When msgshow.php calls msgauth.php, msgshow.php
defines filename on line 10 and sets it equal to msgpasswords.txt. If we try
navigating to
https://www.hackthissite.org/missions/realistic/15/internal_messages/files/ or
https://www.hackthissite.org/missions/realistic/15/internal_messages/files/msgpasswords.txt
in our browser, we get 200 OK status codes but the only text which appears is
the word Forbidden. So much for being able to directly access this directory or
file.

Go back to msgauth.php and take a closer look. Line 24 is of note:
* When msgshow.php calls msgauth.php and passes in the filename variable,
msgauth.php checks that file for the msg_username and msg_password the user
provides. 
* msg_username and msg_password is in a msg_username: msg_password format in
msgpasswords.txt. 
* We have a username we're targeting, admin.

Here's the thing which we can use to our advantage: we can submit data to
msgauth.php on our own using a JavaScript injection, independent of how
msgshow.php calls it. This gives us the ability to post a file of our choosing
to msgauth.php. Where else on this site did we see a page containing the word
admin, followed by a :, followed by a string which could pass as a password? The
Author meta tag on the index page.

#### Giving Ourselves admin Access
From any page on the site, open the Console panel in Developer Tools, and paste
in this JavaScript: `document.write('<form
action="https://www.hackthissite.org/missions/realistic/15/internal_messages/msgauth.php"
method="POST"><input name="msg_password" value="Susy Slack," type="text"><input
name="msg_username" value="admin" type="text"><input name="filename"
value="../../index.htm" type=text><input type="submit" value="send"></form>')`

This will post data to msgauth.php containing the site's index.htm file, where
the Author meta tag has the admin: Suzy Slack, text snippet which allows us to
give ourselves admin privileges. When you submit the form you should see a
message saying set admin OK. Go back to the Internal Messages page, click the
read messages button in the admin row, and you can see an unread message.

### Accessing admin_area/
The message we're now able to read tells us about another directory on the site,
admin_area/. If we go directly to
https://www.hackthissite.org/missions/realistic/15/admin_area/, we get a
Forbidden message in the browser. Like with some of the pages we've just
accessed, however, we do get a 200 OK status code. So this directory is
definitely there. But going back to our decrypted backup archive, there's one
file we haven't found on the live site just yet, and the message we just read
seems to refer to it: shell.php. Try going to
https://www.hackthissite.org/missions/realistic/15/admin_area/shell.php and a
login popup appears. Obvious inputs like admin and password don't work, and when
you click cancel, you're taken to an access denied page.

We haven't looked at shell.php from the cracked backup archive yet, but it's
time to do so now. Lines 42 and 43 immediately jump out. There's a root username
and password, but the password has been removed from the backup file. It appears
to be hashed, too.

I wasn't sure what to look for from here, so I searched for shell files with the
same MyShell version to see if similar files were on the web. I found one
[here](https://github.com/nikicat/web-malware-collection/blob/master/Backdoors/PHP/myshell.txt).
I noticed an important difference between our shell.php file and the version I
found online. When you compare line 123 of shell.php to line 110 of the version
I found online, line 123 of shell.php has this: `$MyShellVersion =  "MyShell
1.1.0 build 20010923 ".$$PHP_AUTH_USER;`

It seems innocuous, but this is a major flaw. The extra $ seems to cause the
program to print the value of a variable if you provide the name of a variable
in the code as your username.

Try it by entering adminEmail in the login popup for User Name, clicking OK, and
then clicking Cancel when the login popup appears again. The ensuing access
denied error page will include admin@seculas.com in the last line on the page.
What if we try this for shellPswd_root? Will we get the hashed password?

It turns out yes, we do. Enter shellPswd_root in the User Name field, click OK,
and then click Cancel. The last line of the access denied message now includes
our hashed password. If you check line 126 of shell.php, you'll notice this hash
is a double MD5 hash. This means in an earlier time we would've had to use a
tool like John the Ripper or Hashcat against this hash twice to reverse the hash
and get the plaintext password. But because this hash has been around for a
while, it's known what this hash resolves to.
[CrackStation](https://crackstation.net/) quickly identifies this hash and tells
us it resolves to foobar. Use root and foobar as your credentials on the login
screen to get into admin_area/.

### Navigating the Shell
We're in and now we've got a web shell interface to work with. This works just
like a shell interface on our local machine, so might as well get a sense of
what files and folders exist by executing the `ls` command. We see there's an
additional page at viewpatents.php. But when we try to access it by going to
https://www.hackthissite.org/missions/realistic/15/admin_area/viewpatents.php,
it's protected by another login portal.

The shell showed us another directory exists at test/, so go to
https://www.hackthissite.org/missions/realistic/15/admin_area/test/. Directory
listing is enabled and we can see a file, chkuserpass.c.zip. Download it, unzip
it, and open the file.

### Buffer Overflow Attack
The file we're looking at provides an additional authentication check for users
trying to access the seculas' patent information. The key is the checkit
functionality which reviews the user's username, password, and password hash and
returns a Y or N value. Depending on that, the backend decides whether or not to
grant the user access.

There's a vulnerability in this script with the concatenated char. It's set up
to contain a value of 200 characters with no error handling in case the value is
larger than 200. This means concatenated is vulnerable to a buffer overflow
attack. If we provide a username input that is larger than 200 characters, it
might overwhelm the script and cause unintended effects.

In our situation, we can see we want to force checkit to return a Y value. So,
the way to do it is to provide a username string of Ys of more than 200
characters. On the backend this overwhelm the system's memory and inadvertently
grants you access to the patents section.

It took me some trial and error, but a string of 228 Ys as the username did the
trick. Click OK and you'll complete the mission.

## Key Concepts
Plaintext attack\
JavaScript injection\
Directory traversal\
Hash cracking\
Buffer overflow

## Key Ideas
### Meta Tags
This was the first mission where meta tags played a role. The content in meta
tags [are of particular value for search engine
optimization](https://support.google.com/webmasters/answer/79812?hl=en). HTML5
also introduced the ability for web developers to [control the
viewport](https://www.w3schools.com/css/css_rwd_viewport.asp), or the user's
visible area of a web page, through a meta tag. It just so happened that the
content in the meta tags of this mission helped us to get admin access and
continue on with our goal.

### Getting the Source Code of Files
It bears repeating that being able to get the source code of important files on
this site was what allowed us to find vulnerabilities and exploit them. But
reading the code – in this case the files were in PHP and C – required time and
attention too. Sometimes the most gaping of vulnerabilities aren't so obvious to
spot at first.

### Hash Cracking
There was an added level of complexity to the MD5 hashing functionality we
encountered. The root password was run through the MD5 hash twice. This still
wasn't a difficult hash to crack because the password was a common string which
tools like CrackStation, John the Ripper, and Hashcat can easily decipher. But I
tried running the hash for shellPswd_others through John the Ripper and Hashcat
and gave up after about 30 minutes. I tried both brute forcing and running the
hash against the
[rockyou.txt](https://www.kaggle.com/wjburns/common-password-list-rockyoutxt)
list, but nothing obvious turned up. I guess the password is complex enough that
it can't be figured out quickly, even though we know so much about MD5's
weaknesses.

### Web Shells
The web shell on seculas' site was put there for legitimate use, but the way we
were able to exploit it shows their risks. Web shells are [a known vector for
malware and
abuse](https://www.acunetix.com/blog/articles/introduction-web-shells-part-1/).
In fact, the shell.php file is flagged by Google's products and systems as
malicious.