# Mission 8
https://www.hackthissite.org/playlevel/8/

- [Overview](#overview)
- [Solution](#solution)
  * [Finding Gary Hunter's Account](#finding-gary-hunter-s-account)
  * [Transferring the Money](#transferring-the-money)
  * [Clearing the Logs](#clearing-the-logs)
- [Key Concepts](#key-concepts)
- [Key Ideas](#key-ideas)

## Overview
One of America's Richest Men plans to donate $10,000,000 to a campaign set on hunting down hackers and locking them up. Please, if you can't do this, then we're all screwed. Can you hack in and move the money?

From: DarkOneWithANeed

Message: Hey man, you gotta help me out, Gary Hunter, one of the richest men in America, has just deposited $10,000,000 into his bank account at the United Banks Of America and plans to donate that money to a campaign to hunt down and lock up all hackers. Now I've tried hacking their site but I'm just not good enough. That's why I need your help, Here's a list of your objectives:
1. Find the account of Gary Hunter (I don't know his account name).
2. Move the $10,000,000 into the account dropCash.
3. Clear The Logs, They're held in the folder 'logFiles'.\
I really hope you can do this, because if you can't we're all screwed

## Solution
### Finding Gary Hunter's Account
The mission site looks like a run-of-the-mill banking website. Click around and when you end up on the [User Info](https://www.hackthissite.org/missions/realistic/8/search.php) page you'll see it's a lookup for users on the site. Seems like a useful place to test out some SQL injection payloads.

Searching for `'` redirects you to https://www.hackthissite.org/missions/realistic/8/search2.php and shows this message: Error Getting Username Information From Table 'users'. Oh boy. Looks like a SQL injection is indeed possible here.

From the [Register](https://www.hackthissite.org/missions/realistic/8/register.php) page we can see that to create an account you need to provide a username, password, and account description (referred to as desc by the site's code). These three fields are probably in the table users. If you enter a valid username on the User Info page, it'll return the username and account description for that account. So, the SQL query on the backend must be something like:
`"SELECT username, desc FROM users WHERE username = '[user input]'"`

If we want to trick the query into displaying *all* of the usernames and account descriptions, an input like `' OR 1=1;` or `' OR '1=1';` will probably work. That's because the query will effectively become:
`"SELECT username, desc FROM users WHERE username = '' OR 1=1;"`

We know 1=1 resolves to True in a SQL query, so the query logically reduces down to:
`"SELECT username, desc FROM users WHERE username = '' OR True;"`

When we search with one of our two SQL injection inputs, the results page successfully displays the username and account descriptions for all rows in the users table. There are now thousands of accounts in the table and several of them have references to Hunter. This row is the correct Hunter: GaryWilliamHunter : -- $$$$$ --.

### Transferring the Money
The User Info page doesn't list each account's password, so unfortunately this step isn't as easy as logging into Hunter's account and transferring the money. To better understand how the site works when you're logged into an account, we need to create an account ourselves. The registration functionality on the [Register](https://www.hackthissite.org/missions/realistic/8/register.php) page actually works. Make an account and log into it using the [Login](https://www.hackthissite.org/missions/realistic/8/login1.php) page. Poke around on the [next page](https://www.hackthissite.org/missions/realistic/8/login2.php) and you'll notice a few things:
* Logging in puts a cookie in your browser. You can view it from your browser's developer tools console by typing `document.cookie`, or you can use an extension like [EditThisCookie](http://www.editthiscookie.com/).
  * The cookie has several values, but the one most relevant to our purposes is accountUsername.
* The Clear Files In Personal Folder button submits a POST request to https://www.hackthissite.org/missions/realistic/8/cleardir.php. There's a hidden input type named dir and its current value is [your_username]SQLFiles.
* The Move Money To A Different Account button submits a POST request to https://www.hackthissite.org/missions/realistic/8/movemoney.php with inputs named TO and AMOUNT.
* The password hash displayed on the page is the MD5 hash of your password. If there was some way to get Hunter's password hash we could probably decrypt it easily using an online tool, but I quickly found out that's not the technique we're supposed to use to solve the mission.

There are two things we can use together to accomplish the money transfer:
* Editing the cookie to spoof Hunter's account
* JavaScript injection

Edit the cookie and change the accountUsername value to GaryWilliamHunter. You can do this from the console in developer tools or by using an extension like EditThisCookie. Next, we can spoof the Move Money To A Different Account functionality by running the following JavaScript in the console:
`document.write('<form action="movemoney.php" method="POST"><input type="submit" value="Move Money To dropCash\'s Account"><input type="text" name="TO" value="dropCash"><input type="text" name="AMOUNT" value="10000000"></form>')`

This JavaScript essentially creates a button pre-populated with the money transfer values we want. In conjunction with the tampered cookie, when we click the button we've just created it'll transfer the money out of Hunter's account.

### Clearing the Logs
Clearing the logs will involve the same JavaScript injection idea. Log back into your account, but let's think things through for a moment. We saw the Clear Files In Personal Folder button clears the data in [your_username]SQLFiles. We want to clear the logs for the bank's whole system. So, our solution will need to change the hidden value. We'll need to change it to logFiles, as mentioned in the mission overview.

Run this JavaScript in the console:
`document.write('<form action="cleardir.php" method="POST"><input type="hidden" name="dir" value="logFiles"><input type="submit" value="Clear Log Files"></form>')`

Similar to our money transfer, this will create a new button pre-populated with clearing logFiles instead of [your_username]SQLFiles. Click the button to clear the logs and complete the mission.

## Key Concepts
SQL injection, specifically retrieving hidden data\
Cookie tampering\
JavaScript injection\

## Key Ideas
Hopefully no legitimate bank would store their user data in a database prone to a SQL injection like we saw in this mission, but plenty of sites might still have this type of setup. Hypothetically, if you were trying to obtain someone's username and/or password for a website and you couldn't just get it from a SQL injection, maybe you'd have to resort to a [phishing or spear phishing](https://www.barracuda.com/glossary/phishing-spear-phishing) attack. Even then, hopefully sensitive sites for services like banking would use two-factor authentication to make unauthorized access more difficult -- though [crooks have workarounds](https://krebsonsecurity.com/2020/04/would-you-have-fallen-for-this-phone-scam/).

As for the cookie tampering and JavaScript injection, the common wisdom is to [never trust data from a user's browser](https://stackoverflow.com/questions/6230565/how-to-prevent-users-from-modifying-cookie-values). Users will tamper with cookies, attempt to inject JavaScript, attempt to modify HTML, you name it. The effective way to cut off these vulnerability vectors is to have server-side validation for anything sent from a user's browser -- strictly control what data your server accepts. For cookies, mechanisms like user or authentication tokens would help protect against cookie tampering, 