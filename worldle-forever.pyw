import pygame, os, csv, random
from unidecode import unidecode

##########
# Appearances
##########

window_width = 1400
window_height = 900

lavender = '#f8edee'
thistle = '#d5c6e0'
quartz ='#aaa1c8'
mountbatten = '#967aa1'
space = '#192a51'

##########
# Classes
##########

class Text_button:
    def __init__(self, text, pos, center=False, small=False, options=False):
        # split lines if too long
        words = text.split(" ")
        self.lines = [" ".join(words[:4]), " ".join(words[4:])] if len(words) >= 4 else [text]
        self.text = text
        self.pos = pos
        self.center=center
        self.small=small
        self.options=options
        self.hovered = False

    def draw(self, screen):
        pygame.draw.rect(screen,lavender,pygame.Rect(self.pos,(700,80)),border_radius = 3)
        if self.options:
            color = mountbatten if self.hovered else quartz
        else:
            color = mountbatten if self.hovered else space
        surf = [button_font_small.render(line,True,color) if self.small else button_font.render(line,True,color) for line in self.lines]
        rect = [surf[i].get_rect(center = tuple(map(lambda i, j: i + j, self.pos, (0, i*35)))) if self.center else surf[i].get_rect(topleft = tuple(map(lambda i, j: i + j, self.pos, (0, i*35)))) for i in range(len(surf))]
        for i in range(len(surf)):
            screen.blit(surf[i], rect[i])

########
# Functions
########

# wipe screen
def wipe():
    pygame.draw.rect(screen, lavender, pygame.Rect(0, 0, window_width, window_height))
    pygame.display.flip()

# start game
def start(countries):
    global started, reached_end, attempts, correct, wrong
    started = True
    reached_end = False
    attempts = 5
    correct = False
    wrong = False
    wipe()
    init_trial(countries)

# initiate a trial
def init_trial(countries):
    global pic, answer, buttons
    buttons = []
    # get a correct answer
    answer = random.choice(list(countries.keys()))
    pic = 'assets/pics/'+answer+'.png'
    # try again if picture doesn't exist
    if not os.path.isfile(pic):
        init_trial(countries)
    # print(countries[answer])

# match player input with the first four countries starting with that name
def get_choices(prefix, dictionary):
    # Normalize the prefix and items to ASCII
    normalized_prefix = unidecode(prefix).lower()
    
    # Find all items that start with the normalized prefix and return the first four values in the dictionary
    matching_items = [item for item in dictionary.keys() if unidecode(item).lower().startswith(normalized_prefix)]
    values = [dictionary[key] for key in matching_items]
    
    return values[:4]

# enter country
def select(selected_button):
    global attempts, correct, wrong, reached_end, response, input, options
    if len(options) > 0:
        attempts -= 1
        wipe_selection()
        response = options[selected_button]
        if response == answer:
            reached_end = True
            correct = True
        elif attempts <= 0:
            reached_end = True
        else:
            wrong = True
    options = []
    input = ''
    wipe()

def wipe_selection():
    global buttons, selected_button
    buttons = []
    selected_button = 0

##########
# Main function
##########

