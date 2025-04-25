from turtle import *

t = Turtle()
t.speed(0)
t.pensize(2)

# Функція для центрального сонця
def draw_sun_body(radius):
    t.penup()
    t.goto(0, -radius)
    t.pendown()
    t.color("orange", "yellow")
    t.begin_fill()
    t.circle(radius)
    t.end_fill()

# Функція для малювання променя-прямокутника
def draw_ray_rect(length, width, angle):
    t.penup()
    t.goto(0, 0)
    t.setheading(angle)
    t.forward(60)  # Відстань від центру до початку променя

    t.begin_fill()
    for _ in range(2):
        t.forward(length)
        t.left(90)
        t.forward(width)
        t.left(90)
    t.end_fill()
    t.penup()

# Малюємо саме сонце
draw_sun_body(60)

# Малюємо 12 променів-прямокутників
t.color("gold", "gold")
for i in range(12):
    draw_ray_rect(length=30, width=6, angle=i * 30)

done()