import sys

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

def handle_opcode_3(ix, opcodes, input_value):
    dst_pos = opcodes[ix+1]
    opcodes[dst_pos] = input_value
    return ix + 2

def handle_opcode_4(ix, opcodes, parameter_modes):
    param1 = opcodes[ix+1]
    if parameter_modes[0] == 0:
        pos = param1
    else:
        pos = ix+1
    value = opcodes[pos]
    return (ix + 2, value)

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

def calc_output(opcodes):
    ix = 0
    num_4s = 0
    cur_opcode = None
    while cur_opcode != 99:
        values = get_opcode_and_parameter_modes(opcodes[ix])
        cur_opcode = values[0]
        parameter_modes = values[1:]
        if cur_opcode == 1:
            ix = handle_opcode_1(ix, opcodes, parameter_modes)
        elif cur_opcode == 2:
            ix = handle_opcode_2(ix, opcodes, parameter_modes)
        elif cur_opcode == 3:
            print("Enter input value: ")
            input_value = int(sys.stdin.readline().strip())
            ix = handle_opcode_3(ix, opcodes, input_value)
        elif cur_opcode == 4:
            ix, output_value = handle_opcode_4(ix, opcodes, parameter_modes)
            print("Output value: {}".format(output_value))
        elif cur_opcode == 99:
            pass
        else:
            raise Exception("Unknown opcode at position {}: {}".format(ix, cur_opcode))
    return opcodes[0]

with open("input.txt", "r") as infile:
    for l in infile:
        opcodes = [int(x) for x in l.strip().split(",")]
        calc_output(opcodes)
