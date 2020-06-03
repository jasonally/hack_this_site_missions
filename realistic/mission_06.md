# Mission 6
https://www.hackthissite.org/playlevel/6/

- [Overview](#overview)
- [Solution](#solution)
  * [The Easy Way](#the-easy-way)
  * [The Harder Way](#the-harder-way)
- [Key Concepts](#key-concepts)
- [Key Idea](#key-idea)

## Overview
Decrypt a heavily encoded message from a CEO trying to bribe ecological inspectors investigating water pollution issues. Help environmentalists uncover corporations plotting to profit from the destruction of mother nature!

From: ToxiCo_Watch

Message: Hello esteemed hacker, I hope you have some decent cryptography skills. I have some text I need decrypted.

I work for this company called ToxiCo Industrial Chemicals, which has recently come under fire because of the toxic chemicals we are dumping into the river nearby. Ecological inspectors have reported no problems, but it is widely speculated that they were paid off by ToxiCo management because the water pollution near the ToxiCo factory has always been a serious and widely publicized issue.

I have done some packet sniffing on my network and I have recovered this email that was sent from the CEO of the company to Chief Ecological Inspector Samuel Smith. However, it is encrypted and I cannot seem to decode it using any of my basic decryption tools. I have narrowed it down to the algorithm used to encrypt it, but it is beyond my scope. I was hoping you can take a look at it.

Please check it out, more details are on the page. If you can unscramble it and reply to this message with the original text, it would be much appreciated. Thank you.

## Solution
### The Easy Way
Click into the mission and you're given the encrypted message as well as a helpful hint that the original document was encrypted using XECryption algorithm. Now that quite some time has passed since this mission was put online, Google helps us easily solve the mission. I found a web-based decryption tool [here](http://telmo.pt/xecryption/) which decrypts the message. Copy the result and message it to user ToxiCo_Watch to complete the mission.

### The Harder Way
If, you want to learn the underlying encryption theory, read on. If you click the XECryption algorithm link from the main mission page, you'll be taken to a tool where you can entrypt text using the algorithm. Try entering a basic input like 'a' (minus quotation marks). Don't enter a password, and encrypt it. The encrypted text is a series of three numbers seperated by periods, like .10.33.-11. Try encrypting 'a' again, and the sequence changes. But each time you encrypt a lower case a without adding a password, check the sum of the three numbers and it always equals 97, the decimal value of lower case a in ASCII. The three numbers are generated at random, but always equal 97.

Try adding a password – I used lower case a as my password and encrypted a lower case a again. The numbers changed, but this time they summed to 194, or 97 * 2. Try changing the password to something like 'ab' and see what happens en you encrypt a lower case a: it sums to 292, or 97 (the lower case a as an input) + 198 (the sum of 97 + 98, the ASCII decimal values of the password). So now we know the pattern. The password text gets converted to ASCII decimal values and summed together. Then for each character in the input text, it gets converted to an ASCII decimal value, added to the sum of the password value, and then it's randomly broken into three values. The key to reversing any messsage encrypted using this algorithm, therefore, seems to be finding the password first.

Google Fu led me to some Python code which I built upon to create a solver, `mission_06_solver.py`. The mechanics are:
* For each line of text, take three numbers at a time and add them together. Now the numbers have been added back into their values before the random split.
* While we don't know the password, there a finite number of possible character combinations since we know the text is in ASCII. So, we can brute force through all the possible character combinations until we find the correct password that turns the encrypted message into readable text.
* The code creates an output file for each possible combination. Simply click through files until you find ones which start to look more readable, and then eventually you'll find the file with the correct decryption.

## Key Concepts
Encryption and decryption

## Key Idea
This mission has become much easier given time because of the web apps which made for easy decrypting. So, some careful searching can help you solve encryption puzzles like this. But even if that shortcut didn't exist, the ability to brute force though all possible password combinations made this encryption easy to crack once you figured out the pattern.