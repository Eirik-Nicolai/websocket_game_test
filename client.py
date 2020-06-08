import pygame
import network_helper

game_width  = 500
game_height = 500

print("starting up...")

window = pygame.display.set_mode((game_width, game_height))
pygame.display.set_caption("Client")

print("pygame initiated")

class Player():
    def __init__(self, posx, posy, width, height, colour):
        self.x = posx
        self.y = posy
        self.width = width
        self.height = height
        self.colour = colour

        self.rect = (self.x, self.y, self.width, self.height)
        self.vel = 1

    def draw(self, window):
        pygame.draw.rect(window, self.colour, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.vel

        if keys[pygame.K_RIGHT]:
            self.x += self.vel

        if keys[pygame.K_UP]:
            self.y += self.vel

        if keys[pygame.K_DOWN]:
            self.y -= self.vel

        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)


def frame_tick(window, p1, p2):
    window.fill((255,255,255))
    p1.draw(window)
    p2.draw(window)
    pygame.display.update()

def read_pos(str):
    str = str.split(",")
    return int(str[0]),int(str[1])

def make_pos(pos):
    return str(pos[0]) + "," + str(pos[1])

def main():
    run = True
    n = network_helper.Helper()
    start_pos = read_pos(n.get_pos())
    p1 = Player(start_pos[0],start_pos[1], 40, 40, (255,0,0))
    p2 = Player(0, 0, 40, 40, (0, 100, 255))
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        p2_pos = read_pos(n.send(make_pos((p1.x,p1.y))))
        p2.x = p2_pos[0]
        p2.y = p2_pos[1]
        p2.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                break;
        p1.move()
        frame_tick(window, p1, p2)

main()
