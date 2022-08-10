import API
import sys

def log(string):
    sys.stderr.write("{}\n".format(string))
    sys.stderr.flush()
def get_adjacent_data(x,y, current_direction):
    """
    Returns the possible directions based on the direction the mouse is facing and its coords
    Inputs:
        x <int>: coordinate data
        y <int>: coordinate data
        current_direction <int>: integer that shows the direction it is facing
    Returns:
        possible_coords <list>: List of possible coordinates at that location and direction
            [forward, right,left]
        possible_directions <list>: List of possible directions the bot can turn
    """
    possible_coords = []
    possible_directions =[]
    if current_direction == 0: #DOWN
        #going down is just going forward
        possible_coords.append((x,y-1))
        possible_directions.append(0)
        #going right
        possible_coords.append((x-1,y))
        possible_directions.append(3)
        #left
        possible_coords.append((x+1,y))
        possible_directions.append(1)
    elif current_direction == 1: #RIGHT
        #Move Foward
        possible_coords.append((x+1,y))
        possible_directions.append(1)
        #Move Right
        possible_coords.append((x,y-1))
        possible_directions.append(0)
        #Moving left
        possible_coords.append((x,y+1))
        possible_directions.append(2)
    elif current_direction == 2: #UP
        #Moving Forward
        possible_coords.append((x,y+1))
        possible_directions.append(2)
        #Moving Right
        possible_coords.append((x+1,y))
        possible_directions.append(1)
        #Moving Left
        possible_coords.append((x-1,y))
        possible_directions.append(3)
    elif current_direction == 3:
        #Moving Forward
        possible_coords.append((x-1,y))
        possible_directions.append(3)
        #Moving Right
        possible_coords.append((x,y+1))
        possible_directions.append(2)
        #Movinging Left
        possible_coords.append((x,y-1))
        possible_directions.append(0)
    return (possible_coords,possible_directions)
def update_cell(x1,y1,direction,movement):
    """Based on the direction of the item, and the movement, the system returns a new cell
    Inputs:
        x<int>: coord data
        y<int>: coord data
        direction <int: Data that shows what direction the robot is facing
            0:down
            1:right
            2:up
            3:left 
        movement <str>: string that informs what direction the robot is moving to
            f: forward
            l: left
            r: right
        Returns:
            (x,y) <Tup>: New data
        """
    x = x1
    y =y1
    if direction == 0:
        if movement == "f":
            y-=1
        elif movement == "l":
            x+=1
        elif movement == "r":
            x-=1
    elif direction == 1:
        if movement == "f":
            x+=1
        elif movement == "l":
            y+=1
        elif movement == "r":
            y-=1
    elif direction == 2:
        if movement == "f":
            y+=1
        elif movement == "l":
            x-=1
        elif movement == "r":
            x+=1
    elif direction == 3:
        if movement == "f":
            x-=1
        elif movement == "l":
            y-=1
        elif movement == "r":
            y+=1
    return (x,y)

            
