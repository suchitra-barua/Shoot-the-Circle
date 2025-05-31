from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

# Colors
white = (1.0, 1.0, 1.0)
red = (1.0, 0.0, 0.0)
teal = (0.0, 1.0, 1.0)
amber = (1.0, 0.75, 0.0)
background = (0.0, 0.0, 0.0)

# Screen dimensions
WIDTH, HEIGHT = 700, 700
game_state = 'playing'

# Button dimensions
button_width, button_height = 120, 200  # Increased button size
button_padding = 10



shooter_pos = WIDTH // 2
center_x, center_y = WIDTH // 2, HEIGHT // 2
radius = 20
circle_color = (1.0, 1.0, 0.0)
game_state = 'playing'
quit_flag = False
falling_circle = [] # falling circle store krtisi
projectiles = []
score = 0
misses = 0 #circle jegula bottom e ashche
missed_shots = 0 #jegula shot hit kore nai missed
timer_active = False


def draw_projectiles():
    glColor3f(1.0, 1.0, 0.0)
    for x, y, radius in projectiles:
        draw_circle(x, y, radius)


for i in range(6):
    x = random.randint(25, WIDTH - 25)
    y = random.randint(650, 750)
    radius = random.randint(15, 25)
    falling_circle.append([x, y, radius])


def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    gluOrtho2D(0, WIDTH, 0, HEIGHT)


def draw_circle(x_center, y_center, radius):#midpoint circle
    x = 0
    y = radius
    p = 1 - radius

    glPointSize(2)
    glColor3f(*circle_color)
    glBegin(GL_POINTS)

    # Plot the initial point in each octant using 8-way symmetry
    plot_circle_points(x_center, y_center, x, y)

    while x < y:
        x += 1
        if p < 0:      #algo
            p += 2 * x + 1
        else:
            y -= 1
            p += 2 * (x - y) + 1
        plot_circle_points(x_center, y_center, x, y)

    glEnd()


def plot_circle_points(x_center, y_center, x, y):
    for zone in range(8):
        x_transformed, y_transformed = eight_way_zero_to_other(x, y, zone)
        glVertex2f(x_center + x_transformed, y_center + y_transformed)


def eight_way_other_to_zero(x1, y1, x2, y2, zone):#(zone o teh nichi)
    if zone == 1:
        return y1, x1, y2, x2
    elif zone == 2:
        return y1, -x1, y2, -x2
    elif zone == 3:
        return -x1, y1, -x2, y2
    elif zone == 4:
        return -x1, -y1, -x2, -y2
    elif zone == 5:
        return -y1, -x1, -y2, -x2
    elif zone == 6:
        return -y1, x1, -y2, x2
    elif zone == 7:
        return x1, -y1, x2, -y2
    return x1, y1, x2, y2


def eight_way_zero_to_other(x, y, zone):#(original zone e back)
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y


def find_zone(x1, y1, x2, y2):
    dy = y2 - y1
    dx = x2 - x1
    if abs(dy) > abs(dx):
        if dy >= 0 and dx >= 0:
            return 1
        elif dy >= 0 and dx <= 0:
            return 2
        elif dy <= 0 and dx <= 0:
            return 5
        elif dy <= 0 and dx >= 0:
            return 6
    else:
        if dy >= 0 and dx >= 0:
            return 0
        elif dy >= 0 and dx <= 0:
            return 3
        elif dy <= 0 and dx <= 0:
            return 4
        elif dy <= 0 and dx >= 0:
            return 7


def draw_midpoint_line(x1, y1, x2, y2):
    zone = find_zone(x1, y1, x2, y2)
    x1_0, y1_0, x2_0, y2_0 = eight_way_other_to_zero(x1, y1, x2, y2, zone)

    dx = x2_0 - x1_0
    dy = y2_0 - y1_0
    d = 2 * dy - dx
    dE = 2 * dy
    dNE = 2 * (dy - dx)
    x = x1_0
    y = y1_0
    glPointSize(2)
    glBegin(GL_POINTS)
    while x <= x2_0:
        a, b = eight_way_zero_to_other(x, y, zone)
        glVertex2f(a, b)
        if d < 0:
            x += 1
            d += dE
        else:
            x += 1
            y += 1
            d += dNE
    glEnd()


