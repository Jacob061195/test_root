#jump_fonction
def turn_right():
    turn_left()
    turn_left()
    turn_left()
#this the jump fonction for hurdle 4   
def jump():
    turn_left()
    while wall_on_right():
        move()
    turn_right()
    move()
    turn_right()
    while front_is_clear():
        move()
    turn_left()
while not at_goal():
    if wall_in_front():
        jump()
    else:
        move() 
"""
#this the jump fonction for hurdle 3
def jump():
    turn_left()
    move()
    turn_right()
    move()
    turn_right()
    move()
    turn_left()
while not at_goal():
    if wall_in_front():
        jump()
    else:
        move()"""
"""    
number_of_hundles = 6
while number_of_hundles > 0:
    jump()
    number_of_hundles -= 1
    print(number_of_hundles)
#for step in range(6):
#    jump()"""
################################################################
# WARNING: Do not change this comment.
# Library Code is below.
################################################################
