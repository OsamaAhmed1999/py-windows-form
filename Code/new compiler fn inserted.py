import re

set = []
s = 0
token = {
        'cp': '',
        'vp': '',
        'line': 0
    }
def Lexical_Analyzer():

    def token_set(cp , vp , line):
        global s
        set.append([])
        set[s].append(cp)       # 0---class part
        set[s].append(vp)       # 1---value part
        set[s].append(line)     # 2---line
        s += 1

    def WriteInFile():
        with open("token.txt", "a") as file:
            file.write(str(token)+"\n")

    def isStrConst(text):
        string_const = re.match("([0-9]*[a-zA-Z]*[-+@*=%\\\!~#&|_<>,./?;:\'\"]$)", text)
        if string_const:
            return True
        else:
            return False


    def isID(text):
        identifier = re.match("([a-zA-Z]+$)|([a-zA-Z]+_[a-zA-Z]+$)", text)
        if identifier:
            return True
        else:
            return False


    def isChar(text):
        char_const = re.match("(\\\[bnort]$|[bnort]$)|(\\\[\'\"\\\]$)|([-+@*=%!~#&|_<>,./?;:]$)", text)
        if char_const:
            return True
        else:
            return False


    def isInt(text):
        int_const = re.match("([+|-][0-9]+$)|([0-9]+$)", text)
        if int_const:
            return True
        else:
            return False


    def isFloat(text):
        float_const = re.match("([+|-][0-9]*\\.[0-9]+$)|([0-9]*\\.[0-9]+$)", text)
        if float_const:
            return True
        else:
            return False


    def isOpr(text):
        pm = {"+", "-"}
        ndm = {"*", "/", "%"}
        uop = {"++", "--", "!"}
        aop = {"=", "+=", "-=", "*=", "/="}
        lop = {'&&': '&&', '||': '||', '!': '||'}
        rop = {"<", ">", "<=", ">=", "==", "!="}
        # sop = {"<<", ">>"}
        if text in pm:
            return "PM"
        elif text in ndm:
            return "MDM"
        elif text in uop:
            return "UOP"
        elif text in aop:
            return "AOP"
        # elif text in sop:
        #     return "SOP"
        elif text in rop:
            return "ROP"
        elif text in lop:
            for key in lop:
                if key == text:
                    return lop[key]
        else:
            return False


    def isPunc(text):
        pun = {
            '.': '.',
            ',': ',',
            '{': '{',
            '}': '}',
            '(': '(',
            ')': ')',
            '[': '[',
            ']': ']',
            ';': ';',
            ':': ':',
            '::': '::',
            '->': '->',
        }
        for key in pun:
            if key == text:
                return pun[key]

        return None


    def isKeyWord(text):
        kw = {
            'void': 'void',
            'int': 'DT',
            'float': 'DT',
            'char': 'DT',
            'string': 'DT',
            'variable': 'DT',
            'bool': 'DT',
            'for': 'for',
            'while': 'while',
            'if': 'if',
            'else': 'else',
            'switch': 'switch',
            'case': 'case',
            'break': 'break',
            'continue': 'continue',
            'default': 'default',
            'return': 'return',
            'true': 'bool_const',
            'false': 'bool_const',
            'class': 'class',
            'public': 'AM',
            'private': 'AM',
            'protected':  'AM',
            'this': 'this',
            'base': 'base',
            'array': 'array',
            'list': 'DT',
            'virtual': 'virtual',
            'const': 'const',
            'static': 'static',
            'def': 'def'
        }
        for key in kw:
            if key == text:
                return kw[key]

        return None


    def word_break(word, line):
        if isID(word):
            kw = isKeyWord(word)
            if kw is not None:
                token['cp'] = kw
                token['vp'] = word
                token['line'] = line
                token_set(kw, word, line)
                WriteInFile()
            else:
                token['cp'] = "ID"
                token['vp'] = word
                token['line'] = line
                token_set("ID", word, line)
                WriteInFile()
        elif isInt(word):
            token['cp'] = "int_const"
            token['vp'] = word
            token['line'] = line
            token_set("int_const", word, line)
            WriteInFile()
        elif isFloat(word):
            token['cp'] = "float const"
            token['vp'] = word
            token['line'] = line
            token_set("float_const", word, line)
            WriteInFile()
        elif isPunc(word):
            value = isPunc(word)
            token['cp'] = value
            token['vp'] = word
            token['line'] = line
            token_set(value, word, line)
            WriteInFile()
        elif isOpr(word):
            value = isOpr(word)
            if value is not None:
                token['cp'] = value
                token['vp'] = word
                token['line'] = line
                token_set(value, word, line)
                WriteInFile()
        else:
            token['cp'] = "Lexical Error"
            token['vp'] = word
            token['line'] = line
            token_set("lexical_error", word, line)
            WriteInFile()


    def opr(text):
        op = {'+', '-', '*', '/', '=', ':', '<', '>', "%", '!', '&', '|'}
        if text in op:
            return True
        else:
            return False


    def id(text):
        identifier = re.match("([a-zA-Z]+$)|_$|[0-9]$", text)
        if identifier:
            return True
        else:
            return False


    def digit(text):
        int_const = re.match("([0-9]$)", text)
        if int_const:
            return True
        else:
            return False


    def pun(text):
        pun = {".", ",", ":", ";", "(", ")", "{", "}", "[", "]"}
        if text in pun:
            return True
        else:
            return False

    def chr(text):
        char_const = {"\\", "\r", "\b", "\t", "@"}
        if text in char_const:
            return True
        else:
            return False




    comment = ''
    char = ''
    string = False
    point = False
    wb = False
    word = ''
    line = 1
    with open("file.txt", "r") as file:
        while True:
            if wb is False:
                char = file.read(1)  # read by character

            if digit(char):
                while True:
                    word = word + char
                    char = file.read(1)
                    if char is "." and point is False:
                        point = True
                    elif char is id(char):
                        word = word + char
                    elif not digit(char) and not id(char):
                        word_break(word, line)
                        word = ''
                        wb = True
                        point = False
                        break
            elif id(char):
                while True:
                    word = word + char
                    char = file.read(1)
                    if not id(char):
                        word_break(word, line)
                        word = ''
                        wb = True
                        break
            elif char is "#":
                while char is not '\n':
                    char = file.read(1)
                    if(char is ''):
                        break
                wb = False
            elif opr(char):
                word = word + char
                char = file.read(1)
                if word == "-" and char == ">":
                    word = word + char
                    word_break(word, line)
                    word = ''
                    wb = False
                elif not opr(char):
                    word_break(word, line)
                    word = ''
                    wb = True
                elif char == word or char == "=":
                    word = word + char
                    word_break(word, line)
                    word = ''
                    wb = False
            elif pun(char):
                if char is ".":
                    word = word + char
                    char = file.read(1)
                    if digit(char):
                        word = word + char
                        while True:
                            char = file.read(1)
                            if digit(char) or id(char):
                                word = word + char
                            else:
                                word_break(word,  line)
                                word = ''
                                wb = True
                                break
                    else:
                        word_break(word, line)
                        word = ''
                        wb = True
                else:
                    word = word + char
                    word_break(word, line)
                    word = ''
                    wb = False

            elif char is "\"":
                while True:
                    char = file.read(1)
                    if char is '\"':
                        token['cp'] = "string_const"
                        token['vp'] = word
                        token['line'] = line
                        token_set("string_const", word, line)
                        WriteInFile()
                        word = ''
                        wb = False
                        break
                    elif char is '\n' or char is '':
                        token['cp'] = "lexical_error"
                        token['vp'] = word
                        token['line'] = line
                        token_set("lexical_error", word, line)
                        WriteInFile()
                        word = ''
                        wb = False
                        string = True
                        break
                    else:
                        word = word + char
            elif char is "\'":
                comment = comment + char
                for i in range(1, 4):
                    char = file.read(1)
                    if char is '\'':
                        comment = comment + char
                        if comment == "''":
                            char = file.read(1)
                            if char is "'":
                                while True:
                                    char = file.read(1)
                                    if char == '\n':
                                        line = line + 1
                                    if char == "'":
                                        char = file.read(1)
                                        if char == "'":
                                            char = file.read(1)
                                            if char == "'":
                                                comment = ''
                                                char = file.read(1)
                                                wb = True
                                                break
                                    elif char is None:

                                        break
                            else:
                                wb = True

                        if comment is not '':
                            token['cp'] = "char_const"
                            token['vp'] = word
                            token['line'] = line
                            token_set("char_const", word, line)
                            WriteInFile()
                            word = ''
                            wb = False
                            string = True
                            break
                        else:
                            string = True
                            break
                    elif char is '\n':
                        token['cp'] = "lexical_error"
                        token['vp'] = word
                        token['line'] = line
                        token_set("lexical_error", word, line)
                        WriteInFile()
                        word = ''
                        wb = False
                        string = True
                        break
                    else:
                        comment = ''
                        word = word + char
                if string is False:
                    word_break(word, line)
                    word = ''
                    wb = False
                comment = ''

            elif chr(char):
                while True:
                    word = word + char
                    char = file.read(1)
                    if not chr(char):
                        word_break(word, line)
                        word = ''
                        wb = True
                        break

            if char is '\0' or char is ' ':
                wb = False

            if char is '\n':
                line += 1
                wb = False

            if not char:
                break
        token['cp'] = "$"
        token['vp'] = "$"
        token['line'] = line
        token_set("$", "$", line)
        WriteInFile()

    # check token class part
    # print(set)
    # i = 0
    # while i<len(set):
    #     print(set[i][0])
    #     i+=1


