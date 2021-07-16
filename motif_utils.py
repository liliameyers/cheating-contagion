# import modules
from datetime import timedelta

def main():
    pass


def get_cheater_dict(cheaters):
    '''Takes the list of cheaters data as input.
    Returns a dictionary where each key is a cheater id
    and each value is a corresponding list of two values:
    1) datetime when player estimated to start cheating
    2) datetime when the cheater was banned for cheating'''

    return {cheater[0]: [cheater[1], cheater[2]] for cheater in cheaters}


def is_active_cheater(cheater_dict, cheater_id, datetime_ref):
    '''Takes three inputs: 1) the cheater dictionary
    of cheater ids and corresponding cheating start
    and ban dates, 2) a player id to check, and
    3) a datetime to check if the player is a
    cheater at the time. Returns True or False if
    the player is an active cheater at the time
    (i.e., time is between start and ban date).'''

    # if id is a cheater,
    if cheater_id in cheater_dict:
        # and if datetime ref is between
        # cheating start and ban date, 
        # cheater is active
        if cheater_dict[cheater_id][0] < datetime_ref < cheater_dict[cheater_id][1]:
            return True
        # else cheater is not active
        else:
            return False
        
    # else id is not a cheater
    else:
        return False

    
def get_cheater_kills_dict(cheater_dict, kills):
    '''Takes two inputs: 1) the dictionary of cheaters
    and 2) list of kills data. Returns a dictionary
    where each key is a match id with active cheaters, 
    and each value is a corresponding nested dictionary,
    where the keys are the match's cheater ids and the 
    values are a list of the cheater's kill times during
    the match.'''

    # initialize cheater kills dictionary
    cheater_kills_dict = {}

    # iterate over each kill
    for match, killer, victim, kill_time in kills:

        # if killer is active cheater
        if is_active_cheater(cheater_dict, killer, kill_time):

            # and if match id not in keys,
            # add match, killer, and kill time 
            # to dictionary 
            if match not in cheater_kills_dict:
                cheater_kills_dict[match] = {killer: [kill_time]}

            # else if match id already in keys
            else:
                # and if killer id doesn't exist,
                # add killer and kill time to match dict
                if killer not in cheater_kills_dict[match]:
                    cheater_kills_dict[match][killer] = [kill_time]

                # else killer id already exists,
                # add their latest kill time
                else:
                    cheater_kills_dict[match][killer].append(kill_time)
    
    return cheater_kills_dict


def get_third_kill_dict(cheater_kills_dict):
    '''Takes cheater kills dictionary as input, where
    keys are match ids and values are dictionaries
    of killer cheaters and a list of their kill times.
    Returns a dictionary where each key is a match id
    and each value is the earliest third kill time of all
    active cheaters within the match (i.e., the minimum
    number of kills by cheaters for another player to
    possibly observe cheating).'''

    # initialize dictionary
    third_kill_dict = {}

    # iterate over each match
    for match, killers in cheater_kills_dict.items():
        # iterate over each killer cheater in match
        for killer, kill_times in killers.items():

            # if killer has killed more than three
            # times, store time of third kill
            if len(kill_times) >= 3:
                third_kill = sorted(kill_times)[2]

                # if match id not in keys, add match
                # and third kill time to dictionary
                if match not in third_kill_dict:
                    third_kill_dict[match] = third_kill

                # if match in keys, and third kill time
                # is earlier than the current stored, 
                # update the earliest third kill time
                else:
                    if third_kill < third_kill_dict[match]:
                        third_kill_dict[match] = third_kill

    return third_kill_dict


def count_motifs(cheaters, kills):
    '''Takes the lists of cheaters and kills data as
    inputs. Returns the number of observer-cheater
    motifs, which is when a player A becomes a
    cheater within five days of observing cheating,
    either by: 1) being killed in a game after a
    cheating player B kills at least three others
    2) being killed by a cheating player B.'''

    # get cheater dictionary of cheater start
    # and ban dates
    cheater_dict = get_cheater_dict(cheaters)

    # get cheater kills dictionary of all 
    # cheater kills in each match
    cheater_kills_dict = get_cheater_kills_dict(cheater_dict, kills)

    # get third kill dictionary of the third
    # kill time in each match
    third_kill_dict = get_third_kill_dict(cheater_kills_dict)

    # initialize motif count
    motif_count = 0

    # iterate over each kill
    for match, killer, victim, kill_time in kills:

        # MOTIF CHECK 1:
        # if the victim is in a match where an active
        # cheater killed 3+ times, and the victim is 
        # killed (by anyone) after the third kill of
        # a cheater in the match
        if ((match in third_kill_dict and kill_time > third_kill_dict[match])\
        
        # MOTIF CHECK 2: 
        # OR if the killer of the victim is an active cheater     
        or is_active_cheater(cheater_dict, killer, kill_time)):

            # AND the victim becomes an active cheater between
            # 0-5 days after killing, then add to motif count
            if victim in cheater_dict and\
            kill_time < cheater_dict[victim][0] < kill_time + timedelta(days = 5):
                motif_count += 1

    return motif_count


if __name__ == '__main__':
    main()
