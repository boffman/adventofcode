import sys
import threading
from queue import Queue


class MemoryDict(dict):
    def __init__(self, *args):
        dict.__init__(self, args)

    def __missing__(self, key):
        return 0

    def __getitem__(self, key):        
        if key < 0:
           raise Exception("Index out of bounds: {}".format(key))
        return dict.__getitem__(self, key)

    def __setitem__(self, key, value):
        if key < 0:
           raise Exception("Index out of bounds: {}".format(key))
        dict.__setitem__(self, key, value)

class Computer(threading.Thread):
    def __init__(self, opcodes):
        threading.Thread.__init__(self)
        self.opcodes = MemoryDict()
        for ix,val in enumerate(opcodes):
            self.opcodes[ix] = val
        self.relative_base_offset = 0
        self.input = Queue()
        self.output = Queue()
        self.running = False

    def is_running(self):
        return self.running

    def add_input(self, input):
        self.input.put(input)

    def get_output(self):
        return self.output.get()

    def _get_input(self):
        return self.input.get()

    def get_opcode_and_parameter_modes(self, value):
        if value == 99:
            return [value, 0, 0, 0]
        opcode = value % 10
        parm3 = value // 10000
        value -= parm3 * 10000
        parm2 = value // 1000
        value -= parm2 * 1000
        parm1 = value // 100
        return [opcode, parm1, parm2, parm3]

    def get_param(self, param_no, ix, opcodes, parameter_modes):
        param_ix = ix + param_no
        p_mode = parameter_modes[param_no-1]
        if p_mode == 0:
            pos = opcodes[param_ix]
            return opcodes[pos]
        elif p_mode == 1:
            return opcodes[param_ix]
        elif p_mode == 2:
            param = opcodes[param_ix]
            pos = self.relative_base_offset+param
            return opcodes[pos]

    # addition
    def handle_opcode_1(self, ix, opcodes, parameter_modes):
        param1 = self.get_param(1, ix, opcodes, parameter_modes)
        param2 = self.get_param(2, ix, opcodes, parameter_modes)
        dst_pos = opcodes[ix+3]
        if parameter_modes[2] == 2:
            dst_pos = self.relative_base_offset+opcodes[ix+3]
        value = param1 + param2
        opcodes[dst_pos] = value
        return ix + 4

    # multiplication
    def handle_opcode_2(self, ix, opcodes, parameter_modes):
        param1 = self.get_param(1, ix, opcodes, parameter_modes)
        param2 = self.get_param(2, ix, opcodes, parameter_modes)
        dst_pos = opcodes[ix+3]
        if parameter_modes[2] == 2:
            dst_pos = self.relative_base_offset+opcodes[ix+3]
        value = param1 * param2
        opcodes[dst_pos] = value
        return ix + 4

    # input
    def handle_opcode_3(self, ix, opcodes, input_value, parameter_modes):
        dst_pos = opcodes[ix+1]
        if parameter_modes[0] == 2:
            dst_pos = self.relative_base_offset+opcodes[ix+1]
        opcodes[dst_pos] = input_value
        return ix + 2

    # output
    def handle_opcode_4(self, ix, opcodes, parameter_modes):
        param1 = opcodes[ix+1]
        if parameter_modes[0] == 0:
            pos = param1
        elif parameter_modes[0] == 1:
            pos = ix+1
        elif parameter_modes[0] == 2:
            pos = self.relative_base_offset+param1
        value = opcodes[pos]
        return (ix + 2, value)

    # jump-if-true
    def handle_opcode_5(self, ix, opcodes, parameter_modes):
        param1 = self.get_param(1, ix, opcodes, parameter_modes)
        param2 = self.get_param(2, ix, opcodes, parameter_modes)
        if param1 != 0:
            return param2
        return ix + 3

    # jump-if-false
    def handle_opcode_6(self, ix, opcodes, parameter_modes):
        param1 = self.get_param(1, ix, opcodes, parameter_modes)
        param2 = self.get_param(2, ix, opcodes, parameter_modes)
        if param1 == 0:
            return param2
        return ix + 3

    # less than
    def handle_opcode_7(self, ix, opcodes, parameter_modes):
        param1 = self.get_param(1, ix, opcodes, parameter_modes)
        param2 = self.get_param(2, ix, opcodes, parameter_modes)
        dst_pos = opcodes[ix+3]
        if parameter_modes[2] == 2:
            dst_pos = self.relative_base_offset+opcodes[ix+3]

        if param1 < param2:
            opcodes[dst_pos] = 1
        else:
            opcodes[dst_pos] = 0
        return ix + 4

    # equals
    def handle_opcode_8(self, ix, opcodes, parameter_modes):
        param1 = self.get_param(1, ix, opcodes, parameter_modes)
        param2 = self.get_param(2, ix, opcodes, parameter_modes)
        dst_pos = opcodes[ix+3]
        if parameter_modes[2] == 2:
            dst_pos = self.relative_base_offset+opcodes[ix+3]

        if param1 == param2:
            opcodes[dst_pos] = 1
        else:
            opcodes[dst_pos] = 0
        return ix + 4

    # relative base offset
    def handle_opcode_9(self, ix, opcodes, parameter_modes):
        param1 = self.get_param(1, ix, opcodes, parameter_modes)
        self.relative_base_offset += param1
        return ix + 2

    def start(self):
        threading.Thread.start(self)
        self.running = True

    def run(self):
        ix = 0
        cur_opcode = None
        opcodes = self.opcodes
        while cur_opcode != 99:
            values = self.get_opcode_and_parameter_modes(opcodes[ix])
            cur_opcode = values[0]
            parameter_modes = values[1:]
            if cur_opcode == 1:
                ix = self.handle_opcode_1(ix, opcodes, parameter_modes)
            elif cur_opcode == 2:
                ix = self.handle_opcode_2(ix, opcodes, parameter_modes)
            elif cur_opcode == 3:
                input_value = self._get_input()
                ix = self.handle_opcode_3(ix, opcodes, input_value, parameter_modes)
            elif cur_opcode == 4:
                ix, output_value = self.handle_opcode_4(ix, opcodes, parameter_modes)
                self.output.put(output_value)
            elif cur_opcode == 5:
                ix = self.handle_opcode_5(ix, opcodes, parameter_modes)
            elif cur_opcode == 6:
                ix = self.handle_opcode_6(ix, opcodes, parameter_modes)
            elif cur_opcode == 7:
                ix = self.handle_opcode_7(ix, opcodes, parameter_modes)
            elif cur_opcode == 8:
                ix = self.handle_opcode_8(ix, opcodes, parameter_modes)
            elif cur_opcode == 8:
                ix = self.handle_opcode_8(ix, opcodes, parameter_modes)
            elif cur_opcode == 9:
                ix = self.handle_opcode_9(ix, opcodes, parameter_modes)
            elif cur_opcode == 99:
                pass
            else:
                raise Exception("Unknown opcode at position {}: {}".format(ix, cur_opcode))
        self.running = False

