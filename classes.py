import random
import pygame
import os
import time

pygame.init()
pygame.font.init()

class Dealer():
    def __init__(self, cards):
        self.cards = cards
        self.dealerCards = []
        self.dealerCardImages = []
        self.numOfDealerCards = 0
        self.dealerTotal = 0
        self.cardWidth = 100
        self.cardHeight = 150
        self.lastDealerCardDealt = 0

    def load_card_images(self):   #Loads the images of the dealer's cards into a list
        self.numOfDealerCards = len(self.dealerCards)   #Gets the number of cards the dealer has
        for i in range(self.lastDealerCardDealt, self.numOfDealerCards):    
            cardNum = self.dealerCards[i][:-1]
            cardSuit = self.dealerCards[i][len(self.dealerCards[i])-1:]
            if cardSuit == "C":     
                suit = "clubs"
            if cardSuit == "S":
                suit = "spades"
            if cardSuit == "D":
                suit = "diamonds"
            if cardSuit == "H":
                suit = "hearts"

            if cardNum > "1" and cardNum < "11":
                card = cardNum + "_of_" + suit + ".png"     #If it is a number card it gets the card num and suit and uses it to find the right png for the card
            else:
                if cardNum == "J":
                    cardNum = "jack"
                if cardNum == "Q":
                    cardNum = "queen"
                if cardNum == "K":
                    cardNum = "king"
                if cardNum == "1":
                    cardNum = "ace"
                card = cardNum + "_of_" + suit + ".png"     #If it is a picture card it does the same
            cardImage = pygame.image.load(os.path.join("images", card))  #Finds the file that has the png
            image = pygame.transform.scale(cardImage, (self.cardWidth, self.cardHeight))    #Changes the size of the png
            self.dealerCardImages.append(image)     #Adds the card images to an array
            self.lastDealerCardDealt += 1

    def convert_card(self, cardNum):    #Converts the dealer's card to an integer and adds it to the total
        try:
            num = int(self.dealerCards[cardNum][:-1])
            if num == 1:
                num += 10
        except:
            num = 10
        self.dealerTotal += num     


    def shuffle_deck(self):    #Shuffles the deck
        random.shuffle(self.cards)
    
    def deal_card(self):
        card = self.cards.pop()     #Removes next card from the deck and stores it
        self.dealerCards.append(card)   #Adds the card to the list of dealer cards

    def dealer_turn(self):
        if self.dealerTotal < 17:   #When it is the dealer's turn if their total is less than 17 they take another card
            self.deal_card()
            self.convert_card(self.lastDealerCardDealt)
            self.load_card_images()
            time.sleep(1.5)
        if self.dealerTotal > 16:   #If their total is greater than 16 they don't draw antoher card
            return True

    def convert_ace(self):
        numOfAces = 0
        for card in self.dealerCards:   #Loops through all of the dealers cards and checks of there are any aces
            if card[:-1] == "1":
                numOfAces += 1  #Adds one to the total if there is an ace
        if numOfAces > 0:
            while self.dealerTotal > 21:    #If the player has any aces and their total is more than 21 it will change the value of the aces from 11 to 1
                self.dealerTotal -= 10
                numOfAces -= 1

    def reset_deck(self):   #Retets the deck if their are less than 10 cards then shuffles it
        if len(self.cards) < 10:
            self.cards += ['1C', '1S', '1D', '1H', '2C', '2S', '2D', '2H', '3C', '3S', '3D', '3H', '4C', '4S', '4D', '4H',
                            '5C', '5S', '5D', '5H', '6C', '6S', '6D', '6H', '7C', '7S', '7D', '7H', '8C', '8S', '8D', '8H',
                            '9C', '9S', '9D', '9H', '10C', '10S', '10D', '10H', 'JC', 'JS', 'JD', 'JH', 'QC', 'QS', 'QD', 'QH',
                            'KC', 'KS', 'KD', 'KH']
            self.shuffle_deck()

    def reset_dealer(self):     #Resets the dealer once the round is done
        self.dealerCards = []
        self.dealerCardImages = []
        self.numOfDealerCards = 0
        self.dealerTotal = 0
        self.lastDealerCardDealt = 0

