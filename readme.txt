
Pindar

README

Pindar is a free and open-source tool to explore, collect and analyse the world's quotes.

Product Description
A free and open-source tool to explore, collect, and analyse the world’s quotes.

Contact Information

* jcgiuffri@gmail.com
* mrbeskin@gmail.com

Web Site

* 

Notice

* 

/*
 * The following is text that is copied from the Google Doc.
 * To be adapted to a true README when project begins
 * taking shape.
 */


1) Create basic MySQL database with web2py backbone
MySQL database: see 6/23 email
allow user to add quotes
allow user to view quotes (e.g. first 20)
allow user to search quotes (basic text search of all fields combined)
populate with existing quotes
2) User management
user registration forms: email/password
user login
basic profile page
account deletion (does NOT delete their quotes)
3) Validation of quotes, authors, and works
basic validation: non-null, non-duplicate, minimum length
for authors, use birth date or wikipedia page to differentiate
for quotes, use N-length strings (exact duplicates)
ask user whether they are duplicates
Allow multi-author books
Tied to each individual author
Allow music bands as authors
Add translators
4) Better user manipulation of database
propose edits to quotes
we would moderate
flag quotes as offensive, duplicate, or false
rate quotes (one dimension or two? style/content)
tag quotes (user-generated tags)
5) More detailed/flexible quotes
Every author automatically has a work named “Unknown” or “Unsourced”
Add “Anonymous” as an author - always unique
Text of quotes should allow italics or stylization
Text of quotes should allow special characters (Unicode)
Allow comments on quotes
Allow notes on quotes (by original submitter) - e.g. chapter name, context
More languages (may need to install fonts)
6) Advanced search functionality
By text, author, work, tag
Filter by rating, language
Sort by rating, date submitted, date of work
Pagination (AJAX? infinite scroll?)
suggestion: Spotify-style multi-field search
fuzzy string matching for deduplication and search
7) Site Structure
Consistent headers on all pages
Homepage: random list of quotes
higher-rated quotes should tend to rise to top, with some randomness
“About” page
Unique pages and URLs for individual quotes, authors, and works
8) Better, prettier UX
OpenID
Unified, basic style
Add CSS to all the forms
Attractive quote presentation
Text, author, and work shown by default
“More information” button shows notes, comments, and information such as the year of the work, dates of the author, ratings
9) Links between quotes
Short quotes contained in longer quotes: keep both?
Interlingual capability: link quotes that are translations of each other
Mark which quotes are original and which are translations
Offer Google Translate translations if none available
“This quote is related to this other one”: user-submitted connections: influence, allusions, etc
Display “related quotes” in a sidebar next to each quote
Show related quotes and comments on hover
10) User curation of quotes
Users can collect “favorite” quotes
Social media sharing functionality
Encourage users to collect and share their favorites
Weight ratings based on user reputation
Users can only rate each quote once (can modify past ratings)
User profile pages showing quotes submitted and favorites
Add a user scoring system visible to users, e.g. gamification
11) Improved design and UX
Logo (by someone else)
color scheme
search while typing
Stars or icons for ratings









12) Analytics
Quote generation
Automatic quote population from a poem or work
How to separate wheat from chaff?
With a sizeable body of existing quotes, could automatically “score” each new quote by likelihood of being influential
machine learning techniques based on vocabulary, style, age, author, length
Automatic quote rating (also machine learning)
Content
Put up full works that are in the public domain (e.g. poems, very short fiction)
Fully integrate quote connections on hover over the text
Analysis
Try to predict what quotes are talking to each other
Try to determine “influence” and rank authors by that
Smarter analysis of user ratings
What separates the great quotes from the okay ones?
Track development of an idea or phrase over time, perhaps using visual organization like a timeline
