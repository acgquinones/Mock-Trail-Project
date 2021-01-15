"""
File:    proj1.py
Author:  Ara Carmel Quinones
Date:    4/6/20
Section: 35
E-mail:  aquinon1@umbc.edu
Description:
  The task for this project is to write a UMBC trail program that mimics some functionality from Oregon Trail.
"""

SKILL_POINTS = 10
MAXIMUM_CHARACTER = 3
MINIMUM_CHARACTER = 2
STARTING_LOCATION = "The Dorms"
FINISHING_LOCATION = "ITE"
CHARISMA = "charisma"
STEALTH = "stealth"


def load_map(map_file_name):
    """
    This function must take a string which is the file name, and return the "map" or some representation of it for the rest of the game to use.
    You can add arguments to the function, but you must pass the file name.  This function must not set any global variables.

    :param map_file_name: the file's name
    :return: the map as dictionary
    """

    map = {}
    # opens and closes file and makes a list of each line from the file
    with open(map_file_name, "r") as f:
        content = f.readlines()
        # strip whitespace and split the value on the comma, if exist, to make a list
        for i in range(len(content)):
            column = content[i].strip()
            column = column.split(',')
            # if the length of the list is 1, set the element value as a dict_ key (place) and set it to an empty dictionary
            if len(column) == 1:
                place = column[0]
                map[place] = {}
            # if length is 2, first element is set as dictionary value of (place) and as dictionary key to second element that becomes a dictionary value
            elif len(column) == 2:
                destination = column[0]
                seconds = column[1]
                map[place][destination] = seconds

    return map


def load_events(event_file_name):
    """
     This function must take a string which is the file name, and return the events for the rest of the game to use.
    You can add arguments to the function, but you must pass the file name.  This function must not set any global variables.
    :param event_file_name: file's name
    :return: return the events in dictionary format
    """

    events = []
    events_dictionary = {}
    # opens and closes files and make a list of each line from the file
    with open(event_file_name, "r") as f:
        content = f.readlines()
        # strip whitespace, split on comma and create a list, append the list to events. This creates a 2d list
        for event in content:
            column = event.strip()
            column = column.split(",")
            events.append(column)
        # the first element in each event is set as a key to event_dictionaries and the rest of the element becomes a dictionary value to place as a list
        for i in range(len(events)):
            place = events[i][0]
            events_dictionary[place] = []
            for j in range(len(events[i])):
                # this ignores the first element and the remaining elements is appended to events_dictionary[place]
                if j > 0:
                    events_dictionary[place].append(events[i][j])

    return events_dictionary


