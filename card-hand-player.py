import random
from random import shuffle
import itertools


class Card():
    """Card class represents a typical playing card (excl. jokers, etc.)
    
    Instance Variables:
        rank -- integer value 1-14
        suit -- integer value 1-4 [clubs, hearts, diamonds, spades]

    Methods:
        value() -- returns cribbage count value of the card
        __str__ -- returns colloquial name of the card
        __eq__ -- allows == comaprisons against other Card instances

    """
    
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
        self.rank_dict = {1:'Ace' ,
                          2:'Two' ,
                          3:'Three' ,
                          4:'Four' ,
                          5:'Five' ,
                          6:'Six' ,
                          7:'Seven' ,
                          8:'Eight' ,
                          9:'Nine' ,
                          10:'Ten' ,
                          11:'Jack' ,
                          12:'Queen' ,
                          13:'King' ,}
        self.suit_dict = {1:'Clubs' ,
                          2:'Hearts' ,
                          3:'Diamonds' ,
                          4:'Spades'}
        
    def __eq__(self, other): 
        if not isinstance(other, Card):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.rank == other.rank and self.suit == other.suit
        
    def __str__( self ):
        return self.rank_dict[self.rank]+' of '+self.suit_dict[self.suit]
        
        
    def value(self):
        if self.rank <= 0:
            return "Error: Rank <= 0"
        elif self.rank <= 10:
            return self.rank
        elif self.rank <= 13:
            return 10
        else:
            return "Error: Rank > 13"
        

class RandomDeck():
    """Creates deck of 52 distinct playing cards in randomized order
    
    Instance Variables:
        cardlist -- randomized list of 52 distinct cards (Card instances)
    
    Methods:
        hand(player) -- takes two integers 1 or 2 (player 1, player 2) and returns 6 of the top 12 cards in a list
    """    

    def __init__(self):
        self.cardlist = []
        for i in range(1,14):
            for j in range(1,5):
                self.cardlist.append(Card(i,j))
        random.shuffle(self.cardlist)
        self.flip_card = self.cardlist[random.randrange(12,51)]
    def hand(self, player):
        # generates dealt hands to each of 2 players
        hand_list = []
        if (player == 1 or player == 2):
            for i in range(1,7):
                hand_list.append(self.cardlist[(i-2+player)*2])
            return hand_list
        else:
            return "Player Must Be 1 or 2"

