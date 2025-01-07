from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

W_Width, W_Height = 500, 600
leftsteps = []
rightsteps = []
step_height = 20
step_distance = 120
gap = 100
ball_x, ball_y = 250, 585
ball_radius = 15
screen_speed = 8
ball_speed = 1.5
score = 0
game_over = False

def init():
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, W_Width, 0, W_Height)
    glMatrixMode(GL_MODELVIEW)
    glViewport(0, 0, W_Width, W_Height)  


def det_zone(x0, y0, x1, y1):
    dx = x1 - x0
    dy = y1 - y0
    if abs(dx) >= abs(dy):
        if dx >= 0:
            if dy >= 0:
                zone = 0
            else:
                zone = 7
        else:
            if dy >= 0:
                zone = 3
            else:
                zone = 4
    else:
        if dx >= 0:
            if dy >= 0:
                zone = 1
            else:
                zone = 6
        else:
            if dy >= 0:
                zone = 2
            else:
                zone = 5
    return zone

def transform_zone(x, y, zone, points):
    if zone == 0:
        points.append((x, y))
    if zone == 1:
        points.append((y, x))
    if zone == 2:
        points.append((-y, x))
    if zone == 3:
        points.append((-x, y))
    if zone == 4:
        points.append((-x, -y))
    if zone == 5:
        points.append((-y, -x))
    if zone == 6:
        points.append((y, -x))
    if zone == 7:
        points.append((x, -y))

def draw_points(coords):
    glBegin(GL_POINTS)
    for x, y in coords:
        glVertex2f(x, y)
    glEnd()

def mid_point_line(x0, y0, x1, y1, zone):
    dx = x1 - x0
    dy = y1 - y0
    incrE = 2 * dy
    incrNE = 2 * (dy - dx)
    d = 2 * dy - dx
    x = x0
    y = y0
    points = []
    while x < x1:
        transform_zone(x, y, zone, points)
        if d < 0:
            d += incrE
            x += 1
        else:
            d += incrNE
            x += 1
            y += 1

    draw_points(points)

def line_drawing_algo(x0, y0, x1, y1):
    zone = det_zone(x0, y0, x1, y1)
    if zone == 0:
        mid_point_line(x0, y0, x1, y1, zone)
    if zone == 1:
        mid_point_line(y0, x0, y1, x1, zone)
    if zone == 2:
        mid_point_line(y0, -x0, y1, -x1, zone)
    if zone == 3:
        mid_point_line(-x0, y0, -x1, y1, zone)
    if zone == 4:
        mid_point_line(-x0, -y0, -x1, -y1, zone)
    if zone == 5:
        mid_point_line(-y0, -x0, -y1, -x1, zone)
    if zone == 6:
        mid_point_line(-y0, x0, -y1, x1, zone)
    if zone == 7:
        mid_point_line(x0, -y0, x1, -y1, zone)


def draw_circle(cntr_x, cntr_y, r):
    x = 0
    y = r
    d = 1 - r

    while x <= y:
        for i in range(cntr_x - x, cntr_x + x + 1):
            glBegin(GL_POINTS)
            glVertex2f(i, cntr_y + y)
            glVertex2f(i, cntr_y - y)
            glEnd()

        for i in range(cntr_x - y, cntr_x + y + 1):
            glBegin(GL_POINTS)
            glVertex2f(i, cntr_y + x)
            glVertex2f(i, cntr_y - x)
            glEnd()

        if d <= 0:
            d += 2 * x + 3
            x += 1
        else:
            d += 2 * (x - y) + 5
            x += 1
            y -= 1


def draw_step(x, y, width, height):
    x = int(x)
    y = int(y)
    width = int(width)
    height = int(height)
    line_drawing_algo(x, y, x + width, y)
    line_drawing_algo(x, y + height, x + width, y + height)
    line_drawing_algo(x, y, x, y + height)
    line_drawing_algo(x + width, y, x + width, y + height)

    for i in range(y, y + height):
        line_drawing_algo(x, i, x + width, i)


def generate_new_step():
    global leftsteps, rightsteps, step_height, W_Width, gap, step_distance
    l_step_width = random.randint(50, 200)
    if not leftsteps:
        new_y= -W_Height
    else:
        new_y=leftsteps[-1][1] - step_distance

    leftsteps.append([0, new_y, l_step_width, step_height])  #(x1, y1, x2, y2)
    rightsteps.append([l_step_width + gap, new_y, W_Width - (l_step_width + gap), step_height]) 


