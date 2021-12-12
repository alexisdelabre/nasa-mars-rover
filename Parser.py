from typing import List

instructions_list = ["M", "L", "R"]
directions_list = ["N", "E", "S", "W"]

class Parser():
    ## —— CLASS INIT
    def __init__(self, file):
        self.file = file
        
        #open file and separate lines
        my_file = open(self.file, 'r')
        global lines
        lines = my_file.readlines()

    ## —— GET LAND SIZE FROM 1ST LINE (use split to get both x and y)
    def get_land_size(self):
        line = lines[0].split()
        land_size = (int(line[0]), int(line[1]))
        return land_size

    ## —— GET EACH ROVER POSITION -> AS A TUPLE (x, y, direction) => LIST
    def get_rovers_positions_list(self) -> List:
        positions = []
        for i in range(len(lines)):
            if lines[i][0].isdigit() == True and i != 0:
                line = lines[i].split()
                position = {}
                position["pos_x"], position["pos_y"] = int(line[0]), int(line[1])
                position["start_direction"] = line[2]
                positions.append(position)  # add rover on rovers list
        return positions
    
    ## —— GET EACH ROVER INSTRUCTION STRING -> "LMLMLMLMM" => LIST
    def get_rovers_instructions_list(self) -> List:
        instructions = []
        for i in range(len(lines)):
            if lines[i][0] in instructions_list and i != 0:
                instruction = lines[i].replace("\n", "")
                instructions.append(instruction)
        return instructions

    ## —— COMPILE INFOS AND RETURN LIST OF ROVERS WITH POSITION AND INSTRUCTIONS FOR EACH => LIST
    def get_rovers(self) -> List:
        positions = self.get_rovers_positions_list()
        instructions = self.get_rovers_instructions_list()
        rovers = []
        if len(positions) == len(instructions):
            for i in range(len(positions)):
                rover = {}
                rover["pos_x"], rover["pos_y"] = positions[i]["pos_x"], positions[i]["pos_y"]
                rover["start_direction"] = positions[i]["start_direction"]
                rover["instructions"] = instructions[i]
                rovers.append(rover)
        return rovers

## —— EXTEND PARSER CLASS TO HANDLE DIFFERENT TYPE OF MISSION FILE
class SuperParser(Parser):
    ## —— CLASS INIT
    def __init__(self, file):
        super().__init__(file)

    ## —— CONVERT PATH TO FINAL POSITIONS INTO INSTRUCTIONS ("LMLMRM") USE BY ROVER TO EXECUTE MISSION
    def convert_path_to_instructions_list(self, start_coord, final_coord, start_direction):
        self.current_direction = start_direction
        x1, y1, x2, y2 = start_coord[0], start_coord[1], final_coord[0], final_coord[1]
        actions, instructions = [], []

        ## —— GET CURRENT DIR, GOAL DIR AND DISTANCE TO GOAL TO COMPUTE ACTION TO DO
        def compute_actions(current_dir, goal_dir, diff_move):
            index_goal_direction = directions_list.index(goal_dir)
            index_current_direction = directions_list.index(current_dir)

            #diff rotation -> number of turn required -> (diff > 0 = turn right | < 0 = turn left)
            diff_rotation = index_goal_direction - index_current_direction

            #add to actions list a dictionnary with number of turn moves and moving distance required
            actions.append({'turn': diff_rotation, 'move': abs(diff_move)})

            #update new direction
            self.current_direction = goal_dir

        ## —— IF x1 OR y1 DIFFERENT TO FINAL POSITION TUPLE (x2, y2) -> COMPUTE TURNS AND MOVES REQUIRED
        if x2 != x1:
            diff_x = x2 - x1
            if diff_x > 0:
                compute_actions(self.current_direction, "E", diff_x)
            elif diff_x < 0:
                compute_actions(self.current_direction, "W", diff_x)
        if y2 != y1:
            diff_y = y2 - y1
            if diff_y > 0:
                compute_actions(self.current_direction, "N", diff_y)
            elif diff_y < 0:
                compute_actions(self.current_direction, "S", diff_y)

        ## —— EACH ACTION IS COMPOSE OF i TURN THEN j MOVES -> ADD RIGHT LETTER TO INSTRUCTIONS LIST
        for action in actions:
            #turn = positif integer -> turn i times to the right -> ex: i = 2 and dir = 'N' ===> new dir = 'S'
            if action['turn'] > 0:
                instructions.extend(['R' for i in range(action['turn'])])
                instructions.extend(['M' for j in range(action['move'])])
            #turn = negatif integer -> turn i times to the left
            elif action['turn'] < 0:
                instructions.extend(['L' for i in range(abs(action['turn']))])
                instructions.extend(['M' for j in range(action['move'])])
            #no need to turn -> right direction -> just move forward
            else:
                instructions.extend(['M' for j in range(action['move'])])

        instructions = "".join(instructions)
        return instructions

    ## —— OVERWRITE TO HANDLE DIFFERENT BEHAVIOR => CONVERTION OF FINAL POSITION INTO MOVES INSTRUCTIONS
    def get_rovers_instructions_list(self) -> List:
        instructions = []
        for i in range(len(lines)):
            if 'END' in lines[i] and i != 0:
                #split line to get elements from start and final positions lines
                line_final = lines[i].split()
                line_start = lines[i-1].split()

                #get start and final coord + start direction -> path ready to be converted into instructions
                final_coord, start_coord = (int(line_final[1]), int(line_final[2])), (int(line_start[0]), int(line_start[1]))
                start_direction = line_start[2]

                #convert path to instructions and add to rovers instuctions list
                instruction = self.convert_path_to_instructions_list(start_coord,final_coord,start_direction)
                instructions.append(instruction)
        return instructions
