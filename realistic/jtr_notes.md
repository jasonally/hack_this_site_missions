# Notes on John the Ripper

- [Overview](#overview)
- [Downloading](#downloading)
- [Installing](#installing)
- [Running](#running)

## Overview
This is meant to be a follow up to `mission_07.md`, where I used JTR to crack an MD5 hash. I could have used JTR in an earlier mission but I sort of ducked out of it and used another password cracking program because I found the install and run instructions a bit confusing at first. But my second attempt was much more successful.

## Downloading
At the time of this writing there are a couple of places where you can get the JTR jumbo code. One is here on [Github](https://github.com/magnumripper/JohnTheRipper), the other is through [Openwall](https://www.openwall.com/john/). Download the version of your choice depending on your operating system (I downloaded the tar.gz version for macOS).

## Installing
When the download completes, extract the folders and files out of the archive. You should see a folder called doc. Click into it, then open the appropriate INSTALL file based on your operating system. From there, just follow the steps.

For me, the relevant section was: Compiling the sources on a Unix-like system. You'll need to run some commands on the command line to do this - JTR doesn't have a GUI, so all JTR use has to happen on the command line.

Once you're in Terminal, navigate to wherever you extracted the JTR folders and files, and use `cd src` to access the src subdirectory. You'll then need to run a ./configure command to create JTR executables. I ran this command and it worked perfectly: `./configure CFLAGS="-g -O2 -mno-avx2"`.

If everything works properly, follow the instructions to change your working directory over to ../run/ and try a test.

## Running
To use JTR for real, you need to supply the program with a hash to crack in an input file. From Realistic Mission 7 we have the contents of a .htpasswd file which we can save in a .txt file on our local machine, then feed that file into JTR. 

I did this by saving the .htpasswd file contents (for me the contents were administrator:$1$AAODv...$gXPqGkIO3Cu6dnclE/sok1) in a .txt file on my desktop, which I called hash_htpasswd.txt. Since the folders containing my JTR install were also on my desktop, when I ran JTR I used a command like `./john ../../hash_htpasswd.txt`. Your input path depends on where you saved your input file, and [here's a useful video example](https://www.youtube.com/watch?v=p_hUc8tCKzE&t=175).

In my case, the password cracking took about two seconds and then JTR displayed both the cracked password and the username in the Terminal window. If the cracking finished successfully but for some reason the results aren't on the screen, you should be able to see them by running something like `./john --show ../../hash_htpasswd.txt` (but again, the path to your input file may be different than mine).