def draw_buttons():
    btn_width, btn_height = button_width, button_height
    vertical_offset = 100

    # Left Corner (Restart button)
    restart_x, restart_y = 50, HEIGHT - btn_height - 50 + vertical_offset #pos
    glColor3f(*teal)
    draw_arrow(restart_x + btn_width // 2, restart_y + btn_height // 2, 'left', button_width)

    # Middle (Play/Pause button)
    play_pause_x = WIDTH // 2 - btn_width // 2        #pos
    play_pause_y = HEIGHT - btn_height - 50 + vertical_offset
    glColor3f(*amber)
    draw_play_pause(play_pause_x + btn_width // 2, play_pause_y + btn_height // 2, button_width)

    # Right Corner (cross button)
    quit_x = WIDTH - btn_width - 50
    quit_y = HEIGHT - btn_height - 50 + vertical_offset #pos
    glColor3f(*red)
    draw_cross(quit_x + btn_width // 2, quit_y + btn_height // 2, button_width)


def draw_shooter():
        x = shooter_pos  # Rocket's horizontal position
        y = 50  # Rocket's vertical position (base)
        width = 40  # Width
        height = 80  # Height

        # rocket
        #red triangle
        glColor3f(1.0, 0.0, 0.0)
        glBegin(GL_TRIANGLES)
        #triangle er points
        glVertex2f(x, y + height)
        glVertex2f(x - width / 2, y + height - 30)
        glVertex2f(x + width / 2, y + height - 30)
        glEnd()

        #  (yellow quad)
        glColor3f(1.0, 1.0, 0.0)
        glBegin(GL_QUADS)
        glVertex2f(x - width / 2, y + height - 30)
        glVertex2f(x + width / 2, y + height - 30)
        glVertex2f(x + width / 2, y)
        glVertex2f(x - width / 2, y)
        glEnd()

def draw_falling_circle():
    global falling_circle
    for elem in falling_circle:
        x, y, radius = elem
        x_transformed = x    #original cordinate
        y_transformed = y
        draw_circle(x_transformed, y_transformed, radius)


def draw_arrow(x, y, direction, size):  #restart er arrow draw
    scale = size / 60
    if direction == 'left':
        draw_midpoint_line(x - 20 * scale, y - 10 * scale, x - 30 * scale, y)  # top Left
        draw_midpoint_line(x - 20 * scale, y + 10 * scale, x - 30 * scale, y)  #bottom Right
        draw_midpoint_line(x - 30 * scale, y, x - 10 * scale, y)  # Base


def draw_play_pause(x, y, size):
    scale = size / 60
    if game_state == 'playing':    #!!
        draw_midpoint_line(x - 10 * scale, y + 5 * scale, x - 10 * scale, y - 10 * scale)
        draw_midpoint_line(x + 10 * scale, y + 5 * scale, x + 10 * scale, y - 10 * scale)
    else:
        draw_midpoint_line(x - 10 * scale, y + 10 * scale, x + 10 * scale, y)
        draw_midpoint_line(x - 10 * scale, y - 10 * scale, x + 10 * scale, y)
        draw_midpoint_line(x - 10 * scale, y + 10 * scale, x - 10 * scale, y - 10 * scale)


def draw_cross(x, y, size):
    scale = size / 60
    draw_midpoint_line(x - 10 * scale, y - 10 * scale, x + 10 * scale, y + 10 * scale)
    draw_midpoint_line(x - 10 * scale, y + 10 * scale, x + 10 * scale, y - 10 * scale)


def handle_button_click(x, y):
    global game_state, shooter_pos, score, misses, missed_shots, projectiles

    btn_width, btn_height = button_width, button_height
    vertical_offset = 70

    # Left Corner (Restart button)
    restart_x, restart_y = 50, HEIGHT - btn_height - 50 + vertical_offset
    if restart_x <= x <= restart_x + btn_width and restart_y <= y <= restart_y + btn_height:
        reset_game()

    # Middle (Play/Pause button)
    play_pause_x = WIDTH // 2 - btn_width // 2
    play_pause_y = HEIGHT - btn_height - 50 + vertical_offset
    if play_pause_x <= x <= play_pause_x + btn_width and play_pause_y <= y <= play_pause_y + btn_height:
        if game_state == 'playing':
            game_state = 'paused'
        else:
            game_state = 'playing'

    # Right Corner (Quit button)
    quit_x = WIDTH - btn_width - 50
    quit_y = HEIGHT - btn_height - 50 + vertical_offset
    if quit_x <= x <= quit_x + btn_width and quit_y <= y <= quit_y + btn_height:
        print("GoodBye")
        glutLeaveMainLoop()  # Exit the main loop immediately when Quit button is clicked
        return


def reset_game():
    global falling_circle, projectiles, score, misses, missed_shots, game_state, timer_active, shooter_pos

    # Clear all relevant game data
    falling_circle.clear()
    projectiles.clear()
    shooter_pos = WIDTH // 2
    score = 0
    misses = 0
    missed_shots = 0

    # Reinitialize falling circles
    for i in range(6):
        x = random.randint(25, WIDTH - 25)
        y = random.randint(650, 750)
        radius = random.randint(15, 25)
        falling_circle.append([x, y, radius])

    game_state = 'playing'  # Set game state back to playing
    glutPostRedisplay()  # Ensure the screen is redrawn

    if not timer_active:  # Start the timer if it is not already running
        glutTimerFunc(25, update, 0)
        timer_active = True  # Mark the timer as active


def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        handle_button_click(x, HEIGHT - y)


def keyboard(key, x, y):
    global quit_flag
    global shooter_pos
    step_size = 15
    if key == b'\x1b':  # cross key
        quit_flag = True
    elif key == b'a':
        shooter_pos -= step_size
        if shooter_pos - radius < 0:  #rocket left e shore ashbe
            shooter_pos = radius
    elif key == b'd':
        shooter_pos += step_size
        if shooter_pos + radius > WIDTH:  #rocket right e shore ashbe
            shooter_pos = WIDTH - radius #screen er modde thkbe baire jbeena
    elif key == b' ':
        projectiles.append((shooter_pos, 50, 10)) #fireee
def draw_score():
    glColor3f(1.0, 1.0, 1.0)  # White color for the score text
    glRasterPos2f(10, HEIGHT - 30)  # Position for the score
    score_text = f"Score: {score}"
    for char in score_text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_18, ord(char))

def update(value):  #projectile movement, falling circle positions, collision detection, score updates, and game-over
    global falling_circle, projectiles, game_state, HEIGHT, score, missed_shots, misses, timer_active

    if game_state == 'playing':
        new_projectiles = []

        for projectile in projectiles:
            px, py, pradius = projectile
            projectile_collided = False    #no collision yet

            # Check for collision with falling circles
            for i in reversed(range(len(falling_circle))):
                x, y, radius = falling_circle[i]
                if check_collision(x, y, radius, px, py, pradius):
                    score += 1  # Increment score for hitting a circle
                    print("Score:", score)
                    falling_circle.pop(i)  # Remove the hit circle
                    projectile_collided = True
                    # Create a new falling circle immediately
                    new_x = random.randint(25, WIDTH - 25)
                    new_y = random.randint(650, 750)
                    new_radius = random.randint(15, 25)
                    falling_circle.append([new_x, new_y, new_radius])
                    break  # Stop checking after one hit

            if not projectile_collided: #missed projectile
                new_y = py + 40
                if new_y < HEIGHT:
                    new_projectiles.append((px, new_y, pradius))
                else:
                    missed_shots += 1  # Count missed shots that go off-screen

        projectiles = new_projectiles

        # Update positions of falling circles
        for i in range(len(falling_circle)):
            if game_state != "over":
                x, y, radius = falling_circle[i]
                y -= 0.90    #falling circles downward

                if y + radius < 0:
                    y = random.randint(650, 750)  # Reset circle to top
                    x = random.randint(radius, WIDTH - radius)
                    misses += 1  # Increment miss count for circles that cross the bottom
                falling_circle[i] = [x, y, radius]

                # Check for collision with the shooter
                if check_collision(x, y, radius, shooter_pos, 50, 20):  # Shooter position and falling circle
                    score += 1  # Increment score for hitting a falling circle
                    print("Score:", score)
                    # Reset the falling circle
                    falling_circle[i] = [random.randint(25, WIDTH - 25), random.randint(650, 750), random.randint(15, 25)]
                    break


                if misses >= 3:
                    game_state = 'over'
                    falling_circle.clear()
                    glutPostRedisplay()
                    print("Game Over: Missed 3 falling circles!")
                    print(f"Final Score: {score}")
                    break

                if missed_shots >= 3:
                    game_state = 'over'
                    falling_circle.clear()
                    glutPostRedisplay()
                    print("Game Over: Missed 3 shots!")
                    print(f"Final Score: {score}")
                    break

    # Continue calling update regardless of the state
    if game_state != 'over':
        glutPostRedisplay()  # Redraw the scene
        glutTimerFunc(25, update, 0)  # Schedule the next update frame
    else:
        timer_active = False

def check_collision(x1, y1, r1, x2, y2, r2):
    # Calculate the distance between the two centers
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 #straight line distance
    return distance < (r1 + r2)  #  if the distance is less than the sum of the radii -collision


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_buttons()
    draw_shooter()
    draw_falling_circle()
    draw_projectiles()
    glutSwapBuffers()


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(WIDTH, HEIGHT)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Shoot the Circle")
init()  # Set up initial OpenGL environment
glutDisplayFunc(display)  # Register display callback
glutMouseFunc(mouse)  # Register mouse click callback
glutKeyboardFunc(keyboard)  # Register keyboard for special keys
glutTimerFunc(25, update, 0)  # Initially register the timer callback to start updates
glutMainLoop()