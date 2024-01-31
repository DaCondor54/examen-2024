import random
import os
import platform

random.seed(0)
class Card:
    def __init__(self, n, s, p):
        self.number = n
        self.suit = s
        self.special = p
    def __str__(self):
        if self.special == '':
            return f'{self.number} {self.suit}'
        else:
            return f'{self.special} {self.suit}'

class Player:
    def __init__(self, name, cards):
        self.name = name
        self.cards = cards
        self.uno = False
    def printHand(self):
        printedCards = [card.__str__()  for card in self.cards] 
        printedCards = [printedCards[i] + f' ({i+1})' for i in range(len(printedCards))]
        print(f'Player {self.name} hand ::: draw (0) | ' + ' | '.join(printedCards))

class Game:
    CARD_NUMBER = 108
    def __init__(self):
        self.deck = self.create_deck()
        self.playedCards = []
        random.shuffle(self.deck)
        self.players = []
        self.currentColor = ''
        self.run = True
        self.stackedCards = 0
        self.playingStacked = False
        # print([x.__str__() for x in self.deck])
        pass
    def game_loop(self):
        print('before playing 2nd to last card write uno')
        playerCount = input('how many players : ')
        response = input('House rules : Stack draw + 2 (yes) / anything else is no : ')
        if response == 'yes':
            self.playingStacked = True
        self.players = [Player(x+1, self.initPlayerHands()) for x in range(int(playerCount))]
        for x in self.players:
            x.printHand()
        self.playedCards = [self.deck.pop()]
        self.currentColor = self.playedCards[-1].suit
        self.playerIndex = 0
        self.unos = []
        
        while self.run:
            previousError = ''
            validPlay = False
            #os.system('cls')len(self.deck) < 90


            while not validPlay:
                self.clearScreen()
                print(f'the card is {self.playedCards[-1]}')
                # self.players[self.playerIndex].printHand()
                self.players[self.playerIndex].printHand()
                # [x.printHand() for x in self.players]
                if previousError != '':
                    print(previousError)
                #if self.stackedCards != 0:
                print(f'Stacked cards : {self.stackedCards} {self.playingStacked}')
                response = input('\nWhat do you play : ')
                if response == 'uno' and len(self.players[self.playerIndex].cards) == 2:
                    self.players[self.playerIndex].uno = True
                elif response == '0':
                    self.drawCard(self.players[self.playerIndex])
                    self.stackCards()
                    validPlay = True
                    continue
                elif response.isnumeric() and int(response) > 0 and int(response) <= len(self.players[self.playerIndex].cards):
                    card_played = self.players[self.playerIndex].cards[int(response)-1]
                    if self.ruleChecks(self.playedCards[-1], card_played):
                        self.players[self.playerIndex].cards.pop(int(response)-1)
                        self.executeCard(self.playedCards[-1], card_played)
                        validPlay = True
                    else:
                        
                        print(card_played)
                        previousError = "this card cant be played"
                else:
                    previousError = f"Wrong Input enter a number from 0 to {len(self.players[self.playerIndex].cards)}"

                

            self.checkWin()
            
            if len(self.deck) < 10:
                self.refill_deck()
            
            self.playerIndex += 1
            if self.playerIndex >= len(self.players):
                self.playerIndex = 0
            


    def create_deck(self):
        deck = []
        suits = ['red', 'green', 'blue', 'yellow']
        for suit in suits:
            deck += [Card(n, suit, '') for n in range(1,10)]
        for suit in suits:
            deck += [Card(-1, suit, 'skip'), Card(-1, suit, 'skip')]
            deck += [Card(-1, suit, 'reverse'), Card(-1, suit, 'skip')]
            deck += [Card(-1, suit, 'draw2'), Card(-1, suit, 'skip')]
        for x in range(4):
            deck.append(Card(-1, '', 'color'))
            deck.append(Card(-1,'', 'draw4'))
        return deck
    
    def initPlayerHands(self):
        return [self.deck.pop() for _ in range(7)]
    
    def ruleChecks(self, lastCard : Card, newCard : Card):
        if self.checkColor(lastCard, newCard):
            return True
        if lastCard.number == newCard.number and lastCard.number != -1:
            return True
        return False

    def checkColor(self,lastCard : Card, newCard : Card):
        if newCard.special == 'color' or newCard.special == 'draw4':
            return True
        elif newCard.suit == self.currentColor:
            return True
        return False
    def drawCard(self, player : Player):
        player.cards.append(self.deck.pop())
    
    def executeCard(self, lastCard :Card, newCard : Card):
        self.playedCards.append(newCard)        
        if newCard.special == 'color':
            self.chooseColor()
            newCard.color = self.currentColor
        elif newCard.special == 'skip':
            self.playerIndex = (self.playerIndex + 1) % len(self.players)
        elif newCard.special == 'draw2':
            playerdraw2 = self.players[(self.playerIndex + 1) % len(self.players)]
            if self.playingStacked:
                self.stackedCards += 2
            else:
                self.drawCard(playerdraw2)
                self.drawCard(playerdraw2)
        elif newCard.special == 'reverse':
            self.players.reverse()
            self.playerIndex = (len(self.players) - self.playerIndex -1)
        elif newCard.special == 'draw4':
            playerdraw2 = self.players[(self.playerIndex+1) % len(self.players)]
            if self.playingStacked:
                self.stackedCards += 4
            else:
                self.drawCard(playerdraw2)
                self.drawCard(playerdraw2)
                self.drawCard(playerdraw2)
                self.drawCard(playerdraw2)
            self.chooseColor()
            newCard.color = self.currentColor
        else:
            self.currentColor = newCard.suit
        
        if newCard.special != 'draw4' and newCard.special != 'draw2':
            self.stackCards()

            
    def chooseColor(self):
        colors = ['red','green','blue','yellow']
        color = input('what color do you want to change (red,green,blue,yellow)')
        while color not in colors:
            print('wrong color')
            color = input('what color do you want to change (red,green,blue,yellow)')
        self.currentColor = color
    
    def checkWin(self):
        player = self.players[self.playerIndex]
        
        if len(player.cards) == 0:
            print(f'Player {self.playerIndex+1} won')
            self.run = False
        elif len(player.cards) == 1 and not player.uno:
            self.drawCard(player)
            self.drawCard(player)
        elif len(player.cards) > 1:
            player.uno = False

    def refill_deck(self):
        lastCard = self.playedCards.pop()
        random.shuffle(self.playedCards)
        for card in self.playedCards:
            if card.special == 'draw4' or card.special == 'color':
                card.suit = ''
        self.deck += self.playedCards
        self.playedCards = [lastCard]
    def stackCards(self):
        if self.playingStacked:
            for i in range(self.stackedCards):
                self.drawCard(self.players[self.playerIndex])
            self.stackedCards = 0
    def clearScreen(self):
        os.system('cls' if os.name=='nt' else 'clear')



if __name__ == '__main__':
    game = Game()
    game.game_loop()

