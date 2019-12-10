import sys
import itertools
import threading
from queue import Queue

# addition
def handle_opcode_1(ix, opcodes, parameter_modes):
    param1 = opcodes[ix+1]
    param2 = opcodes[ix+2]
    dst_pos = opcodes[ix+3]
    if parameter_modes[0] == 0:
        param1 = opcodes[param1]
    if parameter_modes[1] == 0:
        param2 = opcodes[param2]
    value = param1 + param2
    opcodes[dst_pos] = value
    return ix + 4

# multiplication
def handle_opcode_2(ix, opcodes, parameter_modes):
    param1 = opcodes[ix+1]
    param2 = opcodes[ix+2]
    dst_pos = opcodes[ix+3]
    if parameter_modes[0] == 0:
        param1 = opcodes[param1]
    if parameter_modes[1] == 0:
        param2 = opcodes[param2]
    value = param1 * param2
    opcodes[dst_pos] = value
    return ix + 4

# input
def handle_opcode_3(ix, opcodes, input_value):
    dst_pos = opcodes[ix+1]
    opcodes[dst_pos] = input_value
    return ix + 2

# output
def handle_opcode_4(ix, opcodes, parameter_modes):
    param1 = opcodes[ix+1]
    if parameter_modes[0] == 0:
        pos = param1
    else:
        pos = ix+1
    value = opcodes[pos]
    return (ix + 2, value)

# jump-if-true
def handle_opcode_5(ix, opcodes, parameter_modes):
    param1 = opcodes[ix+1]
    param2 = opcodes[ix+2]
    if parameter_modes[0] == 0:
        param1 = opcodes[param1]
    if parameter_modes[1] == 0:
        param2 = opcodes[param2]
    if param1 != 0:
        return param2
    return ix + 3

# jump-if-false
def handle_opcode_6(ix, opcodes, parameter_modes):
    param1 = opcodes[ix+1]
    param2 = opcodes[ix+2]
    if parameter_modes[0] == 0:
        param1 = opcodes[param1]
    if parameter_modes[1] == 0:
        param2 = opcodes[param2]
    if param1 == 0:
        return param2
    return ix + 3

# less than
def handle_opcode_7(ix, opcodes, parameter_modes):
    param1 = opcodes[ix+1]
    param2 = opcodes[ix+2]
    dst_pos = opcodes[ix+3]
    if parameter_modes[0] == 0:
        param1 = opcodes[param1]
    if parameter_modes[1] == 0:
        param2 = opcodes[param2]
    if param1 < param2:
        opcodes[dst_pos] = 1
    else:
        opcodes[dst_pos] = 0
    return ix + 4

# equals
def handle_opcode_8(ix, opcodes, parameter_modes):
    param1 = opcodes[ix+1]
    param2 = opcodes[ix+2]
    dst_pos = opcodes[ix+3]
    if parameter_modes[0] == 0:
        param1 = opcodes[param1]
    if parameter_modes[1] == 0:
        param2 = opcodes[param2]
    if param1 == param2:
        opcodes[dst_pos] = 1
    else:
        opcodes[dst_pos] = 0
    return ix + 4

def get_opcode_and_parameter_modes(value):
    if value == 99:
        return [value, 0, 0, 0]
    opcode = value % 10
    parm3 = value // 10000
    value -= parm3 * 10000
    parm2 = value // 1000
    value -= parm2 * 1000
    parm1 = value // 100
    return [opcode, parm1, parm2, parm3]

class Amp(threading.Thread):
    def __init__(self, opcodes):
        threading.Thread.__init__(self)
        self.ix = 0
        self.opcodes = opcodes
        self.input = Queue()
        self.output_amp = None
        self.last_output = None

    def add_input(self, input):
        self.input.put(input)

    def connect_output_to(self, amp):
        self.output_amp = amp

    def _get_input(self):
        return self.input.get()

    def run(self):
        ix = 0
        cur_opcode = None
        opcodes = self.opcodes
        while cur_opcode != 99:
            values = get_opcode_and_parameter_modes(opcodes[ix])
            cur_opcode = values[0]
            parameter_modes = values[1:]
            if cur_opcode == 1:
                ix = handle_opcode_1(ix, opcodes, parameter_modes)
            elif cur_opcode == 2:
                ix = handle_opcode_2(ix, opcodes, parameter_modes)
            elif cur_opcode == 3:
                input_value = self._get_input()
                ix = handle_opcode_3(ix, opcodes, input_value)
            elif cur_opcode == 4:
                ix, output_value = handle_opcode_4(ix, opcodes, parameter_modes)
                self.output_amp.add_input(output_value)
                self.last_output = output_value
            elif cur_opcode == 5:
                ix = handle_opcode_5(ix, opcodes, parameter_modes)
            elif cur_opcode == 6:
                ix = handle_opcode_6(ix, opcodes, parameter_modes)
            elif cur_opcode == 7:
                ix = handle_opcode_7(ix, opcodes, parameter_modes)
            elif cur_opcode == 8:
                ix = handle_opcode_8(ix, opcodes, parameter_modes)
            elif cur_opcode == 99:
                pass
            else:
                raise Exception("Unknown opcode at position {}: {}".format(ix, cur_opcode))

opcodes_orig = None
with open("input.txt", "r") as infile:
    for l in infile:
        opcodes_orig = [int(x) for x in l.strip().split(",")]


#opcodes_orig = [3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5]
#opcodes_orig = [3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10]

output = 0
max_output = None
done = False
max_phase_setting = None
for phase_setting in itertools.permutations(range(5, 10)):
    print("Phase setting: {}".format(phase_setting))
    output = 0
    completed = False

    # Create and connect amps
    amps = []
    for amp_ix in range(5):
        amps.append(Amp(opcodes_orig.copy()))
        if amp_ix > 0:
            amps[amp_ix-1].connect_output_to(amps[amp_ix])
        amps[amp_ix].add_input(phase_setting[amp_ix])        
    amps[4].connect_output_to(amps[0])
    amps[0].add_input(0)

    for amp_ix in range(5):
        amps[amp_ix].start()

    amps[4].join()

    last_output = amps[4].last_output
    print("Phase completed, output = {}".format(last_output))

    if max_output is None or last_output > max_output:
        max_output = last_output
        max_phase_setting = list(phase_setting)
            

print("Done, max output {} for phase setting {}".format(max_output, max_phase_setting))
