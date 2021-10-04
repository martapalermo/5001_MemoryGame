import turtle
from turtle import *
import random

# set up screen
wn = turtle.Screen()
wn.screensize(840, 800)
wn.title("CS5001 Memory Game")
wn.bgcolor("beige")
    
class Board:
    ''' Board class manages the creation of the specs for the various different
        elements necessary to set the playing board'''
    def __init__(self):
        ''' init create class, and creates the additional elements that are
            necessary for the board settings ie. player name and number of cards
            selected to play'''
    
        self.board = Turtle()
        self.board.up()
        self.board.pensize(5)
        self.board.color("black")
        
        self.leaderboard = []

    def set_player(self):
        ''' Method returns the name of the player'''
        self.player = Turtle()
        self.player.player_name = str(turtle.textinput("CS5001 Memory Game", "Your Name"))
        
        return self.player.player_name

    def set_card_number(self):
        ''' Method returns the selected number of cards to play with. The user input
            will get rounded up or down depending on entered int.'''
        self.card = Turtle()
        self.card.card_num = int(turtle.numinput("Set up", "# of Cards to Play: (8, 10 or 12)",
                                                 12, minval=8, maxval=12))
        wn.register_shape("card_warning.gif")
        if self.card.card_num == 8:
            self.card.card_num = 8
            
        elif self.card.card_num != 10 and self.card.card_num < 10:
            self.card.goto(0,0)
            
            wn.ontimer(self.card.shape("card_warning.gif"), 2000)
            self.card.hideturtle()
            
            self.card.card_num = 10
            
        elif self.card.card_num != 12 and self.card.card_num >= 11:
            self.card.goto(0,0)
            wn.ontimer(self.card.shape("card_warning.gif"), 2000)
            self.card.hideturtle()
            
            self.card.card_num = 12
            
        return self.card.card_num


    def open_leaderboard(self):
        ''' Method opens the leaderboard text file'''
        with open('leaderboard.txt', mode = 'r') as infile:
            for line in infile:
                line = line.strip("\n").split(' ')
                # print(line)
                line[0] = int(line[0])
                self.leaderboard.append(line)
    
        
    def final_leaderboard_sort(self):
        ''' Method sorts lines in leaderboard from
            smallest -> greatest value of guesses '''
        self.leaderboard.sort(key=lambda x: x[0])
        
    def main_gameboard(self):
        ''' Method creates the main game board that will hold the cards.'''
        self.board.goto(-350, 320)
        self.board.down()
        for i in range(2):
            self.board.forward(500)
            self.board.right(90)
            self.board.forward(550)
            self.board.right(90)

    def status_board(self):
        ''' Method creates the smaller status board that keeps track of
            player's number of guesses and matches - score keeper'''
        self.board.up()
        self.board.goto(-350, -270)
        self.board.down()
        for i in range(2):
            self.board.forward(500)
            self.board.right(90)
            self.board.forward(80)
            self.board.right(90)
        self.board.write("Player Status:", font=("Verdana", 20, "normal"))

        

    def leader_board(self):
        ''' Method creates the leader board, which keeps track of all the
            "highscores" with player names'''
        
        self.board.color("blue")
        self.board.up()
        self.board.goto(190, 320)
        self.board.down()
        for i in range(2):
            self.board.forward(210)
            self.board.right(90)
            self.board.forward(550)
            self.board.right(90)
        self.board.up()
        self.board.goto(295, 275)
        self.board.down()
        self.board.write("Leaderboard:", font=("Verdana", 20, "normal"), align='center')

        self.board.up()
        self.board.goto(295, 260) 
        self.board.down()
    
        self.lb_coordinates  = [(295, 225), (295, 175), (295, 125), (295, 75), (295, 25), (295, -25)]
    
        for i in range(len(self.leaderboard)):
            self.board.up()
            self.board.goto(self.lb_coordinates[i][0], self.lb_coordinates[i][1])

            remove_characters=["[", "]", ",", "'"]
            leaderboard_entry = str(self.leaderboard[i])
            for character in remove_characters:
                leaderboard_entry = leaderboard_entry.replace(character, '')
            self.board.write(leaderboard_entry, font=("Verdana", 18, "normal"), align='center')

        self.board.hideturtle()

    def add_new_score(self, score, player):
        '''Method takes care of adding new player's name + guesses to leaderboad
            as well as re-sorting all new data in the correct order'''
        new_score = []
        new_score.append(score)
        new_score.append(player)
        
        self.leaderboard.append(new_score)

        self.leaderboard.sort(key=lambda x: x[0])
        
        if len(self.leaderboard) > 6:
            self.leaderboard = self.leaderboard[:6] # limiting 6 participants on the board
            
        print(self.leaderboard)


    def update_leaderboard(self):
        ''' Method writes the output txt file'''
        with open("leaderboard.txt", mode = 'w') as outfile:
                for element in self.leaderboard:
                    string = str(element[0]) + ' ' + str(element[1]) + '\n'
                    outfile.write(string)
        
    def quit_button(self):
        ''' Method creates and places the "quit" button for the game'''
        quit_turtle = Turtle()
        quit_screen = Screen()
        quit_turtle.up()
        quit_turtle.goto(297, -307)
        quit_turtle.down()

        quit_screen.register_shape("quitbutton.gif")
        quit_turtle.shape("quitbutton.gif")
   