s_stack = []
s_stack.append(0)
scope = 0
scope_num = 0
access_modifier = "null"
func_flag = 0
i = 0
r = 0
L = 0
CDT_flag = -1

class FT_class:
    C_name = ""
    F_name = ""
    F_type = ""

FT_data = FT_class

def Syntax_Analyzer():

    def Start():
        global i,scope
        if(set[i][0]== "DT" or set[i][0] == "ID" or set[i][0] == "UOP" or set[i][0] == "static" or set[i][0] == "const" or set[i][0] == "def" or set[i][0] == "if" or set[i][0] == "class" or set[i][0] == "while" or set[i][0] == "for" or set[i][0] == "switch" or set[i][0] == "$"):

            if(set[i][0] == "$"):
                return True
            elif(set[i][0]== "DT" or set[i][0] == "ID" or set[i][0] == "UOP" or set[i][0] == "static" or set[i][0] == "const" or set[i][0] == "def" or set[i][0] == "if" or set[i][0] == "class" or set[i][0] == "while" or set[i][0] == "for" or set[i][0] == "switch"):
                if(MST()):
                    return True

        return False

    def MST():
        global i
        if(set[i][0]== "DT" or set[i][0] == "ID" or set[i][0] == "UOP" or set[i][0] == "static" or set[i][0] == "const" or set[i][0] == "def" or set[i][0] == "if" or set[i][0] == "class" or set[i][0] == "while" or set[i][0] == "for" or set[i][0] == "switch" or set[i][0] == "$"):

            if (set[i][0] == "$"):
                return True
            elif(set[i][0]== "DT" or set[i][0] == "ID" or set[i][0] == "UOP" or set[i][0] == "static" or set[i][0] == "const" or set[i][0] == "def" or set[i][0] == "if" or set[i][0] == "class" or set[i][0] == "while" or set[i][0] == "for" or set[i][0] == "switch"):
                if(SST()):
                    if(MST()):
                        return True

        return False

    def SST():
        global i,scope,CDT_flag
        if (set[i][0]== "DT" or set[i][0] == "ID" or set[i][0] == "UOP" or set[i][0] == "static" or set[i][0] == "const" or set[i][0] == "def" or set[i][0] == "if" or set[i][0] == "class" or set[i][0] == "while" or set[i][0] == "for" or set[i][0] == "switch"):

            if(set[i][0]== "DT"):
                T = set[i][1]
                CDT_flag = 0
                i+= 1
                if(set[i][0]== "ID"):
                    N = set[i][1]
                    if(not insertST(N, T, s_stack[-1])):
                        print(N, "Redeclaration Error")
                        return False
                    i+=1
                    if(Dec(T, "null", "null", "null")):
                        return True
            elif(set[i][0]== "ID"):
                N = set[i][1]
                CDT_flag = 0
                i+= 1
                if(SST2(N, "null", "null", "null")):
                    return True
            elif(set[i][0] == "UOP"):
                if(Inc_dec()):
                    if(set[i][0] == ";"):
                        i+=1
                        return True
            elif(set[i][0] == "static" or set[i][0] == "const"):
                CDT_flag = 0
                if(TM("null", "null")):
                    return True
            elif(set[i][0]== "def"):
                CDT_flag = 0
                if(F_dec()):
                    return True
            elif(set[i][0] == "if"):
                if(If()):
                    return True
            elif(set[i][0] == "class"):
                CDT_flag = 1
                if(Class()):
                    return True
            elif(set[i][0] == "while"):
                if (While()):
                    return True
            elif(set[i][0] == "for"):
                CDT_flag = 0
                if(For()):
                    return True
            elif(set[i][0] == "switch"):
                if(Switch()):
                    return True

        return False


    def SST2(T, am, tm, C_name): #Object Type
        global i,scope,FT_data
        if(set[i][0]== "ID" or set[i][0] == "[" or set[i][0] == "." or set[i][0] == "(" or set[i][0] == "AOP" or set[i][0] == "UOP"):

            if(set[i][0]== "ID"):
                Type = lookUpDT(T)
                if(not Type):
                    print(T, "is Undeclared")
                    return False

                N = set[i][1]
                if(not insertST(N,T,s_stack[-1])):
                    print(N, "Redeclaration Error")
                    return False
                i+= 1
                if(Dec_O(T, am, tm, C_name)):
                    return True
            elif(set[i][0] == "[" or set[i][0] == "." or set[i][0] == "(" or set[i][0] == "AOP" or set[i][0] == "UOP"):
                Ty = strings
                Ty.p = lookUpST(T)
                store = Ty.p
                if(Array()):
                    Ty.p = store
                    if(L1(Ty)):
                        if(L2(Ty.p,T)):
                            return True
        return False

    def L1(Ty):
        global i,func_flag,FT_data
        if(set[i][0] == "(" or set[i][0] ==  "AOP" or set[i][0] == "UOP" or set[i][0] == ";" or set[i][0] ==  ")" or set[i][0] == "." ):

            if(set[i][0]== "."):
                if(Ty.p == "null"):
                    print("Error: Undeclared")
                    return False
                func_flag = 1
                OP = set[i][1]
                C_name = Ty.p
                FT_data.C_name = Ty.p
                i+= 1
                if(set[i][0]== "ID"):
                    N = set[i][1]
                    FT_data.F_name = N
                    Ty.p = lookUpCDT(C_name,N)
                    FT_data.F_type = Ty.p
                    if(Ty.p == "null"):
                        print("Error:(", N, ") Not Accessible or Undeclared")
                        return False
                    i+= 1
                    if(Array()):
                        if(L1(Ty)):
                            return True
            elif(set[i][0] == "(" or set[i][0] ==  "AOP" or set[i][0] == "UOP" or set[i][0] == ";" or set[i][0] ==  ")"):
                return True

        return False

    def L2(T,N):
        global i,func_flag,FT_data
        if(set[i][0]== "(" or set[i][0] == "AOP" or set[i][0] == "UOP"):

            if(set[i][0]== "("):
                Al = Al_string
                if(F_call(Al)):
                    if(func_flag == 0):
                        Type = lookUpDT(N)
                        if(Type == "null"):
                            print("Error: Function", N, "Undeclared")
                            return False
                        FT_data.F_type = Type
                        FT_data.F_name = N
                        C_name = "Global"
                        Type = lookUpFT(C_name, FT_data.F_name, Al.als)
                        if(Type == "null"):
                            print("Error: Function",FT_data.F_name ,"Undeclared")
                            return False
                    elif(func_flag == 1):
                        func_flag = 0
                        Type = lookUpFT(FT_data.C_name, FT_data.F_name, Al.als)
                        if (Type == "null"):
                            print("Error: Function", FT_data.F_name, "Undeclared")
                            return False
                    Al.als = ""
                    FT_data.F_name = ""
                    FT_data.C_name = ""
                    FT_data.F_type = ""
                    return True
            elif (set[i][0] == "AOP"):
                if (T == "null"):
                    print("Error:(", N, ")is Undeclared")
                if (Assign(T)):
                    if (set[i][0] == ";"):
                        i += 1
                        return True
            elif (set[i][0] == "UOP"):
                if (T == "null"):
                    print("Error:(", N, ")is Undeclared")
                if (T != "int" and T != "float"):
                    print("Error:(", T, ") Wrong Type For Increment Decrement")
                    return False
                i += 1
                if (set[i][0] == ";"):
                    i += 1
                    return True
        return False

    def TM(am, C_name):
        global i
        if(set[i][0]== "static" or set[i][0] == "const"):

            if(set[i][0]== "static"):
                tm = set[i][1]
                i+=1
                if(STM(am, tm, C_name)):
                    return True
            elif(set[i][0] == "const"):
                tm = set[i][1]
                i+=1
                if(CTM(am, tm, C_name)):
                    return True
        return False

    def STM(am, tm, C_name):
        global i
        if(set[i][0]== "DT" or set[i][0] == "ID"):

            if (set[i][0] == "DT"):
                T = set[i][1]
                i += 1
                if (set[i][0] == "ID"):
                    N = set[i][1]
                    if(CDT_flag == 0):
                        if(not insertST(N, T, s_stack[-1])):
                            print(N, "Redeclaration Error")
                            return False
                    elif(CDT_flag == 1):
                        if (not insertCDT(C_name, N, T, am, tm)):
                            print(N, "Redeclaration Error")
                            return False
                    i += 1
                    if (Dec(T, am, tm, C_name)):
                        return True
            elif(set[i][0] == "ID"):
                T = set[i][1]
                Type = lookUpDT(T)
                if (not Type):
                    print(T, "is Undeclared")
                    return False
                i+=1
                if(set[i][0] == "ID"):
                    N = set[i][1]
                    if (CDT_flag == 0):
                        if (not insertST(N, T, s_stack[-1])):
                            print(N, "Redeclaration Error")
                            return False
                    elif (CDT_flag == 1):
                        if (not insertCDT(C_name, N, T, am, tm)):
                            print(N, "Redeclaration Error")
                            return False
                    i+=1
                    if(Dec_O(T, am, tm, C_name)):
                        return True
        return False

    def CTM(am, tm, C_name):
        global i, scope
        if(set[i][0]== "DT" or set[i][0] == "ID"):

            if (set[i][0] == "DT"):
                T = set[i][1]
                i += 1
                if (set[i][0] == "ID"):
                    N = set[i][1]
                    if (CDT_flag == 0):
                        if (not insertST(N, T, s_stack[-1])):
                            print(N, "Redeclaration Error")
                            return False
                    elif (CDT_flag == 1):
                        if (not insertCDT(C_name, N, T, am, tm)):
                            print(N, "Redeclaration Error")
                            return False
                    i += 1
                    if(set[i][0]== "AOP"):
                        i+=1
                        T_Oe = strings
                        T_name = name_string
                        if(OE(T_Oe,T_name)):
                            if(set[i][0]== ";"):
                                i+=1
                                return True
            elif(set[i][0] == "ID"):
                T = set[i][1]
                Type = lookUpDT(T)
                if (not Type):
                    print(T, "is Undeclared")
                    return False
                i += 1
                if (set[i][0] == "ID"):
                    N = set[i][1]
                    if (CDT_flag == 0):
                        if (not insertST(N, T, s_stack[-1])):
                            print(N, "Redeclaration Error")
                            return False
                    elif (CDT_flag == 1):
                        if (not insertCDT(C_name, N, T, am, tm)):
                            print(N, "Redeclaration Error")
                            return False
                    i += 1
                    if(Dec_O(T, am, tm, C_name)):
                        return True
        return False


    def Body():
        global i
        if(set[i][0]== "{" or set[i][0] == ";"):
            if(set[i][0]== "{"):
                i+= 1
                if(MST_B()):
                    if(set[i][0]== "}"):
                        i+=1
                        return True
            elif(set[i][0]== ";"):
                i+=1
                return True
        return False

    def MST_B():
        global i
        if (set[i][0]== "DT" or set[i][0] == "ID" or set[i][0] == "while" or set[i][0] == "for" or set[i][0] == "if" or set[i][0] == "switch" or set[i][0] == "UOP" or set[i][0] == "break" or set[i][0] == "continue" or set[i][0] == "return" or set[i][0] == "}" or set[i][0] == "this"):

            if(set[i][0]== "DT" or set[i][0] == "ID" or set[i][0] == "while" or set[i][0] == "for" or set[i][0] == "if" or set[i][0] == "switch" or set[i][0] == "UOP" or set[i][0] == "break" or set[i][0] == "continue" or set[i][0] == "return" or set[i][0] == "this"):
                if(SST_B()):
                    if(MST_B()):
                        return True
            elif(set[i][0] == "}"):
                return True
        return False

    def SST_B():
        global i
        if (set[i][0]== "DT" or set[i][0] == "ID" or set[i][0] == "while" or set[i][0] == "for" or set[i][0] == "if" or set[i][0] == "switch" or set[i][0] == "UOP" or set[i][0] == "break" or set[i][0] == "continue" or set[i][0] == "return" or set[i][0] == "this"):
            if(set[i][0]== "DT"):
                T = set[i][1]
                i+=1
                if (set[i][0] == "ID"):
                    N = set[i][1]
                    if (not insertST(N, T, s_stack[-1])):
                        print(N, "Redeclaration Error")
                        return False
                    i+=1
                    if(Dec(T, "null", "null", "null")):
                        return True
            elif(set[i][0]== "ID"):
                N = set[i][1]
                am = 0
                tm = 0
                C_name = 0
                i+= 1
                if(SST2(N, "null", "null", "null")):
                    return True
            elif(set[i][0] == "if"):
                if(If()):
                    return True
            elif(set[i][0] == "switch"):
                if(Switch()):
                    return True
            elif(set[i][0] == "while"):
                if(While()):
                    return True
            elif(set[i][0] == "for"):
                if(For()):
                    return True
            elif(set[i][0] == "UOP"):
                if(Inc_dec()):
                    if(set[i][0] == ";"):
                        i+=1
                        return True
            elif(set[i][0] == "break"):
                i+=1
                if(set[i][0] == ";"):
                    return True
            elif(set[i][0] == "continue"):
                i+=1
                if(set[i][0] == ";"):
                    return True
            elif(set[i][0] == "return"):
                if(Return()):
                    return True
            elif(set[i][0] == "this"):
                if(This()):
                    return True
        return False

    def Dec(T, am, tm, C_name):
        global i
        if(set[i][0] == "AOP" or set[i][0] == "[" or set[i][0] == "," or set[i][0] == ";"):
            if(set[i][0] == "AOP" or set[i][0] == "[" or set[i][0] == "," or set[i][0] == ";"):
                if(D(T, am, tm, C_name)):
                    if(set[i][0] == ";"):
                        i+=1
                        return True
        return False

    def D(T, am, tm, C_name):
        global i
        if (set[i][0] == "AOP" or set[i][0] == "[" or set[i][0] == "," or set[i][0] == ";"):

            if(set[i][0] == ","):
                if(D_comma(T, am, tm, C_name)):
                    return True
            elif(set[i][0] == "AOP"):
                    if(D_assign(T, am, tm, C_name)):
                        return True
            elif(set[i][0] == "["):
                i+=1
                T_Oe = strings
                T_name = name_string
                if(OE(T_Oe,T_name)):
                    if (T_Oe.p != "int"):
                        print("Error:(", T_Oe.p, ")Wrong Type for Array Size")
                        return False
                    if(set[i][0] == "]"):
                        i+=1
                        if(D_array(T, am, tm, C_name)):
                            return True
            elif(set[i][0] == ";"):
                return True

        return False

    def D_array(T, am, tm, C_name):
        global i, scope
        if (set[i][0] == "," or set[i][0] == "AOP" or set[i][0] == ";"):

            if(set[i][0] == ","):
                i+=1
                if (set[i][0] == "ID"):
                    N = set[i][1]
                    if (CDT_flag == 0):
                        if (not insertST(N, T, s_stack[-1])):
                            print(N, "Redeclaration Error")
                            return False
                    elif (CDT_flag == 1):
                        if (not insertCDT(C_name, N, T, am, tm)):
                            print(N, "Redeclaration Error")
                            return False
                    i+=1
                    if(set[i][0] == "["):
                        i+=1
                        T_Oe = strings
                        T_name = name_string
                        if(OE(T_Oe,T_name)):
                            if (T_Oe.p != "int"):
                                print("Error:(", T_Oe.p, ")Wrong Type for Array Size")
                                return False
                            if(set[i][0] == "]"):
                                i+=1
                                if(D_array(T, am, tm, C_name)):
                                    return True
            elif(set[i][0] == "AOP"):
                    i += 1
                    if(set[i][0] == "{"):
                        i+=1
                        if(E()):
                            if(set[i][0] == "}"):
                                i+=1
                                return True
            elif(set[i][0] == ";"):
                return True

        return False

    def D_comma(T, am, tm, C_name):
        global i, CDT_flag
        if(set[i][0] == "," or set[i][0] == ";"):

            if(set[i][0] == ","):
                i+=1
                if(set[i][0] == "ID"):
                    N = set[i][1]
                    if (CDT_flag == 0):
                        if (not insertST(N, T, s_stack[-1])):
                            print(N, "Redeclaration Error")
                            return False
                    elif (CDT_flag == 1):
                        if (not insertCDT(C_name, N, T, am, tm)):
                            print(N, "Redeclaration Error")
                            return False
                    i+=1
                    if(D_assign(T, am, tm, C_name)):
                        return True
            elif(set[i][0] == ";"):
                return True

        return False

    def D_assign(T, am, tm, C_name):
        global i
        if(set[i][0] == "AOP" or set[i][0] == "," or set[i][0] == ";"):

            if(set[i][0] == "AOP"):
                Op = set[i][1]
                i+=1
                if(D_assign1(T, Op, am, tm, C_name)):
                    return True
            elif(set[i][0] == ","):
                if(D_comma(T, am, tm, C_name)):
                    return True
            elif(set[i][0] == ";"):
                return True

        return False

    def D_assign1(Tl,Op,am,tm,c_name):
        global i
        if (set[i][0] == "ID" or set[i][0] == "UOP" or set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const" or set[i][0] == "(" or set[i][0] == "!" or set[i][0] == "this" or set[i][0] == "["):

            if (set[i][0] == "ID" or set[i][0] == "UOP" or set[i][0] == "int_const" or set[i][0] == "float_const" or
set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const" or set[i][0] == "(" or set[i][0] == "!" or set[i][0] == "this"):
                T_Oe = strings
                T_name = name_string
                if(OE(T_Oe,T_name)):
                    if(D_comma(Tl,am,tm,c_name)):
                        return True
            elif(set[i][0] == "["):
                i+=1
                if(List()):
                    if(set[i][0] == "]"):
                        i+=1
                        return True

        return False

    def Dec_O(T, am, tm, C_name):
        global i
        if(set[i][0] == "(" or set[i][0] == "[" or set[i][0] == "," or set[i][0] == "AOP" or set[i][0] == ";" ):
            if(Object(T, am, tm, C_name)):
                if(set[i][0] == ";"):
                    i+=1
                    return True
        return False

    def Object(T, am, tm, C_name):
        global i
        if(set[i][0] == "(" or set[i][0] == "[" or set[i][0] == "," or set[i][0] == "AOP" or set[i][0] == ";" ):

            if(set[i][0] == "(" or set[i][0] == "[" or set[i][0] == ","):
                if(O(T, am, tm, C_name)):
                    return True
            elif(set[i][0] == "AOP"):
                if(O_assign(T, am, tm, C_name)):
                    return True
            elif(set[i][0] == ";"):
                return True

        return False

    def O(T, am, tm, C_name):
        global i
        if(set[i][0] == "(" or set[i][0] == "[" or set[i][0] == "," or set[i][0] == ";"):

            if(set[i][0] == "("):
                if(O_paran(T, am, tm, C_name)):
                    return True
            elif(set[i][0] == "["):
                if(O_array(T, am, tm, C_name)):
                    return True
            elif(set[i][0] == ","):
                if(O_comma(T, am, tm, C_name)):
                    return True
            elif (set[i][0] == ";"):
                return True

        return False

    def O_paran(T, am, tm, C_name):
        global i
        if (set[i][0] == "(" ):

            if (set[i][0] == "("):
                i+=1
                if (E()):
                    if (set[i][0] == ")"):
                        i+=1
                        if(O_comma(T, am, tm, C_name)):
                            return True
        return False

    def O_array(T, am, tm, C_name):
        global i
        if(set[i][0] == "["):

            if (set[i][0] == "["):
                i+=1
                T_Oe = strings
                T_name = name_string
                if(OE(T_Oe,T_name)):
                    if (T_Oe.p != "int"):
                        print("Error:(", T_Oe.p, ")Wrong Type for Array Size")
                        return False
                    if(set[i][0] == "]"):
                        i+=1
                        if(O_comma(T, am, tm, C_name)):
                            return True
        return False

    def O_comma(T, am, tm, C_name):
        global i, scope, CDT_flag
        if(set[i][0] == "," or set[i][0] == ";"):

            if (set[i][0] == ","):
                i+=1
                if(set[i][0] == "ID"):
                    N = set[i][1]
                    if (CDT_flag == 0):
                        if (not insertST(N, T, s_stack[-1])):
                            print(N, "Redeclaration Error")
                            return False
                    elif (CDT_flag == 1):
                        if (not insertCDT(C_name, N, T, am, tm)):
                            print(N, "Redeclaration Error")
                            return False
                    i+=1
                    if(O(T, am, tm, C_name)):
                         return True
            elif (set[i][0] == ";"):
                return True

        return False

    def O_assign(T, am, tm, C_name):
        global i
        if (set[i][0] == "AOP" or set[i][0] == "," or set[i][0] == ";"):

            if(set[i][0] == "AOP"):
                i += 1
                if (set[i][0] == "ID"):
                    i += 1
                    if (O_assign1(T, am, tm, C_name)):
                        if(O_assign2(T, am, tm, C_name)):
                            return True
            elif(set[i][0] == "," or set[i][0] == ";"):
                return True

        return False

    def O_assign1(T):
        global i
        if (set[i][0] == "AOP" or set[i][0] == "(" or set[i][0] == "," or set[i][0] == ";"):

            if (set[i][0] == "AOP"):
                if (O_assign(T, am, tm, C_name)):
                    return True
            elif(set[i][0] == "("):
                if(F_call1()):
                    if(O_assign(T, am, tm, C_name)):
                        return True
            elif(set[i][0] == "," or set[i][0] == ";"):
                return True

        return False

    def O_assign2(T, am, tm, C_name):
        global i,scope
        if (set[i][0] == "," or set[i][0] == ";"):

            if(set[i][0] == ","):
                i += 1
                if(set[i][0] == "ID"):
                    N = set[i][1]
                    if (CDT_flag == 0):
                        if (not insertST(N, T, s_stack[-1])):
                            print(N, "Redeclaration Error")
                            return False
                    elif (CDT_flag == 1):
                        if (not insertCDT(C_name, N, T, am, tm)):
                            print(N, "Redeclaration Error")
                            return False
                    i += 1
                    if (O_assign(T, am, tm, C_name)):
                        return True
            elif(set[i][0] == ";"):
                return True

        return False

    def F_dec():
        global i
        if(set[i][0]== "def"):
            i+= 1
            tm = strings
            if(TM_F(tm)):
                C_name = 0
                am = 0
                if(F_dec1(C_name,am,tm.p)):
                    return True
        return False

    def F_dec1(C_name,am,tm):
        global i,scope,CDT_flag,scope_num
        if(set[i][0] == "DT" or set[i][0] == "ID"):

            if(set[i][0] == "DT"):
                Rt = set[i][1]
                i+=1
                if(Array_ret()):
                    if(set[i][0] == "ID"):
                        N = set[i][1]
                        i+=1
                        if(set[i][0] == "("):
                            scope_num += 1
                            s_stack.append(scope_num)
                            scope = scope_num
                            Pl = strings
                            i+=1
                            if(F2(Pl)):
                                if(set[i][0] == ")"):
                                    if(CDT_flag == 0):
                                        if(not insertDT(N, Pl.p + "->" + Rt , 0, 0)):
                                            print(N,"Redeclaration Error")
                                            return False
                                        insertFT("Global", tm, am, Pl.p, Rt, N)
                                    elif(CDT_flag == 1):
                                        if (not insertCDT(C_name, N, Pl.p + "->" + Rt, am, tm)):
                                            print(N, "Redeclaration Error")
                                            return False
                                        insertFT(C_name, tm, am, Pl.p, Rt, N)

                                    i+=1
                                    if(Body()):
                                        scope-=scope_num
                                        s_stack.pop()
                                        return True
            elif(set[i][0] == "ID"):
                Rt = set[i][1]
                Type = lookUpDT(Rt)
                if (not Type):
                    print(Rt, "is Undeclared")
                    return False
                i += 1
                if (Array_ret()):
                    if (set[i][0] == "ID"):
                        N = set[i][1]
                        i += 1
                        if (set[i][0] == "("):
                            scope_num += 1
                            s_stack.append(scope_num)
                            scope = scope_num
                            Pl = strings
                            i += 1
                            if (F2(Pl)):
                                if (set[i][0] == ")"):
                                    if (CDT_flag == 0):
                                        if (not insertDT(N, Pl.p + "->" + Rt, 0, 0)):
                                            print(N, "Redeclaration Error")
                                            return False
                                        insertFT("Global", tm, am, Pl.p, Rt, N)
                                    elif (CDT_flag == 1):
                                        if (not insertCDT(C_name, N, Pl.p + "->" + Rt, am, tm)):
                                            print(N, "Redeclaration Error")
                                            return False
                                        insertFT(C_name, tm, am, Pl.p, Rt, N)
                                    i += 1
                                    if (Body()):
                                        scope-=scope_num
                                        s_stack.pop()
                                        return True
        return False

    def F2(Pl):
        global i
        if(set[i][0]== "DT" or set[i][0] == "ID" or set[i][0] == ")"):

            if(set[i][0]== "DT"):
                T = set[i][1]
                Pl.p = T
                i+= 1
                if(set[i][0]== "ID"):
                    N = set[i][1]
                    if (not insertST(N, T, s_stack[-1])):
                        print(N, "Redeclaration Error")
                        return False
                    i+= 1
                    if(Array()):
                        if(F3(Pl)):
                            return True
            elif(set[i][0]== "ID"):
                T = set[i][1]
                Type = lookUpDT(T)
                if(not Type):
                    print(T, "is Undeclared")
                    return False
                Pl.p = T
                i += 1
                if (set[i][0] == "ID"):
                    N = set[i][1]
                    if(not insertST(N, T, s_stack[-1])):
                        print(N, "Redeclaration Error")
                        return False
                    i+= 1
                    if(Array()):
                        if (F3(Pl)):
                            return True
            elif(set[i][0] == ")"):
                Pl.p = "void"
                return True
        return False

    def F3(Pl):
        global i
        if(set[i][0]== "," or set[i][0] == ")"):

            if(set[i][0] == ","):
                i+= 1
                if(F4(Pl)):
                    return True
            elif(set[i][0] == ")"):
                return True

        return False

    def F4(Pl):
        global i
        if(set[i][0]== "DT" or set[i][0] == "ID"):

            if(set[i][0]== "DT"):
                T = set[i][1]
                Pl.p += ","
                Pl.p += T
                i+= 1
                if(set[i][0]== "ID"):
                    N = set[i][1]
                    if (not insertST(N, T, s_stack[-1])):
                        print(N, "Redeclaration Error")
                        return False
                    i+= 1
                    if(Array()):
                        if(F3(Pl)):
                            return True
            elif(set[i][0]== "ID"):
                T = set[i][1]
                Type = lookUpDT(T)
                if (not Type):
                    print(T, "is Undeclared")
                    return False
                Pl.p += ","
                Pl.p += T
                i += 1
                if (set[i][0] == "ID"):
                    N = set[i][1]
                    if (not insertST(N, T, s_stack[-1])):
                        print(N, "Redeclaration Error")
                        return False
                    i += 1
                    if(Array()):
                        if (F3(Pl)):
                            return True
        return False

    def TM_F(tm):
        global i
        if(set[i][0]== "static" or set[i][0]== "const" or set[i][0]== "DT" or set[i][0]== "ID"):

            if(set[i][0]== "static"):
                tm.p = set[i][1]
                i+=1
                return True
            elif(set[i][0]== "const"):
                tm.p = set[i][1]
                i+=1
                return True
            elif(set[i][0]== "DT" or set[i][0]== "ID"):
                tm.p = 0
                return True

        return False

    def F_call(Al):
        global i
        if(set[i][0]== "("):

            if(set[i][0]== "("):
                i+= 1
                if(E(Al)):
                    if(set[i][0]== ")"):
                        i+=1
                        if(set[i][0]== ";"):
                            i+= 1
                            return True

        return False
    def F_call1(Al):
        global i
        if(set[i][0]== "("):
            i+= 1

            if(E(Al)):
                if(set[i][0]== ")"):
                    i+=1
                    return True
        return False

    def Assign(Tl):
        global i
        if(set[i][0] == "AOP"):

            if(set[i][0] == "AOP"):
                Op = set[i][1]
                i+=1
                if(A1(Tl, Op)):
                    return True
        return False

    def A1(Tl, Op):
        global i
        if (set[i][0] == "ID" or set[i][0] == "[" or set[i][0] == "UOP" or set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const" or set[i][0] == "(" or set[i][0] == "this" or set[i][0] == "!"):

            if (set[i][0] == "ID" or set[i][0] == "UOP" or set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const" or set[i][0] == "(" or set[i][0] == "this" or set[i][0] == "!"):
                T_Oe = strings
                T_name = name_string
                if(OE(T_Oe,T_name)):
                    Type = compatibility(Tl,T_Oe.p,Op)
                    if(Type == "null"):
                        print("Type Not Matched")
                        return False
                    if(A2()):
                        return True
            elif(set[i][0] == "["):
                i+=1
                if(List()):
                    if(set[i][0] == "]"):
                        i+=1
                        return True
        return False

    def A2():
        global i
        if(set[i][0] == "," or set[i][0] == ";"):

            if(set[i][0] == ","):
                i+=1
                if(set[i][0] == "ID"):
                    N = set[i][1]
                    T = lookUpST(N)
                    if (T == "null"):
                        print(N, "is Undeclared")
                        return False
                    i+=1
                    if(A3(T)):
                        return True
            elif(set[i][0] == ";"):
                return True

        return False

    def A3(Tl):
        global i
        if (set[i][0] == "AOP" or set[i][0] == ";"):

            if (set[i][0] == "AOP"):
                Op = set[i][1]
                i += 1
                if(A1(Tl, Op)):
                    return True
            elif (set[i][0] == ";"):
                return True

        return False


    def Inc_dec():
        global i
        if(set[i][0]== "UOP"):
            i+= 1
            if(set[i][0]== "ID"):
                N = set[i][1]
                Ty = strings
                Ty.p = lookUpST(N)
                store = Ty.p
                if (Ty.p == "null"):
                    print("Error:(", N, ")is Undeclared")
                    return False
                i+= 1
                if(Array()):
                    Ty.p = store
                    if(L1(Ty)):
                        if(Ty.p != "int" and Ty.p != "float"):
                            print("Error:(", Ty.p, ")is Undeclared")
                            return False
                        return True

        return False

    def While():
        global i,scope, scope_num, L
        if(set[i][0]== "while"):
            i+= 1
            L+=1
            Lab1 = L
            print("L"+str(L)+":")
            if(set[i][0]== "("):
                i+= 1
                T_Oe = strings
                T_name = name_string
                if(OE(T_Oe,T_name)):
                    L+=1
                    Lab2 = L
                    print("if(",T_name.ns, "== false )\n  jmp","L"+str(L))
                    if(set[i][0]== ")"):
                        i+=1
                        scope_num +=1
                        s_stack.append(scope_num)
                        scope = scope_num
                        if(Body()):
                            print("jmp","L"+str(Lab1),"\nL"+str(Lab2)+":")
                            scope = s_stack[len(s_stack)-2]
                            s_stack.pop()

                            return True
        return False

    def For():
        global i,scope_num
        if(set[i][0]== "for"):
            i+= 1
            if(set[i][0]== "("):
                scope_num += 1
                s_stack.append(scope_num)
                i+= 1
                if(C1()):
                    if(C2()):
                        if(set[i][0]== ";"):
                            i+= 1
                            if(C3()):
                                if(set[i][0]== ")"):
                                    i+=1
                                    if(Body()):
                                        s_stack.pop()
                                        return True
        return False

    def C1():
        global i
        if(set[i][0]== "ID" or set[i][0] == "DT" or set[i][0] == ";"):

            if(set[i][0]== "ID"):
                N = set[i][1]
                T = lookUpST(N)
                if (T == "null"):
                    print(N, "is Undeclared")
                    return False
                i+= 1
                if(Assign(T)):
                    if(set[i][0] == ";"):
                        i+=1
                        return True
            elif(set[i][0]== "DT"):
                T = set[i][1]
                i+= 1
                if(set[i][0]== "ID"):
                    N = set[i][1]
                    if(not insertST(N, T, s_stack[-1])):
                        print(N, "Redeclaration Error")
                        return False
                    i+= 1
                    if(Dec(T, "null", "null", "null")):
                        return True
            elif(set[i][0] == ";"):
                i+=1
                return True

        return False

    def C2():
        global i
        if(set[i][0]== "ID" or set[i][0] == "UOP" or set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const" or set[i][0] == "(" or set[i][0] == "!" or set[i][0] == "this" or set[i][0] == ";" ):

            if (set[i][0] == "ID" or set[i][0] == "UOP" or set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const" or set[i][0] == "(" or set[i][0] == "!" or set[i][0] == "this"):
                T_Oe = strings
                T_name = name_string
                if(OE(T_Oe,T_name)):
                    if(T_Oe.p != "int" and T_Oe.p != "float"):
                        print("Wrong Type")
                        return False
                    return True
            elif(set[i][0] == ";"):
                return True

        return False

    def C3():
        global i
        if (set[i][0] == "ID" or set[i][0] == "UOP" or set[i][0] == ")"):

            if (set[i][0] == "ID"):
                N = set[i][1]
                T = strings
                T.p = lookUpST(N)
                if (T.p == "null"):
                    print("Error:(", T.p, ")is Undeclared")
                    return False
                i += 1
                if (Array()):
                    if(L1(T)):
                        if(C4(T.p)):
                            return True
            elif(set[i][0] == "UOP"):
                if(Inc_dec()):
                    return True
            elif(set[i][0] == ")"):
                return True

        return False

    def C4(T):
        global i
        if(set[i][0]== "(" or set[i][0] == "AOP" or set[i][0] == "UOP"):

            if(set[i][0]== "("):
                if(F_call()):
                    return True
            elif(set[i][0] == "AOP"):
                if(Assign(T)):
                    return True
            elif(set[i][0] == "UOP"):
                if (T != "int" and T != "float"):
                    print("Error:(", T, ") Wrong Type For Increment Decrement")
                    return False
                i+=1
                return True

        return False

    def If():
        global i,scope_num,L
        if(set[i][0]== "if"):
            i+=1
            if(set[i][0]== "("):
                scope_num += 1
                s_stack.append(scope_num)
                i+= 1
                T_Oe = strings
                T_name = name_string
                if(OE(T_Oe,T_name)):
                    if(set[i][0]== ")"):
                        L+=1
                        Lab1 = L
                        print("if(",T_name.ns,"== false )\n  jmp L"+str(L))
                        i+=1
                        if(Body()):
                            s_stack.pop()
                            if(Else()):
                                return True
        return False

    def Else():
        global i,L
        if(set[i][0]== "else" or set[i][0] == "DT" or set[i][0] == "ID" or set[i][0] == "UOP" or set[i][0] == "static" or set[i][0] == "virtual" or set[i][0] == "const" or set[i][0] == "class" or set[i][0] == "while" or set[i][0] == "for" or set[i][0] == "$" or set[i][0] == "if" or set[i][0] == "switch" or set[i][0] == "break" or set[i][0] == "continue" or set[i][0] == "return" or set[i][0] ==  "}" ):

            if(set[i][0] == "else"):
                i+= 1
                if(Else1()):
                    return True
            elif(set[i][0] == "DT" or set[i][0] == "ID" or set[i][0] == "UOP" or set[i][0] == "static" or set[i][0] == "const" or set[i][0] == "class" or set[i][0] == "while" or set[i][0] == "for" or set[i][0] == "$" or set[i][0] == "if" or set[i][0] == "switch" or set[i][0] == "break" or set[i][0] == "continue" or set[i][0] == "return" or set[i][0] ==  "}" ):

                print("L"+str(L)+":")
                return True

        return False

    def Else1():
        global i,scope_num,L
        if(set[i][0]== "if" or set[i][0]== "{" or set[i][0]== ";"):
            if(set[i][0]== "if"):
                if(If()):
                    return True
            elif(set[i][0]== "{" or set[i][0]== ";"):
                Lab1 = L
                L += 1
                Lab2 = L
                print("jmp L"+str(L))
                print("L"+str(Lab1)+":")
                scope_num += 1
                s_stack.append(scope_num)
                if(Body()):
                    print("L" + str(Lab2) + ":")
                    s_stack.pop()
                    return True
        return False

    def Switch():
        global i
        if(set[i][0]== "switch"):
            i+= 1
            if(set[i][0]== "("):
                i+= 1
                T_Oe = strings
                T_name = name_string
                if(OE(T_Oe,T_name)):
                    if(set[i][0]== ")"):
                        i +=1
                        if(set[i][0]== "{"):
                            i += 1
                            if(S_body()):
                                if(set[i][0]== "}"):
                                    i+= 1
                                    return True
        return False

    def S_body():
        global i
        if(set[i][0]== "case" or set[i][0] == "default" or set[i][0] == "}"):

            if(set[i][0]== "case"):
                i+= 1
                T_Oe = strings
                T_name = name_string
                if(OE(T_Oe,T_name)):
                    if(set[i][0]== ":"):
                        i+= 1
                        if(Body()):
                            if(S_body()):
                                return True
            elif(set[i][0] == "default"):
                i += 1
                if (set[i][0] == ":"):
                    i += 1
                    if (Body()):
                        if (S_body1()):
                            return True
            elif(set[i][0] == "}"):
                return True

        return False

    def S_body1():
        global i

        if(set[i][0]== "case" or set[i][0] == "}"):
            if (set[i][0] == "case"):
                i+=1
                T_Oe = strings
                T_name = name_string
                if(OE(T_Oe,T_name)):
                    if(set[i][0]== ":"):
                        i+= 1
                        if(Body()):
                            if(S_body1()):
                                return True
            elif(set[i][0] == "}"):
                return True

        return False

    def Return():
        global i
        if(set[i][0]== "return"):
            if(set[i][0] == "return"):
                i+= 1
                if(R1()):
                    if(set[i][0] == ";"):
                        i+=1
                        return True
        return False

    def R1():
        global i
        if(set[i][0]== "ID" or set[i][0] == "UOP" or set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const" or set[i][0] == "(" or set[i][0] == "!" or set[i][0] == "this" or set[i][0] == ";"):

            if (set[i][0] == "ID" or set[i][0] == "UOP" or set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const" or set[i][0] == "(" or set[i][0] == "!" or set[i][0] == "this"):
                T_Oe = strings
                T_name = name_string
                if(OE(T_Oe,T_name)):
                    return True
            elif(set[i][0] == ";"):
                return True

        return False


    def OE(T,Na):
        global i
        if ( set[i][0]== "ID" or set[i][0] == "UOP" or set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const" or set[i][0] == "(" or set[i][0] == "!" or set[i][0] == "this" ):
            if(AE(T,Na)):
                if(OE_(T,Na)):
                    return True
        return False

    def OE_(T,Na):
        global i,r
        if(set[i][0]== "||" or set[i][0] == "]" or set[i][0] == "AOP" or set[i][0] == ";" or set[i][0] == ")" or set[i][0] == ":" or set[i][0] == "}" or  set[i][0] == ","):

            if(set[i][0] == "||"):
                Op = set[i][1]
                Tl = T.p
                Na_L = Na.ns
                i+= 1
                if(AE(T,Na)):
                    Tr = T.p
                    Na_R = Na.ns
                    T.p = compatibility(Tl,Tr,Op)
                    if(T.p == "null"):
                        print("Type Not Matched")
                        return False
                    r+=1
                    Na.ns = "R" + str(r)
                    print("R"+str(r),"=",Na_L,Op,Na_R)
                    if(OE_(T,Na)):
                        return True
            elif(set[i][0] == "]" or set[i][0] == "AOP" or set[i][0] == ";" or set[i][0] == ")" or set[i][0] == ":" or set[i][0] == "}" or  set[i][0] == ","):
                return True

        return False

    def AE(T,Na):
        global i
        if( set[i][0]== "ID" or set[i][0] == "UOP" or set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const" or set[i][0] == "(" or set[i][0] == "UOP" or set[i][0] == "this" ):
            if(ROP(T,Na)):
                if(AE_(T,Na)):
                    return True
        return False

    def AE_(T,Na):
        global i,r
        if(set[i][0] == "&&" or set[i][0] == "||" or set[i][0] == "]" or set[i][0] == "AOP" or set[i][0] == ";" or set[i][0] == ")" or set[i][0] == ":" or set[i][0] == "}" or  set[i][0] == ","):

            if(set[i][0]== "&&"):
                Op = set[i][1]
                Tl = T.p
                Na_L = Na.ns
                i+= 1
                if(ROP(T,Na)):
                    Tr = T.p
                    Na_R = Na.ns
                    T.p = compatibility(Tl, Tr, Op)
                    if (T.p == "null"):
                        print("Type Not Matched")
                        return False
                    r += 1
                    Na.ns = "R" + str(r)
                    print("R"+str(r), "=", Na_L, Op, Na_R)
                    if(AE_(T,Na)):
                        return True
            elif(set[i][0] == "||" or set[i][0] == "]" or set[i][0] == "AOP" or set[i][0] == ";" or set[i][0] == ")" or set[i][0] == ":" or set[i][0] == "}" or  set[i][0] == ","):
                return True

        return False

    def ROP(T,Na):
        global i
        if( set[i][0]== "ID" or set[i][0] == "UOP" or set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const" or set[i][0] == "(" or set[i][0] == "UOP" or set[i][0] == "this"):
            if (PM(T,Na)):
                if (ROP_(T,Na)):
                    return True
        return False

    def ROP_(T,Na):
        global i,r
        if(set[i][0] == "ROP" or set[i][0] == "&&" or set[i][0] == "||" or set[i][0] == "]" or set[i][0] == "AOP" or set[i][0] == ";" or set[i][0] == ")" or set[i][0] == ":" or set[i][0] == "}" or  set[i][0] == ","):

            if (set[i][0] == "ROP"):
                Op = set[i][1]
                Tl = T.p
                Na_L = Na.ns
                i+=1
                if(PM(T,Na)):
                    Tr = T.p
                    Na_R = Na.ns
                    T.p = compatibility(Tl, Tr, Op)
                    if (T.p == "null"):
                        print("Type Not Matched")
                        return False
                    r += 1
                    Na.ns = "R" + str(r)
                    print("R"+str(r), "=", Na_L, Op, Na_R)
                    if(ROP_(T,Na)):
                        return True
            elif (set[i][0] == "&&" or set[i][0] == "||" or set[i][0] == "]" or set[i][0] == "AOP" or set[i][0] == ";" or set[i][0] == ")" or set[i][0] == ":" or set[i][0] == "}" or  set[i][0] == ","):
                return True

        return False

    def PM(T,Na):
        global i
        if( set[i][0]== "ID" or set[i][0] == "UOP" or set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const" or set[i][0] == "(" or set[i][0] == "!" or set[i][0] == "this"):
            if (MDM(T,Na)):
                if (PM_(T,Na)):
                    return True
        return False

    def PM_(T,Na):
        global i,r
        if(set[i][0]== "PM" or set[i][0] == "ROP" or set[i][0] == "&&" or set[i][0] == "||" or set[i][0] == "]" or set[i][0] == "AOP" or set[i][0] == ";" or set[i][0] == ")" or set[i][0] == ":" or set[i][0] == "}" or  set[i][0] == ","):

            if(set[i][0] == "PM"):
                Op = set[i][1]
                Tl = T.p
                Na_L = Na.ns
                i += 1
                if(MDM(T,Na)):
                    Tr = T.p
                    Na_R = Na.ns
                    T.p = compatibility(Tl, Tr, Op)
                    if (T.p == "null"):
                        print("Type Not Matched")
                        return False
                    r += 1
                    Na.ns = "R" + str(r)
                    print("R"+str(r), "=", Na_L, Op, Na_R)
                    if(PM_(T,Na)):
                        return True
            elif(set[i][0] == "ROP" or set[i][0] == "&&" or set[i][0] == "||" or set[i][0] == "]" or set[i][0] == "AOP" or set[i][0] == ";" or set[i][0] == ")" or set[i][0] == ":" or set[i][0] == "}" or  set[i][0] == ","):
                return True

        return False

    def MDM(TT,Na):
        global i
        if( set[i][0]== "ID" or set[i][0] == "UOP" or set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const" or set[i][0] == "(" or set[i][0] == "!" or set[i][0] == "this"):
            if (T(TT,Na)):
                if (MDM_(TT,Na)):
                    return True
        return False

    def MDM_(TT,Na):
        global i,r
        if (set[i][0]== "MDM" or set[i][0]== "PM" or set[i][0] == "ROP" or set[i][0] == "&&" or set[i][0] == "||" or set[i][0] == "]" or set[i][0] == "AOP" or set[i][0] == ";" or set[i][0] == ")" or set[i][0] == ":" or set[i][0] == "}" or  set[i][0] == ","):

            if(set[i][0] == "MDM" ):
                Op = set[i][1]
                Tl = TT.p
                Na_L = Na.ns
                i += 1
                if(T(TT,Na)):
                    Tr = TT.p
                    Na_R = Na.ns
                    TT.p = compatibility(Tl, Tr, Op)
                    if (TT.p == "null"):
                        print("Type Not Matched")
                        return False
                    r += 1
                    Na.ns = "R"+str(r)
                    print("R"+str(r), "=", Na_L, Op, Na_R)
                    if(MDM_(TT,Na)):
                        return True
            elif(set[i][0]== "PM" or set[i][0] == "ROP" or set[i][0] == "&&" or set[i][0] == "||" or set[i][0] == "]" or set[i][0] == "AOP" or set[i][0] == ";" or set[i][0] == ")" or set[i][0] == ":" or set[i][0] == "}" or  set[i][0] == ","):
                return True

        return False

    def T(TT,Na):
        global i,array_flag
        if(set[i][0]== "ID" or set[i][0] == "UOP" or set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const" or set[i][0] == "(" or set[i][0] == "this" or set[i][0] == "!"):

            if(set[i][0]== "ID"):
                N = set[i][1]
                Na.ns = N
                TT.p = lookUpST(N)
                if (TT.p == "null"):
                    print(N, "Undeclared")
                    return False
                i+= 1
                if(Array()):
                    if(T1(TT,Na)):
                        if(T2(TT,N)):
                            return True
            elif(set[i][0] == "UOP"):
                if(Inc_dec()):
                    return True
            elif(set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const"):
                if(Const(TT,Na)):
                    return True
            elif(set[i][0]== "("):
                i+= 1
                T_Oe = strings
                T_name = name_string
                if(OE(T_Oe,T_name)):
                    if(set[i][0]== ")"):
                        i+= 1
                        return True
            elif(set[i][0]== "!"):
                i+=1
                if(T()):
                    return True
            elif(set[i][0]== "this"):
                i+= 1
                if(set[i][0]== "->"):
                    i+= 1
                    if(set[i][0]== "ID"):
                        i+= 1
                        if(Array()):
                            # if(T1()):
                            return True

        return False

    def T1(T,Na):
        global i
        if(set[i][0]== "[" or set[i][0] == "." or set[i][0] == "(" or set[i][0] == "UOP" or set[i][0]== "MDM" or set[i][0]== "PM" or set[i][0] == "ROP" or set[i][0] == "&&" or set[i][0] == "||" or set[i][0] == "]" or set[i][0] == "AOP" or set[i][0] == ";" or set[i][0] == ")" or set[i][0] == ":" or set[i][0] == "}" or  set[i][0] == ","):

            if(set[i][0] == "."):
                    Op = set[i][1]
                    Na.ns += "."
                    C_name = T.p
                    i+=1
                    if(set[i][0] == "ID"):
                        N = set[i][1]
                        T.p = lookUpCDT(C_name, N)
                        Na.ns += N
                        if(T.p == "null"):
                            print(N,"Not Accessible or Undeclared")
                            return False
                        i+=1;
                        if(Array()):
                            if(T1(T,Na)):
                                return True
            elif(set[i][0] == "(" or set[i][0] == "UOP" or set[i][0]== "MDM" or set[i][0]== "PM" or set[i][0] == "ROP" or set[i][0] == "&&" or set[i][0] == "||" or set[i][0] == "]" or set[i][0] == "AOP" or set[i][0] == ";" or set[i][0] == ")" or set[i][0] == ":" or set[i][0] == "}" or  set[i][0] == ","):
                return True

        return False

    def T2(T, N):
        global i,scope
        if(set[i][0] == "(" or set[i][0] == "UOP" or set[i][0]== "MDM" or set[i][0]== "PM" or set[i][0] == "ROP" or set[i][0] == "&&" or set[i][0] == "||" or set[i][0] == "]" or set[i][0] == "AOP" or set[i][0] == ";" or set[i][0] == ")" or set[i][0] == ":" or set[i][0] == "}" or  set[i][0] == ","):

            if(set[i][0]== "("):
                Al = Al_string
                if(F_call1(Al)):
                    return True
            elif(set[i][0] == "UOP"):
                # T.p = lookUpST(N)
                # if (T.p == "null"):
                #     print(N, "Undeclared")
                #     return False
                if (T.p != "int" and T.p != "float"):
                    print("Error:(", T.p, ") Wrong Type For Increment Decrement")
                    return False
                i+=1;
                return True
            elif(set[i][0]== "MDM" or set[i][0]== "PM" or set[i][0] == "ROP" or set[i][0] == "&&" or set[i][0] == "||" or set[i][0] == "]" or set[i][0] == "AOP" or set[i][0] == ";" or set[i][0] == ")" or set[i][0] == ":" or set[i][0] == "}" or  set[i][0] == ","):
                return True

        return False

    def Class():
        global i
        if(set[i][0]== "class"):
            if(set[i][0]== "class"):
                T = set[i][1]
                i+= 1
                if(set[i][0]== "ID"):
                    N = set[i][1]
                    i+= 1
                    P = strings #parent
                    am = strings
                    if(Inher(P, am)):
                        if(set[i][0]== "{"):
                            if(not insertDT(N,T, P.p, 0)):
                                print(N, T, "Redeclaration Error")
                                return False
                            i+= 1
                            if(C_body(N)):
                                if(set[i][0]== "}"):
                                    i+=1
                                    return True
        return False

    def Inher(P,am):
        global i
        if(set[i][0]== ":" or set[i][0] == "{"):

            if(set[i][0] == ":"):
                i+= 1
                if(AM(am)):
                    if(set[i][0]== "ID"):
                        N = set[i][1]
                        T = lookUpDT(N)
                        if not T:
                            print(N , "Undeclared Error")
                            return False
                        P.p = N
                        i+= 1
                        return True
            elif(set[i][0] == "{"):
                P.p = "null"
                return True

        return False

    def C_body(C_name):
        global i,access_modifier
        if(set[i][0]== "AM" or set[i][0] == "static" or set[i][0] == "const" or set[i][0] == "def" or set[i][0] == "DT" or set[i][0] == "ID" or set[i][0] == "}"):

            if(set[i][0] == "AM"):
                am = set[i][1]
                access_modifier = am
                i+=1
                if(set[i][0]== ":"):
                    i+= 1
                    if(C_TM(am, C_name)):
                        if(C_body(C_name)):
                            return True
            elif(set[i][0] == "static" or set[i][0] == "const" or set[i][0] == "def" or set[i][0] == "DT" or set[i][0] == "ID"):
                if(access_modifier == "null"):
                    am = "private"
                else:
                    am = access_modifier
                if(C_TM(am, C_name)):
                    if(C_body(C_name)):
                        return True
            elif(set[i][0]== "}"):
                return True

        return False

    def AM(am):
        global i
        if(set[i][0]== "AM" or set[i]=="ID"):
            if(set[i][0]== "AM"):
                am.p = set[i][1]
                i+= 1
                return True
        elif(set[i][0]== "ID"):
            am.p = "private"
            return True

        return False

    def C_TM(am, C_name):
        global i
        if (set[i][0] == "static" or set[i][0] == "const" or set[i][0] == "def" or set[i][0] == "DT" or set[i][0] == "ID"):
            if(set[i][0] == "static" or set[i][0] == "const"):
              if(TM(am, C_name)):
                  return True
            elif(set[i][0] == "def"):
                i+=1
                tm = strings
                if(F_TM(tm)):
                    if(F_dec1(C_name,am,tm.p)):
                        return True
            elif(set[i][0] == "DT"):
                T = set[i][1]
                i += 1
                if (set[i][0] == "ID"):
                    N = set[i][1]
                    tm = 0
                    if (not insertCDT(C_name, N, T, am, tm)):
                        print(N, "Redeclaration Error")
                        return False
                    i += 1
                    if (Dec(T, am, tm, C_name)):
                        return True
            elif(set[i][0] == "ID"):
                N = set[i][1]
                i+=1
                if(Class1(N , am, C_name)):
                    return True

        return False

    def F_TM(tm):
        global i
        if(set[i][0] == "static" or set[i][0] == "const" or set[i][0] == "virtual" or set[i][0] == "DT" or set[i][0] == "ID"):

            if(set[i][0] == "static"):
                tm.p = set[i][1]
                i+=1
                return True
            elif(set[i][0] == "const"):
                tm.p = set[i][1]
                i+=1
                return True
            elif(set[i][0] == "virtual"):
                tm.p = set[i][1]
                i += 1
                return True
            elif(set[i][0] == "DT" or set[i][0] == "ID"):
                tm.p = ""
                return True

        return False


    def Class1(T, am, C_name):
        global i,scope
        if(set[i][0]== "ID" or set[i][0] == "("):

            if(set[i][0]== "ID"):
                N = set[i][1]
                tm = 0
                if(not insertCDT(C_name, N, T, am, tm)):
                    print(N, "Redeclaration Error")
                    return False
                i+= 1
                if(Dec_O(T, am, tm, C_name)):
                    return True
            elif(set[i][0]== "("):
                if(Constructor(T, am, C_name)):
                    return True
        return False

    def Constructor(T, am, C_name):
        global i,scope_num
        if(set[i][0]== "("):
            scope_num += 1
            s_stack.append(scope_num)
            Type = lookUpDT(T)
            if not Type:
                print(T, "Undeclared Error")
                return False
            i+= 1
            Pl = strings
            if(F2(Pl)):
                if(set[i][0]== ")"):
                    s_stack.pop()
                    if(T != C_name):
                        print("Wrong Class")
                        return False
                    else:
                        if(not insertCDT(C_name, "constructor", Pl.p, am, "null")):
                            print(N, "Redeclaration Error")
                            return False
                        insertFT(C_name, "null", am, Pl.p, "null", "constructor")
                    i+=1
                    if(Body()):
                        return True
        return False

    def Array_ret():
        global i
        if(set[i][0]== "[" or set[i][0] == "ID"):

            if(set[i][0] == "["):
                i+= 1
                if (set[i][0]== "]"):
                    i+=1
                    return True
            elif(set[i][0] == "ID"):
                return True

        return False

    def Array():
        global i
        if (set[i][0] == "[" or set[i][0] == "." or set[i][0] == "(" or set[i][0] == "AOP" or set[i][0] == "UOP" or set[i][0] == ";" or set[i][0] == ")" or set[i][0] == "MDM" or set[i][0] == "PM" or set[i][0] == "ROP" or set[i][0] == "&&" or set[i][0] == "||" or set[i][0] == "]" or set[i][0] == ":" or set[i][0] == "," or set[i][0] == "}"):

            if(set[i][0] == "["):
                i+=1
                T_Oe = strings
                T_name = name_string
                if(OE(T_Oe,T_name)):
                    if(T_Oe.p != "int"):
                        print("Error:(",T_Oe.p,")Wrong Type for Array Size")
                        return False
                    if(set[i][0] == "]"):
                        i+=1
                        return True

            elif(set[i][0] == "." or set[i][0] == "(" or set[i][0] == "AOP" or set[i][0] == "UOP" or set[i][0] == ";" or set[i][0] == ")" or set[i][0] == "MDM" or set[i][0] == "PM" or set[i][0] == "ROP" or set[i][0] == "&&" or set[i][0] == "||" or set[i][0] == "]" or set[i][0] == ":" or set[i][0] == "," or set[i][0] == "}"):
                return True

        return False

    def E(Al):
        global i
        if(set[i][0]== "ID" or set[i][0] == "UOP" or set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const" or set[i][0] == "(" or set[i][0] == "!" or set[i][0] == "this" or set[i][0] == "}" or set[i][0] == ")"):

            if (set[i][0] == "ID" or set[i][0] == "UOP" or set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const" or set[i][0] == "(" or set[i][0] == "!" or set[i][0] == "this"):
                T_Oe = strings
                T_name = name_string
                if(OE(T_Oe,T_name)):
                    Al.als = T_Oe.p
                    if(E1(Al)):
                        return True
            elif(set[i][0] == "}" or set[i][0] ==  ")"):
                return True

        return False

    def E1(Al):
        global i
        if(set[i][0]== "," or set[i][0] == "}" or set[i][0] == ")" ):

            if (set[i][0]== ","):
                i+= 1
                T_Oe = strings
                T_name = name_string
                if(OE(T_Oe,T_name)):
                    Al.als += "," + T_Oe.p
                    if(E1(Al)):
                        return True
            elif(set[i][0] == "}" or set[i][0] == ")"):
                return True

        return False

    def List():
        global i
        if(set[i][0]== "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const" or set[i][0] == "]"):

            if (set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const"):
                if(Const()):
                    if(List1()):
                        return True
            elif(set[i][0] == "]"):
                return True

        return False

    def List1():
        global i
        if(set[i][0]== "," or set[i][0] == "]" ):

            if(set[i][0] == ","):
                i+= 1
                if(Const()):
                    if(List1()):
                        return True
            elif(set[i][0] == "]"):
                return True

        return False

    def Const(T,Na):
        global i
        if(set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const"):

            if(set[i][0] == "int_const"):
                T.p = "int"
                Na.ns = set[i][1]
                i += 1
                return True
            elif(set[i][0] == "float_const"):
                T.p = "float"
                Na.ns = set[i][1]
                i += 1
                return True
            elif (set[i][0] == "string_const"):
                T.p = "string"
                Na.ns = set[i][1]
                i += 1
                return True
            elif (set[i][0] == "char_const"):
                T.p = "char"
                Na.ns = set[i][1]
                i += 1
                return True
            elif (set[i][0] == "bool_const"):
                T.p = "bool"
                Na.ns = set[i][1]
                i += 1
                return True

        return False

    def This():
        global i
        if (set[i][0] == "this"):
            i += 1
            if (set[i][0] == "->"):
                i += 1
                if (set[i][0] == "ID"):
                    i += 1
                    if (Array()):
                        if (L1(Ty, T)):
                            if (L2()):
                                return True
        return False

    start = Start()
    print(start)
    if(start is False):
        print("Error Line No: " , set[i-1][2] , "\nAt: " , set[i][1])


ST = []
s_t = 0
def insertST(N, T, S):
    global s_t
    if not ST:
        ST.append([])
        ST[s_t].append(N)       # 0---Name
        ST[s_t].append(T)       # 1---Type
        ST[s_t].append(S)   # 2---Scope
        s_t += 1
        return True

    for z in range(s_t):
        if(ST[z][0] == N and ST[z][2] == S):
            return False

    ST.append([])
    ST[s_t].append(N)  # 0---Name
    ST[s_t].append(T)  # 1---Type
    ST[s_t].append(S)  # 2---Scope
    s_t += 1
    return True

DT = []
d_t = 0
def insertDT(N, T, P, ref):
    global d_t
    if not DT:
        DT.append([])
        DT[d_t].append(N)  # 0---Name
        DT[d_t].append(T)  # 1---Type
        DT[d_t].append(P)  # 2---Parent
        DT[d_t].append(ref)  # 3---Class Reference
        d_t += 1
        return True

    for z in range(d_t):
        if(DT[z][0] == N and DT[z][1] == T):
            return False

    DT.append([])
    DT[d_t].append(N)       #0---Name
    DT[d_t].append(T)       #1---Type
    DT[d_t].append(P)       #2---Parent
    DT[d_t].append(ref)     #3---Class Reference
    d_t += 1
    return True

CDT = []
c_d_t = 0
def insertCDT(C_name, N, T, AM, TM):
    global c_d_t
    C_info = []

    C_info.append(N)  # 0---Name
    C_info.append(T)  # 1---Type
    C_info.append(AM)  # 2---Acess Modifier
    C_info.append(TM)  # 3---Type Modifier

    if not CDT:
        CDT.append([])
        CDT[c_d_t].append(C_name)
        CDT[c_d_t].append(C_info)
        c_d_t += 1
        return True

    else:
        for z in range(c_d_t):
            if(CDT[z][0] == C_name):
                CDT1 = CDT[z]
                x = len(CDT1)
                y = 1
                for y in range(x):
                    if(CDT1[y][0] == N and  CDT1[y][1] == T):
                        return False
                CDT[z].append(C_info)
                return True

        CDT.append([])
        CDT[c_d_t].append(C_name)
        CDT[c_d_t].append(C_info)
        c_d_t += 1
        return True

FT = []
f_t = 0
def insertFT(C_name, tm, am, Pl, Rt, N):
    global f_t
    if not FT:
        FT.append([])
        FT[f_t].append(C_name)  # 0---Class Name
        FT[f_t].append(tm)  # 1---Type Modifier
        FT[f_t].append(am)  # 2---Access Modifier
        FT[f_t].append(Pl)  # 3---Parameter List
        FT[f_t].append(Rt)  # 4---Return Type
        FT[f_t].append(N)  # 5---Name
        f_t += 1
        return True

    for z in range(f_t):
        if(FT[z][0] == N and FT[z][3] == Pl and FT[z][5] == N):
            return False

    FT.append([])
    FT[f_t].append(C_name)  # 0---Class Name
    FT[f_t].append(tm)  # 1---Type Modifier
    FT[f_t].append(am)  # 2---Access Modifier
    FT[f_t].append(Pl)  # 3---Parameter List
    FT[f_t].append(Rt)  # 4---Return Type
    FT[f_t].append(N)  # 5---Name
    f_t += 1
    return True

def lookUpFT(C_name, N, T):
    for z in range(f_t):
        if (FT[z][0] == C_name and FT[z][3] == T and FT[z][5] == N):
            return FT[z][4]
    return "null"


def lookUpST(N):
    size = len(s_stack)
    ss = size -1
    for s in range(size):
        for z in range(s_t):
            if(ST[z][0] == N and ST[z][2] == s_stack[ss]):
                return ST[z][1]
        ss -= 1

    return "null"

def lookUpDT(N):
    for z in range(d_t):
        if(DT[z][0] == N):
            return DT[z][1]
    return "null"

def lookUpCDT(C_name, N):
    for z in range(c_d_t):
        if(CDT[z][0] == C_name):
            CDT1 = CDT[z]
            x = len(CDT1)
            y = 1
            for y in range(x):
                if (CDT1[y][0] == N and CDT1[y][2] == "public"):
                    return CDT1[y][1]
    return "null"

def compatibility(TL, TR, OP):
    # print(TL,TR,OP)

    if(TL == "int" and TR == "int" and (OP == "=" or OP == "+" or OP == "-" or OP == "*" or OP == "/" or OP == "%" or OP == "%" or OP == "-=" or OP == "*=" or OP == "/=" or OP == "%=" or OP == "&&" or OP == "||" or OP == "==" or OP == "<=" or OP == ">=" or OP == "!=" or OP == "<" or OP == ">")):
        return "int"

    elif((TL == "float" and TR == "int") or (TL == "int" and TR == "float") or (TL == "float" and TR == "float") and (OP == "=" or OP == "+" or OP == "-" or OP == "*" or OP == "/" or OP == "%" or OP == "%" or OP == "-=" or OP == "*=" or OP == "/=" or OP == "%=" or OP == "&&" or OP == "||" or OP == "==" or OP == "<=" or OP == ">=" or OP == "!=" or OP == "<" or OP == ">")):
        return "float"

    elif(TL == "string" and TR == "string" and (OP == "=" or OP == "+" or OP == "+=" or OP == "&&" or OP == "||" or OP == "==" or OP == "<=" or OP == ">=" or OP == "!=" or OP == "<" or OP == ">")):
        return "string"

    elif((TL == "char" and TR == "char") or (TL == "bool" and TR == "bool") and (OP == "=" or OP == "&&" or OP == "||" or OP == "==" or OP == "<=" or OP == ">=" or OP == "!=" or OP == "<" or OP == ">")):
            if(TL == "char" and TR == "char"):
                return "char"
            if(TL == "bool" and TR == "bool"):
                return "bool"
    elif(TL == TR and OP == "="):
            return TL
    return "null"

class strings:
    p = ""

class name_string:
    ns = ""

class Al_string:
    als = ""

Lexical_Analyzer()
Syntax_Analyzer()
print("ST",ST ,"\nDT", DT , "\nCDT", CDT, "\nFT", FT)