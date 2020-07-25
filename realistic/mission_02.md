# Mission 2
https://www.hackthissite.org/playlevel/2/

- [Overview](#overview)
- [Solution](#solution)
- [Key Concept](#key-concept)
- [Key Ideas](#key-ideas)

## Overview
Racist pigs are organizing an 'anti-immigrant' rally in Chicago. Help
anti-racist activists take over their website!

From: DestroyFascism

Message: I have been informed that you have quite admirable hacking skills.
Well, this racist hate group is using their website to organize a mass gathering
of ignorant racist bastards. We cannot allow such bigoted aggression to happen.
If you can gain access to their administrator page and post messages to their
main page, we would be eternally grateful.

## Solution
The nature of this mission offers a big clue. We're looking to gain access to
the site's administrator page and it's unlikely it's as simple as finding the
correct username and password. So, this means we're likely looking for some sort
of authentication bypass.

Click into the mission page and either do Ctrl+A on the page's contents or check
the page's elements in your browser's developer tools. You'll see a hidden link
with 'update' as its anchor text. Click the link and you'll be taken to a login
page. Absent any other indicators, this setup suggests we're likely looking for
a [SQL injection](https://www.w3schools.com/sql/sql_injection.asp) exploit.

Before jumping right to what the solution looks like, it's important to consider
what's happening on the backend when you provide a username and password. The
site is likely running a SQL query to see if the provided username and password
combination exist in a database. But the code probably looks something like this
[example](https://www.w3schools.com/sql/sql_injection.asp#:~:text=SQL%20Injection%20Based%20on%20%22%22=%22%22%20is%20Always%20True):
```
uName = getRequestString('username');
uPass = getRequestString('password');

sql = "SELECT * FROM [Users] WHERE Name ='" + uName + "' AND Pass ="' + uPass + "'"
```

If username = 'John Doe' and password = 'myPass', the SQL statement would look
something like this:
`SELECT * FROM Users WHERE Name ='John Doe' AND Pass ='myPass'`

I found a list of common SQL injections for bypassing login screens
[here](https://www.netsparker.com/blog/web-security/sql-injection-cheat-sheet/#ByPassingLoginScreens)
and I started trying them in the username box. The `admin' #` input got me the
invalid username/password message, but this text also appeared below the
message: 
```
SQL Error:

.
```

Thinking back to the above example, I think what happened is I gave an invalid
username, then I broke the script and triggered the error. That might be because
`admin' #` was interpreted by the backend as something like this:
`SELECT * FROM Users WHERE Name ='admin' #'AND Pass ='myPass'`

admin is probably an invalid username, but then the # commented out the rest of
the query, mangling it and causing the error message. This is promising because
we triggered an unexpected error. Now we just need to use this unexpected error
to our advantage to get into the site.

Researching further, I learned about the [1=1
trick](https://www.w3schools.com/sql/sql_injection.asp#:~:text=SQL%20Injection%20Based%20on%201%3D1%20is%20Always%20True&text=The%20original%20purpose%20of%20the,with%20a%20given%20user%20id.&text=The%20SQL%20above%20is%20valid,1%3D1%20is%20always%20TRUE.).
1=1 defaults to True in a SQL query, so if used correctly it might work in our
SQL injection input. I tried the input `' OR 1=1 #`, which on the backend would
become something like: 
`SELECT * FROM Users WHERE Name ='' OR 1=1 #'AND Pass ='myPass'`.

That didn't work either. I got the same invalid username/password message plus
the SQL error message. But getting the SQL error messages suggests I'm still on
the right track. If commenting out the rest of the query doesn't work, maybe
prematurely terminating the statement with a semicolon will. Sure enough, `' OR
1=1;` worked. It effectively turned the  query on the backend into this:
`SELECT * FROM Users WHERE Name ='' OR 1=1;`

After finding this initial solution, I also found `' OR '1=1'` worked, too. So,
the working solutions I found:
`' OR 1=1;`
`' OR '1=1'`

## Key Concept
SQL injection, specifically login bypassing

## Key Ideas
SQL injections are an effective way to target databases, but they require you to
first glean some intuition on how the SQL query gets formulated and executed on
the backend. There are also multiple SQL standards and database conventions. So,
once you have the query intution down you might still need to experiment with
syntax and work through error messages. SQL injections can serve several
purposes, but in this mission it allowed us to bypass a login screen.

This mission also reminded me of the classic xkcd comic about [query
inputs](https://xkcd.com/327/). It's important for web developers to sanitize
user inputs to prevent a SQL injection vulnerability.