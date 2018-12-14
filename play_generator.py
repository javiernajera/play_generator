import re
import random
import wikipedia as wiki
import textrazor
import io

"""These variables are used to generate names and to generate category based dialogue"""

CHARACTER_NAMES = ["Kanye", "James", "Javier", "Llewllyn", "Erika", "Lizzi", "Ximena", "Rosa", "Iliana", "Julio", "Estela", "Evelyn", "Agnes", "Jimothy", "Twista", "Gabriel", "Nino", "Thor", "Trump", "Godfather"]
CATEGORIES = ["NEWS", "POLITICS", "DONALD TRUMP", "FOOD", "SCIENCE", "SPORTS", "RELIGION", "FILM", "MUSIC", "SPONGEBOB"]
NUM_CHARACTERS = 0

"""*******************************EXTRACTING KNOWLEDGE***********************"""

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

"""*******************************MARKOV CHAIN FUNCTIONS***********************"""
def generate_contemporary_chain(interest):
    """
    This method generates a markov chain based on local knowledge that
    I pulled from raw text of various different online articles.
    """
    file = open("url_text.txt", "r")
    delim = interest + ":"
    at_topic = False
    text = ""
    for line in file.readlines():
        if "next_category" in line and at_topic:
            break
        elif at_topic:
            if '~' not in line and len(line) != 1:
                line = line.replace("\n", "")
                text += line
        elif delim in line:
            at_topic = True
    text = re.sub("\s\s+", " ", text)
    text = text.replace('"',"")
    chain = build_chain(text)
    return chain

def generate_informative_chain(interest):
    """
    This method generates a markov chain based on wikipedia articles that
    are found by searching through the list of topics that are produced by
    the characters given interest.
    """
    topics = get_topics(interest)
    num_articles = random.randint(3,5)
    while num_articles > 0:
        results = wiki.search(random.choice(topics))
        found_page = False
        #somtimes returns disambiguation error
        while not found_page:
            try:
                page = wiki.page(random.choice(results))
                found_page = True
            except wiki.exceptions.DisambiguationError as e:
                continue


        content = page.content.splitlines()
        knowledge = ""
        #filtering some wikipedia data stuff out of the lines
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

def generate_funnies():
    """This function generates the markov chain from the formatted Conan jokes"""
    file = open("conan_jokes.txt", "r")
    text = ""
    for line in file.readlines():
        if len(line) != 1:
            text += line

    text = re.sub("\n+", "", text)
    chain = build_chain(text)
    return chain
    #return places_list
def build_chain(text):
    """This method builds a first order markov chain with the given text."""
    markov_chain = {}
    index = 1
    #this line is trying to remove words that happen to have a dot in
    #between them
    #text = re.sub(".*[\.].*", ".*[\.\s].*", text)
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
    funny_chain = {}
    for key, interest in interests.items():
        informative_chains[key] = generate_informative_chain(interest)
        contemporary_chains[key] = generate_contemporary_chain(interest)

    funny_chain = generate_funnies()
    return informative_chains, contemporary_chains, funny_chain

"""*******************************GENERATING PLAY SCRIPT***********************"""

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
    return (place, time)
#def generate_chains(interests):
def generate_dialogue(chains, word_count_max, sample):
    """this is used to create dialogue, it basically mixes up what sort of
    phrases the characters are saying.  Sometimes a character will say something
    informative about their interest or say something thats contemporary about
    their interests"""
    informative = chains[0]
    contemporary = chains[1]
    funnies = chains[2]
    dialogue = ""


    word_count = random.randint(word_count_max*.20, word_count_max)
    for character in sample:
        dialogue += character + ":\t"
        randint = random.randint(0, 100)
        if randint < 25:
            dialogue += generate_lines(informative[character], word_count) + "\n\t"
            dialogue += generate_lines(funnies, word_count)
        elif randint < 50:
            dialogue += generate_lines(contemporary[character], word_count)+ "\n\t"
            dialogue += generate_lines(funnies, word_count)
        elif randint < 60:
            dialogue += generate_lines(contemporary[character], word_count)
        elif randint < 70:
            dialogue += generate_lines(informative[character], word_count)
        elif randint < 80:
            dialogue += generate_lines(contemporary[character], word_count)+ "\n\t"
            dialogue += generate_lines(informative[character], word_count)
        elif randint < 90:
            dialogue += generate_lines(contemporary[character], word_count)+ "\n\t"
            dialogue += generate_lines(informative[character], word_count)
        else:
            dialogue += generate_lines(funnies, word_count)
        dialogue += "\n\n"

    return dialogue