def explore_maze():
    #Based on my python script I made before, explores the maze until it reaches 
    #The centre
    """
    Required Data:
        explored_cells <array>: array of tuples that have coords of the cell it has explored
        current_direction <int>: Number that keeps track of where the robot is facing 
            0: facing down (s)
            1: facing right (e)
            2: facing up (n)
            3: facing left (w)
            These coords are with respect to the mms"""
    current_direction = 2
    explored_cells = [(0,0)]
    #needs to check what corner
    x = 0
    y = 0
    #Set up so that up increase y count right increases x count
    while (1):
        #check if can move foward
        #The most efficient way to do this is to make a list of potential coords
        #So the mouse can actually find what path to take
        
        #possible_coords = [(foward_coord,right,left]
        """TODO:!!!!!!!!!!!!!!!!!!!!!!
        DONE: Implement List Directions Use this when backtracking to junction """
        
        


        #The index referes to the posible points
        #(foward)
        (possible_coords,possible_directions) = get_adjacent_data(x,y,current_direction)
        if current_direction<0:
            current_direction = current_direction+4
        elif current_direction>3:
            current_direction =current_direction%3 -1

        #log("Possible Coords{}".format(possible_coords))
        #log("Current Position: {}\nCurrent Direction: {}".format((x,y), current_direction))
        
            
        if (API.wallFront() == False) and possible_coords[0] not in explored_cells:
            API.moveForward()
            #No need to change the direction, as it is just going forward
            y = possible_coords[0][1]
            x = possible_coords[0][0]
            current_direction =possible_directions[0]
        elif (API.wallRight() == False) and possible_coords[1] not in explored_cells:
            API.turnRight()
            API.moveForward()
            y = possible_coords[1][1]
            x = possible_coords[1][0]
            current_direction =possible_directions[1]

            #This could more efficiently be stored in an array
        elif (API.wallLeft() == False) and possible_coords[2] not in explored_cells:
            API.turnLeft()
            API.moveForward()
            y = possible_coords[2][1]
            x = possible_coords[2][0]
            current_direction =possible_directions[2]
            #Again this could be more effectivley stored in an array as well
        else:
            #TODO: Check centre FUNCTION
            log("Dead End at {}".format((x,y)))
            log("current direction {}".format(current_direction))
            #Reverse
            API.turnLeft()
            API.turnLeft()
            #Check Centre
            centre = 0
            squares = 0
            current_direction+=2
            if current_direction<0:
                current_direction+=4
            elif current_direction>3:
                current_direction -=4
            while centre == 0:
                log("searching Centre")
                if get_adjacent_data(x,y,current_direction)[0][1] == explored_cells[-4]:
                    if (API.wallRight() == False) and (API.wallLeft() == True):
                        log("case1")
                        return
                    break
                elif get_adjacent_data(x,y,current_direction)[0][2] == explored_cells[-4]:
                    if (API.wallRight() == True) and (API.wallLeft() == False):
                        log("case2")
                        return
                    break
                else:
                    centre = 1
                    log("Centre Not Found")
                    break
                

            #travel along until reach a point where ther is a junction, that is, greater than
            #two possible pathways
            coord = (x,y)
            checked_cells = []
            end = 0
            while end == 0:
                checked_cells.append((x,y))
                log("in While")
                log("Current Coords: {}".format((x,y)))
                log("Current Direction: {}".format(current_direction))
                
                
                count = 0
                if API.wallLeft() == False:
                    count+=1
                if API.wallRight() == False:
                    count+=1
                if API.wallFront() == False:
                    count+=1
                if (count >1):
                    #TODO: 
                    # Implement system that keeps checking until it reaches junction with unexplored
                    # DOne Implement system that properly determines what cell it is in from x and y
                    log("Current Coord {}".format((x,y)))
                    log("Explored {}".format(explored_cells))
                    for item in get_adjacent_data(x,y,current_direction)[0]:
                        #TODO: Robot gets stuck here cus sees cell thru wall
                        val = get_adjacent_data(x,y,current_direction)[0].index(item)
                        log(item)
                        #Need to ignore parts blocked by walls
                        if (val == 0) and (API.wallFront()):
                            pass
                        elif(val == 1) and (API.wallRight()):
                            pass
                        elif(val == 2) and (API.wallLeft()):
                            pass
                        elif item not in explored_cells:
                            end = 1
                            break
                        
                    #If it reaches this stage, clearly, the bot needs to look for another junction

                if end == 1:
                    continue
                log("no dice")
                            
                #TODO: Sometimes the bot can get stuck Here
                if API.wallRight() == False:
                    #right turn is eqiuvalent to a -1 to the directions
                    current_direction -=1
                    API.turnRight()
                elif API.wallLeft() == False:
                    current_direction+=1
                    API.turnLeft()
                #CHECK DIRECTION BEFORE ANY MOVEMENTS
                if current_direction<0:
                    current_direction = current_direction+4
                elif current_direction>3:
                    current_direction = current_direction-4
                log("direction {} ".format(current_direction))
                
                if API.wallFront() == False:
                    log("Move forward")
                    
                    API.moveForward()
            
                    coord = update_cell(x,y,current_direction,"f")
                    x = coord[0]
                    y = coord[1]
        
        explored_cells.append((x,y))
        API.setText(x,y,str((x,y)))
        API.setColor(x,y,"G")
        

        """
        elif not API.wallRight():
            #iT is going to move right
            #Need to make sure that cell in front is not explored
            if current_direction == 2:


        
            API.turnRight()
        elif not API.wallLeft():
            API.turnLeft()
            """
        




            
def main():
    log("Running...")
    API.setColor(0, 0, "G")
    API.setText(0, 0, "Start")
    explore_maze()
    

if __name__ == "__main__":
    main()
