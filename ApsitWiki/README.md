# Wiki-clone

#### Commands 
python manage.py runserver

#### Packages needed

markdown2

### Overview:

Wikipedia like website that consists of entries on various topics. All entries are listed at the homepage (_index.html_). Clicking on an entry will bring you to the entry page, with the url of the ENTRY as: `/wiki/ENTRY`. Going to a page that does not exist will bring the user to an error page saying that the webpage does not exist (_error.html_). A user can create a new page for an entry that is not in the list of entries `/create` (_create.html_), or they can also edit an existing entry `/wiki/edit?title=ENTRY` (_edit.html_). Users can use markdown to style their entries. A user can search through the list of entries by using the text box in the side pannel `/search/` (_search.html_)..