def main():
    global screen, button_font, button_font_small, text_font_small
    global started, reached_end, correct, wrong, buttons, pic, response, selected_button, input, options

    ##########
    # Initialise
    ##########
    # Set working directory to the location of this .py file
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height))
    clock = pygame.time.Clock()
    icon = pygame.image.load('assets/icon.png')
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Worldle Forever')
    screen.fill(lavender)

    ##########
    # Game assets
    ##########
    # text fonts
    text_font_smaller = pygame.font.Font('assets/joystix-monospace.otf',15)
    text_font_small = pygame.font.Font('assets/joystix-monospace.otf',20)
    text_font = pygame.font.Font('assets/joystix-monospace.otf',30)
    title_font = pygame.font.Font('assets/joystix-monospace.otf',50)
    button_font = pygame.font.Font('assets/joystix-monospace.otf',28)
    button_font_small = pygame.font.Font('assets/joystix-monospace.otf',22)

    ##########
    # Game resources
    ##########
    # get country code
    with open('assets/codes.csv', 'r', encoding='utf-8') as codes_input:
        cr = csv.reader(codes_input)
        countries = {}
        types = {}
        for line in cr:
            countries[line[1]] = line[0].replace('\ufeff', '')
            types[line[0].replace('\ufeff', '').replace("The ", "")] = line[1]
    
    # get scale
    with open('assets/countries_scales.csv', 'r') as scale_input:
        cr = csv.reader(scale_input)
        scales = {}
        first = True
        for line in cr:
            if first:
                first = False
            else:
                scales[line[0]] = [line[5], int(float(line[6]))]
    
    # get distance dictionary
    with open('assets/distances.csv', 'r') as dis_input:
        cr = csv.reader(dis_input)
        distances = {}
        first = True
        for line in cr:
            if first:
                kkeys = line[1:]
                first = False
            else:
                distances[line[0]] = {k:int(float(line[kkeys.index(k)+1])) for k in kkeys}

    # I dont think there's a missing country in the distances dictionary, but let's do this just in case. Remove country form country list if there's no distance or scale info for it
    for item in countries.keys():
        if item not in distances:
            countries.remove(item)
        elif item not in scales:
            countries.remove(item)

    ##########
    # Parameter defaults
    ##########
    started = False
    reached_end = False
    correct = False
    wrong = False
    running = True
    options = []
    input=''
    response = ''
    selected_button = 0
    buttons = [Text_button("start", (700, 550), center=True), Text_button("quit", (700, 650), center=True)]
    buttons[selected_button].hovered = True  # First button is hovered by default
    pic = 'assets/pics/AD.png'

    ##########
    # Main loop
    ##########
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # if esc key pressed, quit the game
                if event.key == pygame.K_ESCAPE:
                    running = False
                # up and down keys to iterate between buttons
                elif event.key == pygame.K_DOWN:
                    buttons[selected_button].hovered = False
                    selected_button = (selected_button + 1) % len(buttons)
                    buttons[selected_button].hovered = True
                elif event.key == pygame.K_UP:
                    buttons[selected_button].hovered = False
                    selected_button = (selected_button - 1) % len(buttons)
                    buttons[selected_button].hovered = True
                # return key to start the game if outside game, or select options if in game
                elif event.key == pygame.K_RETURN:
                    if reached_end or not started:
                        if selected_button == 0:
                            start(countries)
                        else:
                            running = False
                    else:
                        select(selected_button)
                # handle player input
                elif event.key == pygame.K_BACKSPACE:
                    if started and not reached_end:
                        input = input[:-1]
                        wipe()
                        options = get_choices(input, types)
                        buttons = []
                        for i in range(len(options)):
                            buttons.append(Text_button(countries[options[i]], (750, 330+i*80), small = True, options=True))
                        selected_button = 0
                        if len(buttons)>0: 
                            buttons[selected_button].hovered = True # First button is hovered by default 
                        wipe()
                else:
                    if started and not reached_end:
                        input += event.unicode
                        wipe()
                        options = get_choices(input, types)
                        buttons = []
                        for i in range(len(options)):
                            buttons.append(Text_button(countries[options[i]], (750, 330+i*80), small = True, options=True))
                        selected_button = 0
                        if len(buttons)>0:
                            buttons[selected_button].hovered = True # First button is hovered by default
                        wipe()
        
        # draw elements
        if not started:
            message1 = title_font.render('Worldle Forever', True, space)
            message2 = text_font_small.render("Guess the country/territory based on the silhouette!", True, space)
            message3 = text_font_small.render("maps by Mazarin @djaiss", True, mountbatten)
            message4 = text_font_smaller.render("The maps were not created by me, and any inaccuracies are the responsibility of the original creator.", True, mountbatten)
            message5 = text_font_small.render("Scales are approximates.", True, mountbatten)
            screen.blit(message1, message1.get_rect(center = (700, 280)))
            screen.blit(message2, message2.get_rect(center = (700, 380)))
            screen.blit(message3, message3.get_rect(topleft = (100, 845)))
            screen.blit(message4, message4.get_rect(topleft = (100, 865)))
            screen.blit(message5, message5.get_rect(topleft = (100,800)))
        elif reached_end:
            picture = pygame.image.load(pic)
            screen.blit(picture, (95,160))
            if correct: 
                message1 = text_font.render('Correct!', True, space)
            else:
                message1 = text_font.render('No more attempts...', True, space)
            message2 = text_font_small.render('This is: ', True, space)
            message3 = text_font_small.render(countries[answer], True, space)
            message4 = text_font_small.render('Press Enter to get a new one.', True, space)
            screen.blit(message1, message1.get_rect(center = (1000, 250)))
            screen.blit(message2, message2.get_rect(topleft = (710, 400)))
            screen.blit(message3, message3.get_rect(center = (1000, 450)))
            screen.blit(message4, message4.get_rect(center = (1000, 650)))
        else:
            picture = pygame.image.load(pic)
            screen.blit(picture, (95,160))
            message1 = text_font_small.render('Attempts left:'+str(attempts), True, space)
            screen.blit(message1, message1.get_rect(topleft = (1000, 65)))
            message2 = text_font_small.render('type your answer: ', True, space)
            screen.blit(message2, message2.get_rect(topleft = (710, 200)))
            message3 = text_font_small.render(input, True, space)
            screen.blit(message3, message3.get_rect(topleft = (710, 260)))
            # draw scale
            if scales[answer][0] == 'lat':
                pygame.draw.rect(screen, space, pygame.Rect(65, 160, 10, 2))
                pygame.draw.rect(screen, space, pygame.Rect(65, 160, 2, 102.4))
                pygame.draw.rect(screen, space, pygame.Rect(65, 262.4, 10, 2))
                scale = text_font_smaller.render(str(scales[answer][1]/5)+' km', True, space)
                screen.blit(scale, scale.get_rect(topleft = (65, 142)))
            else:
                pygame.draw.rect(screen, space, pygame.Rect(94, 130, 2, 10))
                pygame.draw.rect(screen, space, pygame.Rect(94, 130, 102.4, 2))
                pygame.draw.rect(screen, space, pygame.Rect(196.4, 130, 2, 10))
                scale = text_font_smaller.render(str(scales[answer][1]/5)+' km', True, space)
                screen.blit(scale, scale.get_rect(topleft = (94, 112)))
            if wrong:
                message4 = text_font_small.render('Not there yet...', True, space)
                screen.blit(message4, message4.get_rect(topleft = (100, 730)))
                message5 = text_font_small.render('You guessed: '+countries[response], True, space)
                screen.blit(message5, message5.get_rect(topleft = (100, 780)))
                message4 = text_font_small.render('Distance from answer: '+str(distances[response][answer])+' km', True, space)
                screen.blit(message4, message4.get_rect(topleft = (820, 730)))

        for i, button in enumerate(buttons):
            if not any(pygame.key.get_pressed()):
                if button.hovered:
                    selected_button = i
            button.draw(screen)

        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()