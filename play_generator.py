from nltk.corpus import wordnet
import re
import random
import wikipedia as wiki
import textrazor
import io

"""These variables are used to generate names and to generate category based dialogue"""

CHARACTER_NAMES = ["Kanye", "James", "Javier", "Llewllyn", "Erika", "Lizzi", "Ximena", "Rosa", "Iliana", "Julio", "Estela", "Evelyn", "Agnes", "Jimothy", "Twista", "Gabriel", "Nino", "Thor", "Trump", "Godfather"]
CATEGORIES = ["NEWS", "POLITICS", "DONALD TRUMP", "FOOD", "SCIENCE", "SPORTS", "RELIGION", "FILM", "MUSIC", "SPONGEBOB"]
NUM_CHARACTERS = 0


def generate_famous_locations():
    """This method generates a list of famous locations from the places.txt file"""

    file = open("places.txt", "r")
    places = open("places.txt", "r").read()
    split_places = places.split("Famous Places:")
    # TODO: don't forget to add function docstrings.
    places_list = []
    famous = False
    for line in file.readlines():

        if famous:
            line = re.sub("\s\s+", "", line)
            line = re.sub("\n+", "", line)
            places_list.append(line)

        elif "Famous" in line:
            famous = True

    return places_list


def extract_links(interest):
"""
extract_links uses a characters given interest to grab a list of url's
to webpages that contain articles that are centered on the characters
interest
"""
    file = open("categories.txt", "r")
    delim = interest + ":"
    at_topic = False
    links = []
    for line in file.readlines():
        if "next_category" in line and at_topic:
            break
        elif at_topic:
            line = line.replace("\n", "")
            links.append(line)
        elif delim in line:
            at_topic = True

    return links

def get_topics(interest):
    """
    This method uses the textrazor api to detect common themes or
    topics that are relevant to the articles that are extracted from
    the a characters interest.
    """
    textrazor.api_key = "bea046ca0432a5061367782a082afca77741c83df2a2b7da09e2a075"
    client = textrazor.TextRazor(extractors=["entities", "topics"])
    client.set_cleanup_mode("cleanHTML")
    client.set_classifiers(["textrazor_newscodes"])

    links = extract_links(interest)
    topic_list = []
    sample_links = random.sample(links, 2)
    for link in sample_links:
        response = client.analyze_url(link)

        for topic in response.topics():
            if topic.score > 0.85:
                if topic.label not in topic_list:
                    topic_list.append(topic.label)
    return topic_list


def generate_informative_chain(interest):
    """
    This method generates a markov chain based on wikipedia articles that
    are found by searching through the list of topics that are produced by
    the characters given interest.
    """
    file = open("url_text.txt", "r")


    topics = get_topics(interest)


    num_articles = random.randint(3,5)
    while num_articles > 0:
        results = wiki.search(random.choice(topics))
        page = wiki.page(random.choice(results))

        content = page.content.splitlines()
        knowledge = ""
        for line in content:
            if "== Notes ==" in line or "== References ==" in line:
                break
            if "==" in line:
                continue
            else:
                knowledge += line

        num_articles -= 1

    knowledge = re.sub("\n+", "", knowledge)
    knowledge = knowledge.replace('"',"")
    chain = build_chain(knowledge)
    return chain


    #return places_list
def build_chain(text):
    """This method builds a first order markov chain with the given text."""

    markov_chain = {}
    index = 1
    text_arr = text.split(' ')
    for w in text_arr[index:]:
        prev_state = text_arr[index - 1]
        if prev_state in markov_chain:
            markov_chain[prev_state].append(w)
        else:
            markov_chain[prev_state] = [w]
        index += 1

    return markov_chain

def generate_chains(interests):
    """This method generates the three distinct markov chains the system
    uses to generate dialogue.  It makes an informative, contemporary, and comedic
    chain"""

    informative_chains = {}
    contemporary_chains = {}
    for key, interest in interests.items():
        informative_chains[key] = generate_informative_chain(interest)
        #contemporary_chains[key] = generate_contemporary_chain()
    return informative_chains

def generate_interests(characters):
    """This method just assigns intersts to each character based on the
    categories list"""

    interests = {}
    for character in characters:
        if character == "Trump":
            interests[character] = "DONALD TRUMP"
        else:
            interests[character] = random.choice(CATEGORIES)
    return interests

def generate_setting():
    """This method generates a setting from places.txt file"""

    file = open("places.txt", "r")
    places = open("places.txt", "r").read()
    split_places = places.split("Famous Places:")
    # TODO: don't forget to add function docstrings.
    places_list = []
    for line in file.readlines():
        if "Famous" not in line:
            line = re.sub("\s\s+", "", line)
            line = re.sub("\n+", "", line)
            places_list.append(line)



    time = random.choice(["morning", "midday", "afternoon", "evening", "night"])

    place = random.choice(places_list)
    print("I chose " + place)
    return places_list
#def generate_chains(interests):
def generate_dialogue(chain, word_count):
    """this is used to create dialogue"""
    
    prev_word = random.choice(list(chain.keys()))
    dialogue = prev_word + " "
    #word_count = random.randint(35, 70)
    while len(dialogue.split(' ')) < word_count:

        curr_word = random.choice(chain[prev_word])
        dialogue += curr_word + " "
        prev_word = curr_word
    return dialogue

def generate_play():
    # Setup - organize this better later.
    characters = generate_characters()
    interests = generate_interests(characters)
    NUM_CHARACTERS = len(characters)
    print(characters)
    print(interests)
    informative_chains = generate_chains(interests)
    print(informative_chains)
    print(generate_dialogue(informative_chains[characters[0]]))
    '''
    # TODO: include three-act structure?
    num_scenes = random.randint(3, 8)

    # TODO: generate title and be sure to name my system.
    print('{0:^100}'.format("* * * TITLE GOES HERE * * *"))
    print('{0:^100}'.format("* * * written by my awesome system * * *\n"))

    for scene in range(num_scenes):
        generate_scene(characters)

    print('{0:^100}'.format("FIN"))
    '''
def generate_characters():
    return random.sample(CHARACTER_NAMES, 1)


if __name__ == "__main__":
    generate_play()
    #famous_places = generate_famous_locations()
    #print(places)

















'''
def generate_mood():
    places = generate_setting()
    wn_lemmas = set(wordnet.all_lemma_names())
    syns = wordnet.synsets("science")
    synonyms = []
    antonyms = []

    for syn in wordnet.synsets("politics"):
        for l in syn.lemmas():
            synonyms.append(l.name())
            if l.antonyms():
                antonyms.append(l.antonyms()[0].name())

    print(synonyms)
    print(antonyms)

    for place in places:
        place = place.lower()
        place = place.replace(" ", "_")

        if place in wn_lemmas:
            syns = wordnet.synsets(place)
            print(syns[0].name())

'''
