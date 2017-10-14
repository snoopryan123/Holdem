from itertools import combinations

print("TEXAS HOLDEM POST-FLOP ODDS GENERATOR")

class Player(object):
    """A player has cards"""
    not_yet_dealt = []
    count = 0
    Table_Hands = [] #hands of all of the player who will see the flop
    max_pi = -1
    max_tc = 1
    max_tb1 = 1
    max_tb2 = 1
    max_tb3 = 1
    max_tb4 = 1

    def __init__(self, cards):
        """A list of a player's cards (and the cards' attributes)"""
        self.cards = cards  #the 2 cards dealt to a player
        self.numbers = sorted([c.number for c in cards])
        self.suits = [c.suit for c in cards]
        self.wins = 0

class Card(object):
    """A playing card has a number and suit"""

    def __init__(self, number, suit):
        self.number = number
        self.suit = suit

    def __str__(self):
        return "%s%s" %(self.number, self.suit)

class Hand(object):

    """describes a person's best 5 card combo"""
    def __init__(self, Type, power_index, top_card, tiebreaker1, tiebreaker2, tiebreaker3, tiebreaker4, player):
        self.type = Type
        self.pi = power_index
        self.tc = top_card
        self.tb1 = tiebreaker1
        self.tb2 = tiebreaker2
        self.tb3 = tiebreaker3
        self.tb4 = tiebreaker4
        self.player = player

#***************************************

"""Table is a list consisting of each of the player objects"""
Table = []

"""Deck is a list consisting of non-dealt cards; initially all 52 cards"""
Deck = [Card(2, 'C'),  Card(3, 'C'), Card(4, 'C'), Card(5, 'C'), Card(6, 'C'), Card(7, 'C'), Card(8, 'C'), \
        Card(9, 'C'), Card(10, 'C'), Card(11, 'C'), Card(12, 'C'), Card(13,'C'), Card(14, 'C'), \
        Card(2, 'D'),  Card(3, 'D'), Card(4, 'D'), Card(5, 'D'), Card(6, 'D'), Card(7, 'D'), Card(8, 'D'), \
        Card(9, 'D'), Card(10, 'D'), Card(11, 'D'), Card(12, 'D'), Card(13,'D'), Card(14, 'D'), \
        Card(2, 'H'),  Card(3, 'H'), Card(4, 'H'), Card(5, 'H'), Card(6, 'H'), Card(7, 'H'), Card(8, 'H'), \
        Card(9, 'H'), Card(10, 'H'), Card(11, 'H'), Card(12, 'H'), Card(13,'H'), Card(14, 'H'), \
        Card(2, 'S'),  Card(3, 'S'), Card(4, 'S'), Card(5, 'S'), Card(6, 'S'), Card(7, 'S'), Card(8, 'S'), \
        Card(9, 'S'), Card(10, 'S'), Card(11, 'S'), Card(12, 'S'), Card(13,'S'), Card(14, 'S')]

Suits = {'C': 0, 'D': 1, 'H': 2, 'S': 3}
Numbers = range(2,15)
Royals = {'J': 11, 'Q': 12, 'K': 13, 'A': 14}

#***************************************

def straight_flush(player):
    """called only if player has a straight and a flush,
    return the highest card in the straight-flush if a straight is also a flush"""
    straight_num = straight(player)
    potential_sf_suit = [card.suit for card in player.cards if card.number == straight_num]
    for s in potential_sf_suit:
        if [card for card in player.cards if card.number == straight_num-1 and card.suit == s]:
            if [card for card in player.cards if card.number == straight_num-2 and card.suit == s]:
                if [card for card in player.cards if card.number == straight_num-3 and card.suit == s]:
                    if [card for card in player.cards if card.number == straight_num-4 and card.suit == s]:
                        return straight_num

def quads(player):
    """return the number of a four-of-a-kind"""
    for i in list(reversed(range(len(player.numbers)))):
        if player.numbers[i] == player.numbers[i-1] == player.numbers[i-2] == player.numbers[i-3] and i > 2:
            return player.numbers[i]

def full_house(player):
    """return the number of the three-of-a-kind in a full house, if player has a triple and a pair"""
    return triples(player)

def flush(player):
    """return a list containing [highest number of a flush, suit of flush]"""
    suits = sorted([Suits[s] for s in player.suits])
    for i in [2,1,0]:
        if suits[i] == suits[i+1] == suits[i+2] == suits[i+3] == suits[i+4]:
            for key in Suits:
                if Suits[key] == suits[i]:
                    suited_cards = [c.number for c in player.cards if c.suit == key]
                    return [max(suited_cards), key]