class Card:
    ''' Card class creates an element of playing card'''
    def __init__(self, front, back, coordinate, area):
        ''' init creates card class, creating attritbutes to the card,
            in this case: front of the card = image/number on the card
            back, the same back image for all cards
            coordiantes being the position coordinates for all cards on board
            area being the area available to click on in order to flip cards'''
        
        self.front = front
        self.back = back
        self.coordinate = coordinate
        self.area = area
        
        self.flipped = False

        
class Game:
    ''' Game class manages the game. It uses user input to determine how
        cards are created and set up the board according to the player's
        selections.'''
    
    def __init__(self):
        ''' init creates the class and manages the number of cards
            set by player'''

        self.board = Board()
        self.board.main_gameboard()
        self.board.status_board()
        self.board.open_leaderboard()
        self.board.leader_board()
        self.board.quit_button()
        
        player_name = self.board.set_player()
        card_number = self.board.set_card_number()

        self.player = player_name
        self.score = turtle.Turtle()
        self.t = Turtle()
        self.num_cards = int(card_number)


        self.guesses = 0
        self.matches = 0
        
        self.leaderboard = []
        self.cards_in_game = []
        
        card_list12 = ["2_of_clubs.gif", "2_of_diamonds.gif", "ace_of_diamonds.gif",
                       "jack_of_spades.gif", "king_of_diamonds.gif", "queen_of_hearts.gif",
                       "2_of_clubs.gif", "2_of_diamonds.gif", "ace_of_diamonds.gif",
                       "jack_of_spades.gif", "king_of_diamonds.gif", "queen_of_hearts.gif"]


        card_list12_shuffled = random.shuffle(card_list12)

        card_list10 = ["2_of_clubs.gif", "2_of_diamonds.gif", "ace_of_diamonds.gif", "jack_of_spades.gif",
                      "king_of_diamonds.gif", "2_of_clubs.gif", "2_of_diamonds.gif", "ace_of_diamonds.gif",
                      "jack_of_spades.gif","king_of_diamonds.gif"]

        card_list10_shuffled = random.shuffle(card_list10)

        card_list8 = ["2_of_diamonds.gif", "ace_of_diamonds.gif", "jack_of_spades.gif", "king_of_diamonds.gif",
                     "2_of_diamonds.gif", "ace_of_diamonds.gif", "jack_of_spades.gif", "king_of_diamonds.gif"]

        card_list8_shuffled = random.shuffle(card_list8)


        self.card_lst = []
        
        if self.num_cards == 12:
            self.card_lst = card_list12
            
        elif self.num_cards == 10:
            self.card_lst = card_list10
            
        else:
            self.card_lst = card_list8

        self.shuffled_cards = self.card_lst 

        turtle_list = [] # creates lst of turtles which take care of individual cards
        for i in range(self.num_cards):
            turtle_list.append(turtle.Turtle())


        for element in range(self.num_cards): # element = cards
            wn = turtle.Screen()
            
            coordinate = self.assign_position(self.num_cards, element)
            
            area = self.calculate_xy(coordinate)
            
            # setting the front of the card
            front = self.shuffled_cards.pop()
            wn.register_shape(front)

            # setting the back of the card 
            wn.register_shape("card_back.gif")
            back = "card_back.gif"

            # creating a card with all parameter
            card = Card(front, back, coordinate, area)
            self.cards_in_game.append({'turtle': turtle.Turtle(), 'card':card})

    
    def deal(self):
        ''' Method deals the previously selected number of cards on the board,
            fillped back'''
        
        for i in range(len(self.cards_in_game)):
            card = turtle.Turtle()

        for card in self.cards_in_game:
            card['turtle'].showturtle()
            card['turtle'].up()
            card['turtle'].goto(card['card'].coordinate)
            card['turtle'].down()
            card['turtle'].shape(card['card'].back)
        
            self.flipped = False
        

    def assign_position(self, num_cards, index):
        ''' Method returns a list of coordinates that is dependent on user
            selection of card numbers for playing.'''
        
        coordinate_12lst = [(-280, 215), (-160, 215), (-40, 215), (80, 215),
                            (-280, 45), (-160, 45), (-40, 45), (80, 45),
                            (-280, -125), (-160, -125), (-40, -125), (80, -125)]

        coordinate_10lst = [(-280, 215), (-160, 215), (-40, 215),
                            (-280, 45), (-160, 45), (-40, 45), (80, 45),
                            (-160, -125), (-40, -125), (80, -125)]

        coordinate_8lst = [(-280, 120), (-160, 120), (-40, 120), (80, 120),
                           (-280, -50), (-160, -50), (-40, -50), (80, -50)]
 

        coordinate_lst = []
        if num_cards == 12:
            coordinate_lst = coordinate_12lst
        if num_cards == 10:
            coordinate_lst = coordinate_10lst
        if num_cards == 8:
            coordinate_lst = coordinate_8lst

        return coordinate_lst[index]
    

    def write_score(self):
        ''' Method used to keep score '''
        pen =self.score
        pen.speed(0)
        pen.color("black")
        pen.up()
        pen.hideturtle()
        pen.goto(-320, -325)
        pen.clear()
        pen.write("Guesses: {}   Matches: {}".format(self.guesses, self.matches), font=("Verdana", 20, "normal"))    
    

    def on_click(self, x, y):
        ''' Method specifies coordinates/area of the cards and quit button
            on playing board facilitating onclick event.
            Also takes care of score keeping: matches + guesses'''
        
        quit_screen = turtle.Screen()
        quit_turtle = turtle.Turtle()
        
        chosen = None
        for card in self.cards_in_game:
            if x < card['card'].area[0] and x > card['card'].area[1] and y < card['card'].area[2] and y > card['card'].area[3]:
                chosen = card
                self.flip_card(card)

    
            elif x < 325 and x > 269 and y < -288 and y > -326:
                quit_screen.register_shape("quitmsg.gif")
                quit_screen.ontimer(quit_turtle.shape("quitmsg.gif"), 2000)
                print("Please click one more time on the screen to exit!")
                quit_screen.exitonclick()
                

        count = 0
        for game_card in self.cards_in_game:
            if game_card['card'].flipped and game_card != chosen:
                count= 2 # 2 cards selected

                if game_card['card'].flipped and game_card['card'].front == chosen['card'].front: # 2 flipped cards match
                    match = True
                    previous_card = game_card
                    self.matches += 1 #
                    self.guesses += 1
                    self.write_score()
                    print("matched: ", self.matches)
                else:
                    match = False
                    previous_card = game_card
                    self.matches = self.matches
                    self.guesses += 1
                    self.write_score()
                    print("guessed: ", self.guesses)    

        if count == 2:
            if match == True:
                score = 1
                previous_card['card'].flipped = False
                chosen['card'].flipped=False
                previous_card['turtle'].hideturtle()
                chosen['turtle'].hideturtle()
                 
            else:
                score = 0 
                self.flip_card(previous_card)
                self.flip_card(chosen)
                
        
    
        if self.end_game() == True:
            
            self.board.add_new_score(self.guesses, self.player)
            self.board.update_leaderboard()
            
            quit_screen.register_shape("winner.gif")
            quit_turtle.shape("winner.gif")
            print("Please click one more time on the screen to exit!")
            quit_screen.exitonclick()


    
    def end_game(self):
        ''' Method determines whether there are any more cards on the board.
            It returns booleans to then trigger quit msg/winner msg'''
        if self.matches == (self.num_cards / 2):
            return True
        return False


    def calculate_xy(self, coordinate):
        ''' Method calculates the area of a set card depending on
        the coordinates being passed. The coordinates are from the list
        previously created'''
        area = []
        
        x1 = coordinate[0] + 50
        area.append(x1)

        x2 = coordinate[0] - 50
        area.append(x2)

        y1 = coordinate[1] + 75
        area.append(y1)

        y2 = coordinate[1] - 75
        area.append(y2)
        
        return area
         
    def clear_card(self, card):
        ''' Method clears cards that are matches from the board'''
        self.t = Turtle()
        wn= turtle.Screen()
        
        self.t.up()
        self.t.goto(card.coordinate)
        wn.onclick(self.t.clear())
        self.t.clear()



    def flip_card(self, card):
        ''' Method flips cards accordingly. If a card "flipped" status = False
        meaning the back is facing us, it will turn the status to True and flip
        to the front (where the card's image shows), and vice versa.'''
        self.t = Turtle()
       
        if card['card'].flipped == False:
            card['card'].flipped = True
            card['turtle'].up()
            card['turtle'].goto(card['card'].coordinate)
            card['turtle'].shape(card['card'].front)
        else:
            card['card'].flipped = False
            card['turtle'].up()
            card['turtle'].goto(card['card'].coordinate)
            card['turtle'].shape(card['card'].back)

def main():
    wn = turtle.Screen()

    game = Game()    
    game.deal()

    wn.onclick(game.on_click)

    turtle.mainloop()

main()
    
   
