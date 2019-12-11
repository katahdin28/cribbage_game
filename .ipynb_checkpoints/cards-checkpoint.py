{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [
    {
     "ename": "NameError",
     "evalue": "name 'variable' is not defined",
     "output_type": "error",
     "traceback": [
      "\u001b[1;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[1;31mNameError\u001b[0m                                 Traceback (most recent call last)",
      "\u001b[1;32m<ipython-input-1-7491e8ca283b>\u001b[0m in \u001b[0;36m<module>\u001b[1;34m\u001b[0m\n\u001b[0;32m     71\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0;32m     72\u001b[0m \u001b[1;33m\u001b[0m\u001b[0m\n\u001b[1;32m---> 73\u001b[1;33m \u001b[0mvariable\u001b[0m \u001b[1;33m+=\u001b[0m \u001b[1;36m1\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n\u001b[0m\u001b[0;32m     74\u001b[0m \u001b[0mvariable\u001b[0m\u001b[1;33m\u001b[0m\u001b[1;33m\u001b[0m\u001b[0m\n",
      "\u001b[1;31mNameError\u001b[0m: name 'variable' is not defined"
     ]
    }
   ],
   "source": [
    "import random\n",
    "from random import shuffle\n",
    "\n",
    "class Card():\n",
    "    \"\"\"\n",
    "    Card accepts two integer numeric inputs - rank and suit\n",
    "    rank must be between 1 and 13 inclusive\n",
    "    suit must be between 1 and 4 inclusive\n",
    "    \n",
    "    str value is its common name\n",
    "    \n",
    "    .value() method returns its cribbage count value\n",
    "    \"\"\"\n",
    "    def __init__(self, rank, suit):\n",
    "        self.rank = rank\n",
    "        self.suit = suit\n",
    "        self.rank_dict = {1:'Ace',\n",
    "                          2:'Two',\n",
    "                          3:'Three',\n",
    "                          4:'Four',\n",
    "                          5:'Five',\n",
    "                          6:'Six',\n",
    "                          7:'Seven',\n",
    "                          8:'Eight',\n",
    "                          9:'Nine',\n",
    "                          10:'Ten',\n",
    "                          11:'Jack',\n",
    "                          12:'Queen',\n",
    "                          13:'King',}\n",
    "        self.suit_dict = {1:'Clubs',\n",
    "                          2:'Hearts',\n",
    "                          3:'Diamonds',\n",
    "                          4:'Spades'}\n",
    "        \n",
    "    def __str__( self ):\n",
    "        return self.rank_dict[self.rank]+' of '+self.suit_dict[self.suit]\n",
    "        \n",
    "        \n",
    "    def value(self):\n",
    "        \"\"\"\n",
    "        Takes rank (interger value) and returns numeric (interger value) of card\n",
    "        \"\"\"\n",
    "        if self.rank <= 0:\n",
    "            return \"Error: Rank <= 0\"\n",
    "        elif self.rank <= 10:\n",
    "            return self.rank\n",
    "        elif self.rank <= 13:\n",
    "            return 10\n",
    "        else:\n",
    "            return \"Error: Rank > 13\"\n",
    "        \n",
    "\n",
    "class RandomDeck():\n",
    "    def __init__(self):\n",
    "        self.decklist = []\n",
    "        self.decklist = [Card(i,j) for i in range(1,14) for j in range(1,5)]\n",
    "        random.shuffle(self.decklist)\n",
    "        self.flip_depth = random.randrange(12,51)\n",
    "    \n",
    "    def hand(self, player):\n",
    "        hand_list = []\n",
    "        if (player == 1 or player == 2):\n",
    "            for i in range(1,7):\n",
    "                hand_list.append(self.decklist[(i-2+player)*2])\n",
    "            return hand_list\n",
    "        else:\n",
    "            return \"Player Must Be 1 or 2\"\n",
    "        \n",
    "    def flip_card(self):\n",
    "        return self.decklist[self.flip_depth]\n",
    "\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.7.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