def play_game(start_time, game_map, events, stats):
    """

    This function should handle most of the game functionality.
    Whatever is returned to you in load_map and load_events should go into this function, as well as the amount of time you have to play.
    You are allowed to change the arguments if you need more.  However, you need to at least take in the data contained.
    This function must not set any global variables.

    :param start_time: the starting time for the game
    :param game_map: the map's file name
    :param events: the event's file name
    :return: none. this is a print function
    """

    end = False
    original_where_to_go = ''

    # function calls
    map = load_map(game_map)
    events = load_events(events)

    time = int(start_time)
    where_to_go = STARTING_LOCATION

    while not end:

        # Print some message about where you are and how long you have left to get to ITE.
        print("You are currently in " + where_to_go + " and have " + str(time) + " seconds left to get to ITE.")

        # prints each location and seconds
        for key in map[where_to_go]:
            print(key, map[where_to_go][key])

        # no dead ends or backtracking. this prevents player to backtrack
        if original_where_to_go in map.keys():
            del map[original_where_to_go]

        # keep the old value of where_to_go to use for later as a key
        original_where_to_go = where_to_go
        # Ask where you want to go, and make sure it's a valid location.
        where_to_go = input("Where do you want to go next? ")

        # if the picked location is not valid location, keep asking for the next location to go to
        while where_to_go not in map[original_where_to_go].keys():
            where_to_go = input("Where do you want to go next? ")

        # Subtract the time from time/update time
        seconds = map[original_where_to_go][where_to_go]
        time -= int(seconds)

        # player wins if they reach ITE and there is still time left, or if time is equal to 0,  game ends
        if where_to_go == FINISHING_LOCATION and time >= 0:
            print("You made it to ITE and now can learn the secrets of computer science.  You win!")
            end = True
        # player lose if they reach ITE and time is less than 0, game ends
        elif where_to_go == FINISHING_LOCATION and time < 0:
            print("You have run out of time, and so you lose.")
            end = True

        # check if location has an event
        else:
            #if where_to_go does not have an event, if no time left, player lose, game ends
            if where_to_go not in events.keys():
                # if player runs out of time, game ends
                if time <= 0:
                    print("You have run out of time, and so you lose.")
                    end = True
            else:
                #where_to_go has an event
                if where_to_go in events.keys():
                    # check if player wins or loses the event according to his skills points
                    for i in range(len(events[where_to_go])):
                        # always print the event text (the first element)
                        if i == 0:
                            the_event = events[where_to_go][i]
                            print(the_event)
                        # compare if player's charisma meets the required charisma in element 3, the same for stealth
                        if i == 3:
                            character_charisma = stats[CHARISMA]
                            character_stealth = stats[STEALTH]
                            required_charisma = events[where_to_go][i]
                            required_stealth = events[where_to_go][i + 1]
                            # winning text: bypass the obstruction, and there is no time penalty.
                            if int(character_charisma) >= int(required_charisma) and int(character_stealth) >= int(
                                    required_stealth):
                                win_text = events[where_to_go][i - 1 - 1]
                                print(win_text)
                                #player lose the game if they run out of time, game ends. Else, keep playing the game
                                if time <= 0:
                                    print("You have run out of time, and so you lose.")
                                    end = True
                            # character's stats is not high enough, display the losing message and subtract the time penalty.
                            else:
                                lose_text = events[where_to_go][i - 1]
                                print(lose_text)
                                penalty = events[where_to_go][i + 1 + 1]
                                #if time is 0 or less than 0 even without the penalty, player lose, game ends
                                if time <= 0:
                                    print("You have run out of time, and so you lose.")
                                    end = True
                                # subtract time penalty
                                time -= int(penalty)
                                # if time runs out, player lose the game, end the game
                                if time <= 0:
                                    print("You have run out of time, and so you lose.")
                                    end = True
                                # game keeps going because the player still has time left
                                else:
                                    print("You lose", penalty, "seconds.")

def create_character():
    """
    This function should create your character by getting the name, charisma and stealthiness.
    This function should take no arguments.  This function must not set any global variables.

    :return: this returns stats. the player's charisma and stealth skill points
    """

    end = False
    stats = {}
    sum = 0

    while not end:
        # ask for the player's name and use split to make a list
        name = input("What is your name? Enter a first (middle) last separated by spaces, middle being optional: ")
        name = name.split()
        # keep going with the game if player entered 2 or 3 characters. else, keep asking for their name
        if len(name) == MINIMUM_CHARACTER or len(name) == MAXIMUM_CHARACTER:
            print("You have 10 skill points to distribute, otherwise you aren't going anywhere.")

            # if charisma and stealth does not sum to 10, keep asking for charisma and stealth
            while sum != SKILL_POINTS:
                # ask for charisma and stealth and add to sum
                charisma_points = int(input("How charismatic are you? you have " + str(SKILL_POINTS) + " skill points left: "))
                sum += charisma_points
                sneaky_points = int(input("How sneaky are you? you have " + str(SKILL_POINTS) + " skill points left: "))
                sum += sneaky_points

                # print error message if entered values are negative
                if charisma_points < 0 or sneaky_points < 0:
                    print("You have 10 skill points to distribute, they must all be positive.")
                    sum = 0

                else:
                    # add charisma and stealth to stat dictionary if they sum to 10
                    if sum == SKILL_POINTS:

                        stats[CHARISMA] = charisma_points
                        stats[STEALTH] = sneaky_points

                        return stats

                    # print lose text if charisma and stealth does not sum to 10 or if negative number is entered and set sum back to 0
                    else:
                        print("You have 10 skill points to distribute, they must all be positive.")
                        sum = 0


if __name__ == '__main__':

    map_file_name = input("What is the map file? ") # game_map_1.txt
    event_file_name = input("What is the events file? ") # game_events_1.txt
    start_time = input("How much time do you want to start with? ")

    # makes sure that user input not 0 or less than 0
    while int(start_time) <= 0:
        start_time = input("How much time do you want to start with? ")

    stat = create_character()

    #strip makes sure the input does not crash if mistakenly puts a space before and after
    play_game(start_time.strip(), map_file_name.strip(), event_file_name.strip(), stat)
