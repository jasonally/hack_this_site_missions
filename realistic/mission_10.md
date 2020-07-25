# Mission 10
https://www.hackthissite.org/playlevel/10/

- [Overview](#overview)
- [Solution](#solution)
  * [Details From the Site Layout](#details-from-the-site-layout)
  * [Finding a Staff Account](#finding-a-staff-account)
  * [Changing Your User Agent](#changing-your-user-agent)
  * [Giving Yourself Administrator Privileges](#giving-yourself-administrator-privileges)
  * [Changing Zach's Grades](#changing-zachs-grades)
    + [JavaScript Injection Method](#javascript-injection-method)
    + [URL Tampering Method](#url-tampering-method)
- [Key Concepts](#key-concepts)
- [Key Ideas](#key-ideas)

## Overview
You get to do what every hacker has dreamed of, breaking in and changing grades!
Help Zach get his grades fixed, and prove you're as "skilled" as he thinks you
are.

From: Zach Sanchez

Message: hey man, it's me Zach, I need a favour from you, I'm in big trouble.

if you'll remember, I go to that super uptight religious school. well, two of my
teachers are failing me because my lifestyle does not fall in line with their
moralistic rules for public behaviour. My gym teacher even called me a
'long-haired hippie f*****'! And if I fail any classes, I won't graduate.

Listen, can you hack into the school's grade database and make it so I'm passing
all my classes? I know they have this system set up on their website that allows
teachers to submit grades and stuff, and I heard you pulled a few things in the
past as well. Their web master was not thinking in terms of computer security
when he was designing the website, so it might be easy. Or not. Please check it
out here. The username to my account is 'Zach Sanchez' and my password is
'liberty638'. Thanks man!

## Solution
### Details From the Site Layout
The mission overview implies we'll need to do something along the lines of
logging into the school's teacher portal and changing Zach's grades. But we
don't know which grades we need to change and what they need to be changed to.
With that in mind, the first thing I wanted to solve when I accessed the mission
site was logging into Zach's account via the Student Access System and viewing
his grades as they currently look. Do that and you'll see he currently has
failing grades in both semesters of Bible Study and a failing grade in one
semester of Gym. We'll need to change his grades to 3 or higher in each of these
classes.

Go back to the root page of the site. If there's anything we've learned from
prior missions, it's important to thoroughly check the source of all pages to
learn as much as we can about the site's structure. You'll notice the obvious
links to the [home
page](https://www.hackthissite.org/missions/realistic/10/index.php), [Staff
Listing](https://www.hackthissite.org/missions/realistic/10/listteachers.php)
and [Student Access
System](https://www.hackthissite.org/missions/realistic/10/student.php) we just
viewed. But if you look carefully there's a link to
https://www.hackthissite.org/missions/realistic/10/staff.php on the lefthand
side of the page, hidden in an empty set of pixels. This leads us to a staff
login page.

### Finding a Staff Account
I tried basic SQL injection payloads like the ones which worked for me in
Realistic Mission 2 and Realistic Mission 8. My intention was to see if any of
these payloads would trigger an error or otherwise help me bypass the login
screen. None of them worked. This got me thinking we actually needed to
compromise an account to get into the staff portal, so I went back to the Staff
Listing and looked through each of the teacher pages. Each teacher seems to be
in a table of teachers, each with a unique ID with values from 1 to 21. Each
teacher has an email address with a first initial, last name structure, and it
stands to reason those are probably login names as well.  

I picked some teachers at random, went back to the staff login screen, and tried
logging in using their email username and 'password' as the password. None
worked. I felt like I was still on the right track but I needed some Google Fu
to help: instead of picking an account at random, we needed to focus on a
specific account. In this case, it's the account which likely has administrative
privileges over all of the other accounts. The sequential ordering of each
teacher's ID offers a big giveaway. Whichever teacher has ID = 1 is our target.
https://www.hackthissite.org/missions/realistic/10/teacherinfo.php?id=1 loads
Samantha Miller's profile, with username smiller.

Go back to the staff login and try smiller as the username, password as the
password. No luck. But what's another common password by default? Even now, in
the 2020s? The username. Try smiller as your username, smiller as your password,
and you're in.

### Changing Your User Agent
After logging in with smiller's account you're greeted with this message:\
Welcome, Mrs. Samantha Miller! Please remember that access to the staff
administration area is restricted to the district-supplied 'holy_teacher' web
browser.

This requires us to learn about user agents and the
[User-Agent](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/User-Agent)
HTTP header which tells a server about the computer program trying to access it.
The staff administration area is restricted to a specific web browser, as
indicated by the User-Agent header. Fortunately, we can spoof our User-Agent to
bypass this. In Chrome, the steps
[here](https://www.technipages.com/google-chrome-change-user-agent-string)
worked for me. Open Developer Tools, click the Menu icon (it's represented by
three vertical dots), and go to More tools > Network conditions. Under User
agent, uncheck the box marked Select automatically, and in the free-form box
below, enter holy_teacher. Reload the page after making this change and it
should load correctly now. You might need to keep Developer Tools open to make
the User-Agent change persist.

### Giving Yourself Administrator Privileges
Now that the page loads correctly, you'll see three buttons on the left hand
side of the page. One of them is Change Grades, which seems to be what we want.
But there's a message below the button saying:\
note: you are not an administrator so you cannot change grades

We need to give ourselves administrator privileges. The first thing I checked
after seeing this message was the site cookie. There's a value in the cookie for
admin and it's currently set to 0. Change it to 1 and now you can access the
Change Grades page.

### Changing Zach's Grades
Click Change Grades, click Zach Sanchez from the student listing, and we've got
our form with Zach's grades. But there's a message at the bottom of the form
saying it's too late to change grades. Clearly we need to find a workaround. Use
Developer Tools to look at the elements on the page – take a look at the HTML.
For each class there should be a submit button to submit grade changes, but it's
commented out right now. Even if you tamper with the HTML and uncomment a
button, change a grade and comment, and press submit, it won't work.

#### JavaScript Injection Method
Thinking back to Realistic Mission 9, I thought maybe the answer involved
JavaScript injection. If you look at each class in the raw HTML, you'll see it's
really part of a form sending data via a POST request to staff.php with some URL
parameters. For Bible Study, changing a grade would send data to
staff.php?action=changegrades&amp;changeaction=modrec&amp;rec=4&amp;studentid=1.
So, I tried creating a JavaScript injection like this and running it in the
console:\
`document.write('<form
action="staff.php?action=changegrades&changeaction=modrec&rec=4&studentid=1"
method="post"><input type="text" name="grade" value="5" size="4"><input
type="text" name="comments" value="Best in class"><input type="submit"
value="modify"></form>')`

And it worked! This successfully changed Zach's grade for the first semester of
Bible Study. You could repeat this process for the other two classes by getting
the form action URL for each class and making a similar JavaScript injection.

#### URL Tampering Method
JavaScript injection works and is a valid solution, but there's an even simpler
approach which doesn't involve JavaScript injection. It turns out you can change
Zach's grades using some clever URL tampering and editing.

For instance, this works for updating the Bible Study grade. Just paste this URL
into your browser and try accessing it.
https://www.hackthissite.org/missions/realistic/10/staff.php?action=changegrades&changeaction=modrec&rec=4&studentid=1&grade=5&comments=Best%20in%20class

Similar to the JavaScript injection method, repeat this for the two other
classes Zach is failing and you're done.

## Key Concepts
Hidden links\
Understanding account permissions\
Exploiting weak passwords\
Changing the user agent\
Cookie tampering\
JavaScript injection\
URL tampering

## Key Ideas
The fictional school in this mission made a big mistake by attempting to make
the staff section of the site secure by obscurity. But even if there wasn't a
hidden link to the staff login from the home page, it would be easy to reason
that if there's a student access system, there's likely to be a staff access
system. Once you make that leap, it wouldn't be a far leap to guess the URL and
try navigating directly to it. 

The next mistake was relying on a default, easily guessable password for the
staff administrator account. If 'password' is the most commonly used password
for accounts, using your username again as your password might be the
second-most commonly used password. Default passwords like this should never be
allowed.

Stepping back from the context of this mission, the idea behind the account
compromise was to also show the value of targeting specific accounts. Even if
someone has an account with a strong password, human instinct is the weakest
link in any security setup. People are prone to falling for phishing or spear
phishing schemes which accidentally reveal account credentials, which is why
two-factor authentication using physical hardware is becoming more common
(because even two-factor authentication using SMS messages can be spoofed).

We've already tampered with cookies in other missions, but changing the user
agent provided a detail into how servers recognize users based on
characteristics like browser and device and return different content based on
those values. Last but not least, when you're trying to submit manipulated data
via a POST request, try all the techniques. Some might work and some might not,
depending on the website setup.