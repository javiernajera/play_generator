"""
Here's an example of a skeleton you might have for Monday.  Note that your
code does NOT have to be fully-formed at this point or follow good programming
style.  This is just a quick outline of your overall plan with code.  (I made
this in about 10 minutes on the way to my ad hoc meeting today.)

Feel free to include #TODO comments as part of your outline that indicate
where you will expand (see examples below).

Again - the point of this assignment is NOT to have your computer develop an
entire script on the level of a human writer (unless you would like it to be!).
The main idea is to use play/film/TV scripts as a domain to demonstrate your
understanding of ideas in CC and explore a small, focused topic relating to this
domain (such as "agent personality modeling" or "joke generation").

I will not expect your script to be sophisticated in all degrees and dimensions
of CC. Instead, I'm just looking for you to show that you did some research in a
CC area, you have some interesting results due to that exploration, and you are
able to present and write comfortably about your work.
"""

import random

# TODO: maybe grab more names from somewhere?
CHARACTER_NAMES = ["Agnes", "Jimothy", "Twista", "Gabriel", "Nino", "Thor"]

def generate_setting():
    # TODO: don't forget to add function docstrings.
    time = random.choice(["morning", "midday", "afternoon", "night"])
    abstract_place = random.choice(["EXT.", "INT."])
    place = ""
    # TODO: maybe grab more places from somewhere?
    if abstract_place == "EXT.":
        place = random.choice(["seashore", "forest", "cliffs", "streets"])
    else:
        place = random.choice(["cave", "abandoned warehouse", "hospital"])
    return (time, abstract_place, place)

def generate_scene_description():
    return "describing the scene " * random.randint(0, 20)

def generate_dialogue():
    # TODO: make sure every character can either tell a joke or react to the
    # joke.  Research emphasis will be on generating those jokes, so this
    # will end up being a major component of my system.
    # TODO: also look into appropriate joke reactions based on who is speaking?
    # Maybe that entails emotion and memory - ask others in class for feedback
    # about this on Monday.
    return "talk " * random.randint(1, 20)

def generate_characters():
    return random.sample(CHARACTER_NAMES, random.randint(3,6))

def generate_scene(characters):
    # TODO: this will need some helper functions eventually.
    # TODO: make sure this doesn't generate the same setting consecutively.
    setting_details = generate_setting()
    # TODO: 80-char limit.
    setting = setting_details[1] + " " + setting_details[2].upper() + " - " + setting_details[0].upper()

    # State the setting.
    print('{0:<100}'.format(setting))

    # Describe the scene.
    # TODO: do I want more scene descriptions based on what happens with
    # people reacting to jokes?
    print('{0:<100}'.format(generate_scene_description()))
    print("\n")

    # Have people talk to each other.
    for dialogue in range(random.randint(3, 10)):
        speaker = random.choice(characters).upper()
        voiceover_spot = ""
        if random.randint(0, 20) == 7:
            # TODO: I wonder if a voiceover should always be a reaction.
            voiceover_spot = " (V.O)"
            # TODO: What else could I include like this?  Maybe adjectives
            # or otherwise descriptions of how the actor should act?
        print('{0:^100}'.format(speaker + voiceover_spot))
        print('{0:^100}'.format(generate_dialogue()))
        print("\n")

def generate_play():
    # Setup - organize this better later.
    characters = generate_characters()

    # TODO: include three-act structure?
    num_scenes = random.randint(3, 8)

    # TODO: generate title and be sure to name my system.
    print('{0:^100}'.format("* * * TITLE GOES HERE * * *"))
    print('{0:^100}'.format("* * * written by my awesome system * * *\n"))

    for scene in range(num_scenes):
        generate_scene(characters)

    print('{0:^100}'.format("FIN"))

if __name__ == "__main__":
    # TODO: instead of printing, should probably save to a file for evaluating
    # later.  Also need to figure out evaluation?  I'll look into scholarly work
    # relating to humor and computational creativity and come back to this.
    generate_play()
