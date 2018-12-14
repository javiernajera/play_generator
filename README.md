## READ ME for play_generation.py

### Overview

My system Joyful James attempts to create a set of characters, assign them
roles based on assigned interests, and then have them create dialogue based  
on those roles. The interests of every character affects the kinds of things
that will be reflected in their dialogue.  I identified three parts
(informative, contemporary, and comedic) of speech that would be useful to
model a conversation between characters, that actively tries to reflect
things the character might be interested in.

### Setup
This system was built using python 3.6. These are the imports and dependancies
you need to run play_generator.py:

* import re
* import random
* import wikipedia as wiki
* import textrazor
* import io


you will also need to have these files in your directory:

* conan_jokes.text
* url_text.txt
* play_generator.py
* places.txt
* categories.txt
* story_generator.py
* api_key.text


NOTE: there is a bug in the system where when you run the program
it will not end, and I'm not sure what it could be!
you run the program with this command:

python3 play_generator.py

### System Architecture

Originally the system was supposed to take a script or list of scripts and
perform an analysis on the text using an LTSM.  I landed on the LSTM after
having read some of the implementations done with the TWISTA system
(Platts, Blandford, & Hyucks) and the Twister system.  In both systems, they
had very formal ways of both representing events or episodes that could happen
with the narrative generation.  It makes sense though, because their system
perform very complex tasks that needs many details to accomplish what they
were after.

In twister they had seed shots that they used to produce what they called
glosses. And they use backwords reasoning on all the seed shots to create
a 'concealed story' that will later replace the 'overt story'. To create
the 'concealed story', they leverage a huge knowledge base of lexical scripts
which they create using prolog.  I knew that I would not be able to create a
system such as this, so I looked at some different avenues.

The next model I looked at was a system created by Cheong & Young that
attempted to model suspense. In a similar vain to the Twister model, they
had very sophisticated data structures and algorithms to be able to be able
to accomplish the suspense they were after.  I then settled for the idea you
put forward on the skeleton of code you sent, the generation of jokes.

I found a paper by He Reu that attempted to create jokes by using a recurrent
neural network that made use of Long Short Term Memory (LSTM) analysis to
achieve its results.  I found a tutorial online that was made by Pranjal
Srivastava at this link:

https://www.analyticsvidhya.com/blog/2018/03/text-generation-using-python-nlp/

and decided that by using Keras, it would not be too hard to build knowledge
bases that I could utilize to simulate dialogue.  

My plan at this point was to create a list of categories.  And using those
categories I would create three bodies of knowledge (informative,
contemporary, and comedic) For every category I would pull information from
articles that I found online to generate knowledge that was what I would call
contemporary. And by that I mean knowledge that is more reflective about
people's own opinion over the topic.  So a lot of the knowledge for the
contemporary knowledge bases are articles that are centered on a given
category. I would then make use of the knowledge by performing an LSTM
analysis on it.

This next form of knowledge I wanted to create was informative.  I used
an API called TextRazor to perform a classification analysis on the articles
I collected (Over 50 articles for 10 categories). (I thought that the API would
also let me collect the data, but it actually did not have that functionality.
So I had to go through every article and collect the raw data by hand and
have the knowledge base be saved locally in the URL_text.txt). The informative
would be created by performing an LSTM analyis on wikipedia articles that were
pulled from the TextRazor API. This knowledge would be more technical and
factual instead of personal and opinionated.

The last form of knowledge I wanted to create was comedic (because everyone
loves funny people! and because of He Reu's paper).  I actually used
a data set of Conan jokes that He Reu also used to create his model.  
I would then make use of the knowledge around the Conan data by performing
a LSTM analysis on it as well.  

Now I could make use of all of three of the NN's I had created to randomly
generate dialogue for characters that was dependent on the given interest
that was assigned to them.

The problem was that I unfortunately could not use the Keras API and to
manually encode an LSTM would be impossible to do with my timeframe. So I
settled for a Markov chain analysis to replace the LSTM analysis. The
result is that it is much less coherent, but it still comes up with some
pretty amusing content.

To generate the dialogue to fit the form of a play, I just built some
methods to frame the dialogue in a way that feels like it is being
told as a play.

A block diagram is available in the repository, and it represents how
the system is modeled.  The file is called "Generate_play.png"

### Computational creativity

In terms of Jordanous' SPECS, my system can be seen as creative when you
consider it's knowledge base and the variety, diversity and experimentation
that it is able to leverage with the markov chains.  The system has the
ability to collect a lot of data that is on the internet, and if I was
able to actually use LSTM RNN's then I could have leveraged the knowledge
base a lot more. Even though that's not the case because I used a markov
chain analysis, it is a able to achieve a lot more variety and diversity in
its output, which could lead to a lot of inspiration for experimentation. If
you look at the first three script generations, the dialogues generated at
the beginning are very amusing. I believe that these two metrics (the
knowledge base and the variety, diversity, and experimentation of the system)
support a basis for the Joyful James system to be considered creative.

### Personal Challenges
This project really challenged me to come up with a plan to model something
that is complex as narrative and trying to make it somewhat coherent
and interesting. I think that doing the research let me realize some of the
useful techniques that people have developed to analyze and represent
narrative.  I feel like the model I came up with originally (with the LSTMs)
would have been very interesting. I think that once I can figure out my
difficulties with Keras and see what else I could do with the system. I think
that I am not bad at being creative when it comes to things like music, but
it was really hard for me to come up with a model with something like
narrative. I feel as though I need my system to be very objective or else I
don't feel confident in being able to program something. But I think
ultimately I was able to create or have the ability to create something that
I never thought I would be able to develop. 
