import pygame
import time
import os
from database import *
from classes import *

pygame.init()

FPS = 60

WIDTH = 1200
HEIGHT = 700   #Height and width of the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

GREEN = (39, 130, 51)
BLACK =(20, 20, 20)
GREY = (160, 160, 160)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

MENU_BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join("images", "menu background.XCF")), (WIDTH, HEIGHT))

def blackjack_display(player, deck, betMade, standPressed):
    screen.fill(GREEN)

    rect1 = pygame.Rect(900, 0, 400, 700)
    rect2 = pygame.Rect(925, 520, 250, 50)
    pygame.draw.rect(screen, BLACK, rect1)
    pygame.draw.rect(screen, WHITE, rect2)

    if betMade == True:
        display_player_cards(player, deck)

    if standPressed == True:
        display_dealer_cards(deck)

    display_buttons(betMade)
    display_account()

    player.display_money(screen)
    player.display_bet(screen, betMade)

    player.display_result(screen)

    pygame.display.update()

    if player.won or player.draw or player.lost:
        time.sleep(3)

def display_buttons(betMade):   #Displays all of the buttons
    decreaseBet.display_button(screen)  #Displays the button that decreases the bet
    increaseBet.display_button(screen)  #Displays the button that increases the bet
    placeBet.display_button(screen) #Displays the button that places the bet

    if betMade:
        hit.display_button(screen)  #Only displays the hit and stand button once the bet has been placed
        stand.display_button(screen)

def display_player_cards(player, deck):    #Displays the player's cards
    start_x_position = (WIDTH / 2) - deck.cardWidth
    for i in range(player.numOfPlayerCards): 
        screen.blit(player.playerCardImages[i], ((start_x_position + (deck.cardWidth*i) + (5*i)-150), 530))

def display_dealer_cards(deck): #Displays the dealer's cards
    start_x_position = (WIDTH / 2) - deck.cardWidth
    for i in range(deck.numOfDealerCards): 
        screen.blit(deck.dealerCardImages[i], ((start_x_position + (deck.cardWidth*i) + (5*i)-150), 20)) 

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

def get_result(player, deck, dealerTurnDone):
    if deck.dealerTotal > 21:   #If the dealers total is over 21 the player wins
        player.won = True
    elif player.playerTotal > deck.dealerTotal and dealerTurnDone:  #If the player's total is greater than the dealer's total they win
        player.won = True

    elif player.playerTotal > 21: #If the player's total is over 21 they lose
        player.lost = True
    elif deck.dealerTotal > player.playerTotal and dealerTurnDone:  #If the dealer's total is greater than the player's total the player loses
        player.lost = True

    elif player.playerTotal == deck.dealerTotal and dealerTurnDone:   #If their totals are the same then it's a draw
        player.draw = True

def blackjack():
    userDetails = find_user(username.input)
    if username.input == "":
        money = 100
        signedIn = False
    else:
        Username = userDetails[0][0]
        money = userDetails[0][2]
        signedIn = True

    deck = Deck(cards)
    player = Player(cards, money)

    run = True
    clock = pygame.time.Clock()
    count = 0
    lastPressed = 0

    betMade = False
    standPressed = False
    dealerTurnDone = False
    roundEnd = False
    startRound = True
    deck.shuffle_deck()

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"

        count = counter(count)
        mouse = mouse_rect()

        if startRound:
            player.start_round()
            player.load_player_images()
            deck.load_dealer_images()
            startRound = False

        if betMade == False:    
            lastPressed = change_bet(player, mouse, count, lastPressed)

        if placeBet.button_pressed(mouse) and betMade == False:
            betMade = True
            player.money -= player.bet

        if hit.button_pressed(mouse) and count > (lastPressed+60) and standPressed == False and betMade:
            if player.won == False and player.lost == False and player.draw == False:
                player.deal_player_card()
                player.convert_player_card(player.lastPlayerCardDealt)
                player.load_player_images()
                lastPressed = count

        if stand.button_pressed(mouse) == True and count > (lastPressed+60):
            standPressed = True

        if standPressed and not player.won:
            dealerTurnDone = deck.dealer_turn()
            deck.load_dealer_images()

        player.convert_ace()
        deck.convert_ace()
        print(player.playerTotal)
        get_result(player, deck, dealerTurnDone)

        if player.won:
            player.win()
            
        blackjack_display(player, deck, betMade, standPressed)

        if player.lost == True or player.won == True or player.draw == True:
            roundEnd = True

        if roundEnd == True:
            if signedIn:
                update_money(Username, player.money)
            deck.reset_dealer()
            player.reset_player()   
            betMade = False
            standPressed = False
            dealerTurnDone = False
            roundEnd = False
            startRound = True

