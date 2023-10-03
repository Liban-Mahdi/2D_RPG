import pygame

pygame.init()

clock = pygame.time.Clock()
fps = 60

# Game Window
bottom_panel = 150
screen_width = 800
screen_height = 400 + bottom_panel

screen = pygame.display.set_mode((screen_width, screen_height))  # Fix here
pygame.display.set_caption("Battle")  # Fix typo here

#Define fonts
font = pygame.font.SysFont('Reactor7', 26)

#Define colors
red = (255, 0, 0)
green = ( 0, 255, 0)

# Load background
background_img = pygame.image.load("assets/background/background.jpg").convert_alpha()

# Load panel image
DefaultIMGSize = (800,150)
RawPanelImg = pygame.image.load("assets/panel/panel.png").convert_alpha()
panel_img = pygame.transform.scale(RawPanelImg,DefaultIMGSize)

#Creat function for Drawing text
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img,(x,y))


# Define functions to draw background and panel
def draw_bg():
    screen.blit(background_img, (0, 0))

def draw_panel():
    #Draw panel rectangle
    screen.blit(panel_img, (0, screen_height - bottom_panel))
    #Show Priestess Stats
    draw_text(f'{WaterPriestess.name} HP: {WaterPriestess.hp}', font, red,60,  450 )
    for count, i in enumerate(WindHashashin_list):
        #Show name and health
        draw_text(f'{i.name} HP: {i.hp}', font, red, 450, 420 + count*60)


#Fighter class
class Fighter():
    def __init__(self, x, y, name, max_hp, strength, potion):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.start_potion = potion
        self.potion = potion
        self.alive = True
        self.animation_list = []
        self.frame_index = 0
        self.action = 0 #0: idle, 1:attack, 2: hurt, 3: dead
        self.update_time = pygame.time.get_ticks()

        temp_list = [] #load idle animations
        for i in range(8):
            image = pygame.image.load(f"assets/{self.name}/png/idle/idle_{i}.png")
            image = pygame.transform.scale(image,(image.get_width()*4, image.get_height()*4))
            temp_list.append(image)
        self.animation_list.append(temp_list)

        temp_list = [] #load attack animations
        for i in range(8):
            image = pygame.image.load(f"assets/{self.name}/png/attack/1_atk_{i}.png")
            image = pygame.transform.scale(image, (image.get_width() * 4, image.get_height() * 4))
            temp_list.append(image)
        self.animation_list.append(temp_list)

        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        #handle and update animation
        animation_cooldown = 100
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.update_time = pygame.time.get_ticks()
            self.frame_index +=1
        #loop after 8th frame
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
    def draw(self):
        screen.blit(self.image, self.rect)



class HealthBar():
    def __init__(self,x,y,hp,max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self,hp):
        #update with new health
        self.hp = hp
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150*ratio, 20))



WaterPriestess = Fighter(150,130,"WaterPriestess", 30, 10, 3)
WindHashashin1 = Fighter(500,140,"WindHashashin", 20, 6, 1)
WindHashashin2 = Fighter(700,140,"WindHashashin", 20, 6, 1)

WindHashashin_list = []
WindHashashin_list.append(WindHashashin1)
WindHashashin_list.append(WindHashashin2)

WaterPriestess_health_Bar = HealthBar(60,470, WaterPriestess.hp, WaterPriestess.max_hp)
WindHashashin1_health_Bar = HealthBar(450,440, WindHashashin1.hp, WindHashashin1.max_hp)
WindHashashin2_health_Bar = HealthBar(450,500, WindHashashin2.hp, WindHashashin2.max_hp)



run = True
while run:

    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    #draw screen and bottom panel
    draw_bg()
    draw_panel()
    WaterPriestess_health_Bar.draw(WaterPriestess.hp)
    WindHashashin1_health_Bar.draw(WindHashashin1.hp)
    WindHashashin2_health_Bar.draw(WindHashashin2.hp)

    #Draw Fighter
    WaterPriestess.update()
    WaterPriestess.draw()

    #Draw Enemy
    for WindHashashin in WindHashashin_list:
        WindHashashin.update()
        WindHashashin.draw()

    pygame.display.update()

pygame.quit()