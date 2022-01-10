import turtle
import random

# Constants. Referenced in other parts of the code, so you can easily change things like game speed or window size without causing problems.
WIDTH = 500
HEIGHT = 500
DELAY = 85  # In milliseconds
FOOD_SIZE = 20

offsets = {
    "up": (0, 20),
    "down": (0, -20),
    "left": (-20, 0),
    "right": (20, 0)
}


def bind_direction_keys():
    screen.onkey(lambda: set_snake_direction("up"), "Up",)
    screen.onkey(lambda: set_snake_direction("down"), "Down")
    screen.onkey(lambda: set_snake_direction("left"), "Left")
    screen.onkey(lambda: set_snake_direction("right"), "Right")

# Snake controls. Makes sure that you can't directly reverse onto the body. Also changes direction of the head.
def set_snake_direction(direction):
    global snake_direction
    if direction == "up":
        if snake_direction != "down":
            snake_direction = "up"
            head_stamper.setheading(90)
    if direction == "down":
        if snake_direction != "up":
            snake_direction = "down"
            head_stamper.setheading(270)
    if direction == "left":
        if snake_direction != "right":
            snake_direction = "left"
            head_stamper.setheading(180)
    if direction == "right":
        if snake_direction != "left":
            snake_direction = "right"
            head_stamper.setheading(0)

def gameplay():
    stamper.clearstamps()  # Remove all current stamps on screen

    new_head = snake[-1].copy()
    new_head[0] += offsets[snake_direction][0]
    new_head[1] += offsets[snake_direction][1]

    # Check for collisions with borders or snake itself
    if new_head in snake or new_head[0] < - WIDTH / 2 or new_head[0] > WIDTH / 2 \
            or new_head[1] < - HEIGHT / 2 or new_head[1] > HEIGHT / 2:
        reset()
    else:

        # Attach new head for the body
        snake.append(new_head)


        # Check for food collision
        if not food_collision():
            snake.pop(0)  # Keep length if it does not collide w/ food

        for segment in snake:
            stamper.goto(segment[0], segment[1])
            stamper.stamp()
            #head_stamper.shape(head_segment)
            head_stamper.goto(new_head)



        # Refreshes the screen with new segments
        screen.title(f"Snake! Score: {score}")
        screen.update()

        # Repeat this process
        turtle.ontimer(gameplay, DELAY)


def food_collision():
    global food_pos, score
    if get_distance(snake[-1], food_pos) < 20:
        food_pos = get_random_food()
        food.goto(food_pos)
        score = score + 1
        return True
    return False


def get_random_food():
    x = random.randint(- WIDTH / 2 + FOOD_SIZE, WIDTH / 2 - FOOD_SIZE)
    y = random.randint(- HEIGHT / 2 + FOOD_SIZE, HEIGHT / 2 - FOOD_SIZE)
    return (x, y)


def get_distance(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    distance = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
    return distance

# Reset. Happens on collision with screen edge, snake body, and when first running the game.
def reset():
    global score, snake, head, snake_direction, food_pos
    score = 0
    snake = [[0, 0], [20, 0], [40, 0], [60, 0]]
    head = snake[-1]
    snake_direction = "up"
    head_stamper.setheading(90)
    food_pos = get_random_food()
    food.goto(food_pos)
    gameplay()


# Creates a screen.
screen = turtle.Screen()
screen.setup(WIDTH, HEIGHT)
screen.title("Snake")
screen.bgpic("grass.gif")
screen.tracer(0)  # Stops automatic animation

# Imports drawn images to use as food and body segments.
apple = "apple.gif"
screen.addshape(apple)
bod_segment = "body.gif"
screen.addshape(bod_segment)

# Turtle won't allow a custom image to turn, so I use this section to draw the snake's head as a compound of shapes.
skully = turtle.Shape("compound")

pen = turtle.Turtle()
pen.begin_poly()
pen.up()
pen.goto(-10,0)
pen.begin_fill()
pen.goto(-10,10)
pen.goto(10,10)
pen.goto(10,-10)
pen.goto(-10,-10)
pen.goto(-10,10)
pen.end_fill()
pen.end_poly()
screen.colormode(255)
skully.addcomponent(pen.get_poly(), (158, 33, 255), (158, 33, 255))

pen.up()
pen.goto(-5,-8)
pen.begin_poly()
pen.begin_fill()
pen.pencolor("white")
pen.circle(3)
pen.end_fill()
pen.end_poly()
pen.up()
skully.addcomponent(pen.get_poly(), "white", "white")

pen.up()
pen.goto(-5,-4)
pen.begin_poly()
pen.begin_fill()
pen.pencolor("white")
pen.circle(1)
pen.end_fill()
pen.end_poly()
pen.up()
skully.addcomponent(pen.get_poly(), "black", "black")

pen.up()
pen.begin_fill()
pen.pencolor("white")
pen.up()
pen.goto(5,-8)
pen.begin_poly()
pen.circle(3)
pen.end_fill()
pen.up()
pen.end_poly()
skully.addcomponent(pen.get_poly(), "white", "white")

pen.up()
pen.begin_fill()
pen.pencolor("white")
pen.up()
pen.goto(5,-4)
pen.begin_poly()
pen.circle(1)
pen.end_fill()
pen.up()
pen.end_poly()
skully.addcomponent(pen.get_poly(), "black", "black")

pen.goto(0,10)
pen.pensize(3)
pen.down()
pen.pencolor("pink")
pen.begin_poly()
pen.goto(0,15)
pen.goto(3,20)
pen.goto(0,15) 
pen.goto(-3,20)
pen.end_poly()
skully.addcomponent(pen.get_poly(), "pink", "pink")

pen.hideturtle()
pen.clear()
# End of drawing section

# Registers the drawn head as a custom shape.
screen.register_shape("skull", skully)

# Event handlers, used for arrow key controls
screen.listen()
bind_direction_keys()

# Stamp for the body sections.
stamper = turtle.Turtle()
stamper.shape(bod_segment)
stamper.shapesize(25 / 20)
stamper.penup()

# Special stamper just for the snake's head.
head_stamper = turtle.Turtle()
head_stamper.shape("skull")
stamper.shapesize(25 / 20)
head_stamper.penup()

# The food. Uses an apple picture.
food = turtle.Turtle()
food.shape(apple)
food.color("red")
food.shapesize(FOOD_SIZE / 25)
food.penup()

# Starts the game, but also serves as the point for restarting it.
reset()

turtle.done()