class Player(Dealer):   
    def __init__(self, cards, money):
        super(Player, self).__init__(cards)
        self.money = money
        self.playerCards = []
        self.playerCardImages = []
        self.numOfPlayerCards = 0
        self.playerTotal = 0
        self.lastPlayerCardDealt = 0
        self.bet = 10
        self.Moneyfont = pygame.font.SysFont("comicsans", 25)
        self.Betfont = pygame.font.SysFont("comicsans", 35)
        self.won = False
        self.lost = False
        self.draw = False
        self.winnings = 0

    def load_card_images(self):      #Loads the images of the player's cards into an array
        self.numOfPlayerCards = len(self.playerCards)
        for i in range(self.lastPlayerCardDealt, self.numOfPlayerCards):
            cardNum = self.playerCards[i][:-1]
            cardSuit = self.playerCards[i][len(self.playerCards[i])-1:]
            if cardSuit == "C":
                suit = "clubs"
            if cardSuit == "S":
                suit = "spades"
            if cardSuit == "D":
                suit = "diamonds"
            if cardSuit == "H":
                suit = "hearts"

            if cardNum > "1" and cardNum < "11":
                card = cardNum + "_of_" + suit + ".png"     #If it is a number card it gets the card num and suit and uses it to find the right png for the card
            else:
                if cardNum == "J":
                    cardNum = "jack"
                if cardNum == "Q":
                    cardNum = "queen"
                if cardNum == "K":
                    cardNum = "king"
                if cardNum == "1":
                    cardNum = "ace"
                card = cardNum + "_of_" + suit + ".png"     #If it is a picture card it does the same
            cardImage = pygame.image.load(os.path.join("images", card))     #Finds the file that has the array
            image = pygame.transform.scale(cardImage, (self.cardWidth, self.cardHeight))    #Changes the size of the image
            self.playerCardImages.append(image)     #Adds the image to an array
            self.lastPlayerCardDealt += 1

    def convert_card(self, cardNum):    #Converts the player's card to an integer and adds it to the total
        try:
            num = int(self.playerCards[cardNum][:-1])
            if num == 1:
                num += 10
        except:
            num = 10
        self.playerTotal += num

    def convert_ace(self):  #Converts the value of an ace to 1 if the total is over 21
        numOfAces = 0
        for card in self.playerCards:
            if card[:-1] == "1":
                numOfAces += 1
        if numOfAces > 0:
            while self.playerTotal > 21:
                self.playerTotal -= 10
                numOfAces -= 1

    def deal_card(self):
        card = self.cards.pop()     #Removes next card from the deck and stores it
        self.playerCards.append(card)   #Adds the card to the list of player cards

    def display_money(self, screen):
        moneyText = self.Moneyfont.render("Money: £" + str(self.money), 1, (0, 0, 0))   
        screen.blit(moneyText, (10, 40))    #Displays the user's money in the top left

    def display_bet(self, screen, betMade): #Displays the bet amount
        if not betMade:
            betText = self.Betfont.render("£" + str(self.bet), 1, (255, 0, 0))
        else:   #Bet changes to green when bet placed
            betText = self.Betfont.render("£" + str(self.bet), 1, (0, 200, 0))
        screen.blit(betText, (930, 520))

    def increase_bet(self):
        if self.money > self.bet:   #Increases the bet by 10 if the player has enough money
            self.bet += 10

    def decrease_bet(self): #Decrease the bet amount by 10 if it is over 10
        if self.bet > 10:
            self.bet -= 10

    def display_result(self, screen):   #Displays how much the player has won or lost or if they've drawn
        resultFont = pygame.font.SysFont("comicsans", 100)
        resultText = ""
        if self.won:
            resultText = "You won £" + str(self.winnings)
        if self.lost:
            resultText = "You lost £" + str(self.bet)
        if self.draw:
            resultText = "Draw"
        result = resultFont.render(resultText, 1, (255, 0, 0))
        screen.blit(result, (225, 300))

    def win(self):
        self.winnings = self.bet * 2
        self.money += self.winnings

    def reset_player(self): #Resets the player at the end of the round
        self.playerCards = []
        self.playerCardImages = []
        self.numOfPlayerCards = 0
        self.playerTotal = 0
        self.lastPlayerCardDealt = 0
        self.bet = 10
        self.won = False
        self.lost = False
        self.draw = False
        self.winnings = 0

class Button():
    def __init__(self, x_pos, y_pos, width, height, colour, text, text_size, text_x, text_y):
        self.width = width
        self.height = height
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.colour = colour
        self.text = text
        self.text_size = text_size
        self.text_y = text_y
        self.text_x = text_x
        self.rect = pygame.Rect(self.x_pos, self.y_pos, self.width, self.height)
        self.font = pygame.font.SysFont("dejavuserif", self.text_size)

    def display_button(self, screen):   #Displays the button
        buttonText = self.font.render(self.text, 1, (0, 0, 0))
        pygame.draw.rect(screen, self.colour, self.rect, 0, 30)
        screen.blit(buttonText, (self.text_x, self.text_y))

    def button_pressed(self, mouse):    #Checks if the button has been pressed
        mouseButtons = pygame.mouse.get_pressed(num_buttons=3)
        if pygame.Rect.colliderect(mouse, self.rect) and mouseButtons[0]:
            return True
        else:
            return False
        

class Text_box():
    def __init__(self, x_pos, y_pos, header, hidden):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.header = header
        self.hidden = hidden
        self.rect = pygame.Rect(self.x_pos, self.y_pos, 500, 50)
        self.boxSelected = False
        self.input = ""
        self.font = pygame.font.SysFont("dejavuserif", 30)

    def display_box(self, screen):  #Displays the box that can be typed in
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 0, 5)
        self.display_header(screen)
        self.display_input(screen)

    def display_header(self, screen):   #Displays the header that says what the box is for
        headerText = self.font.render(self.header, 1, (0, 0, 0))
        screen.blit(headerText, (self.x_pos, self.y_pos-35))

    def check_if_selected(self, mouse): #Checks if the box has been selected
        mouseButtons = pygame.mouse.get_pressed(num_buttons=3)
        if pygame.Rect.colliderect(mouse, self.rect) and mouseButtons[0]:
            self.boxSelected = True
        elif not pygame.Rect.colliderect(mouse, self.rect) and mouseButtons[0]:
            self.boxSelected = False

    def enter_text(self, event):    #Stores the input from the keyboard and if the backspace is pressed to delete characters
        if self.boxSelected:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.input = self.input[:-1:]
                elif len(self.input) <= 30:
                    self.input += event.unicode

    def display_input(self, screen):    #Displays the input from the user and replaces it with an asterisk if it is hidden
        if self.hidden:
            newText = "*" * len(self.input)
        else:
            newText = self.input
        inputText = self.font.render(newText, 1, (0, 0, 0))
        screen.blit(inputText, (self.x_pos+5, self.y_pos+7))
