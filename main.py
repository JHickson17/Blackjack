import pygame
import time
import os
from database import *
from classes import *

pygame.init()

FPS = 60

WIDTH = 1200
HEIGHT = 700   #Height and width of the screen
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

GREEN = (39, 130, 51)       #RGB values for the colours
BLACK =(20, 20, 20)
GREY = (160, 160, 160)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

MENU_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("images", "menu background.XCF")), (WIDTH, HEIGHT))

def blackjack_display(player, dealer, betMade, standPressed, doublePressed):
    SCREEN.fill(GREEN)

    rect1 = pygame.Rect(900, 0, 400, 700)
    rect2 = pygame.Rect(925, 520, 250, 50)
    pygame.draw.rect(SCREEN, BLACK, rect1)
    pygame.draw.rect(SCREEN, WHITE, rect2)

    if betMade:
        display_player_cards(player, dealer)  #Once the player has placed their bet it will display their cards

    if standPressed:
        display_dealer_cards(dealer)  #Once the player has pressed stand it will display the dealer's cards

    display_buttons(betMade, player, doublePressed)    #Displays the buttons
    display_account()   #Displays the account that the player has signed in to

    player.display_money(SCREEN)    #Displays how much money the player has
    player.display_bet(SCREEN, betMade) #Displays the player's bet

    player.display_result(SCREEN)   #Once the user has won, lost or drawn it will display the result and how much money they have won or lost
    
    pygame.display.update()

    if player.won or player.draw or player.lost:
        time.sleep(3)       #Pauses the program for 3 seconds at the end of the round

def check_for_split(player):
    card1 = player.playerCards[0][:-1]
    card2 = player.playerCards[1][:-1]
    if card1 == card2:
        return True
    else:
        return False

def check_for_double(player):
    card1 = player.playerCards[0][:-1]
    card2 = player.playerCards[1][:-1]
    if player.playerTotal >= 9 and player.playerTotal <= 11:
        if card1 != "1" and card2 != "1":
            return True
    return False

def display_buttons(betMade, player, doublePressed):   #Displays all of the buttons
    decreaseBet.display_button(SCREEN)  #Displays the button that decreases the bet
    increaseBet.display_button(SCREEN)  #Displays the button that increases the bet
    placeBet.display_button(SCREEN) #Displays the button that places the bet
    returnToMenu.display_button(SCREEN)

    if betMade:
        hit.display_button(SCREEN)  #Only displays the hit and stand button once the bet has been placed
        stand.display_button(SCREEN)

        if check_for_split(player):
            split.display_button(SCREEN)

        if check_for_double(player) and not doublePressed:
            double.display_button(SCREEN)
        
def display_player_cards(player, dealer):    #Displays the player's cards
    start_x_position = (WIDTH / 2) - dealer.cardWidth
    for i in range(player.numOfPlayerCards): 
        SCREEN.blit(player.playerCardImages[i], ((start_x_position + (dealer.cardWidth*i) + (5*i)-150), 530))

def display_dealer_cards(dealer): #Displays the dealer's cards
    start_x_position = (WIDTH / 2) - dealer.cardWidth
    for i in range(dealer.numOfDealerCards): 
        SCREEN.blit(dealer.dealerCardImages[i], ((start_x_position + (dealer.cardWidth*i) + (5*i)-150), 20)) 

def mouse_rect():   #Creates a rect on the mouse and returns it
    mousePos = pygame.mouse.get_pos()
    mouse = pygame.Rect(mousePos[0], mousePos[1], 5, 5)
    return mouse

def counter(count):
    count += 1
    return count

def change_bet(player, mouse, count, lastPressed):  
    if decreaseBet.button_pressed(mouse) == True and count > (lastPressed+13):  #If the decrease the bet button is pressed it deceases the bet by £10
        player.decrease_bet()
        lastPressed = count
    if increaseBet.button_pressed(mouse) == True and count > (lastPressed+13):  #If the increase the bet button is pressed it inceases the bet by £10
        player.increase_bet()
        lastPressed = count
    return lastPressed

