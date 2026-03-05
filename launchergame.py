import pgzrun

WIDTH = 800
HEIGHT = 600

#launcher config
launcher_x = 100
x_movement_launcher = 0
launcher_y = 300
y_movement_launcher = 0
launcher_radius = 30
launcher_color = "orange"

#projectile config
projectile_x = 100
x_movement_projectile = 0
projectile_y = 300
y_movement_projectile = 0
projectile_radius = 10
projectile_color = "orange"

# settings:
mouse_directed_movement = False
posx = 0
posy = 0
difx = 0
dify = 0
movement_sensitivity = 2
launch = False
launch_count = 0
projectile_vel = 8
friction = False
friction_value = 0.05
gravity = False
gravitational_accl = 0.05
time = 0

def draw():
    screen.clear()
    screen.draw.text(f"Time: {round(time, 2)}", (50, 100), background = "black", fontsize = 20)
    screen.draw.text(f"Times Launch: {launch_count}", (50, 500), background = "black", fontsize = 30)
    screen.draw.filled_circle((launcher_x, launcher_y), launcher_radius, launcher_color)
    screen.draw.filled_circle((projectile_x, projectile_y), projectile_radius, projectile_color)

def update():
    global launcher_x, x_movement_launcher, launcher_y, y_movement_launcher, projectile_x, x_movement_projectile, projectile_y, y_movement_projectile, projectile_radius, launch, gravity, gravitational_accl, friction, friction_value, time, mouse_directed_movement, difx, dify, movement_sensitivity
    time += 1/60
    
    #mouse directed movement
    difx = posx - launcher_x
    dify = posy - launcher_y
    launcher_x += difx * movement_sensitivity/10
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


    #projectile location
    if launch == False:
        gravity = False
        friction = False
        projectile_x = launcher_x
        projectile_y = launcher_y
    else: #launch == True
        gravity = True
        friction = True
        if projectile_x >= (WIDTH - projectile_radius) or projectile_y >= (HEIGHT - projectile_radius):
            launch = False
            x_movement_projectile = 0
            y_movement_projectile = 0

    #gravity    
    if gravity == True:
        y_movement_projectile += gravitational_accl

    #friction
    if friction == True:
        print('.  hhhhhldhflkdsa')
        x_movement_projectile -= friction_value
        if x_movement_projectile <= 0:
            x_movement_projectile = 0
            friction = False 

    #update launcher pos
    launcher_x += x_movement_launcher
    launcher_y += y_movement_launcher

    #update pojectile pos
    projectile_x += x_movement_projectile
    projectile_y += y_movement_projectile

    print(mouse_directed_movement)
    print(difx)
    print(dify)
    print()


def on_mouse_down(button):
    global x_movement_projectile, launch, projectile_vel, launch_count
    if button == mouse.LEFT and launch == False:
        launch = True
        launch_count += 1
        x_movement_projectile = projectile_vel

def on_mouse_move(pos):
    global launcher_x, launcher_y, difx, dify, mouse_directed_movement, posx, posy
    mouse_directed_movement = True
    posx, posy = pos

pgzrun.go()