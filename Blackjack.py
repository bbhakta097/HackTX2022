from ast import Continue
from asyncore import ExitNow
from bdb import Breakpoint #A library to manually exit programs
from email.policy import default #A library to have default key word
import random
from sys import breakpointhook
from turtle import reset


CardDict = {
    "Ace of Spades": 10,  "Ace of Hearts": 11, "Ace of Clubs": 12, "Ace of Diamonds": 13, 
    "2 of Spades": 20,  "2 of Hearts": 21, "2 of Clubs": 22, "2 of Diamonds": 23, 
    "3 of Spades": 30, "3 of Hearts": 31, "3 of Clubs": 32, "3 of Diamonds": 33,
    "4 of Spades": 40,  "4 of Hearts": 41, "4 of Clubs": 42, "4 of Diamonds": 43,
    "5 of Spades": 50, "5 of Hearts": 51, "5 of Clubs": 52, "5 of Diamonds": 53,
    "6 of Spades": 60, "6 of Hearts": 61, "6 of Clubs": 62, "6 of Diamonds": 63,  
    "7 of Spades": 70, "7 of Hearts": 71, "7 of Clubs": 72, "7 of Diamonds": 73,
    "8 of Spades": 80, "8 of Hearts": 81, "8 of Clubs": 82, "8 of Diamonds": 83,
    "9 of Spades": 90, "9 of Hearts": 91, "9 of Clubs": 92, "9 of Diamonds": 93,
    "10 of Spades": 100, "10 of Hearts": 101, "10 of Clubs": 102, "10 of Diamonds": 103,
    "Jack of Spades": 110, "Jack of Hearts": 111, "Jack of Clubs": 112, "Jack of Diamonds": 113,
    "Queen of Spades": 120, "Queen of Hearts": 121, "Queen of Clubs": 122, "Queen of Diamonds": 123,
    "King of Spades": 130, "King of Hearts": 131, "King of Clubs": 132, "King of Diamonds": 133,
    }

#a function to store and return card values based on which card was pulled from the dictionary(using key values)
def counting_card_value(tracker_value):
    if 10 <= tracker_value <= 13 :#a case for an Ace card(default value 11)(any suit)
       card_value = 11 
    elif 20 <= tracker_value <= 23 :#a case for a 2 card(any suit)
       card_value = 2
    elif 30 <= tracker_value <= 33 :#a case for a 3 card(any suit)
       card_value = 3
    elif 40 <= tracker_value <= 43 :#a case for a 4 card(any suit)
       card_value = 4
    elif 50 <= tracker_value <= 53 :#a case for a 5 card(any suit)
       card_value = 5
    elif 60 <= tracker_value <= 63 :#a case for a 6 card(any suit)
       card_value = 6
    elif 70 <= tracker_value <= 73 :#a case for a 7 card(any suit)
       card_value = 7
    elif 80 <= tracker_value <= 83 :#a case for a 8 card(any suit)
       card_value = 8
    elif 90 <= tracker_value <= 93 :#a case for a 9 card(any suit)
       card_value = 9
    else : #a case for a face card(any suit)
       card_value = 10
    return card_value

def userPlays(userHand, player_choice, bet_amount, user_count, chips):#a function to track users turn during a round
  random_card = random.choice(list(CardDict.keys()))
  userHand.append(random_card)
  tracker_value = CardDict.get(random_card)
  user_count = user_count + counting_card_value(tracker_value)
  del CardDict[random_card]
  while user_count < 21 :
    match player_choice :
      case 1: #If the player chooses to hit(draw another card)
          random_card = random.choice(list(CardDict.keys()))
          userHand.append(random_card)
          tracker_value = CardDict.get(random_card)
          user_count = user_count + counting_card_value(tracker_value)
          del CardDict[random_card]
      case 2: #if the user chooses to stand(draw no more cards)
          print("You've decided to stand.")
          break
      case 3: #if the user chooses to double down(increase their bet by 2 and only draw 1 extra card)
          chips = chips - bet_amount
          random_card = random.choice(list(CardDict.keys()))
          userHand.append(random_card)
          tracker_value = CardDict.get(random_card)
          user_count = user_count + counting_card_value(tracker_value)
          del CardDict[random_card]
          break
  return user_count


