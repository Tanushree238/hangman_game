import pygame
import math
import random

pygame.init()

## setup display
WIDTH, HEIGHT = 900, 500 #constant values
win = pygame.display.set_mode((WIDTH,HEIGHT)) #to set display size , this func accepts tupple argument 
# ( in starting with only this code window will just open nd then close)
pygame.display.set_caption("Hangman Game!") 
## end


## button variables
RADIUS = 25
GAP = 15
letters = []
startx = round((WIDTH - (RADIUS *2 + GAP) * 13) / 2)
starty = 400
for i in range(26):
	x = startx + GAP * 2 + ((RADIUS * 2 + GAP) * (i % 13))
	y = starty + ((i // 13) * (GAP + RADIUS * 2))
	letters.append([x, y, chr(i+65), True])
## end

## fonts
LETTER_FONT = pygame.font.SysFont('comicsans',40)
WORD_FONT = pygame.font.SysFont('comicsans',60)
TITLE_FONT = pygame.font.SysFont('comicsans',65)
## end

## load images
images = []
for i in range(7):
	image = pygame.image.load("images/hangman{}.png".format(i))
	images.append(image)
## end

## game variables
game_status = True
hangman_status = 0
words = ["HELLO","CODING","PYTHON","GAMES","DEVELOPER"]
word = random.choice(words)
guessed = []

## end

## colors
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,12)
RED = (255,0,0)
## end 

## choice variables
yes_text = LETTER_FONT.render("YES", 1, GREEN)
no_text = LETTER_FONT.render("NO", 1, RED)
## end

def draw():
	win.fill(WHITE) 

	# draw title 
	text = TITLE_FONT.render("DEVELOPER HANGMAN", 1, BLACK)
	win.blit(text, (WIDTH/2 - text.get_width()/2, 20))
	# draw word
	display_word = ""
	for letter in word:
		if letter in guessed:
			display_word += letter +" "
		else:
			display_word += "_ "
	text = WORD_FONT.render(display_word, 1, BLACK)
	win.blit(text, (450,200))

	# draw button 
	for letter in letters:
		x, y, ltr, visible = letter
		if visible:
			pygame.draw.circle(win, BLACK, (x,y), RADIUS, 3)
			text = LETTER_FONT.render(ltr, 1, BLACK)
			win.blit(text, (x - text.get_width()/2, y - text.get_height()/2))

	win.blit(images[hangman_status],(100,100)) #draw image or some surface
	pygame.display.update()


def display_message(msg):
	pygame.time.delay(1000)
	win.fill(WHITE)

	msg_text = WORD_FONT.render(msg, 1, BLACK)
	start_text = HEIGHT/2 - msg_text.get_height()/2
	win.blit(msg_text, (WIDTH/2 - msg_text.get_width()/2, start_text))

	continue_text = LETTER_FONT.render("Do you want to Continue?", 1, BLACK)
	win.blit(continue_text, (WIDTH/2 - continue_text.get_width()/2, start_text + 50))

	
	choice_start_x = WIDTH/2 - (yes_text.get_width() +  no_text.get_width() + 50)/2
	choice_start_y = start_text + 100
	win.blit(yes_text, (choice_start_x, choice_start_y))
	win.blit(no_text, (choice_start_x + yes_text.get_width() + 25 , choice_start_y))

	pygame.display.update()


## setup game loop
FPS = 60 # Frames per Second
clock = pygame.time.Clock() # this clock object will make sure that our loop runs
run =True #This controls our while loop
##end

while run:
	clock.tick(FPS) # this necessary to make that our while loop runs at the speed mentioned

	# Every event triggered like mouse click, key pressed, etc will be stored in pygame.event.get() (make think of as a list) 
	for event in pygame.event.get():

		if event.type == pygame.QUIT:
			run = False

		if event.type == pygame.MOUSEBUTTONDOWN:
			m_x, m_y = pygame.mouse.get_pos()  # this will give the x,y position where mouse is clicked
			if game_status:
				for letter in letters:
					x, y, ltr, visible = letter
					if visible:
						dis = math.sqrt((x-m_x)**2 + (y-m_y)**2)
						if dis < RADIUS:
							letter[3] = False
							guessed.append(ltr)
							if ltr not in word:
								hangman_status+=1
			else:
				choice_start_x = WIDTH/2 - (yes_text.get_width() +  no_text.get_width() + 50)/2
				choice_start_y = (HEIGHT/2 - yes_text.get_height()/2 ) + 100
				if choice_start_y <= m_y <= choice_start_y + yes_text.get_height():
					if choice_start_x <= m_x <= choice_start_x + yes_text.get_width():
						game_status = True
						hangman_status = 0
						word = random.choice(words)
						guessed = []
						for letter in letters:
							letter[3] = True
						continue
					elif choice_start_x + yes_text.get_width() + 25 <= m_x <= choice_start_x + yes_text.get_width() + 25 + no_text.get_width():
						run = False
						break

	if game_status:	
		draw()

		won = True
		for letter in word:
			if letter not in guessed:
				won = False
				break

		if won:
			game_status = False
			display_message("You WON!")
			
		if hangman_status == 6:
			game_status = False
			display_message("You LOST!")

pygame.quit()