class EmergencyHull(dict):
    def __init__(self, *args):
        dict.__init__(self, args)

    def __missing__(self, key):
        return 0

class Robot(object):
    def __init__(self, opcodes):
        self.brain = Computer(opcodes)
        self.hull = EmergencyHull()
        self.direction = "up"
        self.position = (0,0)
        self._paint_hull(1)

    def _paint_hull(self, new_color):
        self.hull[self.position] = new_color

    def _move_forward(self, steps=1):
        x, y = self.position
        if self.direction == "up":
            y -= 1
        elif self.direction == "right":
            x += 1
        elif self.direction == "down":
            y += 1
        elif self.direction == "left":
            x -= 1
        else:
            raise Exception("Invalid direction: {}".format(self.direction))
        self.position = (x,y)

    def _handle_new_color(self, new_color):
        self._paint_hull(new_color)

    def _handle_new_direction(self, new_direction):
        if new_direction == 1:
            if self.direction == "up":
                self.direction = "right"
            elif self.direction == "right":
                self.direction = "down"
            elif self.direction == "down":
                self.direction = "left"
            elif self.direction == "left":
                self.direction = "up"
            else:
                raise Exception("Invalid direction: {}".format(self.direction))
        elif new_direction == 0:
            if self.direction == "up":
                self.direction = "left"
            elif self.direction == "left":
                self.direction = "down"
            elif self.direction == "down":
                self.direction = "right"
            elif self.direction == "right":
                self.direction = "up"
            else:
                raise Exception("Invalid direction: {}".format(self.direction))
        else:
            raise Exception("Unknown direction: {}".format(new_direction))        
        self._move_forward()

    def get_number_of_painted_panels(self):
        return len(self.hull)

    def print_hull(self):
        min_x = None
        min_y = None
        max_x = None
        max_y = None
        for x, y in self.hull.keys():
            if min_x is None or x < min_x:
                min_x = x
            if min_y is None or y < min_y:
                min_y = y
            if max_x is None or x > max_x:
                max_x = x
            if max_y is None or y > max_y:
                max_y = y

        rows = max_y - min_y + 1
        cols = max_x - min_x + 1

        for y in range(rows):
            s = ""
            for x in range(cols):
                color = str(self.hull[(min_x+x,min_y+y)])
                if color == "1":
                    s += "#"
                else:
                    s += "."
            print(s)

    def run(self):
        self.brain.start()

        while self.brain.is_running():
            color = self.hull[self.position]      
            self.brain.add_input(color)
            
            new_color = self.brain.get_output()
            self._handle_new_color(new_color)

            new_direction = self.brain.get_output()
            self._handle_new_direction(new_direction)

opcodes = []
with open("input", "r") as infile:
    for l in infile:
        opcodes = [int(x) for x in l.strip().split(",")]

robot = Robot(opcodes)
robot.run()
print(robot.get_number_of_painted_panels())
robot.print_hull()