def reset_game():
    global ball_x, ball_y, ball_speed, score, leftsteps, rightsteps, game_over
    ball_x, ball_y = 250, 585
    ball_speed = 0.5
    score = 0
    leftsteps.clear()
    rightsteps.clear()
    generate_new_step()
    game_over = False
    print("Game Over! Score reset. Press 'R' to restart.")


def display():
    global leftsteps, rightsteps, ball_x, ball_y, ball_radius, score, game_over

    glClear(GL_COLOR_BUFFER_BIT)

    if game_over:
        # reset_game()
        glutSwapBuffers()
        return

    glColor3f(0.87, 0.89, 0.93)
    draw_circle(ball_x, ball_y, ball_radius)

    if score <= 50:
        glColor3f(0.38, 0.565, 0.82)  
    elif 50 < score <= 150:
        glColor3f(0.012, 0.22, 0.988)  
    elif 150 < score <= 300:
        glColor3f(0.0196, 0.098, 0.38)  
    else:
        glColor3f(1.0, 0.0, 0.0)  

    for step in leftsteps:
        draw_step(step[0], step[1], step[2], step[3])
    for step in rightsteps:
        draw_step(step[0], step[1], step[2], step[3])

    glutSwapBuffers()

def animate():
    global ball_y, ball_x, ball_speed, leftsteps, rightsteps, screen_speed, W_Height, score, game_over

    if game_over:
        return
    
    # Ball speed and screen speed depending on score
    if score > 50:
        ball_speed = 3 + (score * 0.015)
        screen_speed = 10 + (score * 0.03)
    elif score > 100:
        ball_speed = 3 + (score * 0.02)
        screen_speed = 10 + (score * 0.04)
    elif score > 150:
        ball_speed = 3 + (score * 0.03)
        screen_speed = 10 + (score * 0.05)
    else:
        ball_speed = 3 + (score * 0.01)
        screen_speed = 10 + (score * 0.02)

    ball_speed = min(ball_speed, 12)
    screen_speed = min(screen_speed, 25)

    step_collision = check_collision()

    if ball_y - ball_radius <= 0:
        ball_speed = 0  
        ball_y = -ball_radius  


        if step_collision:
            ball_y = step_collision[1] + step_collision[3] + ball_radius  
            ball_speed = 3 
    
    elif step_collision:
        ball_y += screen_speed

        step_left = step_collision[0]
        step_right = step_collision[0] + step_collision[2]
        if ball_x - ball_radius < step_left:
            ball_x = step_left + ball_radius
        elif ball_x + ball_radius > step_right:
            ball_x = step_right - ball_radius
    else:
        ball_y -= ball_speed
        ball_speed += 0.1

    # step's speed
    for step in leftsteps:
        step[1] += screen_speed
    for step in rightsteps:
        step[1] += screen_speed

    # Remove steps that have moved from the screen
    if leftsteps and leftsteps[0][1] > W_Height:
        leftsteps.pop(0)
        rightsteps.pop(0)
        score += 1

    # Generate new steps 
    if not leftsteps or leftsteps[-1][1] >= 150:
        generate_new_step()

    #ceiling touch---> Game Over
    if ball_y + ball_radius >= W_Height:
        game_over = True
        return

    glutPostRedisplay()




def check_collision():
    global ball_x, ball_y, ball_radius, leftsteps, rightsteps

    ball_left = ball_x - ball_radius 
    ball_right = ball_x + ball_radius
    ball_bottom = ball_y - ball_radius

    for step in leftsteps + rightsteps:
        step_left = step[0]
        step_right = step[0] + step[2]
        step_top = step[1] + step[3]
        step_bottom = step[1]

        if step_left <= ball_x <= step_right and ball_bottom <= step_top and ball_bottom > step_bottom:
            return step 

    return None




def keyboard_listener(key, x, y):
    global ball_x, ball_y, game_over

    if key == b'a' and (ball_x >= 25) and not game_over:
        ball_x -= 20
    elif key == b'd' and (ball_x <= 475) and not game_over:
        ball_x += 20
    elif key == b'r':
        reset_game()



def timer(value):
    global screen_speed
    glutPostRedisplay()
    glutTimerFunc(int(1500 / screen_speed), timer, 0)


glutInit()
glutInitWindowSize(W_Width, W_Height)
glutCreateWindow(b"Falling Ball Game")
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB) 
glClearColor(0.0, 0.0, 0.0, 0.0)
init()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard_listener)
glutTimerFunc(1000, timer, 0)
glutIdleFunc(animate)
glutMainLoop()