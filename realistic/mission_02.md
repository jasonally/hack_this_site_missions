# Mission 2
https://www.hackthissite.org/playlevel/2/

Racist pigs are organizing an 'anti-immigrant' rally in Chicago. Help anti-racist activists take over their website!

From: DestroyFascism

Message: I have been informed that you have quite admirable hacking skills. Well, this racist hate group is using their website to organize a mass gathering of ignorant racist bastards. We cannot allow such bigoted aggression to happen. If you can gain access to their administrator page and post messages to their main page, we would be eternally grateful.

**Answer:** The nature of this mission offers a big clue. We're looking to gain access to the site's administrator page, so that means we're likely looking for a [SQL injection](https://www.w3schools.com/sql/sql_injection.asp) exploit.

Click into the mission page and either do Ctrl+A on the page's contents or check the page's elements in your browser's developer tools. Either way, you'll see a hidden link with 'update' as its anchor text. Click the link and you'll be taken to a login page. This is where we'll need to do our SQL injection magic.

I found a list of common SQL injections for bypassing login screens [here](https://www.netsparker.com/blog/web-security/sql-injection-cheat-sheet/#ByPassingLoginScreens) and I started trying them in the username box. The `admin' #` input got me the invalid username/password message, but I also got this text to appear:
```
SQL Error:

.
```

Progress. If we think back to the examples from the w3schools.com page, I believe what happened is I gave an invalid username, but then I broke the script by adding the comment tag. I need provide an input which will cause the backend SQL statement to resolve to True. Something like `' or 1=1 #`.

That didn't work either and got me the same invalid username/password message and SQL error message. But I'm close. What if I added a semicolon to terminate the SQL statement? Sure enough, `' or 1=1;` worked for me.

**Key Idea:** SQL injections can help you bypass improperly configured login windows, but they require some intuition of how the SQL query gets formulated and executed on the backend. Each SQL implementation has its syntax quirks, so keep experimenting. For me, the clue I was onto something was getting the error messages. If you're a developer, [sanitize your inputs](https://xkcd.com/327/).