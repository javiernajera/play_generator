## READ ME for play_generation.py

### Overview

My system attempts to create a set of characters, assign them roles
based on assigned interests, and then have them create dialogue based on those
roles. The interests of every character affects the kinds of things that will
be reflected in their dialogue.  I identified three parts (informative,
contemporary, and comedic) of speech that would be useful to model a
conversation between characters, that actively tries to reflect things the
character might be interested in.

### Setup
These are the imports and dependancies you need to run play_generator.py:

* import re
* import random
* import wikipedia as wiki
* import textrazor
* import io


you will also need to have these files in your directory:

*conan_jokes.text
url_text.txt
play_generator.py
places.txt
categories.txt
story_generator.py
api_key.text*


This system was built using python 3.6

NOTE: their is a bug in the system where when you run the program
it will not end, and I'm not sure what it could be!

you run the program with this command:

python3 play_generator.py

### System Architecture

Originally the system was supposed to take a script or list of scripts and
perform an analysis on the text using an LTSM.  I landed on the LSTM after
having read some of the implementations done with the TWISTA system
() and the ___ system.  In both systems, they had very formal ways of both
representing events or episodes that could happen with the narrative
generation.  It makes sense though, because their system perform very complex
tasks that needs many details to accomplish what they were after.
