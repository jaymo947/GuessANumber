import pygame
import random

pygame.init()

print('\n')
#fonts
LETTER_FONT = pygame.font.SysFont('comicsans', 40)
main_font = pygame.font.SysFont('comicsans', 65)
small_font = pygame.font.SysFont('comicsans', 30)
sub_font = pygame.font.SysFont('comicsans', 20)
title_font = pygame.font.SysFont('comicsans', 65)
large_font = pygame.font.SysFont('comicsans',150)

#SCREEN SETUP
SCREEN_WIDTH = 350
SCREEN_HEIGHT = 590
WIN = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
pygame.display.set_caption('GAN')

#colors
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (77,0,255)
GREY = (170,170,170)
BLACK = (0,0,0)
MINT = (1,255,205)
INS_COLOR = (252,246,80)
ORANGE = (255,100,0)
YELLOW = (233,164,3)
PINK = (255,127,200)

#defining the size and location of number grid
GRID_WIDTH = 300
GRID_HEIGHT = 350
GRID_TOP = SCREEN_HEIGHT-GRID_HEIGHT-20
GRID_LEFT = (SCREEN_WIDTH/2)-(GRID_WIDTH/2)
GUESS_BLOCK = (10,50)
ANSWER_BLOCK = (20,200)
INFO_BLOCK = (215,200)
difficulty = 0
FPS = 60
#creating a list to store the number of attempts made per game
attempts = []
if attempts:
    average_attempts = (sum(attempts))/len(attempts)

