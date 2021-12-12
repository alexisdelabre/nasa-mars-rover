directions_list = ["N", "E", "S", "W"]

class Rover():
    ## —— CLASS INIT
    def __init__(self, land_size, pos_x=0, pos_y=0, start_direction="N"):
        self.land_size = land_size
        self.pos_x, self.pos_y = pos_x, pos_y
        self.current_direction = start_direction

    ## —— MOVE METHOD
    def move(self):
        #init frontier | min = 0 and max = x,y of the canva size
        x_min, y_min, x_max, y_max = 0, 0, self.land_size[0], self.land_size[1]

        #check the rover current direction -> then if move is legal (in the canva) => move the rover
        if self.current_direction == "N" and self.pos_y + 1 <= y_max:
                self.pos_y += 1  # make the rover move
        elif self.current_direction == "E" and self.pos_x + 1 <= x_max:
                self.pos_x += 1
        elif self.current_direction == "S" and self.pos_y - 1 >= y_min:
                self.pos_y -= 1
        elif self.current_direction == "W" and self.pos_x - 1 >= x_min:
                self.pos_x -= 1

    ## —— TURN METHOD
    def turn(self, instruction):
        #current direction in dir list? yes -> get index of this direction in dir list
        if self.current_direction in directions_list:
            index = directions_list.index(self.current_direction)

        #instruction R -> increase index => turn clock side | opposite behavior for L
        if instruction == "R":
            index += 1
        elif instruction == "L":
            index -= 1

        #if current direction is W -> new index is 4 (max in range list is 3) -> reset to 0 => N (right after W)
        if index == len(directions_list):
            index = 0

        #new current direction
        self.current_direction = directions_list[index]