def get_result(player, dealer, dealerTurnDone):
    if dealer.dealerTotal > 21:   #If the dealers total is over 21 the player wins
        player.won = True
    elif player.playerTotal > dealer.dealerTotal and dealerTurnDone:  #If the player's total is greater than the dealer's total they win
        player.won = True

    elif player.playerTotal > 21: #If the player's total is over 21 they lose
        player.lost = True
    elif dealer.dealerTotal > player.playerTotal and dealerTurnDone:  #If the dealer's total is greater than the player's total the player loses
        player.lost = True

    elif player.playerTotal == dealer.dealerTotal and dealerTurnDone:   #If their totals are the same then it's a draw
        player.draw = True

def blackjack():
    statistics = {"roundsPlayed": 0,
                  "roundsWon": 0,
                  "roundsLost": 0,
                  "roundsDrawn": 0}
    userDetails = find_user(username.input) #Gets the users details if they have signed in

    if username.input == "":    #If they haven't signed in then they get given £100
        money = 100
        signedIn = False
    else:
        stats = load_statistics(username.input)[0]
        statistics["roundsPlayed"] = stats[0]
        statistics["roundsWon"] = stats[1]
        statistics["roundsLost"] = stats[2]
        statistics["roundsDrawn"] = stats[3]
        Username = userDetails[0][0] #If they have signed in it loads their username and the amount of money they have from the database
        money = userDetails[0][2]
        signedIn = True

    dealer = Dealer(cards)
    player = Player(cards, money)

    run = True
    clock = pygame.time.Clock()
    count = 0
    lastPressed = 0

    betMade = False
    standPressed = False
    doublePressed = False
    dealerTurnDone = False
    roundEnd = False
    startRound = True
    dealer.shuffle_deck() #Shuffles the deck of cards

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        count = counter(count)
        mouse = mouse_rect()

        if startRound:  #Checks if it is the start of the round
            player.start_round()    #The dealer and the player both get 2 cards
            player.load_player_images() #Loads the players card images into an array
            dealer.load_dealer_images()   #Loads the dealers card images into an array
            startRound = False

        canDouble = check_for_double(player)
        canSplit = check_for_split(player)

        if betMade == False:    #Checks if the player hasn't made a bet
            lastPressed = change_bet(player, mouse, count, lastPressed) #Lets the player change their bet

        if placeBet.button_pressed(mouse) and betMade == False: #Checks if the player has pressed the place bet button and if they haven't already placed a bet
            betMade = True 
            player.money -= player.bet  #Takes the bet from the players money

        if hit.button_pressed(mouse) and count > (lastPressed+60) and standPressed == False and betMade: #Checks if the player has pressed hit, if theu've pressed stand and if they've made a bet
            if player.won == False and player.lost == False and player.draw == False: #Checks that the player hasn't already won, lost or drawn
                player.deal_player_card()   #Gives the player another card
                player.convert_player_card(player.lastPlayerCardDealt)  #Converts the card into an integer and adds it onto their total
                player.load_player_images() #Loads the image for the card dealt and adds it to the array with the other images
                lastPressed = count

        if stand.button_pressed(mouse) and count > (lastPressed+60): #Checks if the player presses stand
            standPressed = True

        if betMade and double.button_pressed(mouse) and canDouble:
            player.money -= player.bet
            player.bet *= 2
            standPressed = True
            doublePressed = True
            player.deal_player_card()
            player.convert_player_card(player.lastPlayerCardDealt)
            player.load_player_images()

        if standPressed and not player.won: #Checks if the player has pressed stand and that they haven't already won
            dealerTurnDone = dealer.dealer_turn() #Gives the dealer a card if their total is 16 or less
            dealer.load_dealer_images()   #Loads the image for the card and adds it to the array with the other images

        player.convert_ace()    #If the players total is over 21 and they have and ace it changes the aces value to 1
        dealer.convert_ace()      #If the dealers total is over 21 and they have and ace it changes the aces value to 1

        get_result(player, dealer, dealerTurnDone)    #Checks if the player has won, lost or drawn

        if player.won:  #Checks if the player has won
            player.win()    #Pays the player double their bet
        
        blackjack_display(player, dealer, betMade, standPressed, doublePressed)

        if player.lost or player.won or player.draw:    #Checks if the round has ended
            roundEnd = True

        if roundEnd: #Checks if the round has ended
            if signedIn:    #Checks if the player is signed in to an account
                statistics["roundsPlayed"] += 1
                if player.won:
                    statistics["roundsWon"] += 1
                elif player.lost:
                    statistics["roundsLost"] += 1
                elif player.draw:
                    statistics["roundsDrawn"] += 1
                update_statistics(username.input, statistics["roundsPlayed"], statistics["roundsWon"], statistics["roundsLost"], statistics["roundsDrawn"])
                update_money(Username, player.money)    #Updates their money in the database
            dealer.reset_dealer() #Resets the dealers cards
            player.reset_player()   #Resets the players cards
            betMade = False
            standPressed = False
            dealerTurnDone = False
            roundEnd = False
            startRound = True

        if returnToMenu.button_pressed(mouse):
            break

