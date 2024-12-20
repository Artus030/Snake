import pygame, sys
from time import time
from random import randint
pygame.init()
pygame.font.init()

clock = pygame.time.Clock()
FPS: int = 40

window_width: int = 1200
window_height: int = 600

def game_loop() -> None:
    generate_window(window_width, window_height)
    game_over_flag: bool = False
    timer: float = time()
    score: int = 0
    while not game_over_flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or is_key_pressed(pygame.K_ESCAPE):
                sys.exit()
        full_snake[0].set_direction()
        if time() - timer > 0.1:
            timer = time()
            move()
            match check_collision():
                case "game_over":
                    game_over_flag = True
                case "apple":
                    score += 1
                    repos_apple()
                case _:
                    pass
            update_graphics()
        clock.tick(FPS)
    game_over(score)


# collisions
def repos_apple() -> None:
    every_apple[0] = Apple(20, randint(0, window_width//20-20)*20, randint(0, window_height//20-20)*20)
    for i in range(len(full_snake)):
        hitbox_body = pygame.Rect(full_snake[i].x,full_snake[i].y,full_snake[i].size,full_snake[i].size)
        hitbox_apple = pygame.Rect(every_apple[0].x, every_apple[0].y, every_apple[0].size, every_apple[0].size)
        if hitbox_body == hitbox_apple:
            repos_apple()

def check_collision() -> str:
    hitbox_head = pygame.Rect(full_snake[0].x,full_snake[0].y,full_snake[0].size,full_snake[0].size)
    if hit_wall():
        return "game_over"
    for i in range(1, len(full_snake)):
        hitbox_body = pygame.Rect(full_snake[i].x,full_snake[i].y,full_snake[i].size,full_snake[i].size)
        if hitbox_head.colliderect(hitbox_body):
            return "game_over"
    for elements in every_apple:    
        hitbox_apple = pygame.Rect(elements.x,elements.y,elements.size,elements.size)
        if hitbox_apple.colliderect(hitbox_head):
            add_bodypart()
            return "apple"
    return ""
            
def hit_wall() -> bool:
    if window_width < full_snake[0].x or full_snake[0].x < 0 or window_height < full_snake[0].y or full_snake[0].y < 0:
        return True


# game over
def game_over(score: int) -> None:
    screen.fill((0,0,0))
    my_font = pygame.font.SysFont("Comic Sans MS", 30)
    text_surface = my_font.render(f"You ate {score} apples. Press Enter to quit.", False, (255,255,255))
    screen.blit(text_surface, (0,0))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or is_key_pressed(pygame.K_RETURN):
                sys.exit()


# body
def move() -> None:
    for i in range(len(full_snake)):
        full_snake[i].old_x = full_snake[i].x
        full_snake[i].old_y = full_snake[i].y
        full_snake[i].x += full_snake[i].moves[0][0] * full_snake[i].speed
        full_snake[i].y += full_snake[i].moves[0][1] * full_snake[i].speed
        full_snake[i].last_direction = full_snake[i].moves[0]
        full_snake[i].moves[0] = full_snake[i-1].last_direction

def add_bodypart() -> None:
    new_bodypart = Snake(full_snake[0].size, full_snake[len(full_snake)-1].old_x, full_snake[len(full_snake)-1].old_y, full_snake[len(full_snake)-1].last_direction, full_snake[0].speed)
    full_snake.append(new_bodypart)


# Key management 
def is_key_pressed(key_in_question: int) -> bool:
    keys_pressed = pygame.key.get_pressed()
    return keys_pressed[key_in_question]
    

# Graphics
def generate_window(width: int, height: int) -> None:
    global screen
    screen = pygame.display.set_mode([width,height])
    pygame.display.set_caption("Snake")
    pygame.display.update()

def update_graphics() -> None:
    paint_window()
    paint_snake()
    paint_apple()
    pygame.display.update()

def paint_window() -> None:
    background = pygame.image.load("Grafiken/hintergrund.png")
    screen.blit(background, (0,0))

def paint_snake() -> None:
    for element in full_snake:
        pygame.draw.rect(screen,(0,0,0),(element.x, element.y, element.size, element.size))

def paint_apple() -> None:
    for element in every_apple:
        pygame.draw.rect(screen, (255,0,0), (element.x, element.y, element.size, element.size))


# classes
class Snake():
    def __init__(self, size: int, x: int, y: int, direction: list[int], speed):
        self.size = size
        self.x = x
        self.y = y
        self.old_x = x
        self.old_y = y
        self.speed = speed
        self.direction = direction
        self.last_direction = direction
        self.moves: list = [direction]

    def set_direction(self) -> None:
        if is_key_pressed(pygame.K_w) or is_key_pressed(pygame.K_UP):
            if not self.last_direction == [0,1]:
                self.direction = [0,-1]
        if is_key_pressed(pygame.K_a) or is_key_pressed(pygame.K_LEFT):
            if not self.last_direction == [1,0]:
                self.direction = [-1,0]
        if is_key_pressed(pygame.K_s) or is_key_pressed(pygame.K_DOWN):
            if not self.last_direction == [0,-1]:
                self.direction = [0,1]
        if is_key_pressed(pygame.K_d) or is_key_pressed(pygame.K_RIGHT):
            if not self.last_direction == [-1,0]:
                self.direction = [1,0]
        full_snake[0].moves[0] = full_snake[0].direction

class Apple():
    def __init__(self, size: int, x: int, y: int):
        self.size = size
        self.x = x
        self.y = y


# start
full_snake: list[Snake] = [Snake(20, 100, 100, [1,0], 20)]
every_apple: list[Apple] = [Apple(20, 120, 100)]
game_loop()