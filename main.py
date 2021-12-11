from Mission import *

def mission():
    file_path = 'instructions/basic_instructions.txt'
    obj = Mission(file_path)
    obj.mission()
    print(f'————————— Mission results: {obj.get_final_position()}\n')

def super_mission():
    file_path = 'instructions/adv_instructions.txt'
    obj = SuperMission(file_path)
    obj.mission()
    print(f'————————— Super mission results: {obj.get_final_position()}\n')

if __name__ == "__main__":
    mission()
    super_mission()
