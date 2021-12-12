# import turtle package
import turtle

# create screen object
sc = turtle.Screen()

# create turtle object
pen = turtle.Turtle()

# method to draw square
def draw():
    for i in range(4):
        pen.forward(30)
        pen.left(90)

    pen.forward(30)

sc.setup(600, 600)

pen.speed(100)

for i in range(8):
    print(turtle.position())
    pen.up()
    pen.setpos(0, 30 * i)
    pen.down()

    # row
    for j in range(8):

        if (i + j) % 2 == 0:
            col = 'black'
        else:
            col = 'white'

        pen.fillcolor(col)
        pen.begin_fill()
        draw()
        pen.end_fill()

pen.hideturtle()

