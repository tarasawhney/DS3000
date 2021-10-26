# Part 1
def get_coop_copycat(opp_last_coop=True):
    """ copies the opponents last strategy 
    
    Args:
        opp_last_coop (bool): True if opponent chooses to
            cooperate in last round, otherwise False
            
    Returns:
        coop_copycat (bool): True if copycat cooperates
            in current round, otherwise False    
    """
    return opp_last_coop
    
 # test cases
assert get_coop_copycat(opp_last_coop=True) == True
assert get_coop_copycat(opp_last_coop=False) == False

#Part 2 
import numpy as np

def get_coop_friendly():
    """ cooperates 90% of the time 
    
    Returns:
        coop_friendly (bool): True if friendly cooperates
            in current round, otherwise False    
    """
    p_coop = .9
    coop = np.random.choice((0, 1), size=1, p=(1 - p_coop, p_coop))
    return bool(coop)

#Part 3 
# one way to test if the random function works is to ensure that if we run it many 
# times the result is close to its expected value.  In other words, our friendly
# player should produce about 900 cooperates given 1000 rounds of playing.  we'll
# check if they're between 800 and 1000
friendly10k = 0
for _ in range(10000):
    friendly10k += int(get_coop_friendly())
assert 8000 <= friendly10k <= 10000

#Part4 
def score_pdil(p0_coop, p1_coop, verbose=False):
    """ scores a single round of prisoner's dilemma
    
    Args:
        p0_coop (bool): True if player 0 cooperates,
            otherwise false
        p1_coop (bool): True if player 1 cooperates,
            otherwise false
        verbose (bool): toggles output to command line
            
    Returns:
        p0_points (int): "points" earned by p0 this round
        p1_points (int): "points" earned by p1 this round
    """
    # cast both inputs to boolean
    p0_coop = bool(p0_coop)
    p1_coop = bool(p1_coop)
    
    # lookup scores per player
    if (p0_coop, p1_coop) == (True, True):
        msg = 'both players cooperate'
        p0_point = 2
        p1_point = 2
    elif (p0_coop, p1_coop) == (True, False):
        msg = 'one player cooperates, the other does not'
        p0_point = 0
        p1_point = 3
    elif (p0_coop, p1_coop) == (False, True):
        msg = 'one player cooperates, the other does not'
        p0_point = 3
        p1_point = 0
    else:
        msg = 'neither player cooperates'
        p0_point = 1
        p1_point = 1
        
    # output msg if in verbose mode
    if verbose:
        print(msg)
        
    return p0_point, p1_point
    
 # test cases
assert score_pdil(p0_coop=True, p1_coop=True) == (2, 2)
assert score_pdil(p0_coop=True, p1_coop=False) == (0, 3)
assert score_pdil(p0_coop=False, p1_coop=True) == (3, 0)
assert score_pdil(p0_coop=False, p1_coop=False) == (1, 1)

# Part 6 
def repeated_pdil(score_to_win, coop_friendly_init=True):
    """ runs repeated prisoners dilemma friendly vs copycat
    
    game ends when one player reaches score_to_win.
    
    note that copycat strategy requires the opponents last choice to
    produce a new cooperation decision.  In the first round we use
    coop_friendly_init as the friendly players "previous round" to
    determine coop_copycat, the copycat's current round cooperation
    
    Args:
        score_to_win (int): min threshold to declare (at least)
            one player a winner and end game
        coop_friendly_init (bool): initial condition of friendly
            players "previous round"
            
    Returns:
        score_copycat (int): total copycat player points
        score_friendly (int): total friendly player points
        num_rounds (int): number of rounds played
    """
    # initialize counters
    score_copycat = 0
    score_friendly = 0
    num_rounds = 0
    
    # initialize coop_friendly_last
    coop_friendly_last = coop_friendly_init

    while True:
        # increment round counter
        num_rounds += 1
        
        # get new strategies from each player
        coop_friendly = get_coop_friendly()
        coop_copycat = get_coop_copycat(opp_last_coop=coop_friendly_last)

        # get round score for each player
        r_score_copycat, r_score_friendly = score_pdil(p0_coop=coop_friendly, 
                                                       p1_coop=coop_copycat,
                                                       verbose=False)

        # add to totals
        score_copycat += r_score_copycat
        score_friendly += r_score_friendly

        # quit loop if somebody wins
        if max(score_copycat, score_friendly) >= score_to_win:
            break    

        # mark current strategies as "last" (prep next loop)
        coop_copycat_last = coop_copycat
        coop_friendly_last = coop_friendly
        
    return score_copycat, score_friendly, num_rounds
    
#Part 7 
# experiment parameters
total_games = 1000
score_to_win = 20
coop_friendly_init = True

score_count_dict = dict()
for _ in range(total_games):
    # run a game of repeated prisoner's dilemma
    score_copycat, score_friendly, _ = repeated_pdil(score_to_win=score_to_win,
                                                     coop_friendly_init=coop_friendly_init)
    
    # build score_tuple, more conveneient to address dict
    score_tuple = score_copycat, score_friendly
    
    if score_tuple in score_count_dict.keys():
        # we've seen score_tuple before, increment existing entry
        score_count_dict[score_tuple] += 1
    else:
        # this is first time score_tuple is observed
        score_count_dict[score_tuple] = 1
    
# note0: its good practice to keep all parameters together @ top rather than
# send a user looking through long script to change them.  this is doubly true if 
# value is used more than once as its a pain to change it in two places!
    
# note1: its common practice to "discard" variables by assigning them
# to underscores in python.  We do this with the loop index (we never use it)
# as well as the num_rounds output of repeated_pdil (also not needed)

# another solution using defaultdict
from collections import defaultdict

# experiment parameters
total_games = 1000
score_to_win = 20
coop_friendly_init = True

score_count_dict = defaultdict(lambda: 0)
for _ in range(total_games):
    # run a game of repeated prisoner's dilemma
    score_copycat, score_friendly, _ = repeated_pdil(score_to_win=score_to_win,
                                                     coop_friendly_init=coop_friendly_init)
    
    # build score_tuple, more conveneient to address dict
    score_tuple = score_copycat, score_friendly
    
    # increment score_tuple entry
    score_count_dict[score_tuple] += 1
    
#Part 8 
    