def display_account():
    if username.input != "":    #Checks if the player is signed in
        font = pygame.font.SysFont("dejavuserif", 30)
        displayusername = font.render("Account: " + username.input, 1, RED)
        SCREEN.blit(displayusername, (50, 650))     #Displays the player's account

def display_menu():
    SCREEN.blit(MENU_BACKGROUND, (0, 0))

    display_account()
    play.display_button(SCREEN)     #Displays all of the buttons in the menu
    signIn.display_button(SCREEN)
    createAcc.display_button(SCREEN)
    leaderboardButton.display_button(SCREEN)
    if username.input != "":
        statisticsButton.display_button(SCREEN)
        signOut.display_button(SCREEN)
    quit.display_button(SCREEN)

    pygame.display.update() #Updates the display

def menu():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        mouse = mouse_rect()
        if play.button_pressed(mouse):  #If they press the play button it returns play
            return "play"
        
        if createAcc.button_pressed(mouse): #If they press the create account button it returns create account
            return "create account"
        
        if signIn.button_pressed(mouse):    #If they press the sign in button it returns sign in
            return "sign in"
        
        if leaderboardButton.button_pressed(mouse):
            return "leaderboard"
        
        if statisticsButton.button_pressed(mouse) and username.input != "":
            return "statistics"
        
        if signOut.button_pressed(mouse) and username.input != "":
            username.input = ""
            password.input = ""
            confirmPassword.input = ""
        
        if quit.button_pressed(mouse):  #If they press the quit button it returns quit
            return "quit"

        display_menu()  #Displays the menu

def sign_in_display():
    SCREEN.blit(MENU_BACKGROUND, (0, 0))    #Background image

    username.display_box(SCREEN)    #Displays the input boxes for the username and password
    password.display_box(SCREEN)

    back.display_button(SCREEN)     #Displays the buttons to confirm the sign in or go back to the menu
    confirm.display_button(SCREEN)

    pygame.display.update()     #Updated the display

def check_details(mouse):
    if confirm.button_pressed(mouse):   #Checks if the player has pressed confirm
        userDetails = find_user(username.input) #Gets the players details from the database using the username they inputted 
        try:
            Password = userDetails[0][1]    
        except:
            Password = None
        if Password == password.input:
            return True
        else:
            return False

def signed_in():
    font = pygame.font.SysFont("dejavuserif", 30)
    message = font.render("Signed in!", 1, RED)
    SCREEN.blit(message, (530, 450))
    pygame.display.update()
    time.sleep(2)

def incorrect_details():
    font = pygame.font.SysFont("dejavuserif", 30)
    errorMessage = font.render("Incorrect details. Try again.", 1, RED)
    SCREEN.blit(errorMessage, (440, 450))
    pygame.display.update()
    time.sleep(2)