def straight(player):
    """return the highest card number of a straight"""
    nums = player.numbers

    def s(nums):
        for i in [2,1,0]:
            if nums[i]+4 == nums[i+1]+3 == nums[i+2]+2 == nums[i+3]+1 == nums[i+4] and i < 3:
                return nums[i+4]

    #Account for the A2345 straight, where A is 1 instead of 14
    s = s(nums)
    if not s and (14 in nums) and (2 in nums) and (3 in nums) and (4 in nums) and (5 in nums):
        return 5
    else:
        return s

def triples(player):
    """return the number of the highest three-of-a-kind"""
    for i in list(reversed(range(len(player.numbers)))):
        if player.numbers[i] == player.numbers[i-1] == player.numbers[i-2] and i > 1:
            return player.numbers[i]

def pair_num(lst):
    """return the number of the highest pair in a list of numbers"""
    for i in list(reversed(range(len(lst)))):
        if lst[i] == lst[i-1] and i > 0:
            return lst[i]

def second_pair(player):
    """return the number of the second highest pair"""
    high_pair = pair(player)
    if high_pair:
        others = player.numbers[:]
        others.remove(high_pair)
        others.remove(high_pair)
        return pair_num(others)

def pair(player):
    """return the number of the highest pair, outside of a triple"""
    #make sure you don't double count the triple and the pair
    triple = triples(player)
    if triple:
        others = player.numbers[:]
        others.remove(triple)
        others.remove(triple)
        others.remove(triple)
        return pair_num(others)
    else:
        return pair_num(player.numbers)

def high_card(player):
    return max(player.numbers)

#***************************************

def quads_tiebreaker(player, quad_num):
    """return the number of the highest card not in the four of a kind"""
    cards_for_tiebreak = player.cards[:]
    cards_for_tiebreak = list(reversed(sorted([c.number for c in cards_for_tiebreak if c.number != quad_num])))
    return cards_for_tiebreak[0]

def full_house_tiebreaker(player, triples_num):
    """return the number of the pair in the full house (the hand's highest pair)"""
    cards_for_tiebreak = player.cards[:]
    cards_for_tiebreak = list(sorted([c.number for c in cards_for_tiebreak if c.number != triples_num]))
    return pair_num(cards_for_tiebreak)

def flush_tiebreaker(player, flush_suit):
    """return a list containing the 4 non-top flush card numbers in descending order"""
    cards_for_tiebreak = player.cards[:]
    cards_for_tiebreak = list(reversed(sorted([c.number for c in cards_for_tiebreak if c.suit == flush_suit])))
    return cards_for_tiebreak[:4]

def triples_tiebreaker(player, triples_num):
    """return a list containing the highest and 2nd highest cards outside the three-of-a-kind"""
    cards_for_tiebreak = player.cards[:]
    cards_for_tiebreak = list(reversed(sorted([c.number for c in cards_for_tiebreak if c.number != triples_num])))
    return cards_for_tiebreak[:2]

def two_pair_tiebreaker(player, pair1_num, pair2_num):
    """return the highest card outside the two pair"""
    cards_for_tiebreak = player.cards[:]
    cards_for_tiebreak = list(reversed(sorted([c.number for c in cards_for_tiebreak if c.number != pair1_num and c.number != pair2_num])))
    return cards_for_tiebreak[0]

def pair_tiebreaker(player, pair_num):
    """return a list containing the 3 highest cards outside the pair"""
    cards_for_tiebreak = player.cards[:]
    cards_for_tiebreak = list(reversed(sorted([c.number for c in cards_for_tiebreak if c.number != pair_num])))
    return cards_for_tiebreak[:3]

def high_card_tiebreaker(player, hc):
    """return a list containing the 4 non-top high cards in descending order"""
    cards_for_tiebreak = player.cards[:]
    cards_for_tiebreak = list(reversed(sorted([c.number for c in cards_for_tiebreak if c.number != hc])))
    return cards_for_tiebreak[:4]

#***************************************

