import threading
from queue import Queue
from collections import Counter
from graphics import *
import time

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
        self.waiting_for_input = False

    def poke(self, address, value):
        self.opcodes[address] = value

    def is_running(self):
        return self.running

    def add_input(self, input):
        self.input.put(input)

    def is_waiting_for_input(self):
        return self.waiting_for_input

    def get_output(self):
        if self.running:
            return self.output.get()
        else:
            if self.output.empty():
                return None
            else:
                return self.output.get(block=False)

    def has_output(self):
        return self.output.qsize() > 0 #not self.output.empty()

    def has_input(self):
        return self.input.qsize() > 0

    def _get_input(self):
        if not self.has_input():
            self.waiting_for_input = True
        i = self.input.get()
        self.waiting_for_input = False
        return i


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

def print_screen(screen, xres, yres):
    for y in range(yres+1):
        l = []
        for x in range(xres+1):
            if (x,y) in screen.keys():
                t = screen[(x,y)]
                if t == 0:
                    l.append(" ")
                elif t == 1:
                    l.append("█")
                elif t == 2:
                    l.append("░")
                elif t == 3:
                    l.append("▔")
                elif t == 4:
                    l.append("●")
            else:
                l.append(" ")
        print("".join(l))


def draw_screen(win, screen, xres, yres, scale):
    for y in range(yres+1):
        l = []
        for x in range(xres+1):
            if (x,y) in screen.keys():
                t = screen[(x,y)]
                p1 = Point(x*scale, y*scale)
                p2 = Point(x+scale, y+scale)
                pc = Point(x+scale//2, y+scale//2)
                if t == 0:
                    r = Rectangle(p1, p2)
                    r.setOutline('white')
                    r.setFill('white')
                    r.draw(win)
                elif t == 1:
                    r = Rectangle(p1, p2)
                    r.setOutline('black')
                    r.setFill('brown')
                    r.draw(win)
                elif t == 2:
                    r = Rectangle(p1, p2)
                    r.setOutline('black')
                    r.setFill('yellow')
                    r.draw(win)
                elif t == 3:
                    r = Rectangle(p1, p2)
                    r.setOutline('black')
                    r.setFill('black')
                    r.draw(win)
                elif t == 4:
                    c = Circle(pc, scale)
                    c.setOutline('black')
                    c.setFill('red')
                    c.draw(win)
            else:
                r = Rectangle(p1, p2)
                r.setOutline('white')
                r.setFill('white')
                r.draw(win)

opcodes = []
with open("input", "r") as infile:
    for l in infile:
        opcodes = [int(x) for x in l.strip().split(",")]

game = Computer(opcodes)
game.poke(0, 2)

game.start()

# win = GraphWin()
# pt = Point(100, 50)
# pt.draw(win)

#input_data = [int(x.strip()) for x in sys.argv[1].split(",")]

screen = {}
xres = 0
yres = 0
score = 0
tile_pos = None
ball_pos = None
started = False
tile = None
game_started = False
steer_direction = None
input_data = []
with open("jinput.txt", "r") as jfile:
    for l in jfile:
        for x in l.split(","):
            if len(x) > 0:
                input_data.append(int(x))
xtra_input = []
# for i in input_data:
#     game.add_input(i)

while game.is_running() or game.has_output():

    while game.has_output():
        x = game.get_output()
        y = game.get_output()
        tile = game.get_output()
        if x == -1 and y == 0:
            score = tile
        elif tile == 3:
            tile_pos = (x,y)
        elif tile == 4:
            if ball_pos and (x != ball_pos[0] or y != ball_pos[1]):
                game_started = True
            ball_pos = (x,y)

        screen[(x,y)] = tile
        xres = max([x, xres])
        yres = max([y, yres])
    #draw_screen(win, screen, xres, yres, 10)
    print_screen(screen, xres, yres)
    if steer_direction is not None:
        print(f"score: {score}   steering: {steer_direction}  ball: {ball_pos}  pad: {tile_pos}  input q: {game.input.qsize()}")
    
    qsize = game.input.qsize()
    oqsize = game.output.qsize()
    print(f"score: {score}   ball: {ball_pos}  pad: {tile_pos}  input q: {qsize}  output q: {oqsize}")

    if game_started:
        time.sleep(0.01)

    if qsize == 0 and game.is_waiting_for_input():
        game.add_input(input_data.pop(0))
        # print("INPUT: ")
        # ival = sys.stdin.readline().strip()
        # if ival == "":
        #     i = 0
        # else:
        #     i = int(ival)
        # #i = 0
        # game.add_input(i)
        # xtra_input.append(i)
        # with open("jinput.txt", "a") as jfile:
        #     jfile.write("," + str(i))

    # if game.is_waiting_for_input() and ball_pos is not None and tile_pos is not None:
    #     game_started = True
    #     if ball_pos[0] < tile_pos[0]:
    #         print("STEERING LEFT (-1)")
    #         steer_direction = -1
    #     elif ball_pos[0] > tile_pos[0]:
    #         print("STEERING RIGHT (1)")
    #         steer_direction = 1
    #     else:
    #         print("STEERING NEUTRAL (0)")
    #         steer_direction = 0
    #     game.add_input(steer_direction)

#        game.add_input(0)



num_blocks = len(list(filter(lambda x: x == 2, screen.values())))
print(f"Num blocks: {num_blocks}")
