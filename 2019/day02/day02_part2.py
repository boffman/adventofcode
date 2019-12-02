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

def set_noun_and_verb(opcodes, noun, verb):
    opcodes[1] = noun
    opcodes[2] = verb

def calc_output(opcodes):
    ix = 0
    while True:
        cur_opcode = opcodes[ix]
        if cur_opcode == 1:
            ix = handle_opcode_1(ix, opcodes)
        elif cur_opcode == 2:
            ix = handle_opcode_2(ix, opcodes)
        elif cur_opcode == 99:
            break
        else:
            raise Exception("Unknown opcode at position {}: {}".format(ix, cur_opcode))
    return opcodes[0]

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