def best_hand(player):
    """A function that returns a player's best hand, in the form of a Hand object, out of her list of 7 cards"""
    sf = None
    q = quads(player)
    fh = None
    f = None
    f_full = flush(player)
    if f_full:
        f = f_full[0]
    s = straight(player)
    t = None
    tp = None

    qtb = None
    fhtb = None
    ftb = None
    ttb = None
    tptb = None
    ptb = None
    hctb = None

    #DETERMINE A PLAYER'S BEST POKER HAND
    if f and s:
        sf = straight_flush(player)
    elif not q:
        t = triples(player)
        p = pair(player)
        if t and p:
            fh = full_house(player)
            fhtb = full_house_tiebreaker(player, t)
        elif p and not fh:
            tp = second_pair(player)

    if sf:
        Type, PI, TC, TB1, TB2, TB3, TB4 = "straight-flush", 8, sf, None, None, None, None
    elif q:
        qtb = quads_tiebreaker(player, q)
        Type, PI, TC, TB1, TB2, TB3, TB4 = "four-of-a-kind", 7, q, qtb, None, None, None
    elif fh:
        Type, PI, TC, TB1, TB2, TB3, TB4 = "full-house", 6, fh, fhtb, None, None, None
    elif f:
        ftb = flush_tiebreaker(player, f_full[1])
        Type, PI, TC, TB1, TB2, TB3, TB4 = "flush", 5, f, ftb[0], ftb[1], ftb[2], ftb[3]
    elif s:
        Type, PI, TC, TB1, TB2, TB3, TB4 = "straight", 4, s, None, None, None, None
    elif t:
        ttb = triples_tiebreaker(player, t)
        Type, PI, TC, TB1, TB2, TB3, TB4 = "three-of-a-kind", 3, t, ttb[0], ttb[1], None, None
    elif tp:
        tptb = two_pair_tiebreaker(player, p, tp)
        Type, PI, TC, TB1, TB2, TB3, TB4 = "two-pair", 2, p, tp, tptb, None, None
    elif p:
        ptb = pair_tiebreaker(player, p)
        Type, PI, TC, TB1, TB2, TB3, TB4 = "pair", 1, p, ptb[0], ptb[1], ptb[2], None
    else:
        hc = high_card(player)
        hctb = high_card_tiebreaker(player, hc)
        Type, PI, TC, TB1, TB2, TB3, TB4 = "high-card", 0, hc, hctb[0], hctb[1], hctb[2], hctb[3]

    return Hand(Type, PI, TC, TB1, TB2, TB3, TB4, player)

#************************************

"""ODDS  POST-FLOP / PRE-TURN"""
def account_for_undealt_cards(num_undealt):

    #store a player's original lists: cards, numbers, suits
    Player.count = 0
    for player in Table:
        player.ogcards = player.cards[:]
        player.ognumbers = player.numbers[:]
        player.ogsuits = player.suits[:]

    for combo in list(combinations(Deck, num_undealt)):
        Player.count += 1
        Player.not_yet_dealt += list(combo)

        #temporarily add the num_undealt card combo to the player's lists: cards, numbers, suits
        for player in Table:
            for c in Player.not_yet_dealt:
                player.cards += [c]
                player.numbers += [c.number]
                player.numbers = sorted(player.numbers)
                player.suits += [c.suit]

        calculate_winning_hands()

        #RESTORE VARIABLES
        for player in Table:
            player.cards = player.ogcards[:]
            player.numbers = player.ognumbers[:]
            player.suits = player.ogsuits[:]
        Player.not_yet_dealt = []
        Player.Table_Hands = []
        Player.max_pi = -1
        Player.max_tc = 1
        Player.max_tb1 = 1
        Player.max_tb2 = 1
        Player.max_tb3 = 1
        Player.max_tb4 = 1

    calculate_odds()

    #RESET Player.count and player.wins
    Player.count = 0
    for p in Table:
        p.wins = 0

