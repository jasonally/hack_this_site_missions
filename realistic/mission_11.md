# Mission 11
https://www.hackthissite.org/playlevel/11/

- [Overview](#overview)
- [Solution](#solution)
  * [Details From the Site Layout](#details-from-the-site-layout)
  * [Listing Directory Contents](#listing-directory-contents)
  * [Details From the Site Layout, Part 2](#details-from-the-site-layout--part-2)
  * [Dumping Tables](#dumping-tables)
  * [Logging Into the Service Panel](#logging-into-the-service-panel)
  * [Recover the Archive](#recover-the-archive)
- [Key Concepts](#key-concepts)
- [Key Ideas](#key-ideas)
  * [Regarding Perl](#regarding-perl)
  * [BudgetServ's Bad Security Practices](#budgetserv-s-bad-security-practices)
  * [Other Techniques](#other-techniques)
  * [Hosting Services](#hosting-services)
  * [Hosting Terms and Laws](#hosting-terms-and-laws)

## Overview
The Space46 hacker community has been taken down not by mindless script kiddies, but by uptight network administrators! Help Space46 get his files back so he can restore the community and find a better host.

From: Space46

Message: Hello, I'm space46 from space46.nod. Up until recently, BudgetServ used to be a good host, but the company got new owners and some lame hosted site was deleted somehow. The administrators think that it was me and they've suspended my account. I've contacted them numerous times about getting my files back but they refuse. As it so happens, I made a backup in my web root named src.tar.gz right before the account was suspended. Can you get this file back so that I can move to a better host?

## Solution
### Details From the Site Layout
Like we've done with recent missions, click into the [mission site](https://www.hackthissite.org/missions/realistic/11/) and click through the pages we can currently access.
* [Features](https://www.hackthissite.org/missions/realistic/11/page.pl?page=features) describes the software BudgetServ's servers use.
* [FAQ](https://www.hackthissite.org/missions/realistic/11/page.pl?page=faq) links to an [administration script](https://www.hackthissite.org/missions/realistic/11/admin/) which takes you to a Service Panel login screen.
* [Terms of Service](https://www.hackthissite.org/missions/realistic/11/page.pl?page=terms) lists examples of material BudgetServ won't allow on its servers.
* [Pricing](https://www.hackthissite.org/missions/realistic/11/page.pl?page=pricing) lists the service packages available to customers.
* [WebMail](https://www.hackthissite.org/missions/realistic/11/page.pl?page=email) leads to another login screen. Entering any sort of username/password combination leads to https://www.hackthissite.org/missions/realistic/11/webmail.php where you're told that due to a recent security breach, WebMail is currently unavailable.

The Features page has clues to what technologies we might need to tap into to solve this mission. BudgetServ users can use Linux or Windows operating systems, PHP and Perl programming languages, and MySQL and SQLite database engines. The administration script from the FAQ page looks useful, but maybe later on in the mission once we've figured out more about the site layout and how to access accounts. The Terms of Service page isn't directly relevant to the mission, but it's worthy of discussion later. Pricing isn't too relevant to the mission either, but it's funny how the prices for each package are woefully out of whack when you think about how cheap storage and bandwidth have become in the 2020s.

The URL structure of the pages also provides an important detail. page.pl is a Perl script and it takes in a parameter called page. Perhaps we can tamper with this.

### Listing Directory Contents
Think back to [Basic Mission 8](https://github.com/jasonally/hack_this_site_missions/blob/master/basic/mission_08.md) and [Basic Mission 9](https://github.com/jasonally/hack_this_site_missions/blob/master/basic/mission_09.md) and how we could use [Server Side Includes](https://en.wikipedia.org/wiki/Server_Side_Includes) in PHP to list the directory contents. We might be able to do something similar in this mission with Perl.

Try accessing a page which doesn't exist, like https://www.hackthissite.org/missions/realistic/11/page.pl?page=x. Rather than getting a definitive 404 error, you get an error message saying:\
open(file, "pages/x") failed: No such file or directory

On the backend, whatever follows page= gets put into an open() function and Perl tries to execute it, returning whatever is at that file path. Now that we know how this code works, we can really start to mangle with it and see what happens. Try a URL like this: https://www.hackthissite.org/missions/realistic/11/page.pl?page=hello%22)open(file,%20%22hello and you'll get a really strange error:
Page cannot m{[\0.<>\/&\s]}

That's more proof there's improper error handling. We might be able to abuse this and list the directory contents. From previous missions we know the Unix command is `ls`, but the proper Perl syntax in this case is to surround it with vertical bars, like `|ls|`. Try this URL: https://www.hackthissite.org/missions/realistic/11/page.pl?page=|ls|. The resulting page shows the full directory contents.

The bs.dbase file looks like a database file which may be of interest. But we need a way to access it, similar to what we did with database files in [Realistic Mission 8](https://github.com/jasonally/hack_this_site_missions/blob/master/realistic/mission_08.md) and [Realistic Mission 9](https://github.com/jasonally/hack_this_site_missions/blob/master/realistic/mission_09.md). The client_http_docs directory also looks promising. Try accessing it by going to https://www.hackthissite.org/missions/realistic/11/client_http_docs/.

Directory listing is enabled and there are four directories for BudgetServ customers. space46/ is the one we want, but it's inaccessible because the account has been suspended. We'll need to find another way in. wonderdiet/ and potatoworks/ take us to other sites which aren't of much use to us (check them out yourself, but you won't find anything of use). therightwayradio/, meanwhile, takes us to a site with many functionalities worth exploring.

### Details From the Site Layout, Part 2
We're now accessing The Right Way Radio's site via BudgetServ's systems. With respect to BudgetServ's security, we've manipulated some pretty gaping holes to get here, though where we are right now doesn't seem relevant to the main objective of this mission. But let's see if this does relate back to the mission objective. Click through the site we're on now and see what you can learn.
* forum is meant to be a user discussion space.
* radio and about are both static pages which don't seem to be very useful for us.
* register allows people to create accounts, but you're now required to have an auth code to create an account, which we don't have.

The main page, meanwhile, has links to a script which records the user agent of recent visitors as well as to the user rsmith's profile. Viewing rsmith's profile opens a URL like this: https://www.hackthissite.org/missions/realistic/11/client_http_docs/therightwayradio/?page=userinfo&id=-1. Recall from [Realistic Mission 10](https://github.com/jasonally/hack_this_site_missions/blob/master/realistic/mission_10.md) that the user with id=0 is often an administrator. Try navigating to https://www.hackthissite.org/missions/realistic/11/client_http_docs/therightwayradio/?page=userinfo&id=0 or https://www.hackthissite.org/missions/realistic/11/client_http_docs/therightwayradio/?page=userinfo (that is, remove the id parameter entirely). Depending on what you tried, you'll either get a full list of profiles for a couple dozen users or the profile details for one user, aclu_bomber_08290. aclu_bomber_08290 has an edit account button visible. You can actually change this account's password though this functionality. Change the password to something you'll remember, like password. Then log into this account using the login box in the top left corner of the screen.

### Dumping Tables
Sure enough, this account has administrative privileges. Once you're logged in you'll see the top right corner of the ensuing page has different links, including one called mod. Click that and you're taken to a page where you can input a SQL query. The intent here seems to be that you can query a database containing data from The Right Way Radio's site. There's a helpful message telling us the backend uses [SQLite](https://www.sqlite.org/index.html) for database management. If you inspect the form using Developer Tools you'll see this:
```
<form method="post" action="./?page=mod" enctype="multipart/form-data">
	<input type="hidden" name="page" value="mod">
	<input type="hidden" name="sql_db" value="rwr.dbase">
	<input type="text" name="sql_query" style="width: 80%"> 
	<input type="submit" name=".submit" value="sql query" class="submit">
	<br>
	<span style="font-size: 8pt">SQLite access for moderators has been tightened to read-only due to the recent security breech.</span>
</form>
```

We've got a form which submits a SQL query input to a database called rwr.dbase. Maybe this can help us access the bs.dbase file we saw earlier. The directory traversal technique we used in [Realistic Mission 3]https://github.com/jasonally/hack_this_site_missions/blob/master/realistic/mission_03.md) and Realistic Mission 7(https://github.com/jasonally/hack_this_site_missions/blob/master/realistic/mission_07.md) might be relevant here. Since we're currently on the page https://www.hackthissite.org/missions/realistic/11/client_http_docs/therightwayradio/?page=userinfo and the bs.dbase file is located at https://www.hackthissite.org/missions/realistic/11/bs.dbase, the relative path to bs.dbase is ../../../bs.dbase. Edit the HTML of the form so sql_db's value is ../../../bs.dbase. The form will now look like this:
```
<form method="post" action="./?page=mod" enctype="multipart/form-data">
	<input type="hidden" name="page" value="mod">
	<input type="hidden" name="sql_db" value="../../../bs.dbase">
	<input type="text" name="sql_query" style="width: 80%"> 
	<input type="submit" name=".submit" value="sql query" class="submit">
	<br>
	<span style="font-size: 8pt">SQLite access for moderators has been tightened to read-only due to the recent security breech.</span>
</form>
```

Since we've edited the form to query the database file we want to access, we need to give the database a useful query. The detail that this is a SQLite implementation is useful, since every [SQLite's official FAQ](https://www.sqlite.org/faq.html) explains every SQLite database contains a sqlite_master table which lists table and index name. Type `SELECT * FROM sqlite_master` and click the sql query button.

The resulting page loads a table with one row and four columns. There's one table called web_hosting and we can see web_hosting has columns including web_user, web_pass, web_package, and web_email.

If you think back to the Service Panel Login page we found earlier at https://www.hackthissite.org/missions/realistic/11/admin/, we're getting close to being able to get into it. We've accessed data in the bs.dbase file, we found the table BudgetServ uses to store account credentials, and now we just need to query the table itself. Using the same SQL query input box, type `SELECT * FROM web_hosting` and click the sql query button. When the page loads, we'll see email addresses, usernames, and passwords for BudgetServ's users -- all in plain text.

### Logging Into the Service Panel
Go back to the Service Panel at https://www.hackthissite.org/missions/realistic/11/admin/ and let's try some login credentials. Try space46's username and password if you want, but you'll get a message saying: This account has been suspended due to inappropriate content. We'll need to try another account. Either therightwayradio or wonderdiet will work. Pick the account and credentials of your choosing log in. For me, I used therightwayradio and its corresponding password.

### Recover the Archive
Tinker around with the admin panel and you'll see you can download different parts of the customer's site for backup purposes. Check Developer Tools and you'll see each radio option has a value corresponding to the appropriate file path. I tried editing the value for one of the options to /var/www/budgetserv/html/client_http_docs/space46/src.tar.gz, selecting that radio option, and clicking download, but I got an access denied message. I was on the right track but you have to be a bit more clever.

If you select another radio option and click download, you'll most likely see a download prompt appear. Cancel out of that window and then check Developer Tools' Network tab to better understand what happened. You should see a GET request to a path with a d.pl?file=/ structure, like https://www.hackthissite.org/missions/realistic/11/admin/d.pl?file=/var/www/budgetserv/html/client_http_docs/therightwayradio/./. What if you edited this URL directly and tried navigating to it?

Change the URL to https://www.hackthissite.org/missions/realistic/11/admin/d.pl?file=/var/www/budgetserv/html/client_http_docs/space46/src.tar.gz and try accessing it in your browser. It'll trigger the download for space46's backup and finish the mission.

## Key Concepts
Command injection\
Directory traversal\
Privilege escalation

## Key Ideas
### Regarding Perl
The first thing which threw me for a loop in this mission was how BudgetServ's scripts were in Perl. At the time of this writing, the last time I heard of Perl was 5+ years ago. It turns out that's not just me. Perl has steadily been on the decline as articles [like this](https://www.fastcompany.com/3026446/the-fall-of-perl-the-webs-most-promising-language) and [this](https://insights.dice.com/2019/07/29/5-programming-languages-probably-doomed/) explain. It sounds like a lot of Perl's use cases have been superseded by Python for reasons including Python's readability, spread into academia, and passionate developer community. That's not to say, however, the ideas in this mission are obsolete. If BudgetServ used Python scripts instead and was still vulnerable to a command injection attack at the beginning, you theoretically would go about completing the mission in a similar manner. Python has [similar abilities to list directory contents](https://www.freecodecamp.org/news/python-list-files-in-a-directory-guide-listdir-vs-system-ls-explained-with-examples/).

### BudgetServ's Bad Security Practices
While my solution already highlights BudgetServ's bad security practices, this mission particularly shows the problems with privilege escalation and storing account credentials in plain text. It was one thing for us to have been able to compromise aclu_bomber_08290's account, but we shouldn't have been able to then use it to query BudgetServ's user account database. That's a bad enough security flaw in its own right, but that BudgetServ stored account credentials in plain text is especially bad. At a minimum, BudgetServ should have encrypted passwords while they're at rest, preferably through a process like [salting and hashing](https://auth0.com/blog/adding-salt-to-hashing-a-better-way-to-store-passwords/#:~:text=A%20cryptographic%20salt%20is%20made,compute%20them%20using%20the%20salts.).

### Other Techniques
I saw that in earlier years users completed this mission using XSS/cookie stealing and user agent spoofing techniques. The script on The Right Way Radio's website logging users' user agents probably helped in this way. But I couldn't figure out how to replicate these techniques so I'm not sure if they're still working properly. In any case, I didn't need to use these techniques to finish the mission.

### Hosting Services
As mentioned above, I also thought BudgetServ's product offerings were pretty inadequate given the high monthly cost. I suppose that's what the cloud storage world looked like before the rise of products like [Amazon Web Services](https://aws.amazon.com/), [Google Cloud](https://cloud.google.com/), and [Microsoft Azure](https://azure.microsoft.com/). These offerings ushered in a new era of low-cost cloud storage and hosting capabilities, though plenty of more traditional web hosting companies like [GoDaddy](https://www.godaddy.com/), [Namecheap](https://www.namecheap.com/), [Bluehost](https://www.bluehost.com/), [NearlyFreeSpeech.NET](https://www.nearlyfreespeech.net/), and [HostGator](https://www.hostgator.com/) are still around.

### Hosting Terms and Laws
The premise for this mission was BudgetServ suspended space46's account. If you're using another entity's service to put your content online, then yes, you're subject to their rules and policies. The laws surrounding acceptable content and user privacy might also vary depending on what country you're in and what country the hosting company's based in. These are important things to consider. Not only might a hosting company have inconsistent rules and policies with respect to their customers, but a hosting company might also be inconsistent in the opposite way. For instance, a 'bulletproof' hosting company is one which might refuse to terminate customer accounts even if that customer's websites engage in clearly illegal or unethical behavior. Brian Krebs at KrebsOnSecurity [has reported on bulletproof hosting services for years](https://krebsonsecurity.com/tag/bulletproof-hosting-providers/). Bulletproof hosting companies often operate out of countries where it's difficult to seek out legal recourse for customers engaging in illegal or unethical behavior. 

