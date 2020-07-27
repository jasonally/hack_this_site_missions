# Mission 6
https://www.hackthissite.org/missions/basic/6/

- [Overview](#overview)
- [Solution](#solution)
- [Key Ideas](#key-ideas)

## Overview
Network Security Sam has encrypted his password. The encryption system is
publically available and can be accessed with this form:  
[form box]  
You have recovered his encrypted password. It is: 84eh:f>7  
Decrypt the password and enter it below to advance to the next level.

## Solution
Try encrypting several inputs and see what outputs you get. The input which
was useful for me was `aaaaaa`. The encrypted result was `abcdef`.

This helped me realize the encryption is nothing more than shifting the input n
characters on an ASCII table like
[this](https://www.rapidtables.com/code/text/ascii-table.html), n being the
spot the character is in in the input string. So, aaaaaa` becomes: `a (n = 0,
so a + 0 = a) b (n = 1, so a + 1 = b) c (a + 2 = c) d (a + 3 = d) and so on.

We know the encrypted password, so reverse it using the same pattern and
looking at an ASCII table. 84eh:f>7 becomes 83ce6a80.

## Key Ideas
The random inputs idea from Mission 2 is applicable again. But having a
methodology to your inputs is helpful too, like in this case with `aaaaaa`
helping me discover the sequence in the encryption.

Also, be careful with using encryption. Much has been said about
[not creating your own encryption](https://www.schneier.com/blog/archives/2011/04/schneiers_law.html).
But using encryption which is reliable, well-maintained, and not obvious is
also important. Don't use something like a
[Caesar cipher](https://en.wikipedia.org/wiki/Caesar_cipher).