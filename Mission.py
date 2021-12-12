from Parser import Parser, SuperParser
from Rover import Rover

class Mission():
    ## —— CLASS INIT
    def __init__(self, file_path):
        self.land_size = Parser(file_path).get_land_size()
        self.rovers = Parser(file_path).get_rovers()
        self.final_positions = []

    def follow_instructions(self, rover, instructions):
        #iterate on instructions string -> do each action (turn or move)
        for instruction in instructions:
            if instruction == "R" or instruction == "L":
                rover.turn(instruction=instruction)
            elif instruction == "M":
                rover.move()

        #add final position of the rover in results
        self.final_positions.append([(rover.pos_x, rover.pos_y), rover.current_direction])

    def mission(self):
        #iterate on rovers list -> create Rover object -> call follow instructions function
        for rover in self.rovers:
            instructions = rover['instructions']
            print(rover)
            my_rov = Rover(
                pos_x=rover["pos_x"],
                pos_y=rover["pos_y"],
                start_direction=rover["start_direction"],
                land_size=self.land_size)
            self.follow_instructions(my_rov, instructions)

    def get_final_position(self):
        return self.final_positions

## —— EXTEND MISSION CLASS => SUPER PARSER TO USE ADVANCED MISSION FILE
class SuperMission(Mission):
    ## —— CLASS INIT
    def __init__(self, file_path):
        super().__init__(file_path)
        self.land_size = SuperParser(file_path).get_land_size()
        self.rovers = SuperParser(file_path).get_rovers()