def calculate_winning_hands():
    #add Hand object (a player's best hand) to the list Table_Hands
    for player in Table:
        Player.Table_Hands += [best_hand(player)]

    #REMOVE HANDS WITH LOWER POWER-INDECES
    Player.max_pi = max([hand.pi for hand in Player.Table_Hands])
    for hand in Player.Table_Hands:
        Player.Table_Hands = [hand for hand in Player.Table_Hands if hand.pi == Player.max_pi]

    #IF ONE HAND ALONE HAS THE HIGHEST POWER-INDEX, THAT PLAYER WINS
    if len(Player.Table_Hands) == 1:
        Player.Table_Hands[0].player.wins += 1

    #IF MULTIPLE HANDS HAVE THE SAME POWER-INDEX
    else:
        #REMOVE HANDS WITH LOWER TOP-CARDS
        Player.max_tc = max([hand.tc for hand in Player.Table_Hands])
        for hand in Player.Table_Hands:
            Player.Table_Hands = [hand for hand in Player.Table_Hands if hand.tc == Player.max_tc]

        #IF ONE HAND ALONE HAS THE HIGHEST TOP-CARD, THAT PLAYER WINS
        if Player.Table_Hands:
            if len(Player.Table_Hands) == 1:
                Player.Table_Hands[0].player.wins += 1

            #IF MULTIPLE HANDS HAVE THE SAME TOP-CARD
            else:
                Player.max_tb1 = max([hand.tb1 if hand.tb1 else 1 for hand in Player.Table_Hands])
                if Player.max_tb1 > 1:
                    for hand in Player.Table_Hands:
                        Player.Table_Hands = [hand for hand in Player.Table_Hands if hand.tb1 == Player.max_tb1]
                    if len(Player.Table_Hands) == 1:
                        Player.Table_Hands[0].player.wins += 1
                    #IF MULTIPLE HANDS HAVE THE SAME 1ST-HIGH-CARD
                    else:
                        Player.max_tb2 = max([hand.tb2 if hand.tb2 else 1 for hand in Player.Table_Hands])
                        if Player.max_tb2 > 1:
                            for hand in Player.Table_Hands:
                                Player.Table_Hands = [hand for hand in Player.Table_Hands if hand.tb2 == Player.max_tb2]
                            if len(Player.Table_Hands) == 1:
                                Player.Table_Hands[0].player.wins += 1
                            #IF MULTIPLE HANDS HAVE THE SAME 2ND-HIGH-CARD
                            else:
                                Player.max_tb3 = max([hand.tb3 if hand.tb3 else 1 for hand in Player.Table_Hands])
                                if Player.max_tb3 > 1:
                                    for hand in Player.Table_Hands:
                                        Player.Table_Hands = [hand for hand in Player.Table_Hands if hand.tb3 == Player.max_tb3]
                                    if len(Player.Table_Hands) == 1:
                                        Player.Table_Hands[0].player.wins += 1
                                    #IF MULTIPLE HANDS HAVE THE SAME 3RD-HIGH-CARD
                                    else:
                                        Player.max_tb4 = max([hand.tb4 if hand.tb4 else 1 for hand in Player.Table_Hands])
                                        if Player.max_tb4 > 1:
                                            for hand in Player.Table_Hands:
                                                Player.Table_Hands = [hand for hand in Player.Table_Hands if hand.tb4 == Player.max_tb4]
                                            if len(Player.Table_Hands) == 1:
                                                Player.Table_Hands[0].player.wins += 1

def calculate_odds():
    #CALCULATE AND PRINT ODDS
    tie_odds = 100
    playerid = 0
    for p in Table:
        if float(Player.count) > 0:
            odds = round( (float(p.wins)/float(Player.count)) , 2 ) * 100
        else:
            odds = round( float(p.wins), 2 ) * 100
        print("player %d odds to win: %d%%" %(playerid, odds) )
        playerid += 1
        tie_odds -= odds
    tie_odds = round(tie_odds, 2)
    if tie_odds > 0:
        print("tie odds: %d%%" %(tie_odds))

#************************************
"""PRE-FLOP"""

num_players = int(raw_input("enter number of players who will progress to see the flop: "))

def collect_deal_info():
    for n in range(num_players):
        print("enter player %d information:" %(n))
        print("suit format: C D H S / royals format: J Q K A")

        card1number = raw_input("enter first card number: ")
        if card1number in Royals:
            card1number = Royals[card1number]
        card1number = int(card1number)
        assert (card1number in Numbers), "please enter a valid number"
        card1suit = raw_input("enter first card suit: ")
        assert (card1suit in Suits), "please enter correct suit format"

        card2number = raw_input("enter second card number: ")
        if card2number in Royals:
            card2number = Royals[card2number]
        card2number = int(card2number)
        assert (card2number in Numbers), "please enter a valid number"
        card2suit = raw_input("enter second card suit: ")
        assert (card2suit in Suits), "please enter correct suit format"

        #add dealt cards to cards_on_table, the list of cards shared by all players
        Table.append( Player([Card(card1number, card1suit), Card(card2number, card2suit)]) )

    #remove dealt cards from the deck"""
    for p in Table:
        for c in p.cards:
            [Deck.remove(d) for d in Deck if c.number == d.number and c.suit == d.suit]

