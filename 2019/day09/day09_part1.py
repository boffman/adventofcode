import sys

class Computer(object):
    def __init__(self, opcodes):
        self.opcodes = opcodes
        self.relative_code_base = 0

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
            pos = opcodes[ix+param_no]
            return opcodes[pos]
        elif p_mode == 1:
            return opcodes[ix+param_no]
        elif p_mode == 2:
            pos = opcodes[self.relative_code_base+ix+param_no]
            return opcodes[pos]

    # addition
    def handle_opcode_1(self, ix, opcodes, parameter_modes):
        param1 = self.get_param(1, ix, opcodes, parameter_modes)
        param2 = self.get_param(2, ix, opcodes, parameter_modes)
        dst_pos = opcodes[ix+3]
        value = param1 + param2
        opcodes[dst_pos] = value
        return ix + 4

    # multiplication
    def handle_opcode_2(self, ix, opcodes, parameter_modes):
        param1 = self.get_param(1, ix, opcodes, parameter_modes)
        param2 = self.get_param(2, ix, opcodes, parameter_modes)
        dst_pos = opcodes[ix+3]
        value = param1 * param2
        opcodes[dst_pos] = value
        return ix + 4

    # input
    def handle_opcode_3(self, ix, opcodes, input_value):
        dst_pos = opcodes[ix+1]
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
            pos = self.relative_code_base+ix+1
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
        if param1 < param2:
            opcodes[dst_pos] = 1
        else:
            opcodes[dst_pos] = 0
        return ix + 4

    # equals
    def handle_opcode_8(self, ix, opcodes, parameter_modes):
        param1 = self.get_param(1, ix, opcodes, parameter_modes)
        param2 = self.get_param(2, ix, opcodes, parameter_modes)
        if param1 == param2:
            opcodes[dst_pos] = 1
        else:
            opcodes[dst_pos] = 0
        return ix + 4

    # relative base offset
    def handle_opcode_9(self, ix, opcodes):
        param1 = opcodes[ix+1]
        self.relative_code_base += param1
        return ix + 2

    def compute(input=None):
        ix = 0
        num_4s = 0
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
                input_value = None
                if not input is None:
                    input_value = input
                else:
                    print("Enter input value: ")            
                    input_value = int(sys.stdin.readline().strip())
                ix = handle_opcode_3(ix, opcodes, input_value)
            elif cur_opcode == 4:
                ix, output_value = handle_opcode_4(ix, opcodes, parameter_modes)
                print("Output value: {}".format(output_value))
                return output_value
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
            elif cur_opcode == 8:
                ix = self.handle_opcode_9(ix, opcodes)
            elif cur_opcode == 99:
                pass
            else:
                raise Exception("Unknown opcode at position {}: {}".format(ix, cur_opcode))
        return None


with open("input.txt", "r") as infile:
    for l in infile:
        opcodes = [int(x) for x in l.strip().split(",")]
        calc_output(opcodes)
