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

    def get_land_size(self):
        line = lines[0].split()
        land_size = (int(line[0]), int(line[1]))
        return land_size

    def get_rovers_positions_list(self):
        positions = []
        for i in range(len(lines)):
            if lines[i][0].isdigit() == True and i != 0:
                line = lines[i].split()
                position = {}
                position["pos_x"], position["pos_y"] = int(line[0]), int(line[1])
                position["start_direction"] = line[2]
                positions.append(position)  # add rover on rovers list
        return positions
    
    def get_rovers_instructions_list(self):
        instructions = []
        for i in range(len(lines)):
            if lines[i][0] in instructions_list and i != 0:
                instruction = lines[i].replace("\n", "")
                instructions.append(instruction)
        return instructions

    def get_rovers(self):
        positions = self.get_rovers_positions_list()
        instructions = self.get_rovers_instructions_list()
        rovers = []
        if len(positions) == len(instructions):
            for i in range(len(positions)):
                rover = {}
                rover["pos_x"] = positions[i]["pos_x"]
                rover["pos_y"] = positions[i]["pos_y"]
                rover["start_direction"] = positions[i]["start_direction"]
                rover["instructions"] = instructions[i]
                rovers.append(rover)
        return rovers

class SuperParser(Parser):
    def __init__(self, file):
        super().__init__(file)

    def convert_path_to_instructions_list(self, start_coord, final_coord, start_direction):
        self.current_direction = start_direction
        x1, y1, x2, y2 = start_coord[0], start_coord[1], final_coord[0], final_coord[1]
        actions, instructions = [], []

        def compute_actions(current_dir, goal_dir, diff_move):
            index_goal_direction = directions_list.index(goal_dir)
            index_current_direction = directions_list.index(current_dir)
            diff_rotation = index_goal_direction - index_current_direction

            actions.append({'turn': diff_rotation, 'move': abs(diff_move)})
            self.current_direction = goal_dir

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

        for action in actions:
            if action['turn'] > 0:
                instructions.extend(['R' for i in range(action['turn'])])
                instructions.extend(['M' for i in range(action['move'])])
            elif action['turn'] < 0:
                instructions.extend(['L' for i in range(abs(action['turn']))])
                instructions.extend(['M' for i in range(action['move'])])
            else:
                instructions.extend(['M' for i in range(action['move'])])

        instructions = "".join(instructions)
        return instructions

    def get_rovers_instructions_list(self):
        instructions = []
        for i in range(len(lines)):
            if 'END' in lines[i] and i != 0:
                line_final = lines[i].split()
                line_start = lines[i-1].split()

                final_coord = (int(line_final[1]), int(line_final[2]))
                start_coord = (int(line_start[0]), int(line_start[1]))
                start_direction = line_start[2]

                instruction = self.convert_path_to_instructions_list(start_coord,final_coord,start_direction)
                instructions.append(instruction)
        return instructions
