# Mission 7
https://www.hackthissite.org/playlevel/7/

## Overview
A homophobic hate group is spreading their conservative propaganda of blind obedience and bigoted war mongering. Help tolerance activists take over their website of ignorance and discrimination.

From: FreedomOfChoice

Message: Friend of freedom and liberty, I invite you to take a look at the hate speech being spewed over the web at http://www.hackthissite.org/missions/realistic/7/. It's so funny that conservatives keep saying they want to protect the values of America - freedom, tolerance, and democracy - but when it comes to personal choices like private marijuana use or same-sex marriages, they damn them to burn in eternal hell and send them to jail.

This is a personal freedom issue. No one else is hurt if two consenting adults decide to marry. But people who claim to have the moral high ground decide to ruin it for everyone else and discriminate against same-sex couples. To think that they are talking about making a constitutional amendment to STOP OUR FREEDOM TO MARRY is ludicrous. This injustice must be stopped.

There is an admin section on that website somewhere, perhaps hidden among their directory structure. It would be a great fight against moral tyranny and a victory for freedom if you could somehow hack into their website. Thank you.

## Solution
### Locating the admin Section
This mission returns to concepts from the Basic missions. For instance, the clue about an admin section possibly hidden amongst the directory structure is a callback to [Basic Mission 11](https://github.com/jasonally/hack_this_site_missions/blob/master/basic/mission_11.md).

With that in mind, click into the mission site and check out the deeper pages. Specifically, we're looking for something which helps us understand the site's directory tree. If you check out any of the images on the deeper pages, you'll get your clue: the URL structure like https://www.hackthissite.org/missions/realistic/7/images/bush1.jpg.

Recall from Basic Mission 11 that Apache is a popular web server software - as of May 2020 roughly [38% of the web](https://w3techs.com/technologies/history_overview/web_server) runs on Apache. Also recall that many Apache instances have directory listing enabled by default, allowing anyone accessing the website in question to click through the directory tree. Now that we know of a directory on the site, try going to it: https://www.hackthissite.org/missions/realistic/7/images/.

There we go, we can see the full directory contents of /images - not good for whoever built this site but good for us. Sure enough, there's an /admin directory hidden inside the /images directory. But if you click it, a prompt asks us for a username and password which we don't have.

### Finding the Login Credentials
You can password protect directories on a server [using a .htaccess file](https://www.hostwinds.com/guide/password-protect-files-directories-htaccess/) which you create and place in the directory you're trying to protect. The username and password credentials are then stored in [an .htpasswd file](https://www.hostwinds.com/guide/create-use-htpasswd/) which is also put in the directory you're trying to protect. If only there was a way we could use URL inputs to trick this site into giving us the contents of the .htpasswd file...

Fortunately, there is. If you look back at one of the deep URLs like https://www.hackthissite.org/missions/realistic/7/showimages.php?file=patriot.txt, that parameter at the end of the URL is a dead giveaway. If we could use our knowledge of Linux shell commands to pass the path to the .htpasswd file into showimages.php, we might be in luck. The .htpasswd file we're trying to access is in /images/admin/.htpasswd, so the URL we're trying to craft is this: https://www.hackthissite.org/missions/realistic/7/showimages.php?file=/images/admin/.htpasswd.

Try accessing that URL and darn, a broken image icon appears in the center of the page. Or could there be more do it? Hover over the icon and you'll see what looks like a key-value pair. I see something like: administrator:$1$AAODv...$gXPqGkIO3Cu6dnclE/sok1. The .htpasswd file guide linked  above mentions this: `User credentials are stored on separate lines, with each line containing a username and password separated by a colon (:). Usernames are stored in plain text, however passwords are stored in an encrypted hashed format. This encryption is usually MD5, although in Linux it can be based on the crypt() function.` Sounds like we know our username (it's administrator) and we have a password hash to crack.

As an aside, it makes perfect sense that this URL structure caused the broken image icon to appear. The page template was expecting an image, but the contents of a .htpasswd file, well, aren't an image.

### Cracking the Hash
In Realistic Mission 5 I used Hashcat to crack the MD4 hash in part because I was a bit confused at how to use John the Ripper. From the mission tips I found, however, it seemed like JTR really was the way to go for this mission. I think this is because it has wordlists which would significantly decrease the time to crack the password. Knowing that I really had no choice but to use JTR for this mission, I grinded out how to use it and was able to crack the hash in seconds. See `jtr_notes.md` for more details.

After using JTR to crack the password hash, I went back to https://www.hackthissite.org/missions/realistic/7/images/admin/, entered in the username and decrypted password, and that completed the mission.

## Key Concepts
Directory listing
Path traversal
Hash cracking

## Key Ideas 
This mission again demonstrated how websites are, at their core, essentially programs running on a computer. If you know what the backend technology looks like (e.g., many websites run Apache and/or have a Linux operating system), it gives you some clues as to what sort of settings are in place by default, how security measures work by default, and how you can poke and prod at them. 