def get_character_sequence(characters):
    """generates a sequence of character from character list"""
    prev_character = random.choice(characters)
    sequence = [prev_character]
    rand_num = random.randint(6,13)
    while rand_num > 0:
        character = random.choice(characters)
        if prev_character != character:
            sequence.append(character)
            rand_num -= 1
            prev_character = character
    return sequence

def generate_lines(chain, word_count):
    """uses markov chain and word_count to generate lines of dialogue"""

    prev_word = random.choice(list(chain.keys()))
    while '.' in prev_word and '."' in prev_word and ')' in prev_word:
        print(prev_word)
        prev_word = random.choice(list(chain.keys()))

    prev_word.capitalize()
    dialogue = prev_word + " "
    #word_count = random.randint(35, 70)
    break_limit = 7
    count = 0
    line_done = False
    while not line_done:
        if count % break_limit == 0 and count != 0:
            dialogue += "\n"
            dialogue += "\t"
        found = False
        #make sure that the key is actually in the dictionary
        while not found:
            try:
                curr_word = random.choice(chain[prev_word])
                found = True
            except KeyError as error:
                continue

        dialogue += curr_word + " "
        count += 1
        if len(dialogue.split(' ')) >= word_count:
            if '.' in curr_word:
                line_done = True
        prev_word = curr_word
    print("choosing words")
    return dialogue

def generate_scene(characters, chains):
    """Generates scene by randomly choosing location and places
    depending on the characters and their corresponding markov
    chains, it will also generate dialogue"""
    setting_details = generate_setting()
    setting = "Place: " + setting_details[0].upper() + " \nTime: " + setting_details[1].upper() + "\n\n"
    char_list = get_character_sequence(characters)
    print("creating dialogue")
    scene = generate_dialogue(chains, 40, char_list)

    # State the setting.
    return setting + scene


def generate_characters():
    """returns a random sample of 4-7 characters from all possible characters"""
    return random.sample(CHARACTER_NAMES, random.randint(4,7))


def generate_play():
    """this function generates a list of characters and assigns them all a specific
    interest from the interests list. It then uses every characters interest to creates
    three specific markov chains.  An informative chain, a contemporary chain, and a
    funny chain that they all share.  It uses all these chains to create dialogue
    that is specific to every characters interest, and it occasionally generates
    dialogue from the funny chain to add in some comedy.  It suprisingly does a good
    job at generating odd, but amusing dialogue."""

    characters = generate_characters()
    interests = generate_interests(characters)
    NUM_CHARACTERS = len(characters)


    informative_chains, contemporary_chains, funny_chain = generate_chains(interests)
    chains = [informative_chains, contemporary_chains, funny_chain]
    num_scenes = random.randint(2, 4)
    script = ""

    """it will generate dialogue for a given number of scenes"""
    while num_scenes > 0:
        print("starting first scene")
        character_set = random.sample(characters, random.randint(3, NUM_CHARACTERS))
        script += generate_scene(characters, chains)
        script += "\n"
        if num_scenes != 1:
            script += "*****************************NEXT SCENE****************************\n\n"
        num_scenes -= 1



    print('{0:^100}'.format("* * * Crude Experts * * *\n"))
    print('{0:^100}'.format("* * * written by my awesome system * * *\n\n"))


    print('{0:^100}'.format(script))


    print('{0:^100}'.format("FIN"))




if __name__ == "__main__":
    generate_play()
    #famous_places = generate_famous_locations()
    #print(places)













"""**********************************STUFF I DIDN'T USE*********************"""



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

'''
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
            line = re.sub("\s\s+", " ", line)
            line = re.sub("\n+", "", line)
            places_list.append(line)

        elif "Famous" in line:
            famous = True

    return places_list
'''
