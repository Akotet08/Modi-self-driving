from shutil import move
import modi
import time
import math
import random

from flake_v3 import trainer

# midterm - RL implementation with obstacles on 24th
# we have only 40 minutes for practice, testing
# number of collision is deducted
# the frozen map is in gym/toy_text_frozen_lake.py

# speeds for caliberating
sl = (0, 30)
sr = (-30, 0) # change the 40 for speed

# speeds for turning left and right
l  = (32, 45)
r = (-45, -32)

# forward speed
f = (47, -45)
cf = (42, -40)
turn_iter = 7

BP = 60  # proximity level at black
DF = 30  # the difference to calibrate


''' 
    Defined Moves
        M1 - To go forward one cell - Move until a black line, calibrate if needed, then move to the center of the next cell....
            to move to the center of the next cell: motor.speed = 100, 100 (once or more ---- to be determined)
        M2 - To go to the left of the current cell - turn left and do M1.
        M3 - To go right of the current cell - turn right and do M1

'''

    
if __name__ == '__main__':
    # modi.update_module_firmware()
    bundle = modi.MODI()
    ir1 = bundle.irs[0] # left
    ir0 = bundle.irs[1] # right
    motor = bundle.motors[0]
    motor2 = bundle.motors[1]
    thrs = 23

    def stop_motors():
        motor.speed = 0, 0
        motor2.speed = 0, 0

    def calibrate(right, left):
        if right.proximity > left.proximity:
            motor.speed = sl
            motor2.speed = sl
            print('caliberating left')
        if left.proximity > right.proximity:
            motor.speed = sr
            motor2.speed = sr
            print('caliberating right')
        # move_forward()
    def init_ir():
        while ir0.proximity == 0 or ir1.proximity == 0:
            continue

    def cross():
        for _ in range(10):
            cross_speed  = cf
            motor.speed = cross_speed
            motor2.speed = cross_speed
        stop_motors()

    def move_forward():
        # implementaion of M1: Move forward until a black line and then calibrate if need and then move to the center of the next cell.
        while True:
            if ir1.proximity < BP or ir0.proximity  < BP:
                stop_motors()
                print('stop')
                diff = abs(ir1.proximity - ir0.proximity)
                if diff > 10:
                    pass
                    calibrate(ir0, ir1)
                return
            if abs(ir1.proximity - ir0.proximity) > DF:
                stop_motors()
                print('stop')
                calibrate(ir0, ir1)
                return
            else:
                motor.speed = f
                motor2.speed = f

    def turn_left():
        # implementation of M2: turn left -> M1
        for i in range(turn_iter):
            motor.speed = l
            motor2.speed = l
        # motor.speed = (0, 35)
        # motor2.speed = (0, 35)

    def turn_right():
        # implementaion of M3: turn right -> M2 
        for i in range(turn_iter):
            motor.speed = r 
            motor2.speed = r  
        # motor.speed = (-35, 0)
        # motor2.speed = (-35, 0)

    #['up', 'down', 'left', 'right']
    def convert(list):
        # to be implemented 
        pass



    ''' Test pathes '''
    # p1 = list('FLRFLFRLRFL')
    # p2 = list('FLLL')
    # p3 = list('FRRR')
    # p4 = list('FFFFFFFFFFFFFFFFFFFF')
    # P6 = list('FLFRFLFRLFR')

    r_path = trainer.train() 
    # convert the robot path to our path
    path = convert(r_path)


    print(path)
    index = 0
    n = len(path)

    init_ir()

    # turn_right()

    # stop_motors()
    while True:
        print(f'ir1: {ir1.proximity}')
        print(f'ir0:  {ir0.proximity + 7}')

        #move_forward()
       
        
        d = path[index]
        print(d)
        if d == 'F':
            move_forward()
            cross()
            move_forward()
            index += 1
        if d == 'L':
            turn_left()
            move_forward()
            cross()
            move_forward()
            index += 1
        if d == 'R':
            turn_right()
            move_forward()
            cross()
            move_forward()
            index += 1

        if index >= n:
            stop_motors()
            break


              

        

        

            

