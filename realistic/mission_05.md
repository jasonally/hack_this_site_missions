# Mission 5
https://www.hackthissite.org/playlevel/5/

- [Overview](#overview)
- [Solution](#solution)
  * [Searching for Useful Clues](#searching-for-useful-clues)
  * [Decrypting the Password Hash with Hashcat](#decrypting-the-password-hash-with-hashcat)
- [Key Concepts](#key-concepts)
- [Key Ideas](#key-ideas)

## Overview
Telemarketers are invading people's privacy and peace and quiet. Get the
password for the administrative section of the site to delete their database and
return the privacy of their victims!

From: spiffomatic64

Message: Yo! This is Spiffomatic64 from Hackthissite.org! I'm a bit of a hacker
myself as you can see, but I recently came upon a problem I couldn't
resolve.....

Lately I've been getting calls day and night from the telemarketing place. I've
gone to their website and hacked it once deleting all of their phone numbers so
they wouldn't call me anymore. That was a temporary fix but they put their
database back up, this time with an encrypted password. When I hacked them I
noticed everything they used was 10 years out of date and the new password seems
to be a 'message digest'. I have done some research and I think it could be
something like a so-called hash value. I think you could somehow reverse
engineer it or brute force it. I also think it would be a good idea to look
around the server for anything that may help you.

## Solution
### Searching for Useful Clues
The mission overview provides two clues:
* Googling the term 'message digest' led me to the Wikipedia page for
[cryptographic hash function](https://en.wikipedia.org/wiki/Cryptographic_hash_function), 
which is also known as a message digest. So we'll be doing something involving
hashes and how they can be used to encrypt passwords and other sensitive
information.
* The detail about the site being 10 years out of date is now, in 2020, even
more out of date. The site now is more like 20-25 years out of date.

Click into the site and we're taking on Compu-Global-Hyper-Mega-Net, a nod to
The Simpsons (episode details [here](https://simpsons.fandom.com/wiki/Das_Bus);
excellent scenes [here](https://www.youtube.com/watch?v=9STeegpxSb0) and
[here](https://www.youtube.com/watch?v=nB8LflLMiCQ)). Click through the site's
pages and the News page has a history of updates. It includes this nugget:
9/15/03 - Google was grabbing links it shouldn't be so I have taken extra
precautions.

Google crawling parts of the site that the webmaster didn't want crawled means
two things:
* Those pages might still be in Google search results
* The site's
[robots.txt](https://support.google.com/webmasters/answer/6062608?hl=en) file
might have clues as to what part of the site the webmaster is trying to keep
hidden.

The robots.txt file is usually right off the root page of a host, which in our
case is https://www.hackthissite.org/missions/realistic/5/. Try going to
https://www.hackthissite.org/missions/realistic/5/robots.txt, and there you have
it: there are two semi-hidden directories at /lib and /secret. Navigate to
https://www.hackthissite.org/missions/realistic/5/secret/ and you'll see two PHP
files. In admin.bak.php, I see this message: `error matching hash
cdbb3e741a3086fa64c17f12b63815ce`.

Similarly, if you do a Google search for
site:https://www.hackthissite.org/missions/realistic/5/, you should find the URL
for http://www.hackthissite.org/missions/realistic/5/secret/admin.bak.php (you
might have to click a link to repeat the search with omitted results included to
find this page).

### Decrypting the Password Hash with Hashcat
We've got our hash to decrypt. I figured, taking the '10 years out of date' part
literally, that this was probably an [MD5
hash](https://en.wikipedia.org/wiki/MD5), but after getting some hints online,
it turns out this is actually even older -- it's an [MD4
hash](https://en.wikipedia.org/wiki/MD4). I tried several free online decryption
tools to see if they could reverse the hash, but none of them could. I ended up
downloading [Hashcat](https://hashcat.net/hashcat/) onto my machine and running
it in Terminal to decrypt the password.

It took a bit to understand Hashcat's flags and syntax, but this [Stack Exchange
thread](https://security.stackexchange.com/questions/167767/cracking-md4-hash)
helped me formulate the right command to brute-force an MD4 hash: `hashcat -m
900 cdbb3e741a3086fa64c17f12b63815ce -a 3 -o cracked.txt`. You might, however,
first need to create the cracked.txt file in your current working directory
before running the command. MD4 is so easily broken now that Hashcat should
decrypt the password in a few seconds. Open the cracked.txt file and you'll see
the decrypted password appended to your input hash following a colon. Enter in
the password at https://www.hackthissite.org/missions/realistic/5/submit.html,
submit, and you're done.

## Key Concepts
robots.txt  
Hash cracking

## Key Ideas
Several things came together to make this site hackable:
* It's possible tomorrow's more powerful computers can break today's common
cryptographic hash functions. For this mission, it was effectively game over
once we found the hash and found it was generated using MD4. While researching
this mission I found an interesting paper
[here](https://tools.ietf.org/html/rfc6150) detailing RSA Security's decision to
 move MD4 to Historic status.
* A robots.txt file is helpful in telling search engines like Google what parts
of your site to crawl, but the file by itself isn't an effective way to tell
search engines what *not* to crawl and it's especially not an effective way at
hiding parts of your site from users. To reference concepts from other missions,
[disabling directory listing](https://github.com/jasonally/hack_this_site_missions/blob/master/basic/mission_11.md) or password-protecting sensitive files would help with
preventing users and search engines from finding pages like
http://www.hackthissite.org/missions/realistic/5/secret/admin.bak.php.
* The news updates on the site were a dead giveaway of what to target. Seemingly
innocent details like site updates can be used to damaging effect in the wrong
hands.
* Running Hashcat requires some knowledge of shell commands, which isn't really
covered in these missions. I also used [Homebrew](https://brew.sh/) to install
Hashcat, which is a great package manager for macOS or Linux.
