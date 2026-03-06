import pgzrun
import random

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
times = 0

class Bullet():
    def __init__(self):
        self.x = launcher_x
        self.y = launcher_y
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.radius = 10
        self.speed = 2
    def draw_shape(self):
        screen.draw.filled_circle((self.x, self.y), self.radius, self.color)
    def fire(self):
        self.x += self.speed
    def destroy(self):
        bullets.remove(self)

class Target():
    def __init__(self):
        self.radius = random.randint(20, 30)
        self.x = random.randint((50+launcher_radius+self.radius), (WIDTH - self.radius))
        self.y = random.randint(self.radius, (HEIGHT - self.radius))
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    def draw_shape(self):
        screen.draw.filled_circle((self.x, self.y), self.radius, self.color)
    def destroy(self):
        targets.remove(self)

def add_target():
    targets.append(Target())

add_target()

clock.schedule_interval(add_target, 1.5)

def draw():
    screen.clear()
    for bullet in bullets:
        bullet.draw_shape()
    for target in targets:
        target.draw_shape()
    screen.draw.filled_circle((launcher_x, launcher_y), launcher_radius, launcher_color)
    screen.draw.text(f"Time: {round(times, 2)}", (50, 100), background = "black", fontsize = 20)
    screen.draw.text(f"Hits: {hits}", (50, 500), background = "black", fontsize = 30)

def update():
    global launcher_x, x_movement_launcher, launcher_y, y_movement_launcher, launch, gravity, gravitational_accl, friction, friction_value, times, mouse_directed_movement, difx, dify, movement_sensitivity, hits
    times += 1/60

    for bullet in bullets:
        bullet.fire()

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


def on_mouse_down(button):
    global launch, projectile_vel
    bullets.append(Bullet())

def on_mouse_move(pos):
    global launcher_x, launcher_y, difx, dify, mouse_directed_movement, posx, posy
    mouse_directed_movement = True
    posx, posy = pos

pgzrun.go()