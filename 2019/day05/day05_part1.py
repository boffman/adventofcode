import sys

def handle_opcode_1(ix, opcodes):
    num1_pos = opcodes[ix+1]
    num2_pos = opcodes[ix+2]
    dst_pos = opcodes[ix+3]
    opcodes[dst_pos] = opcodes[num1_pos] + opcodes[num2_pos]
    return ix + 4

def handle_opcode_2(ix, opcodes):
    num1_pos = opcodes[ix+1]
    num2_pos = opcodes[ix+2]
    dst_pos = opcodes[ix+3]
    opcodes[dst_pos] = opcodes[num1_pos] * opcodes[num2_pos]
    return ix + 4

def handle_opcode_3(ix, opcodes, input_value):
    dst_pos = opcodes[ix+1]
    opcodes[dst_pos] = input_value
    return ix + 1

def handle_opcode_4(ix, opcodes):
    output_value = opcodes[ix+1]
    return (ix + 1, output_value)

def set_noun_and_verb(opcodes, noun, verb):
    opcodes[1] = noun
    opcodes[2] = verb

def calc_output(opcodes):
    ix = 0
    while True:
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
            ix = handle_opcode_3(ix, opcodes, input_value, parameter_modes)
        elif cur_opcode == 4:
            ix, output_value = handle_opcode_4(ix, opcodes, parameter_modes)
        elif cur_opcode == 99:
            break
        else:
            raise Exception("Unknown opcode at position {}: {}".format(ix, cur_opcode))
    return opcodes[0]

def get_opcode_and_parameter_modes(value):
    opcode = value % 10
    parm3 = value // 10000
    value -= parm3 * 10000
    parm2 = value // 1000
    value -= parm2 * 1000
    parm1 = value // 100
    return [opcode, parm1, parm2, parm3]

print(get_opcode_and_parameter_modes(1002))
sys.exit(0)

start_opcodes = None
with open("input.txt", "r") as infile:
    for l in infile:
        start_opcodes = [int(x) for x in l.strip().split(",")]

target_output = 19690720
noun = 0
verb = 0
output = 0
found_target_output = False
while not found_target_output:
    opcodes = start_opcodes.copy()
    set_noun_and_verb(opcodes, noun, verb)
    output = calc_output(opcodes)
    if output == target_output:
        found_target_output = True
    else:
        verb += 1
        if verb > 99:
            noun += 1
            verb = 0
            if noun > 99:
                raise Exception("Unable to find target output")

answer = 100 * noun + verb
print("Answer: {} (noun: {}, verb: {})".format(answer,noun,verb))

