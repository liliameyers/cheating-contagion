# import modules
from motif_tools import *
import random

def main():
    pass


def get_all_matches_dict(kills):
    '''Takes list of kills data as input. Returns
    a dictionary where each key is a unique match id
    and each value is a list of kills in the match, 
    where each kill is a list of the killer id, 
    victim id, and kill time.'''

    # initialize dictionary for all matches
    all_matches_dict = {}

    # iterate over each kill
    for match, killer, victim, kill_time in kills:

        # if match id not an existing key,
        # create an initial match, kill pair
        if match not in all_matches_dict:
            all_matches_dict[match] = [[killer, victim, kill_time]]

        # else if match id already a key, append
        # another kill list to the match value
        else:
            all_matches_dict[match].append([killer, victim, kill_time])
            
            
    return all_matches_dict


def get_match_cheating_dict(cheater_dict, all_matches_dict, kills):
    '''Takes cheating dictionary and the list of kills
    data as inputs. Returns a dictionary where each key
    is a match id and each value is a list of two values:
    1) a list of all the match's cheater ids
    2) a list of all the match's non cheater ids.
    *Note: Each player id is labeled as the first 
    identity they appear as during a match, even in 
    a possible rare case it changes later on (e.g., if 
    during a player's first kill of a match they are a
    non-cheater, but during a later kill they are a cheater,
    this player id will be considered a non-cheater in this
    match for consistency purposes.'''

    # initialize match dictionary where each 
    # value is a list of two lists
    match_cheating_dict = {match: [[] for i in range(2)] for match in all_matches_dict}

    # iterate over each kill in the kills list
    for match, killer, victim, kill_time in kills:

        # CHEATER CHECK 1: KILLERS
        # if killer is not already in either list
        if killer not in match_cheating_dict[match][0] and\
        killer not in match_cheating_dict[match][1]:

            # and if killer is an active cheater at
            # time of kill, add id to first list
            # of the match's cheater ids
            if is_active_cheater(cheater_dict, killer, kill_time):
                match_cheating_dict[match][0].append(killer)

            # else if killer is not an active cheater,
            # add to the second list of non-cheaters
            else:
                match_cheating_dict[match][1].append(killer)

        # CHEATER CHECK 2: VICTIMS
        # if victim is not already in either list
        if victim not in match_cheating_dict[match][0] and\
        victim not in match_cheating_dict[match][1]:

            # and if victim is an active cheater at
            # time of kill, add id to cheater list
            if is_active_cheater(cheater_dict, victim, kill_time):
                match_cheating_dict[match][0].append(victim)

            # else if victim is not a cheater, 
            # add id to list of non-cheaters
            else:
                match_cheating_dict[match][1].append(victim)

    return match_cheating_dict


def get_mapping_dict(match_cheating_dict):
    '''Takes match cheating dictionary as input,
    where the keys are matches and values are lists 
    of cheaters and non cheaters in each match.
    Returns a dictionary where each key is a match id
    and each value is a nested dictionary which maps
    the match's cheaters to themselves and randomly maps 
    non-cheaters to other non-cheaters (each mapping is
    a key-value pair in the nested dictionary).'''

    # initialize mapping dictionary
    mapping_dict = {}

    # iterate over each match
    for match, cheat_lists in match_cheating_dict.items():

        # MAPPING 1: CHEATERS
        # if match has cheater(s), iterate over each
        for cheater in cheat_lists[0]:
            # if match id not already in dictionary, 
            # add initial match and cheater mapping
            if match not in mapping_dict:
                mapping_dict[match] = {cheater: cheater}
            # else append mapping to existing match id key
            else:
                mapping_dict[match][cheater] = cheater

        # MAPPING 2: NON CHEATERS
        # make a copy of the list of non-cheaters,
        # and randomize the ids for mapping
        noncheaters_copy = cheat_lists[1][:]
        random.shuffle(noncheaters_copy)

        # simulataneously iterate over each 
        # non-cheater and a corresponding 
        # random non-cheater
        for noncheater, noncheater_random in zip(cheat_lists[1], noncheaters_copy):
            # if match id not already in dictionary,
            # add initial match and the mapping of the
            # non-cheater to random non-cheater 
            if match not in mapping_dict:
                mapping_dict[match] = {noncheater: noncheater_random}
            # else append mapping to existing match id key
            else:
                mapping_dict[match][noncheater] = noncheater_random

    return mapping_dict


def get_randomized_kills(all_matches_dict, mapping_dict):
    '''Takes two inputs: 1) a dictionary where keys
    are matches and values the list of kills and 
    2) a mapping dictionary where keys are matches
    and values are dictionaries mapping cheaters to
    themselves and non-cheaters to random non-cheaters
    witin the match. Returns a list of randomized kills,
    where each kill value is represented by a list of the 
    match id, killer id, victim id, and kill time. In the
    randomized list of kills, the non-cheaters are 
    re-assigned within each match, whereas cheaters preserve
    their position in the network.'''

    # initialize list of randomized kills
    kills_random = []

    # iterate over each match and kill
    # and append to the random kills list
    # each kill value but with player ids
    # mapped using the mapping dict
    # (where non cheaters are re-assigned and 
    # cheaters are preserved)
    for match, kills in all_matches_dict.items():
        for kill in kills:
            kills_random.append([match, mapping_dict[match][kill[0]],\
                                    mapping_dict[match][kill[1]], kill[2]])

    return kills_random


def run_simulations(cheaters, kills, n_times):
    '''Takes three inputs: the list of cheaters
    and kills data and the number of times to 
    run an alternate reality simulation. 
    Returns a list where each value is the number 
    of observer-cheater motifs for each simulation,
    in order of the simulations.'''

    # get cheater dictionary of cheater start and
    # ban dates
    cheater_dict = get_cheater_dict(cheaters)

    # get dictionary of all matches and their kills
    all_matches_dict = get_all_matches_dict(kills)

    # get dictionary of all matches and lists of
    # their cheaters and non-cheaters
    match_cheating_dict = get_match_cheating_dict(cheater_dict, all_matches_dict, kills)

    # initialize motif count
    motif_count = []

    # iterate through n number of simulations
    for i in range(n_times):

        # get mapping dictionary of all matches and 
        # simulation mappings of each player
        mapping_dict = get_mapping_dict(match_cheating_dict)

        # get list of randomized kills for the second 
        # input in count_motif function and
        # append result to motif count list
        motif_count.append(count_motifs(cheaters,\
        get_randomized_kills(all_matches_dict, mapping_dict)))

    return motif_count


if __name__ == '__main__':
    main()
