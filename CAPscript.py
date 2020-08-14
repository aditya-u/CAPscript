import sys
import re
def listify(code):
    if type(code) == list:
        return code
    else:
        code = remove_comments(code)
        return re.findall('...?', code)
def interpreter(code):
    global mem, cell, rem_input
    additive = [-255,1]
    slider = []
    vc = listify(code)
    code_list = vc
    after_loop = []
    if code_list:
        for index, Instruct in enumerate(code_list):
            current_value = mem[cell]
            if Instruct == 'INC':
                mem[cell] += additive[current_value < 255]
            elif Instruct == 'DEC':
                mem[cell] -= additive[current_value > 0]
            elif Instruct == "DBL":
                mem[cell] = (current_value * 2) & 255
            elif Instruct == "HAL":
                mem[cell] >>= 1
            elif Instruct == "PRC":
                print(chr(mem[cell]), end = '')
            elif Instruct == "CLR":
                mem[cell] = 0
            elif Instruct == "SQR":
                mem[cell] = (current_value ** 2) & 255
            elif Instruct == "CUB":
                mem[cell] = (current_value ** 3) & 255
            elif Instruct == "PRI":
                print(str(current_value), end = '')
            elif Instruct == "INI":
                new_value = int(input())
                if new_value < 0 or new_value >= 255:
                    error("Out Of Range (0, 255)")
                    break
                mem[cell] = new_value
            elif Instruct == "RIG":
                cell = (cell + 1) & 255
            elif Instruct == "LEF":
                cell = (cell - 1) & 255
            elif Instruct == "LOO":
                later_code = code_list[index:]
                contents = find_loop(later_code)
                after_loop = code_list[ (index + len(contents) + 2): ]
                while mem[cell] > 0:
                    interpreter(contents)
                break
            elif Instruct == "OOP":
                pass
            elif Instruct == "INP":
                if rem_input:
                    new_value = ord(rem_input) if len(rem_input) == 1 else ord(rem_input[0])
                    if len(rem_input) > 1:
                        rem_input = rem_input[1:]
                    else:
                        rem_input = ""
                    if 0 < new_value < 255:
                        mem[cell] = new_value
                    else:
                        error("Out Of Range (0,255)")
                else:
                    val = input()
                    new_value = ord(val) if len(val) == 1 else ord(val[0])
                    if len(val) > 1:
                        rem_input = val[1:]
                    if 0 < new_value < 255:
                        mem[cell] = new_value
                    else:
                        error("Out Of Range (0,255)")
            else:
                error("{} Not valid .caps code".format(Instruct))
        if after_loop:
            interpreter(after_loop)
    else:
        error("Code has unintended spacing.")
def find_loop(code):
    index = 0
    counter = 0
    while True:
        find = code[counter]
        if find == "LOO":
            index+=1
        elif find == "OOP":
            index-=1
        if index == 0:
            return code[1:counter]
        counter+=1


def remove_comments(code):
    remove_lower = lambda text: re.sub('[a-z]', '', text)
    code = remove_lower(code)
    for findings in  ignored_chars:
        code = code.replace(findings, "")
    return code

def error(message):
    print("\n Error :: " + message)


def openfile(filename):
    data = open(filename, "r")  
    data = data.read()          

    interpreter(data)


def run():
    global values, cell
    if len(sys.argv) == 1:
        try:
            while True:
                mem = [0]*256
                cell = 0

                interpreter(input("\n>>> "))
        except:
            error("Unknown Error")
    else:
        try:
            current_file = sys.argv[1]
            openfile(current_file)
        except:
            error("Unknown Error")
mem = [0]*256 
cell = 0
rem_input = ""
ignored_chars = [" ", "\t", "\n", chr(13), ";"]
print("CAPscript 1.0.0 \n> ")
run()