collect_deal_info()
""" VVV  COMMENT OUT THE BELOW LINE TO TAKE OUT PRE-FLOP ODDS, WHICH TAKES 2 MINUTES TO COMPUTE  VVV """
# account_for_undealt_cards(5)
#***************************************

# def account_for_folding():
#     folded = raw_input("type in the numbers of the player(s) (if any) separated by spaces \
#                         who folded after the flop; click enter if none: ")
#     if len(folded) > 2:
#         num_folded = len(folded)//2
#         for n in folded:
#             if n in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
#                 i = int(n)
#                 Table.pop(i)

#***************************************
"""POST-FLOP / PRE-TURN"""

def collect_flop_info():
    print("enter flop information:")

    card1number = raw_input("enter first card number: ")
    if card1number in Royals:
        card1number = Royals[card1number]
    card1number = int(card1number)
    assert (card1number in Numbers), "please enter a valid number"
    card1suit = raw_input("enter first card suit: ")
    assert (card1suit in Suits), "please enter correct suit format"

    card2number = raw_input("enter second card number: ")
    if card2number in Royals:
        card2number = Royals[card2number]
    card2number = int(card2number)
    assert (card2number in Numbers), "please enter a valid number"
    card2suit = raw_input("enter first card suit: ")
    assert (card2suit in Suits), "please enter correct suit format"

    card3number = raw_input("enter third card number: ")
    if card3number in Royals:
        card3number = Royals[card3number]
    card3number = int(card3number)
    assert (card3number in Numbers), "please enter a valid number"
    card3suit = raw_input("enter first card suit: ")
    assert (card3suit in Suits), "please enter correct suit format"

    #add dealt cards to cards_on_table, the list of cards shared by all players
    # Player.cards_on_table.extend( [Card(card1number, card1suit), Card(card2number, card2suit), Card(card3number, card3suit)] )
    flop = [Card(card1number, card1suit), Card(card2number, card2suit), Card(card3number, card3suit)]

    #add the number and suit of cards in the FLOP to each individual player's numbers and suits lists
    for p in Table:
        for c in flop:
            p.cards += [c]
            p.numbers += [c.number]
            p.suits += [c.suit]
        p.numbers = sorted(p.numbers)

    #remove dealt cards from the deck
    for c in flop:
        [Deck.remove(d) for d in Deck if c.number == d.number and c.suit == d.suit]

collect_flop_info()
account_for_undealt_cards(2)
#***************************************
"""POST-TURN / PRE-RIVER"""

def collect_turn_info():
    print("enter turn information:")

    card1number = raw_input("enter card number: ")
    if card1number in Royals:
        card1number = Royals[card1number]
    card1number = int(card1number)
    assert (card1number in Numbers), "please enter a valid number"
    card1suit = raw_input("enter card suit: ")
    assert (card1suit in Suits), "please enter correct suit format"

    turn = [Card(card1number, card1suit)]

    #add the number and suit of the TURN card to each individual player's numbers and suits lists
    for p in Table:
        for c in turn:
            p.cards += [c]
            p.numbers += [c.number]
            p.suits += [c.suit]
        p.numbers = sorted(p.numbers)

    #remove dealt card from the deck
    for c in turn:
        [Deck.remove(d) for d in Deck if c.number == d.number and c.suit == d.suit]

collect_turn_info()
account_for_undealt_cards(1)
#************************************
"""POST-RIVER"""

def collect_final_info():
    print("enter river information:")

    card1number = raw_input("enter card number: ")
    if card1number in Royals:
        card1number = Royals[card1number]
    card1number = int(card1number)
    assert (card1number in Numbers), "please enter a valid number"
    card1suit = raw_input("enter card suit: ")
    assert (card1suit in Suits), "please enter correct suit format"

    river = [Card(card1number, card1suit)]

    #add the number and suit of the RIVER card to each individual player's numbers and suits lists
    for p in Table:
        for c in river:
            p.cards += [c]
            p.numbers += [c.number]
            p.suits += [c.suit]
        p.numbers = sorted(p.numbers)

    #remove dealt card from the deck
    for c in river:
        [Deck.remove(d) for d in Deck if c.number == d.number and c.suit == d.suit]

    calculate_winning_hands()
    calculate_odds()

collect_final_info()
#************************************