def sign_in():
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            username.enter_text(event)  #Allows the user to type in the username and password boxes
            password.enter_text(event)

        mouse = mouse_rect()

        username.check_if_selected(mouse)   #Checks if the user has selected to type in either of the boxes
        password.check_if_selected(mouse)

        if back.button_pressed(mouse):  #If the user presses the back button it goes back to the menu
            username.input = ""
            password.input = ""
            confirmPassword.input = ""
            break

        correctDetails= check_details(mouse)

        if correctDetails:
            signed_in()
            break
        elif not correctDetails and confirm.button_pressed(mouse):
            incorrect_details()

        sign_in_display()   #Displays the sign in menu

def create_account_display(mouse, validPassword):
    SCREEN.blit(MENU_BACKGROUND, (0, 0))

    username.display_box(SCREEN)
    password.display_box(SCREEN)
    confirmPassword.display_box(SCREEN)

    back.display_button(SCREEN)
    confirm.display_button(SCREEN)

    if validPassword == "invalid" and confirm.button_pressed(mouse):
            password_error()
    elif validPassword == "username taken" and confirm.button_pressed(mouse):
        existing_username()
    elif validPassword == "passwords not matching" and confirm.button_pressed(mouse):
        passwords_not_matching()

    pygame.display.update()

def password_error():
    font = pygame.font.SysFont("dejavuserif", 30)
    errorMessage = font.render("Password must be between 8 and 20 character and contain at least 1 number", 1, RED)
    SCREEN.blit(errorMessage, (150, 515))
    pygame.display.update()
    time.sleep(2)

def existing_username():
    font = pygame.font.SysFont("dejavuserif", 30)
    errorMessage = font.render("Username taken. Try again", 1, RED)
    SCREEN.blit(errorMessage, (425, 515))
    pygame.display.update()
    time.sleep(2)

def passwords_not_matching():
    font = pygame.font.SysFont("dejavuserif", 30)
    errorMessage = font.render("Passwords do not match.", 1, RED)
    SCREEN.blit(errorMessage, (425, 515))
    pygame.display.update()
    time.sleep(2)

def account_created():
    font = pygame.font.SysFont("dejavuserif", 30)
    message = font.render("Account Created!", 1, RED)
    SCREEN.blit(message, (490, 515))
    pygame.display.update()
    time.sleep(2)

def create_account():
    run = True
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            username.enter_text(event)
            password.enter_text(event)
            confirmPassword.enter_text(event)

        mouse = mouse_rect()

        username.check_if_selected(mouse)
        password.check_if_selected(mouse)
        confirmPassword.check_if_selected(mouse)

        if back.button_pressed(mouse):
            username.input = ""
            password.input = ""
            confirmPassword.input = ""
            break

        validPassword = validate_password(mouse)

        if validPassword == "valid":
            add_user(username.input, password.input, 100)
            account_created()
            break

        create_account_display(mouse, validPassword)

def validate_password(mouse):
    existingRecord = find_user(username.input)
    containsNumber = False
    for i in range(10):
        if str(i) in password.input:    #Iterates through all of the characters in the password and checks if it contains a number
            containsNumber = True 
    try:
        if existingRecord[0][0] == username.input:
            return "username taken"
    except:
        pass
    if confirm.button_pressed(mouse):   #Only checks it once confirm has been pressed
        if len(password.input) >= 8 and len(password.input) <= 20:    #Checks if it's between 8 and 20 character long
            if password.input == confirmPassword.input:     #Checks if the same password has been entered both times
                if containsNumber == True:     #Checks if it contains a number
                    return "valid"     #Returns true if it's valid
            else:
                return "passwords not matching"
    return "invalid"    #Returns false if it isn't valid

def leaderboard():
    run = True
    clock = pygame.time.Clock()
    players = load_leaderboard()
    
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
        mouse = mouse_rect()
        SCREEN.blit(MENU_BACKGROUND, (0, 0))

        if len(players) < 10:
            n = len(players)
        else:
            n = 10
        for i in range(0, n):
            leaderboardPlace = str(i+1)
            player = players[i]
            if player[0] == username.input:
                colour = YELLOW
            else:
                colour = RED
            font = pygame.font.SysFont("dejavuserif", 45)
            text = font.render(leaderboardPlace+". "+str(player[0])+"    £"+str(player[1]), 1, colour)
            SCREEN.blit(text, (450, 135+(50*i)))
        returnToMenu.display_button(SCREEN)
        if returnToMenu.button_pressed(mouse):
            break
        pygame.display.update()