def endCases(user_count, dealer_count, chips, bet_amount, dealerHand):
  #The following conditional statements are based upon the results of the round of poker
  #Below this point you will find many different scenarios and unique outputs to inform the user
  #of the outcome of the round
  if (dealer_count > user_count) and (dealer_count < 21) and (user_count < 21) :
    print("\nDealer total is:: ", dealer_count, "\nYour total is:: ", user_count)
    print("\nHouse wins :(\n")#for any round the user loses, their bet amount will not be returned to them, and their chips will be updated for the next round
    print("\nDealer's hidden card was ", dealerHand[0])
    return chips
  elif (dealer_count < user_count) and (dealer_count < 21) and (user_count < 21) :
    print("\nDealer total is:: ", dealer_count, "\nYour total is:: ", user_count)
    print("\nYou win! :D\n")
    print("\nDealer's hidden card was ", dealerHand[0])
    chips = chips + (bet_amount * 2)#For any round the user wins, they will have their bet amount returned double
    return chips
  elif user_count > 21 and dealer_count < 21:
    print("\nYour total is:: ", user_count)
    print("\nYou broke 21 and lost :( \n")
    print("\nDealer's hidden card was ", dealerHand[0])
    return chips
  elif dealer_count > 21 and user_count < 21:
    print("\nDealer total is:: ", dealer_count)
    print("\nDealer broke 21, so you win! :D ")
    print("\nDealer's hidden card was ", dealerHand[0])
    chips = chips + (bet_amount * 2)
    return chips
  elif dealer_count > 21 and user_count > 21:
    print("\nDealer total is:: ", dealer_count, "\nYour total is:: ", user_count)
    print("\nYou and the dealer broke 21, so the round is a tie.\n")
    print("\nDealer's hidden card was ", dealerHand[0])
    chips = chips + bet_amount
    return chips
  elif (user_count == 21) and (dealer_count != 21):
    print("\nDealer total is:: ", dealer_count, "\nYour total is:: ", user_count)
    print("\nBLACKJACK!!!! You win! :D\n")
    print("\nDealer's hidden card was \n", dealerHand[0])
    chips = chips + (bet_amount * 2.5)
    return chips
  elif (dealer_count is 21) and (user_count is not 21):
    print("\nDealer total is:: ", dealer_count, "\nYour total is:: ", user_count)
    print("\nDealer got blackjack, so you lose :( \n")
    print("\nDealer's hidden card was ", dealerHand[0])
    return chips
  elif user_count == dealer_count and user_count != 21 and dealer_count != 21:
    print("\nThe dealer's total is:: ", dealer_count, "\nYour total is:: ", user_count)
    print("\nDealer's hidden card was ", dealerHand[0])
    print("\nIt is a tie\n")
    chips = chips + bet_amount
    return chips
  else:
    print("\nDealer total is:: ", user_count, "\nYour total is:: ", user_count)
    print("\nYou both got blackjack, so the round is a tie.\n")
    print("\nDealer's hidden card was ", dealerHand[0])
    chips = chips + bet_amount
    return chips
  #end of round

chips = 50 #default chip starting value
Welc1 = "\n\n-------------------------------------------\n" #formatting 
Welc2 = "Welcome to Blackjack.\n" #welcomes user to the game of blackjack
Welc3 = "Starting amount: 50 chips" #informs the user of starting chips upon opening the game

print(Welc1.center(40)) #center text on the screen
print(Welc2.center(40))
print(Welc3.center(40))
print(Welc1.center(40))

'''
dealerHand = []#an array to hold the dealer's hand
userHandsplit1 = []#an array to hold the user's first hand after a split(a blackjack rule)
userHandsplit2 = []#an array to hold the user's second hand after a split
userHand = [] #an array to hold the user's hand
dealer_count = 0 #initial value for the dealer point total(based on card values defined later in the code)
user_count = 0 #initial value for the user point total
'''

