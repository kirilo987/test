import turtle

def home():
    turtle.shape("turtle")
    turtle.color("black")
    turtle.speed(0)

    turtle.forward(164)
    turtle.left(90)
    turtle.forward(140)
    turtle.left(90)
    turtle.forward(164)
    turtle.left(90)
    turtle.forward(140)

    turtle.left(180)
    turtle.forward(140)
    turtle.right(55)
    turtle.forward(100)
    turtle.right(70) 
    turtle.forward(100)
    turtle.right(55)

    turtle.penup()
    turtle.goto(164 / 2 - 30, 0)
    turtle.setheading(90)
    turtle.pendown()
    turtle.forward(90)
    turtle.right(90)
    turtle.forward(40)
    turtle.right(90)
    turtle.forward(90)

home()
turtle.done()