class Hand():
    """Represents a four-card cribbage hand and can optionally be passed a single flip card
    
    Instance Variables:
        cardlist -- list of 4 Card instances
        ranklist -- list of card rank_list
        suitlist -- list of card suits
        flip_card -- None if not passed, Card instance otherwise

    Public Methods:
        score() -- returns the score of the four-card hand, including the flip card if passed
        
    """    
    def __init__(self, card_list, flipcard):
        self.cardlist = card_list
        self.flip_card = flipcard
    
    def string_rep(self):
        str_rep = ''
        for item in self.cardlist:
            if item.rank <= 10:
                str_rep += str(item.rank)+str(item.suit_dict[item.suit])[0]+'-'
            else:
                str_rep += str(item.rank_dict[item.rank])[0]+str(item.suit_dict[item.suit])[0]+'-'
        return(str_rep)

    def _return_ranks(self, card_list):
        # converts list of Cards to list of rank_list (integers 1-14)
        rank_list = []
        for card in card_list: rank_list.append(card.rank)
        return rank_list

    def _return_suits(self, card_list):
        # converts list of Cards to list of suits (integers 1-4)
        suit_list = []
        for card in card_list: suit_list.append(card.suit)
        return suit_list

    def _is_15(self, card_list):
        # takes list of Cards, returns bool of whether cards add to 15
        value = 0
        for card in card_list:
            value += card.value()
        return value == 15

    def _flush_score(self):
        # returns points from flush for this hand
        flush_points = 0
        suitlist = self._return_suits(self.cardlist)
        if suitlist.count(suitlist[0]) == len(suitlist) : flush_points += 4
        if self.flip_card != None:
            if suitlist[0] == self.flip_card.suit: flush_points += 1
        return flush_points

    def _pair_score(self, rank_list):       
        # takes list of rank_list, returns pair score 
        pair_count = 0
        for pair in itertools.combinations(rank_list,2):
            if pair[0] == pair[1]:
                pair_count += 1
        return pair_count * 2
        
    def _fifteen_score(self, card_list):
        # takes list of cards, returns score from fifteens
        hand_size = len(card_list)
        fifteens = 0
        for i in range(hand_size-1):
            for ntuple in itertools.combinations(card_list,2+i):
                if self._is_15(ntuple):
                    fifteens += 1
        return fifteens * 2

    def _right_jack_score(self):
        # checks hand for 1-point Right Jack
        right_jack = 0
        if self.flip_card != None:
            for card in self.cardlist:
                if (card.rank == 11 and card.suit == self.flip_card.suit):
                    right_jack = 1
        return right_jack   

    def _straight_score(self, rank_list):
        uniques = list(set(rank_list))
        uniques.sort()
        
        str_dict = {}

        for item in uniques:
            if (item + 1 in uniques) or (item - 1 in uniques):
                str_dict[item] = True
            else:
                str_dict[item] = False

        str_cands = []
        for item in uniques:
            if str_dict[item]:
                str_cands.append(item)
        
        if len(str_cands) < 3:
            return 0
        elif len(str_cands) > 3:
            if max(str_cands) - min(str_cands) != len(str_cands)-1:
                if len(str_cands) == 5:
                    top3 = str_cands[2] - str_cands[0] == 2
                    bot3 = str_cands[4] - str_cands[2] == 2
                    if top3 and bot3:
                        return 5
                    elif top3:
                        str_cands = str_cands[0:3]
                    elif bot3:
                        str_cands = str_cands[2:]
                if len(str_cands) == 4:
                    return 0
        str_ranks = []
        for rank in rank_list:
            if (rank <= max(str_cands)) and (rank >= min(str_cands)):
                str_ranks.append(rank)

        if len(str_ranks) - 1 == max(str_cands)-min(str_cands):
            return len(str_ranks)
        elif (len(str_ranks) == 5) and (max(str_cands)-min(str_cands) == 3):
            return 8
        else:
            max_count = 1
            for rank in str_ranks:
                max_count = max(max_count, str_ranks.count(rank))

            if max_count == 2:
                return 12
            if max_count == 3:
                return 9
        print("whoops i left out a situation in my straight counting code")
        pass


    def score(self):
        # checks for all possible points in the hand, returns hand score (integer 0-29)
        
        points = 0

        if self.flip_card == None:
            points += self._fifteen_score(self.cardlist)
            points += self._pair_score(self._return_ranks(self.cardlist))
            points += self._flush_score()
            points += self._straight_score(self._return_ranks(self.cardlist))
        else:
            cardlist_withflip = self.cardlist
            cardlist_withflip.append(self.flip_card)
            points += self._fifteen_score(cardlist_withflip)
            points += self._pair_score(self._return_ranks(cardlist_withflip))
            points += self._flush_score()
            points += self._right_jack_score()
            points += self._straight_score(self._return_ranks(cardlist_withflip))
        
        return points



import operator