def main(playValue, chips):
  
  #while the user wishes to continue to play and the user has at least 1 chip to play with
  while playValue == 1 and chips > 0:
    '''print("Press [1] if you would like to play, [2] to exit")
    playValue = int(input())
    if(playValue == 2):
        print("Error: Invalid Input. Exiting...")#exits program upon invalid input
        break'''
    
    dealerHand = []#an array to hold the dealer's hand
    userHandsplit1 = []#an array to hold the user's first hand after a split(a blackjack rule)
    userHandsplit2 = []#an array to hold the user's second hand after a split
    userHand = [] #an array to hold the user's hand
    dealer_count = 0 #initial value for the dealer point total(based on card values defined later in the code)
    user_count = 0 #initial value for the user point total
    
    #informs the user of the updated chip count from the previous round
    print("\nYour current amount of chips is::", chips, "\nHow much would you like to bet?")
    bet_amount = int(input())#takes input from user for their bet amount
    if bet_amount is 0 or (bet_amount > chips) :#testing for invalid input type
      print("Error: Invalid Input. Exiting...") 
      break#exit program upon invalid input
    chips = chips - bet_amount #subtract the bet amount from chip total
    print("\nYour chip count is now:: ", chips, "\n")#inform the user of their chip amount after their bet has been placed
    bet_amount_split = 0 #an initial value for the bet amount if the user chooses to split
    
    #This defines a dictionary for our deck of cards, each with a name and key
    #Each round, this dictionary will be reset as a full new deck of cards, ignoring any deletions in the previous round
    CardDict = {
    "Ace of Spades": 10,  "Ace of Hearts": 11, "Ace of Clubs": 12, "Ace of Diamonds": 13, 
    "2 of Spades": 20,  "2 of Hearts": 21, "2 of Clubs": 22, "2 of Diamonds": 23, 
    "3 of Spades": 30, "3 of Hearts": 31, "3 of Clubs": 32, "3 of Diamonds": 33,
    "4 of Spades": 40,  "4 of Hearts": 41, "4 of Clubs": 42, "4 of Diamonds": 43,
    "5 of Spades": 50, "5 of Hearts": 51, "5 of Clubs": 52, "5 of Diamonds": 53,
    "6 of Spades": 60, "6 of Hearts": 61, "6 of Clubs": 62, "6 of Diamonds": 63,  
    "7 of Spades": 70, "7 of Hearts": 71, "7 of Clubs": 72, "7 of Diamonds": 73,
    "8 of Spades": 80, "8 of Hearts": 81, "8 of Clubs": 82, "8 of Diamonds": 83,
    "9 of Spades": 90, "9 of Hearts": 91, "9 of Clubs": 92, "9 of Diamonds": 93,
    "10 of Spades": 100, "10 of Hearts": 101, "10 of Clubs": 102, "10 of Diamonds": 103,
    "Jack of Spades": 110, "Jack of Hearts": 111, "Jack of Clubs": 112, "Jack of Diamonds": 113,
    "Queen of Spades": 120, "Queen of Hearts": 121, "Queen of Clubs": 122, "Queen of Diamonds": 123,
    "King of Spades": 130, "King of Hearts": 131, "King of Clubs": 132, "King of Diamonds": 133,
    }
    
    x = 0
    tracker_value = 0
    
    for x in range(2) : #this will loop 2 times, once for each of the two initial cards drawn in a single hand
      random_card = random.choice(list(CardDict.keys()))#This will generate random cards from the deck dictionary
      dealerHand.append(random_card)#for each random card drawn, it is added to the dealer's hand(an array append)
      tracker_value = CardDict.get(random_card)#tracker value holds the key values within our deck dictionary
      dealer_count = dealer_count + counting_card_value(tracker_value)#The user point total is updated with the function call for counting card value
      del CardDict[random_card]#when a card is drawn, it is removed from the deck(CardDict)

    for x in range(2) :#this will loop 2 times, once for each of the two initial cards drawn in a single hand
      random_card = random.choice(list(CardDict.keys()))#This will generate random cards from the deck dictionary
      userHand.append(random_card)#for each random card drawn, it is added to the user's hand(an array append)
      tracker_value = CardDict.get(random_card)#tracker value holds the key values within our deck dictionary
      user_count = user_count + counting_card_value(tracker_value)#The user point total is updated with the function call for counting card value
      del CardDict[random_card]#when a card is drawn, it is removed from the deck(CardDict)
    
    
    print("You have:: ", userHand, " to start\n")#these statements inform the user of their hand and one card from the dealer
    print("Dealer has:: [", dealerHand[1], "] and one hidden card to start\n")
    if dealer_count == 21 :
      print("Dealer's second card was ", dealerHand[0])
      print("Dealer drew a blackjack to start. You lost.")
      print("Error: Invalid Input. Exiting...")#exits program upon invalid input
      breakpointhook
    elif user_count is 21:
      print("Dealer's second card was ", dealerHand[0])
      print("You drew a blackjack to start. You win! ")
      chips = chips + (bet_amount * 2.5)
      breakpointhook
    elif user_count is 21 and dealer_count is 21 :
      print("Both of you drew blackjack at the start, so its a tie")
      chips = chips + bet_amount
      breakpointhook    
     
    
    
    ace_count = 0 #a counter for the number of aces in each hand
    ace_usercount = 0 #a counter for the number of aces in each hand

    player_choice = 0 #a value tracker for which choices the user makes each round
    
    #user plays
    # 1 means hit
    # 2 means stand
    # 3 means double down
    # 4 means split
    
    #the following algorithm is based around the users plays and choices during the round
    #below this point the user will make multiple decisions and the program will update the hand(s) value(s)
    while user_count < 21 :
      print("Please enter [1] to hit, [2] to stand, [3] to double down")
      player_choice = int(input())
      if ( 1 > player_choice > 3) :
        print("Error: Invalid Input. Exiting...")
        chips = chips + bet_amount 
        break
      match player_choice :
          case 1: #If the player chooses to hit(draw another card)
              random_card = random.choice(list(CardDict.keys()))
              userHand.append(random_card)
              print("\nYou drew a(n) ", random_card)
              tracker_value = CardDict.get(random_card)
              user_count = user_count + counting_card_value(tracker_value)
              for i in range(len(userHand)) :  
                if (userHand[i] is "Ace of Hearts") or (userHand[i] is "Ace of Spades") or (userHand[i] is "Ace of Clubs") or (userHand[i] is "Ace of Diamonds") :
                  ace_usercount = ace_usercount + 1
                  print("Would you like that Ace,[", userHand[i],"] to be a 1? [y] or [n]")
                  ans = input()
                  if ans == 'y':
                    user_count = user_count - 10
                  
              print("\nYour current total is:: ", user_count)
              del CardDict[random_card]
          case 2: #if the user chooses to stand(draw no more cards)
              print("\nYou've decided to stand.")
              break
          case 3:#if the user chooses to double down(increase their bet by 2 and only draw 1 extra card)
              chips = chips - bet_amount
              bet_amount = bet_amount * 2
              random_card = random.choice(list(CardDict.keys()))
              userHand.append(random_card)
              print("\nYou doubled your bet and drew a(n) ", random_card)
              tracker_value = CardDict.get(random_card)
              user_count = user_count + counting_card_value(tracker_value)
              del CardDict[random_card]
              break
            
          case _: #for if the user does not enter a number 1-4
            print("Error: Invalid Input. Exiting...")
            break
        
    #the following algorithm is based upon standard house rules for a dealers play style
    while dealer_count < 16:
      random_card = random.choice(list(CardDict.keys()))
      dealerHand.append(random_card)
      tracker_value = CardDict.get(random_card)
      dealer_count = dealer_count + counting_card_value(tracker_value)
      print("\nDealer drew ", random_card, "and their total is now", dealer_count)
      del CardDict[random_card]
      if dealer_count > 21 or dealer_count < 16:
        for i in range(len(dealerHand)) :  
          if (dealerHand[i] is "Ace of Hearts") or (dealerHand[i] is "Ace of Spades") or (dealerHand[i] is "Ace of Clubs") or (dealerHand[i] is "Ace of Diamonds") :
            ace_count = ace_count + 1
            if (len(dealerHand) > 2 and dealer_count < 16) or (ace_count > 1 and dealer_count > 21):
              dealer_count = dealer_count - 10
              print("\nDealer drew ", random_card, "and their total is now", dealer_count)
    
    
    
    chips = endCases(user_count, dealer_count, chips, bet_amount, dealerHand)
    #chips = endCases(userCountSplit1, dealer_count, chips, bet_amount)
    #chips = endCases(userCountSplit1, dealer_count, chips, bet_amount)


    print("\n\nWould you like to play again?([y] or [n])\n")#ask user if they want to play again after end of round
    
    answer = input() 
    if answer == "y" :#if user wishes to play again
      playValue = 1
    elif answer == "n":#if user does not choose to play again
      playValue = 0
      break
    else:
      print("Error: Invalid Input. Exiting...")#exits program upon invalid input
      break
    
    
main(1, 50)