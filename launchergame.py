import pgzrun
import random
import time
import csv

history_a = open("highscore.txt", "a")
history_r= open("highscore.txt", "r")


WIDTH = 800
HEIGHT = 600

#launcher config
launcher_x = 50
x_movement_launcher = 0
launcher_y = 300
y_movement_launcher = 0
launcher_radius = 30
launcher_color = "orange"

#projectile config
bullets = []
targets = []

# settings:
mouse_directed_movement = False
posx = 0
posy = 0
difx = 0
dify = 0
movement_sensitivity = 2
launch = False
hits = 0
projectile_vel = 8
friction = False
friction_value = 0.05
gravity = False
gravitational_accl = 0.05
timer = 0.1
blood = 6
gameover = False
highscore = []
pause = False

class Bullet():
    def __init__(self):
        self.x = launcher_x
        self.y = launcher_y
        self.color = ("orange")
        self.radius = 10
        self.speed = 4
    def draw_shape(self):
        screen.draw.filled_circle((self.x, self.y), self.radius, self.color)
    def fire(self):
        self.x += self.speed
    def destroy(self):
        bullets.remove(self)

class Target():
    def __init__(self):
        self.radius = random.randint(20, 60)
        self.x = (WIDTH + self.radius)
        self.y = random.randint(self.radius, (HEIGHT - self.radius))
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.speed = (1.001**(timer*0.8)+3)
    def draw_shape(self):
        screen.draw.filled_circle((self.x, self.y), self.radius, self.color)
    def move(self):
        self.x -= self.speed
    def destroy(self):
        targets.remove(self)
    


def add_target():
    if pause == False and gameover == False:
        targets.append(Target())
    clock.schedule_unique(add_target, 1.02**(-1*timer))

add_target()

def draw():
    screen.clear()
    if gameover == False and pause == False:
        for bullet in bullets:
            bullet.draw_shape()
        for target in targets:
            target.draw_shape()
        screen.draw.filled_circle((launcher_x, launcher_y), launcher_radius, launcher_color)
        screen.draw.text(f"Score: {round(timer, 2)}", (50, 100), background = "black", fontsize = 20)
        screen.draw.text(f"Hits: {hits}", (50, 500), background = "black", fontsize = 30)
        screen.draw.text(f"Blood: {blood}", (150, 500), background = "black", fontsize = 30)
    if gameover == True:
        screen.draw.text(f"GAME", (175, 120), background = "black", fontsize = 225)
        screen.draw.text(f"OVER", (190, 280), background = "black", fontsize = 225)
        screen.draw.text(f"Score: {round(timer, 0)}    High Score: {max(highscore)}", (275, 500), background = "black", fontsize = 30)
    if pause == True:
        screen.draw.text(f"GAME", (175, 120), background = "black", fontsize = 225)
        screen.draw.text(f"PAUSED", (100, 280), background = "black", fontsize = 225)


def update():
    global launcher_x, x_movement_launcher, launcher_y, y_movement_launcher, launch, gravity, gravitational_accl, friction, friction_value, timer, mouse_directed_movement, difx, dify, movement_sensitivity, hits, blood, gameover, highscore, pause
    if gameover == False and pause == False:
        timer += 1/60

        #fire bullet across screen
        for bullet in bullets:
            bullet.fire()
        
        #move targets across screen
        for target in targets:
            target.move()

        #check for bullet hitting target
        for bullet in bullets:
            for target in targets:
                distance = ((bullet.x - target.x)**2 + (bullet.y - target.y)**2)**(1/2)
                if distance <= (target.radius + bullet.radius):
                    hits += 1
                    target.destroy()
                    bullet.destroy()
        
        #check for bullet out of screen
        for bullet in bullets:
            if bullet.x > (WIDTH + bullet.radius):
                bullet.destroy()
        
        #check for target going past defense
        for target in targets:
            if target.x < (100+launcher_radius):
                blood -= 1
                target.destroy()
        
        #mouse directed movement
        dify = posy - launcher_y
        launcher_y += dify * movement_sensitivity/10

        #launcher stay inside screen
        if launcher_x <= launcher_radius:
            launcher_x = launcher_radius
        if launcher_x >= (WIDTH - launcher_radius):
            launcher_x = (WIDTH - launcher_radius)
        if launcher_y <= launcher_radius:
            launcher_y = launcher_radius
        if launcher_y >= (HEIGHT - launcher_radius):
            launcher_y = (HEIGHT - launcher_radius)

        
        #update launcher pos
        launcher_x += x_movement_launcher
        launcher_y += y_movement_launcher

        #check for gameover
        if blood < 1 and gameover == False:
            gameover = True
            history_a.write(f"{round(timer, 0)} \n")
            for bullet in bullets:
                bullet.destroy
            for target in targets:
                target.destroy
    if gameover == True:
        #find highest history score
        for line in history_r:
            line = line.strip()
            highscore.append(float(line))


# def on_mouse_down(button):
#     global launch, projectile_vel
#     bullets.append(Bullet())

def on_mouse_move(pos):
    global launcher_x, launcher_y, difx, dify, mouse_directed_movement, posx, posy
    mouse_directed_movement = True
    posx, posy = pos

def on_key_down(key):
    global pause, bullets
    if key == keys.P and pause == False:
        pause = True
        print("hj")
    elif key == keys.P and pause == True:
        pause = False
        print("hj")
    if key == keys.SPACE:
        bullets.append(Bullet())


pgzrun.go()