def statistics():
    run = True
    clock = pygame.time.Clock()
    stats = load_statistics(username.input)[0]
    
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
        mouse = mouse_rect()
        SCREEN.blit(MENU_BACKGROUND, (0, 0))
        rect = pygame.Rect(120, 200, 1000, 100)
        pygame.draw.rect(SCREEN, GREY, rect, 0, 10)

        font = pygame.font.SysFont("dejavuserif", 37)
        text = font.render("Rounds Played     Rounds Won     Rounds Lost     Rounds Drawn", 1, BLACK)
        SCREEN.blit(text, (140, 200))
        for i in range(4):
            statistic = font.render(str(stats[i]), 1, RED)
            SCREEN.blit(statistic, (230+(i*250), 250))
        returnToMenu.display_button(SCREEN)
        if returnToMenu.button_pressed(mouse):
            break
        pygame.display.update()


def main():
    run = True
    while run:
        time.sleep(0.5)
        menuSelection = menu()      

        if menuSelection == "play":
            menuSelection = blackjack()
        if menuSelection == "create account" and username.input == "":
            menuSelection = create_account()
        if menuSelection == "sign in" and username.input == "":
            menuSelection = sign_in()
        if menuSelection == "leaderboard":
            menuSelection = leaderboard()
        if menuSelection == "statistics" and username.input != "":
            menuSelection = statistics()
        if menuSelection == "quit":
            run = False



cards = ['1C', '1S', '1D', '1H', '2C', '2S', '2D', '2H', '3C', '3S', '3D', '3H', '4C', '4S', '4D', '4H',
        '5C', '5S', '5D', '5H', '6C', '6S', '6D', '6H', '7C', '7S', '7D', '7H', '8C', '8S', '8D', '8H',
        '9C', '9S', '9D', '9H', '10C', '10S', '10D', '10H', 'JC', 'JS', 'JD', 'JH', 'QC', 'QS', 'QD', 'QH',
        'KC', 'KS', 'KD', 'KH']

decreaseBet = Button(925, 575, 120, 50, GREY, "<--", 50, 955, 568)
increaseBet = Button(1055, 575, 120, 50, GREY, "-->", 50, 1085, 568)
placeBet = Button(925, 630, 250, 50, GREY, "Place bet", 40, 975, 630)
hit = Button(925, 465, 120, 50, GREY, "Hit", 40, 960, 470)
stand = Button(1055, 465, 120, 50, GREY, "Stand", 35, 1075, 472)
double = Button(925, 405, 120, 50, GREY, "Double", 30, 940, 412)
split = Button(1055, 405, 120, 50, GREY, "Split", 35, 1080, 410)
returnToMenu = Button(10, 10, 100, 30, GREY, "Quit", 25, 37, 11)

play = Button(400, 200, 400, 90, GREY, "PLAY", 70, 517, 205)
signIn = Button(400, 300, 400, 90, GREY, "SIGN IN", 60, 490, 310)
createAcc = Button(400, 400, 400, 90, GREY, "CREATE ACCOUNT", 40, 420, 420)
statisticsButton = Button(1030, 610, 150, 35, GREY, "STATISTICS", 20, 1055, 617)
leaderboardButton = Button(1030, 650, 150, 35, GREY, "LEADERBOARD", 15, 1050, 658)
signOut = Button(10, 10, 100, 30, GREY, "SIGN OUT", 17, 23, 15)
quit = Button(400, 500, 400, 90, GREY, "QUIT", 70, 517, 505)

username = Text_box(350, 200, "Enter Username:", False)
password = Text_box(350, 325, "Enter Password:", True)
confirmPassword = Text_box(350, 450, "Confirm Password:", True)
back = Button(350, 560, 225, 50, GREY, "Back", 40, 415, 560)
confirm = Button(610, 560, 225, 50, GREY, "Confirm", 40, 655, 560)

if __name__ == "__main__":
    main()