def display_account():
    if username.input != "":
        font = pygame.font.SysFont("dejavuserif", 30)
        displayusername = font.render("Account: " + username.input, 1, RED)
        screen.blit(displayusername, (50, 650))     

def display_menu():
    screen.blit(MENU_BACKGROUND, (0, 0))

    display_account()
    play.display_button(screen)     #Displays all of the buttons in the menu
    signIn.display_button(screen)
    createAcc.display_button(screen)
    quit.display_button(screen)

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
        
        if quit.button_pressed(mouse):  #If they press the quit button it returns quit
            return "quit"

        display_menu()  #Displays the menu

def sign_in_display():
    screen.blit(MENU_BACKGROUND, (0, 0))    #Background image

    username.display_box(screen)    #Displays the input boxes for the username and password
    password.display_box(screen)

    back.display_button(screen)     #Displays the buttons to confirm the sign in or go back to the menu
    confirm.display_button(screen)

    pygame.display.update()     #Updated the display

def check_details(mouse):
    if confirm.button_pressed(mouse):
        userDetails = find_user(username.input)
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
    screen.blit(message, (530, 450))
    pygame.display.update()
    time.sleep(2)

def incorrect_details():
    font = pygame.font.SysFont("dejavuserif", 30)
    errorMessage = font.render("Incorrect details. Try again.", 1, RED)
    screen.blit(errorMessage, (440, 450))
    pygame.display.update()
    time.sleep(2)

def sign_in():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            username.enter_text(event)  #Allows the user to type in the username and password boxes
            password.enter_text(event)

        mouse = mouse_rect()

        username.check_if_selected(mouse)   #Checks if the user has selected to type in either of the boxes
        password.check_if_selected(mouse)

        if back.button_pressed(mouse):  #If the user presses the back button it goes back to the menu
            break

        correctDetails= check_details(mouse)

        if correctDetails:
            signed_in()
            break
        elif not correctDetails and confirm.button_pressed(mouse):
            incorrect_details()

        sign_in_display()   #Displays the sign in menu

def create_account_display(mouse, validPassword):
    screen.blit(MENU_BACKGROUND, (0, 0))

    username.display_box(screen)
    password.display_box(screen)
    confirmPassword.display_box(screen)

    back.display_button(screen)
    confirm.display_button(screen)

    if not validPassword and confirm.button_pressed(mouse):
            password_error()

    pygame.display.update()

def password_error():
    font = pygame.font.SysFont("dejavuserif", 30)
    errorMessage = font.render("Password must be between 8 and 20 character and contain at least 1 number", 1, RED)
    screen.blit(errorMessage, (150, 515))
    pygame.display.update()
    time.sleep(2)

def account_created():
    font = pygame.font.SysFont("dejavuserif", 30)
    message = font.render("Account Created!", 1, RED)
    screen.blit(message, (490, 515))
    pygame.display.update()
    time.sleep(2)

def create_account():
    run = True
    while run:
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
            break

        validPassword = validate_password(mouse)

        if validPassword:
            add_user(username.input, password.input, 100)
            account_created()
            break

        create_account_display(mouse, validPassword)

def validate_password(mouse):
    containsNumber = False
    for i in range(10):
        if str(i) in password.input:    #Iterates through all of the characters in the password and checks if it contains a number
            containsNumber = True 
    if confirm.button_pressed(mouse):   #Only checks it once confirm has been pressed
        if len(password.input) >= 8 and len(password.input) <= 20:    #Checks if it's between 8 and 20 character long
            if password.input == confirmPassword.input:     #Checks if the same password has been entered both times
                if containsNumber == True:     #Checks if it contains a number
                    return True     #Returns true if it's valid

    return False    #Returns false if it isn't valid


def main():
    run = True
    while run:
        time.sleep(0.5)
        menuSelection = menu()      

        if menuSelection == "play":
            menuSelection = blackjack()
        if menuSelection == "create account":
            menuSelection = create_account()
        if menuSelection == "sign in":
            menuSelection = sign_in()
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

play = Button(400, 200, 400, 90, GREY, "PLAY", 70, 517, 205)
signIn = Button(400, 300, 400, 90, GREY, "SIGN IN", 60, 490, 310)
createAcc = Button(400, 400, 400, 90, GREY, "CREATE ACCOUNT", 40, 420, 420)
quit = Button(400, 500, 400, 90, GREY, "QUIT", 70, 517, 505)

username = Text_box(350, 200, "Enter Username:", False)
password = Text_box(350, 325, "Enter Password:", True)
confirmPassword = Text_box(350, 450, "Confirm Password:", True)
back = Button(350, 560, 225, 50, GREY, "Back", 40, 415, 560)
confirm = Button(610, 560, 225, 50, GREY, "Confirm", 40, 655, 560)

if __name__ == "__main__":
    main()
