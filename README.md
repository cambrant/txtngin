txtngin (TextEngine) is a simple experiment with web.py which runs a web
server and allows users to create, edit and delete static text files on the
server.

In addition to the simple wiki-like behavior, if a file is prepended with a line
containing the following string:
```
!py
```
it will allow the user to manipulate the text (or anything really) with Python
code. For example, the user can write one text file (think a wiki page) and then
process the contents of that file in another file which runs as a script. An
example is included under /contents/, where "today" pulls and processes data
from "tobuy" and "todo".
