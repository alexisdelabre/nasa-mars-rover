directions_list = ["N", "E", "S", "W"]
instructions_list = ["M", "L", "R"]

class Rover():
    ## CLASS INIT
    def __init__(self, pos_x=0, pos_y=0, start_direction="N", land_size=(5,5)):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.current_direction = start_direction
        self.land_size = land_size

    ## —— MOVE METHOD
    def move(self):
        #init frontier | min = 0 and max = x,y of the canva size
        x_min, y_min, x_max, y_max = 0, 0, self.land_size[0], self.land_size[1]

        #check the rover current direction -> then if move is legal (in the canva) => move the rover
        if self.current_direction == "N": #check direction
            if self.pos_y + 1 <= y_max: #check if inside position
                self.pos_y += 1 #make the rover move
        elif self.current_direction == "E":
            if self.pos_x + 1 <= x_max:
                self.pos_x += 1
        elif self.current_direction == "S":
            if self.pos_y - 1 >= y_min:
                self.pos_y -= 1 
        elif self.current_direction == "W":
            if self.pos_x - 1 >= x_min:
                self.pos_x -= 1
    
    ## —— TURN METHOD
    def turn(self, instruction):
        #current direction in dir list? yes -> get index of this direction in dir list
        if self.current_direction in directions_list:
            index = directions_list.index(self.current_direction)
        
        #instruction R -> increase index => turn clock side | opposite behavior for L
        if instruction == "R":
            index +=1
        elif instruction == "L":
            index -= 1

        #if current direction is W -> new index is 4 (max in range list is 3) -> reset to 0 => N (right after W)
        if index == len(directions_list):
            index = 0

        #new current direction
        self.current_direction = directions_list[index]

def nasa_mission():
    ## —— INSTRUCTIONS FILE PARSER
    def instructions_parser():
        #open file and separate lines
        file = open("rovers_instructions.txt", 'r')
        Lines = file.readlines()

        #go throught each line to get instructions -> dictionnary (land size + list of rovers)
        clean_instruction = {}
        for i in range(len(Lines)):
            #1st line is about the land size -> get it => save it and instanciate rover list
            if i == 0:
                land_size = (int(Lines[0][0]), int(Lines[0][2])) #tuple of x and y
                clean_instruction["land_size"] = land_size
                clean_instruction['rovers'] = []
            #other lines -> line is a rover instruction? get it => get this rover attributs from the previous line
            else:
                if Lines[i][0] in instructions_list:
                    rover = {}
                    rover["instructions"] = Lines[i][:-1] #instructions str | [:-1] -> remove backline (/n)
                    rover["pos_x"] = int(Lines[i-1][0]) #position of x from previous line
                    rover["pos_y"] = int(Lines[i-1][2])
                    rover["start_direction"] = Lines[i-1][4]
                    clean_instruction['rovers'].append(rover) #add rover on rovers list
        return clean_instruction

    ## —— RUNNING METHOD
    def run():
        #get instructions and land size from the parser
        instructions = instructions_parser()
        land_size = instructions['land_size']
        rovers = instructions['rovers']
        
        #iterate on rovers list -> create Rover object -> do the instructions => print/return final pos and dir
        for rover in rovers:
            my_rov = Rover(
                pos_x=rover["pos_x"],
                pos_y=rover["pos_y"],
                start_direction=rover["start_direction"],
                land_size=land_size)

            #iterate on instructions string -> do each action (turn or move)
            for instruction in rover['instructions']:
                if instruction == "R" or instruction == "L":
                    my_rov.turn(instruction=instruction)
                elif instruction == "M":
                    my_rov.move()

            print(my_rov.pos_x, my_rov.pos_y, my_rov.current_direction)
    run()
nasa_mission()