#___IMAGES___
off_images = []
for i in range(10):
    off_images.append(pygame.image.load(f'number{i}.png'))
    off_images[i] = pygame.transform.scale(off_images[i], ((off_images[i].get_width()//3), off_images[i].get_height()//3))

#submit buttons
submit_off = pygame.image.load('submit_button_off.png')
submit_off = pygame.transform.scale(submit_off, ((submit_off.get_width()//3),(submit_off.get_height()//3)))
guess_the_number = pygame.image.load('guess_the_number.png')
guess_the_number = pygame.transform.scale(guess_the_number,((guess_the_number.get_width()//2),guess_the_number.get_height()//2))
give_the_number = pygame.image.load('give_the_number.png')
give_the_number = pygame.transform.scale(give_the_number,((give_the_number.get_width()//2),give_the_number.get_height()//2))
GUESS_THE_NUMBER_POSITION = (((SCREEN_WIDTH//2)-(guess_the_number.get_width()//2)),225)
GIVE_THE_NUMBER_POSITION = (((SCREEN_WIDTH//2)-(guess_the_number.get_width()//2)),400)

# main menu rectangles for clicking on mode
guess_rectangle = give_the_number.get_rect(topleft = GUESS_THE_NUMBER_POSITION)
give_rectangle = give_the_number.get_rect(topleft = GIVE_THE_NUMBER_POSITION)
main_menu_list = []
main_menu_list.append([guess_rectangle,'guess'])
main_menu_list.append([give_rectangle,'give'])

#loading in too high, too low and correct buttons for com_guess()
too_low = pygame.image.load('too_low.png')
too_high = pygame.image.load('too_high.png')
correct = pygame.image.load('correct.png')
TOO_LOW_POSITION = (((SCREEN_WIDTH//2)-too_low.get_width()//2),270)
TOO_HIGH_POSITION = (((SCREEN_WIDTH//2)-too_high.get_width()//2),375)
CORRECT_POSITION = (((SCREEN_WIDTH//2)-correct.get_width()//2),480)
#making clickable rectangles for com_guess()
too_low_rect = too_low.get_rect(topleft = TOO_LOW_POSITION)
too_high_rect = too_high.get_rect(topleft = TOO_HIGH_POSITION)
correct_rect = correct.get_rect(topleft = CORRECT_POSITION)
com_guess_list = []
com_guess_list.append([too_low_rect,'low'])
com_guess_list.append([too_high_rect, 'high'])
com_guess_list.append([correct_rect,'correct'])

#main menu button in bottom left hand corner
main_menu_button = pygame.image.load('main_menu.png')
main_menu_button = pygame.transform.scale(main_menu_button,((main_menu_button.get_width()//3),(main_menu_button.get_height()//3)))
MAIN_MENU_BUTTON_POS = (5,SCREEN_HEIGHT-(main_menu_button.get_height()-5))

#calculating the positions of the buttons ons the grid and storing htem into a list
gap = 10 
positions = []
for i in range(1,4):
    x, y = (GRID_LEFT+gap), (GRID_TOP+10)
    gap += off_images[i].get_width() + 15
    positions.append((x,y)) #now holds upperleft for 1-3
gap = 10
for i in range(4,7):
    x,y = (GRID_LEFT+gap, GRID_TOP+off_images[i].get_height())
    gap += off_images[i].get_width() + 15
    positions.append((x,y))#now holds upperleft for 1-6
gap = 10
for i in range(7,10):
    x,y = (GRID_LEFT+gap),(GRID_TOP+(off_images[i].get_height()*2)-10)
    gap += off_images[i].get_width() + 15
    positions.append((x,y))#now holds upperleft for 1-9
gap = 10
x,y = (GRID_LEFT+gap), (GRID_TOP+(off_images[i].get_height()*3)-20)
positions.append((x,y)) # now holds position for 1-9 and 0
x, y = ((GRID_WIDTH//2)-(off_images[0].get_width()//2)+25, GRID_TOP+(off_images[i].get_height()*3)-20)
positions.append((x,y))# now holds position for 1-9, 0 and the submit button

#loading rects of the buttons into a list
box_list = []
value = 1
for i in range(len(off_images)):
    rectangle = off_images[i].get_rect(topleft=(positions[i]))
    value = value
    if value == 10:
        value = 0
    box_list.append([rectangle,value])
    value += 1
submit_rect = submit_off.get_rect(topleft=(positions[10]))

#since the grid will be drawn in several differnt windows, I seperated this out so I can call to it whenever
def draw_grid():
    #pygame.draw.rect(WIN, (236,235,199), pygame.Rect(27,230,300,360))
    for i in range(len(off_images)):
        WIN.blit(off_images[i],(positions[i]))
    WIN.blit(submit_off, positions[10])

# -- main function that will run the game --
def main_menu():
    clock = pygame.time.Clock()
    #local constants
    main_menu = True
    mode = ""
    while main_menu:
        clock.tick(FPS)
        # Drawing the screen
        WIN.fill(GREY)
        title1 = title_font.render('Welcome',1,(0,0,0))
        WIN.blit(title1,((SCREEN_WIDTH//2)-(title1.get_width()//2),20))
        title2 = title_font.render('to',1,(0,0,0))
        WIN.blit(title2,((SCREEN_WIDTH//2)-(title2.get_width()//2),60))
        title3 = title_font.render('G.A.N!',1,(0,0,0))
        mode_text = small_font.render('-- Click to select Game Mode --',1,(BLACK))
        WIN.blit(mode_text,((SCREEN_WIDTH//2)-(mode_text.get_width()//2),190))
        WIN.blit(title3,((SCREEN_WIDTH//2)-(title3.get_width()//2),100))
        WIN.blit(guess_the_number,(GUESS_THE_NUMBER_POSITION))
        WIN.blit(give_the_number,(GIVE_THE_NUMBER_POSITION))
        WIN.blit(main_menu_button,MAIN_MENU_BUTTON_POS)
        

        # checking for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                elif event.key == pygame.K_RETURN:
                    main_menu = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(main_menu_list)):
                    if main_menu_list[i][0].collidepoint(pygame.mouse.get_pos()):
                        mode = main_menu_list[i][1]

        if mode == 'guess':
            guess(guess_main_menu(difficulty))
        elif mode == 'give':
            com_guess_setup()

        pygame.display.update()

def guess_main_menu(difficulty):
    clock = pygame.time.Clock()
    #local constants
    guess_main_menu = True
    while guess_main_menu:
        clock.tick(FPS)
        WIN.fill(WHITE)
        #    -- TITLE --
        title1 = title_font.render('Guess',1,(0,0,0))
        WIN.blit(title1,((SCREEN_WIDTH//2)-(title1.get_width()//2),20))
        title2 = title_font.render('the',1,(0,0,0))
        WIN.blit(title2,((SCREEN_WIDTH//2)-(title2.get_width()//2),60))
        title3 = title_font.render('Number',1,(0,0,0))
        WIN.blit(title3,((SCREEN_WIDTH//2)-(title3.get_width()//2),100)) 
        title4 = small_font.render('Select Difficulty (enter 1-5)',1,(BLACK))
        WIN.blit(title4,((SCREEN_WIDTH//2)-(title4.get_width()//2),200))
        #Drawing difficulties onto the screen
        diff1 = small_font.render('1. Easy (GAN - 10)',1,(BLUE))
        WIN.blit(diff1,((SCREEN_WIDTH//2)-(title4.get_width()//2)+20,240))
        diff2 = small_font.render('2. Medium (GAN - 50)',1,(YELLOW))
        WIN.blit(diff2,((SCREEN_WIDTH//2)-(title4.get_width()//2)+20,270))
        diff3 = small_font.render('3. Hard (GAN - 200)',1,(ORANGE))
        WIN.blit(diff3,((SCREEN_WIDTH//2)-(title4.get_width()//2)+20,300))
        diff4 = small_font.render('4. Extreme (GAN - 500)',1,(RED))
        WIN.blit(diff4,((SCREEN_WIDTH//2)-(title4.get_width()//2)+20,330))
        diff5 = small_font.render('5. RANDOM',1,(PINK))
        WIN.blit(diff5,((SCREEN_WIDTH//2)-(title4.get_width()//2)+20,360))
        #checking for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                elif event.key == pygame.K_1  or event.key == pygame.K_KP_1:
                    difficulty = 10
                    print(f'Difficulty - Easy (1-{difficulty})')
                    return difficulty
                elif event.key == pygame.K_2 or event.key == pygame.K_KP_2:
                    difficulty = 50
                    print(f'Difficulty - Medium (1-{difficulty})')
                    return difficulty
                elif event.key == pygame.K_3 or event.key == pygame.K_KP_3:
                    difficulty = 200
                    print(f'Difficulty - Hard (1-{difficulty})')
                    return difficulty
                elif event.key == pygame.K_4 or event.key == pygame.K_KP_4:
                    difficulty = 500
                    print(f'Difficulty - Extreme (1-{difficulty})')
                    return difficulty
                elif event.key == pygame.K_5 or event.key == pygame.K_KP_5:
                    difficulty = 0
                    print(f'Difficulty - Random')
                    return difficulty
                
        pygame.display.update()

def you_win(num):
    clock = pygame.time.Clock()
    #local constants
    win_screen = True
    while win_screen:
        clock.tick(FPS)
        # drawing the screen
        WIN.fill(MINT)
        small_font = pygame.font.SysFont('comicsans', 30)
        correct_guess_text = main_font.render('You win!',1,(0,0,0))
        WIN.blit(correct_guess_text,(75,100))
        win_text = small_font.render('Hit ENTER to play again',1,(0,0,0))
        WIN.blit(win_text, (50,200))
        if num == 1:
            guesses = small_font.render(f'Wow! It took you {num} guess...',1,(RED))
            WIN.blit(guesses, (45,150))
        else:
            guesses = small_font.render(f'It took you {num} guesses',1,(RED))
            WIN.blit(guesses, (65,150))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    win_screen = False
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                main_menu()
        pygame.display.update()

def guess(difficulty):
    clock = pygame.time.Clock()
    #local constants
    ans = ""
    running = True
    FPS = 60
    main_font = pygame.font.SysFont('comicsans', 65)
    small_font = pygame.font.SysFont('comicsans', 30)
    submissions = []
    if difficulty == 0:
        difficulty = random.randint(100,1000)
    secret_number = random.randint(1,difficulty)
    clock = pygame.time.Clock()
    num_of_answers = 0
    while running:
        clock.tick(FPS)
        #drawing the screen
        WIN.fill(WHITE)
        draw_grid()
        instructions = small_font.render(f'Guess a number between 1 and {difficulty}',1,BLUE)
        WIN.blit(instructions,((SCREEN_WIDTH//2)-(instructions.get_width()//2),5))
        instructions2 = sub_font.render(f'Click or use keys to enter guess, BACKSPACE to clear',1,BLACK)
        WIN.blit(instructions2,((SCREEN_WIDTH//2)-(instructions2.get_width()//2),25))
        #checking for user events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_1 or event.key == pygame.K_KP_1:
                    print(f'button pressed - 1')
                    ans += '1'
                elif event.key == pygame.K_2 or event.key == pygame.K_KP_2:
                    print(f'button pressed - 2')
                    ans += '2'
                elif event.key == pygame.K_3 or event.key == pygame.K_KP_3:
                    print(f'button pressed - 3')
                    ans += '3'
                elif event.key == pygame.K_4 or event.key == pygame.K_KP_4:
                    print(f'button pressed - 4')
                    ans += '4'
                elif event.key == pygame.K_5 or event.key == pygame.K_KP_5:
                    print(f'button pressed - 5')
                    ans += '5'
                elif event.key == pygame.K_6 or event.key == pygame.K_KP_6:
                    print(f'button pressed - 6')
                    ans += '6'
                elif event.key == pygame.K_7 or event.key == pygame.K_KP_7:
                    print(f'button pressed - 7')
                    ans += '7'
                elif event.key == pygame.K_8 or event.key == pygame.K_KP_8:
                    print(f'button pressed - 8')
                    ans += '8'
                elif event.key == pygame.K_9 or event.key == pygame.K_KP_9:
                    print(f'button pressed - 9')
                    ans += '9'
                elif event.key == pygame.K_0 or event.key == pygame.K_KP_0:
                    print(f'button pressed - 0')
                    ans += '0'
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if ans != '0' and ans != "":
                        print(f'submission detected --> {ans}')
                        submissions.append(int(ans))
                        sub = small_font.render(ans,1,(255,0,0))
                        ans = ""
                        num_of_answers += 1
                elif event.key == pygame.K_BACKSPACE:
                    if ans != "":
                        ans = ans[:-1]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(box_list)):
                    if box_list[i][0].collidepoint(pygame.mouse.get_pos()):
                        print(f'button pressed - {box_list[i][1]}')
                        ans += str(box_list[i][1])
                if submit_rect.collidepoint(pygame.mouse.get_pos()) and ans != "" and ans != '0':
                    print(f'submission detected --> {ans}')
                    submissions.append(int(ans))
                    sub = small_font.render(ans,1,(255,0,0))
                    ans = ""
                    num_of_answers += 1
        
        #drawing dynamic screen in response to guess input
        guess = main_font.render(f'Guess: {str(ans)}',1,(0,0,0)) #creates an object that will render the text of the guess in black
        WIN.blit(guess,GUESS_BLOCK)
        wrong_guess_text = small_font.render('Previous guess: ',1,(0,0,0))
        low_guess_text = small_font.render('-->Too low',1,(0,0,0))
        high_guess_text = small_font.render('-->Too high',1,(0,0,0))
        if submissions:
            submission = submissions[-1]
            if submission == secret_number:
                submissions = []
                attempts.append(num_of_answers)
                you_win(num_of_answers)
                num_of_answers = 0
                main_menu()
            elif submission > difficulty:
                out_of_range_text = small_font.render(f'<Error_Type: Out of Range.>',1,(RED))
                out_of_range_text2 = small_font.render(f'Guess count incremented',1,(BLACK))
                WIN.blit(out_of_range_text,(35,170))
                WIN.blit(out_of_range_text2,(50,200))                    
            elif submission < secret_number:
                WIN.blit(wrong_guess_text,ANSWER_BLOCK)
                WIN.blit(low_guess_text,INFO_BLOCK)
                WIN.blit(sub, (178,201))
            elif submission > secret_number:
                WIN.blit(wrong_guess_text,ANSWER_BLOCK)
                WIN.blit(high_guess_text,INFO_BLOCK)
                WIN.blit(sub, (178,201))
            
        pygame.display.update()

    pygame.quit()

def com_guess_setup():
    clock = pygame.time.Clock()
    #local constants
    com_guess_setup = True
    ans = ""
    secret_number = None
    while com_guess_setup:
        clock.tick(FPS)
        # drawing the screen
        WIN.fill(WHITE)
        instructions_text = small_font.render('Enter a # between 1-500',1,BLACK)
        WIN.blit(instructions_text, (((SCREEN_WIDTH//2)-(instructions_text.get_width()//2)),5))
        instructions2 = sub_font.render(f'Click or use keys to enter, BACKSPACE to clear',1,BLACK)
        WIN.blit(instructions2,((SCREEN_WIDTH//2)-(instructions2.get_width()//2),25))
        pygame.draw.rect(WIN,(BLACK),pygame.Rect(50,50,245,170),4)
        draw_grid()
        # checking for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                elif event.key == pygame.K_1 or event.key == pygame.K_KP_1:
                    print(f'button pressed - 1')
                    ans += '1'
                elif event.key == pygame.K_2 or event.key == pygame.K_KP_2:
                    print(f'button pressed - 2')
                    ans += '2'
                elif event.key == pygame.K_3 or event.key == pygame.K_KP_3:
                    print(f'button pressed - 3')
                    ans += '3'
                elif event.key == pygame.K_4 or event.key == pygame.K_KP_4:
                    print(f'button pressed - 4')
                    ans += '4'
                elif event.key == pygame.K_5 or event.key == pygame.K_KP_5:
                    print(f'button pressed - 5')
                    ans += '5'
                elif event.key == pygame.K_6 or event.key == pygame.K_KP_6:
                    print(f'button pressed - 6')
                    ans += '6'
                elif event.key == pygame.K_7 or event.key == pygame.K_KP_7:
                    print(f'button pressed - 7')
                    ans += '7'
                elif event.key == pygame.K_8 or event.key == pygame.K_KP_8:
                    print(f'button pressed - 8')
                    ans += '8'
                elif event.key == pygame.K_9 or event.key == pygame.K_KP_9:
                    print(f'button pressed - 9')
                    ans += '9'
                elif event.key == pygame.K_0 or event.key == pygame.K_KP_0:
                    print(f'button pressed - 0')
                    ans += '0'
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    if ans != '':
                        if int(ans) <= 500 and ans[0] != '0':
                            print(f'submission detected --> {ans}')
                            secret_number = int(ans)
                            ans = ""
                            com_guess(secret_number)
                elif event.key == pygame.K_BACKSPACE and ans != "":
                    ans = ans[:-1]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(box_list)):
                    if box_list[i][0].collidepoint(pygame.mouse.get_pos()):
                        print(f'button pressed - {box_list[i][1]}')
                        ans += str(box_list[i][1])
                    if submit_rect.collidepoint(pygame.mouse.get_pos()) and ans != "" and ans[0] != '0' and int(ans) <= 500:
                        print(f'submission detected --> {ans}')
                        secret_number = int(ans)
                        ans = ""
                        com_guess(secret_number)
        if ans:
            if ans[0] =='0':
                ans = ''
        #dynamic screen drawing to display the secret number...
        number = large_font.render(ans,1,BLUE)
        WIN.blit(number, (((SCREEN_WIDTH//2)-number.get_width()//2),90))

        pygame.display.update()

def com_guess(secret_number):
    clock = pygame.time.Clock()
    adjustment = ''
    #local constants
    com_guess_main = True
    num_of_answers = 1
    lowest = 1
    highest = 500
    com_guess = random.randint(lowest,highest)
    while com_guess_main:
        clock.tick(FPS)
        #drawing the screen 
        WIN.fill(GREY)
        pygame.draw.rect(WIN,(BLACK),pygame.Rect(50,50,245,170),4)
        instructions_text = LETTER_FONT.render("My guess is:",1,BLACK)
        WIN.blit(instructions_text, (((SCREEN_WIDTH//2)-(instructions_text.get_width()//2)),15))
        instructions2 = small_font.render(f'Click an answer',1,BLACK)
        WIN.blit(instructions2,((SCREEN_WIDTH//2)-(instructions2.get_width()//2),250))
        WIN.blit(too_low,TOO_LOW_POSITION)
        WIN.blit(too_high,TOO_HIGH_POSITION)
        WIN.blit(correct,CORRECT_POSITION)
        # Instructions on screen
        com_guess_text = large_font.render(str(com_guess),1,RED)
        WIN.blit(com_guess_text, (((SCREEN_WIDTH//2)-com_guess_text.get_width()//2),90))
        #checking for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    adjustment = 'correct'
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i in range(len(com_guess_list)):
                    if com_guess_list[i][0].collidepoint(pygame.mouse.get_pos()):
                        adjustment = com_guess_list[i][1]
        if adjustment != '':
            if adjustment == 'high':
                if com_guess == secret_number:
                    num_of_answers += 1
                    cheater(secret_number)
                elif com_guess > secret_number:
                    highest = com_guess-1
                    com_guess = random.randint(lowest,(highest))
                    adjustment = ''
                    num_of_answers += 1
            elif adjustment == 'low':
                if com_guess == secret_number:
                    cheater(secret_number)
                elif com_guess < secret_number:
                    lowest = com_guess+1
                    com_guess = random.randint((lowest),highest)
                    adjustment = ''
                    num_of_answers += 1
            elif adjustment == 'correct':
                if com_guess == secret_number:
                    comp_wins(num_of_answers)
                else:
                    are_you_sure = small_font.render('I don\'t think I got it...',1,BLACK)
                    WIN.blit(are_you_sure,(((SCREEN_WIDTH//2)-are_you_sure.get_width()//2),200))

        pygame.display.update()

def cheater(secret_number):
    clock = pygame.time.Clock()
    cheater = True
    while cheater:
        clock.tick(FPS)
        WIN.fill(RED)
        angry_text1 = large_font.render('NO!',1,BLACK)
        WIN.blit(angry_text1,(((SCREEN_WIDTH//2)-angry_text1.get_width()//2),50))
        angry_text2 = large_font.render('I WON',1,BLACK)
        WIN.blit(angry_text2,(((SCREEN_WIDTH//2)-angry_text2.get_width()//2),145))
        number_text = small_font.render(f'The secret number was {secret_number}',1,BLACK)
        WIN.blit(number_text,(((SCREEN_WIDTH//2)-number_text.get_width()//2),250))
        angry_text = small_font.render('Press Enter...',1,BLACK)
        WIN.blit(angry_text,(((SCREEN_WIDTH//2)-angry_text.get_width()//2),(SCREEN_HEIGHT)-40))
        # checking for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    main_menu()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                main_menu()

        pygame.display.update()

def comp_wins(num_of_guesses):
    clock = pygame.time.Clock()
    winner = True
    while winner:
        clock.tick(FPS)
        WIN.fill(MINT)
        angry_text1 = large_font.render('YES!',1,BLACK)
        WIN.blit(angry_text1,(((SCREEN_WIDTH//2)-angry_text1.get_width()//2),50))
        angry_text2 = LETTER_FONT.render(f'I got it in',1,BLACK)
        WIN.blit(angry_text2,(((SCREEN_WIDTH//2)-angry_text2.get_width()//2),150))
        angry_text3 = LETTER_FONT.render(f'{num_of_guesses} guesses!',1,BLACK)
        WIN.blit(angry_text3,(((SCREEN_WIDTH//2)-angry_text3.get_width()//2),175))
        angry_text = small_font.render('Press Enter to play again.',1,BLACK)
        WIN.blit(angry_text,(((SCREEN_WIDTH//2)-angry_text.get_width()//2),(SCREEN_HEIGHT-40)))
        # checking for events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                    main_menu()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                main_menu()

        pygame.display.update()


main_menu()