class Player():
    def __init__(self):
        self.initial_hand = []
        self.play_hand = []

    def crib_value(self,twocard_ranklist):
        crib_comp = (min(twocard_ranklist),max(twocard_ranklist))
        value_dict = {
                        (1,1) : 5.4,
                        (1,2) : 4.1,
                        (1,3) : 4.4,
                        (1,4) : 5.4,
                        (1,5) : 5.5,
                        (1,6) : 3.8,
                        (1,7) : 3.8,
                        (1,8) : 3.8,
                        (1,9) : 3.4,
                        (1,10) : 3.4,
                        (1,11) : 3.7,
                        (1,12) : 3.4,
                        (1,13) : 3.4,
                        (2,2) : 5.7,
                        (2,3) : 6.9,
                        (2,4) : 4.4,
                        (2,5) : 5.4,
                        (2,6) : 3.8,
                        (2,7) : 3.8,
                        (2,8) : 3.6,
                        (2,9) : 3.7,
                        (2,10) : 3.5,
                        (2,11) : 3.8,
                        (2,12) : 3.5,
                        (2,13) : 3.5,
                        (3,3) : 5.9,
                        (3,4) : 4.7,
                        (3,5) : 5.9,
                        (3,6) : 3.7,
                        (3,7) : 3.7,
                        (3,8) : 3.9,
                        (3,9) : 3.7,
                        (3,10) : 3.6,
                        (3,11) : 3.8,
                        (3,12) : 3.5,
                        (3,13) : 3.5,
                        (4,4) : 5.7,
                        (4,5) : 6.4,
                        (4,6) : 3.8,
                        (4,7) : 3.8,
                        (4,8) : 3.8,
                        (4,9) : 3.7,
                        (4,10) : 3.6,
                        (4,11) : 3.8,
                        (4,12) : 3.5,
                        (4,13) : 3.5,
                        (5,5) : 8.6,
                        (5,6) : 6.5,
                        (5,7) : 6.0,
                        (5,8) : 5.4,
                        (5,9) : 5.4,
                        (5,10) : 6.6,
                        (5,11) : 6.9,
                        (5,12) : 6.6,
                        (5,13) : 6.6,
                        (6,6) : 5.8,
                        (6,7) : 4.8,
                        (6,8) : 4.5,
                        (6,9) : 5.2,
                        (6,10) : 3.1,
                        (6,11) : 3.4,
                        (6,12) : 3.1,
                        (6,13) : 3.1,
                        (7,7) : 5.9,
                        (7,8) : 6.6,
                        (7,9) : 4.0,
                        (7,10) : 3.1,
                        (7,11) : 3.5,
                        (7,12) : 3.2,
                        (7,13) : 3.2,
                        (8,8) : 5.4,
                        (8,9) : 4.6,
                        (8,10) : 3.8,
                        (8,11) : 3.4,
                        (8,12) : 3.2,
                        (8,13) : 3.2,
                        (9,9) : 5.2,
                        (9,10) : 4.2,
                        (9,11) : 3.9,
                        (9,12) : 3.0,
                        (9,13) : 3.1,
                        (10,10) : 4.8,
                        (10,11) : 4.5,
                        (10,12) : 3.4,
                        (10,13) : 2.8,
                        (11,11) : 5.3,
                        (11,12) : 4.7,
                        (11,13) : 3.9,
                        (12,12) : 4.8,
                        (12,13) : 3.4,
                        (13,13) : 4.8
                    }
        return(value_dict[crib_comp]-2.8)

        
    def crib_discard(self):
        iter_dict = {}
        flip_cards = []
        for i in range(1,14):
            for j in range(1,5):
                flip_cards.append(Card(i,j))
        for item in self.initial_hand:
            flip_cards.remove(item)

        for quad in itertools.combinations(self.initial_hand,4):
            handClass = Hand(list(quad),None)
            #print(handClass.string_rep())
            base_score = handClass.score()
            flip_potential = 0

            for card in flip_cards:
                full_handClass = Hand(list(quad),card)
                potential_score = full_handClass.score()
                flip_potential += (potential_score - base_score)/46
            
            discard_ranks = []
            for card in self.initial_hand:
                discard_ranks.append(card.rank)
            for card in quad:
                discard_ranks.remove(card.rank)

            discard_tuple = (discard_ranks[0],discard_ranks[1])
            discard_value = self.crib_value(discard_tuple)
            iter_dict[handClass.string_rep()] = base_score + flip_potential - discard_value
            print(("......"))
            for card in quad:
                print (card)
            print('*******')
            for card in discard_tuple:
                print(card)
            print('*******')
            print('base: '+str(base_score),'flip: ' + str(round(flip_potential,2)),'discard: ' + str(round(discard_value,2)))
            print(("......"))
        hand_choice = max(iter_dict, key=iter_dict.get)
        self.play_hand = hand_choice
        pass


deck = RandomDeck()
player1 = Player()
player1.initial_hand = deck.hand(1)
for card in player1.initial_hand:
    print(card)
player1.crib_discard()
print('--------')
print(player1.play_hand)
