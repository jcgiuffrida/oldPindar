
Pindar

README

Pindar is a free and open-source tool to explore, collect and analyse the world's quotes.

Product Description
A free and open-source tool to explore, collect, and analyse the world’s quotes.

Contact Information

*

Web Site

*

Notice

*

/*
 * The following is text that is copied from the Google Doc.
 * To be adapted to a true README when project begins
 * taking shape.
 */

Phase I (minimum viable product)
Management
GitHub repo
web2py, perhaps with PythonAnywhere
Color scheme I think that we should keep this neutral for now 
Migrate existing quotes (~300)
Backend
MySQL database
Tables: quotes, authors, works, users, ratings, tags
Authors: including dates
Works: including year published
Every author automatically has a work named “Unknown” or “Unsourced”
Scalable to at least 10 GB
User Management
User registration (email/password or Google/Facebook)
Validation
Avoid duplicate authors and works
Consider a minimum author fame status, such as a Wikipedia page
Text of quotes should allow special characters (Unicode)
Text of quotes should allow italics or stylization
Frontend
Homepage: show random list of quotes
Quote presentation
Text, author, and work shown by default
Buttons to rate, edit, flag
“More information” shows additional information about the quote, year of the work, and user-submitted notes
AJAX pagination or infinite scroll
Higher-rated quotes should tend to rise to top, but some randomness is desirable
“About” page
User login and account management
Forms
Add quotes
Add authors and works
Basic validation (non-null, non-duplicate, length)
Functionality
Edit quotes (who should moderate?) talk about this Thursday -M
Flag quotes as offensive, duplicate, or false
Rate quotes for content and style
Search
By text, author, work, tag
Filter by rating, language
Search while typing
Option to search verbatim
Suggestion: Spotify-style multi-field search
Features
Multiple languages (start with just English and Spanish)
Unique pages and URLs for individual quotes, authors, and works
Simple duplicate detection: fuzzy string matching
User-generated tags of quotes
Plugins
JQuery stars, for ratings
http://eligeske.com/jquery/jquery-star-comment-rating/
JQuery Typing for instant search
https://github.com/lucaluca/jquery-typing
Responsive searchbox
http://yensdesign.com/2009/01/improving-search-boxes-with-jquery/
May need to install fonts for other languages (Arabic, Greek, Chinese, etc)




Phase II (More Intelligent Functionality)
Better Quote Management
Smarter de-duplication
e.g. short quotes contained in longer quotes: keep both? 
Automatic duplicate recognition based on user flagging and string matching
Interlingual capability
Determine what quotes are translations of each other
Mark which quotes are original and which are translations
Offer Google Translate translations if none available
Connections
Allow users to identify quotes which reference or allude to each other
Automatically identify full string matches (quotes quoting quotes)
Display “related quotes” in a sidebar
Show related quotes and comments on hover
Add notes to quotes (e.g. context, analysis of the quote)
Better User Engagement
Add a user scoring system visible to users, e.g. gamification
Users can collect “favorite” quotes
Social media sharing functionality
Encourage users to collect and share their favorites
Weight ratings based on user reputation
Users can only rate each quote once (can modify past ratings)
User profile pages showing quotes submitted and favorited
Additional Considerations
Add “Anonymous” as an author
how to manage the dating?
Allow multi-author books
Tied to each individual author
Allow music bands as authors
Add translators
Logo again, I am prone to getting this done right by a friend maybe
Copyright issues?




Phase III (More Analytics)
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
