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
            'true': 'bool-constant',
            'false': 'bool-constant',
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
            'static': 'static'
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

scope = 0
i = 0
def Syntax_Analyzer():

    def Start():
        global i,scope
        if(set[i][0]== "DT" or set[i][0] == "ID" or set[i][0] == "UOP" or set[i][0] == "static" or set[i][0] == "virtual" or set[i][0] == "const" or set[i][0] == "if" or set[i][0] == "class" or set[i][0] == "while" or set[i][0] == "for" or set[i][0] == "switch" or set[i][0] == "$"):

            if(set[i][0] == "$"):
                return True
            elif(set[i][0]== "DT" or set[i][0] == "ID" or set[i][0] == "UOP" or set[i][0] == "static" or set[i][0] == "virtual" or set[i][0] == "const" or set[i][0] == "if" or set[i][0] == "class" or set[i][0] == "while" or set[i][0] == "for" or set[i][0] == "switch"):
                if(MST()):
                    return True

        return False

    def MST():
        global i
        if(set[i][0]== "DT" or set[i][0] == "ID" or set[i][0] == "UOP" or set[i][0] == "static" or set[i][0] == "virtual" or set[i][0] == "const" or set[i][0] == "if" or set[i][0] == "class" or set[i][0] == "while" or set[i][0] == "for" or set[i][0] == "switch" or set[i][0] == "$"):

            if (set[i][0] == "$"):
                return True
            elif(set[i][0]== "DT" or set[i][0] == "ID" or set[i][0] == "UOP" or set[i][0] == "static" or set[i][0] == "virtual" or set[i][0] == "const" or set[i][0] == "if" or set[i][0] == "class" or set[i][0] == "while" or set[i][0] == "for" or set[i][0] == "switch"):
                if(SST()):
                    if(MST()):
                        return True

        return False

    def SST():
        global i
        if (set[i][0]== "DT" or set[i][0] == "ID" or set[i][0] == "UOP" or set[i][0] == "static" or set[i][0] == "virtual" or set[i][0] == "const" or set[i][0] == "if" or set[i][0] == "class" or set[i][0] == "while" or set[i][0] == "for" or set[i][0] == "switch"):

            if(set[i][0]== "DT"):
                # T = set[i][1]
                i+= 1
                if(SST1()):#T
                    return True
            elif(set[i][0]== "ID"):
                # N = set[i][1]
                i+= 1
                if(SST2()):#N
                    return True
            elif(set[i][0] == "UOP"):
                if(Inc_dec()):
                    if(set[i][0] == ";"):
                        i+=1
                        return True
            elif(set[i][0] == "static" or set[i][0] == "const"):
                if(TM()):
                    return True
            elif(set[i][0] == "if"):
                if(If()):
                    return True
            elif(set[i][0] == "class"):
                if(Class()):
                    return True
            elif(set[i][0] == "while"):
                if (While()):
                    return True
            elif(set[i][0] == "for"):
                if(For()):
                    return True
            elif(set[i][0] == "switch"):
                if(Switch()):
                    return True

        return False

    def SST1():#T
        global i,scope
        if(set[i][0]== "[" or set[i][0] == "ID" ):

            if(set[i][0]== "["):
                i+= 1
                if(set[i][0]== "]"):
                    i+=1
                    if(set[i][0]== "ID"):
                        i+= 1
                        if(F_dec()):
                            return True
            elif(set[i][0]== "ID"):
                # N = set[i][1]
                i+= 1
                if(X1()):#N,T
                    return True

        return False

    def X1():#N,T
        global i,scope
        if(set[i][0]== "AOP" or set[i][0] == "[" or set[i][0] == "," or set[i][0] == "(" or set[i][0] == ";"):

            if(set[i][0]== "AOP" or set[i][0] == "[" or set[i][0] == "," or set[i][0] == ";"):
                # if(not insertST(N,T,scope)):
                #     print(N, T, scope)
                #     print("Redeclaration Error")
                #     return False
                if(Dec()):#T
                    return True
            elif(set[i][0] == "("):
                if(F_dec()):
                    return True

        return False

    def SST2(): #previous name P_N
        global i,scope
        if(set[i][0]== "ID" or set[i][0] == "[" or set[i][0] == "." or set[i][0] == "(" or set[i][0] == "AOP" or set[i][0] == "UOP"):

            if(set[i][0]== "ID"):
                # T = lookUpDT(P_N)
                # if(not T):
                #     print(P_N, "is Undeclared")
                #     return False
                #
                # N = set[i][1]
                # if(not insertST(N,P_N,scope)):
                #     print(N,P_N,scope)
                #     print("Redeclaration Error")
                #     return False
                i+= 1
                if(Z()):
                    return True
            elif(set[i][0] == "[" or set[i][0] == "." or set[i][0] == "(" or set[i][0] == "AOP" or set[i][0] == "UOP"):
                # T = lookUpST(P_N)
                # if (not T):
                #     print(P_N, "is Undeclared")
                #     return False

                if(Array()):
                    if(L1()):#T
                        if(L2()):
                            return True
        return False

    def Z():
        global i
        if (set[i][0] == "[" or set[i][0] == "," or set[i][0] == "AOP" or set[i][0] == ";" or set[i][0] == "("):
            if (set[i][0] == "[" or set[i][0] == "," or set[i][0] == "AOP" or set[i][0] == ";"):
                if (Dec_O()):
                    return True
            elif (set[i][0] == "("):
                i += 1
                if (Z1()):
                    return True
        return False

    def Z1():
        global i
        if (set[i][0] == "DT" or set[i][0] == "UOP" or set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const" or set[i][0] == "(" or set[i][0] == "!" or set[i][0] == "ID" or set[i][0] == ")"):
            if(set[i][0] == "DT"):
                i+=1
                if(set[i][0] == "ID"):
                    i+=1
                    if(F3()):
                        if(set[i][0] == ")"):
                            if(Body()):
                                return True
            elif(set[i][0] == "UOP" or set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const" or set[i][0] == "(" or set[i][0] == "!"):
                if(O_paran()):
                    if(E1()):
                        if(set[i][0] == ")"):
                            i += 1
                            if(set[i][0] == ";"):
                                i += 1
                                return True
            elif(set[i][0] == "ID"):
                i+=1
                if(Z2()):
                    return True
            elif(set[i][0] == ")"):
                i+=1
                if(Body()):
                    return True
        return False

    def O_paran():
        global i
        if (set[i][0] == "UOP" or set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const" or set[i][0] == "(" or set[i][0] == "!"):

            if (set[i][0] == "UOP"):
                if (Inc_dec()):
                    return True
            elif (set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const"):
                if (Const()):
                    return True
            elif(set[i][0] == "("):
                i+=1
                if(OE()):
                    if(set[i][0] == ")"):
                        i+=1
                        return True
            elif(set[i][0] == "!"):
                i+=1
                if(T()):
                    return True
        return False

    def Z2():
        global i
        if (set[i][0] == "ID" or set[i][0] == "[" or set[i][0] == "." or set[i][0] == "(" or set[i][0] == "UOP" or set[i][0] == "," or set[i][0] == ")"):
            if(set[i][0] == "ID"):
                i+=1
                if(F3()):
                    if(set[i][0] == ")"):
                        i+=1
                        if(Body()):
                            return True
            elif(set[i][0] == "[" or set[i][0] == "." or set[i][0] == "(" or set[i][0] == "UOP" or set[i][0] == "," or set[i][0] == ")"):
                if(Array()):
                    if(T1()):
                        if(T2()):
                            if(E1()):
                                if (set[i][0] == ")"):
                                    i += 1
                                    if (set[i][0] == ";"):
                                        i += 1
                                        return True
        return False

    def L1():#T
        global i
        if(set[i][0] == "(" or set[i][0] ==  "AOP" or set[i][0] == "UOP" or set[i][0] == ";" or set[i][0] ==  ")" or set[i][0] == "." ):

            if(set[i][0]== "."):
                # OP = set[i][1]
                i+= 1
                if(set[i][0]== "ID"):
                    # N = set[i][1]
                    # T1 = lookUpST(N)
                    # if(not T1):
                    #     print(N, "Undecleared")
                    #     return False
                    # Type = compatibility(T,T1,OP)
                    # if(not Type):
                    #     print("Type Miss Match")
                    i+= 1
                    if(Array()):
                        if(L1()):#T
                            return True
            elif(set[i][0] == "(" or set[i][0] ==  "AOP" or set[i][0] == "UOP" or set[i][0] == ";" or set[i][0] ==  ")"):
                return True

        return False

    def L2():
        global i
        if(set[i][0]== "(" or set[i][0] == "AOP" or set[i][0] == "UOP"):

            if(set[i][0]== "("):
                if(F_call()):
                    return True
            elif(set[i][0] == "AOP"):
                if(Assign()):
                    if(set[i][0] == ";"):
                        i+=1
                        return True
            elif(set[i][0] == "UOP"):
                i += 1
                if (set[i][0] == ";"):
                    i += 1
                    return True
        return False

    def TM():
        global i
        if(set[i][0]== "static" or set[i][0] == "const"):

            if(set[i][0]== "static"):
                i+=1
                if(STM()):
                    return True
            elif(set[i][0] == "const"):
                i+=1
                if(CTM()):
                    return True
        return False

    def STM():
        global i
        if(set[i][0]== "DT" or set[i][0] == "ID"):

            if(set[i][0]== "DT"):
                i+=1
                if(SST1()):#T
                    return True
            elif(set[i][0] == "ID"):
                i+=1
                if(set[i][0] == "ID"):
                    i+=1
                    if(Z()):
                        return True
        return False

    def CTM():
        global i
        if(set[i][0]== "DT" or set[i][0] == "ID"):

            if(set[i][0]== "DT"):
                i+=1
                if(CTM1()):
                    return True
            elif(set[i][0] == "ID"):
                i+=1
                if(set[i][0] == "ID"):
                    i+=1
                    if(Z()):
                        return True
        return False

    def CTM1():
        global i
        if(set[i][0]== "ID" or set[i][0] == "["):

            if(set[i][0]== "ID"):
                i+=1
                if(CTM2()):
                    return True
            elif(set[i][0] == "["):
                i+=1
                if (set[i][0] == "]"):
                    i += 1
                    if (set[i][0] == "ID"):
                        i += 1
                        if (F_dec()):
                            return True
        return False

    def CTM2():
        global i
        if (set[i][0] == "AOP" or set[i][0] == "("):

            if (set[i][0] == "AOP"):
                if (Assign()):
                    if(set[i][0] == ";"):
                        i+=1
                        return True
            elif (set[i][0] == "("):
                if(F_dec()):
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
        if (set[i][0]== "DT" or set[i][0] == "ID" or set[i][0] == "while" or set[i][0] == "for" or set[i][0] == "if" or set[i][0] == "switch" or set[i][0] == "inc_dec" or set[i][0] == "break" or set[i][0] == "continue" or set[i][0] == "return" or set[i][0] == "}" or set[i][0] == "this"):

            if(set[i][0]== "DT" or set[i][0] == "ID" or set[i][0] == "while" or set[i][0] == "for" or set[i][0] == "if" or set[i][0] == "switch" or set[i][0] == "inc_dec" or set[i][0] == "break" or set[i][0] == "continue" or set[i][0] == "return" or set[i][0] == "this"):
                if(SST_B()):
                    if(MST_B()):
                        return True
            elif(set[i][0] == "}"):
                return True
        return False

    def SST_B():
        global i
        if (set[i][0]== "DT" or set[i][0] == "ID" or set[i][0] == "while" or set[i][0] == "for" or set[i][0] == "if" or set[i][0] == "switch" or set[i][0] == "AOP" or set[i][0] == "break" or set[i][0] == "continue" or set[i][0] == "return" or set[i][0] == "this"):
            if(set[i][0]== "DT"):
                i+= 1
                if(set[i][0]== "ID"):
                    i+=1
                    if(Dec()):#T
                        return True
            elif(set[i][0]== "ID"):
                i+= 1
                if(SST_B1()):
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

    def SST_B1():
        global i
        if (set[i][0] == "ID" or set[i][0] == "[" or set[i][0] == "." or set[i][0] == "(" or set[i][0] == "UOP" or set[i][0] == "AOP"):
            if (set[i][0] == "ID"):
                i += 1
                if (SST_B2()):
                    return True
            elif (set[i][0] == "[" or set[i][0] == "." or set[i][0] == "(" or set[i][0] == "AOP" or set[i][0] == "UOP"):
                    # T = lookUpST(P_N)
                    # if (not T):
                    #     print(P_N, "is Undeclared")
                    #     return False

                    if (Array()):
                        if (L1()):#T
                            if (L2()):
                                return True
        return False

    def SST_B2():
        global i
        if (set[i][0] == "[" or set[i][0] == "," or set[i][0] == "AOP" or set[i][0] == ";" or set[i][0] == "("):
            if (set[i][0] == "[" or set[i][0] == "," or set[i][0] == "AOP" or set[i][0] == ";"):
                if (Dec_O()):
                    return True
            elif (set[i][0] == "("):
                i += 1
                if (E()):
                    if (set[i][0] == ")"):
                        i += 1
                        if (set[i][0] == ";"):
                            i += 1
                            return True
        return False


    def Dec():#T
        global i
        if(set[i][0] == "AOP" or set[i][0] == "[" or set[i][0] == "," or set[i][0] == ";"):
            if(set[i][0] == "AOP" or set[i][0] == "[" or set[i][0] == "," or set[i][0] == ";"):
                if(D()):#T
                    if(set[i][0] == ";"):
                        i+=1
                        return True
        return False

    def D():#T
        global i
        if (set[i][0] == "AOP" or set[i][0] == "[" or set[i][0] == "," or set[i][0] == ";"):

            if(set[i][0] == ","):
                if(D_comma()):#T
                    return True
            elif(set[i][0] == "AOP"):
                    if(Assign()):
                        return True
            elif(set[i][0] == "["):
                i+=1
                if(OE()):
                    if(set[i][0] == "]"):
                        i+=1
                        if(D_array()):
                            return True
            elif(set[i][0] == ";"):
                return True

        return False

    def D_array():
        global i
        if (set[i][0] == "," or set[i][0] == "AOP" or set[i][0] == ";"):

            if(set[i][0] == ","):
                i+=1
                if(set[i][0] == "ID"):
                    i+=1
                    if(set[i][0] == "["):
                        i+=1
                        if(OE()):
                            if(set[i][0] == "]"):
                                i+=1
                                if(D_array()):
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

    def D_comma():#T
        global i
        if(set[i][0] == "," or set[i][0] == ";"):

            if(set[i][0] == ","):
                i+=1
                if(set[i][0] == "ID"):
                    # N = set[i][1]
                    # if (not insertST(N, T, scope)):
                    #     print(N, T, scope)
                    #     print("Redeclaration Error")
                    i+=1
                    if(D_comma()):#T
                        return True
            elif(set[i][0] == ";"):
                return True

        return False

    def Dec_O():
        global i
        if(set[i][0] == "[" or set[i][0] == "," or set[i][0] == "AOP" or set[i][0] == ";" ):
            if(Object()):
                if(set[i][0] == ";"):
                    i+=1
                    return True
        return False

    def Object():
        global i
        if(set[i][0] == "[" or set[i][0] == "," or set[i][0] == "AOP" or set[i][0] == ";" ):

            if(set[i][0] == "[" or set[i][0] == ","):
                if(O()):
                    return True
            elif(set[i][0] == "AOP"):
                if(O_assign()):
                    return True
            elif(set[i][0] == ";"):
                return True

        return False

    def O():
        global i
        if(set[i][0] == "[" or set[i][0] == "," or set[i][0] == ";"):

            if(set[i][0] == "["):
                if(O_array()):
                    return True
            elif(set[i][0] == ","):
                if(O_comma()):
                    return True
            elif (set[i][0] == ";"):
                return True

        return False

    def O_array():
        global i
        if(set[i][0] == "["):

            if (set[i][0] == "["):
                i+=1
                if(OE()):
                    if(set[i][0] == "]"):
                        i+=1
                        if(O_comma()):
                            return True
        return False

    def O_comma():
        global i
        if(set[i][0] == "," or set[i][0] == ";"):

            if (set[i][0] == ","):
                i+=1
                if(set[i][0] == "ID"):
                    i+=1
                    if(O()):
                         return True
            elif (set[i][0] == ";"):
                return True

        return False

    def O_assign():
        global i
        if (set[i][0] == "AOP" or set[i][0] == "," or set[i][0] == ";"):

            if(set[i][0] == "AOP"):
                i += 1
                if (set[i][0] == "ID"):
                    i += 1
                    if (O_assign1()):
                        if(O_assign2()):
                            return True
            elif(set[i][0] == "," or set[i][0] == ";"):
                return True

        return False

    def O_assign1():
        global i
        if (set[i][0] == "AOP" or set[i][0] == "(" or set[i][0] == "," or set[i][0] == ";"):

            if (set[i][0] == "AOP"):
                if (O_assign()):
                    return True
            elif(set[i][0] == "("):
                if(F_call1()):
                    if(O_assign()):
                        return True
            elif(set[i][0] == "," or set[i][0] == ";"):
                return True

        return False

    def O_assign2():
        global i
        if (set[i][0] == "," or set[i][0] == ";"):

            if(set[i][0] == ","):
                i += 1
                if(set[i][0] == "ID"):
                    i += 1
                    if (O_assign()):
                        return True
            elif(set[i][0] == ";"):
                return True

        return False

    # def F1(TM):
    #     global i,scope
    #     if(set[i][0]== "DT" or set[i][0] == "ID" ):
    #         if(set[i][0]== "DT"):
    #             RT = set[i][1]
    #             i+= 1
    #             if(Array_ret()):
    #                 if(set[i][0]== "ID"):
    #                     N = set[i][1]
    #                     i+= 1
    #                     if(set[i][0]== "("):
    #                         scope += 1
    #                         i+= 1
    #                         PL = parameter # Parameter List Object
    #                         if(F2(PL)):
    #                             PL.p += "->" + RT
    #                             print("PL",PL.p)
    #                             if(set[i][0] == ")" ):
    #                                 if(not insertDT(N, PL.p, TM, 0)):
    #                                     print(N,PL.p)
    #                                     print("Redeclaration Error")
    #                                 i+=1
    #                                 if(Body()):
    #                                     return True
    #         elif (set[i][0]== "ID"):
    #             i+= 1
    #             if (Array_ret()):
    #                 if (set[i][0]== "ID"):
    #                     i+= 1
    #                     if (set[i][0]== "("):
    #                         i+= 1
    #                         if (F2()):
    #                             if(set[i][0] == ")" ):
    #                                 if (Body()):
    #                                     return True
    #     return False



    def F_dec():
        global i
        if(set[i][0]== "("):
            i+= 1
            if(F2()):
                if(set[i][0] == ")"):
                    i+=1
                    if(Body()):
                        return True
        return False

    def F2():#PL
        global i
        if(set[i][0]== "DT" or set[i][0] == "ID" or set[i][0] == ")"):

            if(set[i][0]== "DT"):
                # T = set[i][1]
                # PL.p += T
                i+= 1
                if(set[i][0]== "ID"):
                    # N = set[i][1]
                    # if (not insertST(N, T, scope)):
                    #     print(N, T, scope)
                    #     print("Redeclaration Error")
                    #     return False
                    i+= 1
                    if(Array()):
                        if(F3()):#PL
                            return True
            elif(set[i][0]== "ID"):
                i+= 1
                if (set[i][0]== "ID"):
                    i+= 1
                    if(Array()):
                        if (F3()):#PL
                            return True
            elif(set[i][0] == ")"):
                return True
        return False

    def F3():#PL
        global i
        if(set[i][0]== "," or set[i][0] == ")"):

            if(set[i][0] == ","):
                i+= 1
                if(F4()):#PL
                    return True
            elif(set[i][0] == ")"):
                return True

        return False

    def F4():#PL
        global i
        if(set[i][0]== "DT" or set[i][0] == "ID"):

            if(set[i][0]== "DT"):
                # T = set[i][1]
                # PL.p += ","
                # PL.p += T
                i+= 1
                if(set[i][0]== "ID"):
                    # N = set[i][1]
                    # if (not insertST(N, T, scope)):
                    #     print(N, T, scope)
                    #     print("Redeclaration Error")
                    #     return False
                    i+= 1
                    if(Array()):
                        if(F3()):#PL
                            return True
            elif(set[i][0]== "ID"):
                i+= 1
                if (set[i][0]== "ID"):
                    i+= 1
                    if(Array()):
                        if (F3()):
                            return True
        return False

    def F_call():
        global i
        if(set[i][0]== "("):

            if(set[i][0]== "("):
                i+= 1
                if(E()):
                    if(set[i][0]== ")"):
                        i+=1
                        if(set[i][0]== ";"):
                            i+= 1
                            return True

        return False
    def F_call1():
        global i
        if(set[i][0]== "("):
            i+= 1
            if(E()):
                if(set[i][0]== ")"):
                    i+=1
                    return True
        return False

    def Assign():
        global i
        if(set[i][0] == "AOP"):

            if(set[i][0] == "AOP"):
                i+=1
                if(A()):
                    if(A2()):
                        return True
        return False

    def A():
        global i
        if (set[i][0] == "ID" or set[i][0] == "[" or set[i][0] == "UOP" or set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const" or set[i][0] == "(" or set[i][0] == "this" or set[i][0] == "!"):

            if (set[i][0] == "ID"):
                i += 1
                if(A1()):
                    return True
            elif(set[i][0] == "["):
                i+=1
                if(List()):
                    if(set[i][0] == "]"):
                        i+=1
                        return True
            elif (set[i][0] == "UOP"):
                if (Inc_dec()):
                    if (set[i][0] == ";"):
                        i += 1
                        return True
            elif (set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const"):
                if (Const()):
                    return True
            elif (set[i][0] == "("):
                i += 1
                if (OE()):
                    if (set[i][0] == ")"):
                        i += 1
                        return True
            elif (set[i][0] == "!"):
                i += 1
                if (T()):
                    return True
            elif (set[i][0] == "this"):
                i += 1
                if (set[i][0] == "->"):
                    i += 1
                    if (set[i][0] == "ID"):
                        i += 1
                        if (Array()):
                            # if (T1()):
                            return True

        return False

    def A1():
        global i
        if(set[i][0] == "AOP" or set[i][0] == ";" or set[i][0] == "." or set[i][0] == "UOP" or set[i][0] == "(" or set[i][0] == ","):

            if(set[i][0] == "AOP"):
                i+=1
                if(A()):
                    return True
            elif(set[i][0] == "." or set[i][0] == "UOP" or set[i][0] == "("):
                if(T1()):
                    if(T2()):
                        return True
            elif(set[i][0] == ";" or set[i][0] == ","):
                return True

        return False

    def A2():
        global i
        if (set[i][0] == "," or set[i][0] == ";"):

            if (set[i][0] == ","):
                i += 1
                if (set[i][0] == "ID"):
                    i += 1
                    if(set[i][0] == "AOP"):
                        i += 1
                        if(A()):
                            return True

            elif (set[i][0] == ";"):
                return True

        return False


    def Inc_dec():
        global i
        if(set[i][0]== "UOP"):
            i+= 1
            if(set[i][0]== "ID"):
                i+= 1
                if(Array()):
                    if(L1()):
                        return True

        return False

    def While():
        global i
        if(set[i][0]== "while"):
            i+= 1
            if(set[i][0]== "("):
                i+= 1
                if(OE()):
                    if(set[i][0]== ")"):
                        i+=1
                        if(Body()):
                            return True
        return False

    def For():
        global i
        if(set[i][0]== "for"):
            i+= 1
            if(set[i][0]== "("):
                i+= 1
                if(C1()):
                    if(C2()):
                        if(set[i][0]== ";"):
                            i+= 1
                            if(C3()):
                                if(set[i][0]== ")"):
                                    i+=1
                                    if(Body()):
                                        return True
        return False

    def C1():
        global i
        if(set[i][0]== "ID" or set[i][0] == "DT" or set[i][0] == ";"):

            if(set[i][0]== "ID"):
                i+= 1
                if(Dec(T)):
                    return True
            elif(set[i][0]== "DT"):
                i+= 1
                if(set[i][0]== "ID"):
                    i+= 1
                    if(Dec()):#T
                        return True
            elif(set[i][0] == ";"):
                i+=1
                return True

        return False

    def C2():
        global i
        if(set[i][0]== "ID" or set[i][0] == "UOP" or set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const" or set[i][0] == "(" or set[i][0] == "!" or set[i][0] == "this" or set[i][0] == ";" ):

            if (set[i][0] == "ID" or set[i][0] == "UOP" or set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const" or set[i][0] == "(" or set[i][0] == "!" or set[i][0] == "this"):
                if(OE()):
                    return True
            elif(set[i][0] == ";"):
                return True

        return False

    def C3():
        global i
        if (set[i][0] == "ID" or set[i][0] == "UOP" or set[i][0] == ")"):

            if (set[i][0] == "ID"):
                i += 1
                if (Array()):
                    if (L1()):
                        if(C4()):
                            return True
            elif(set[i][0] == "UOP"):
                if(Inc_dec()):
                    return True
            elif(set[i][0] == ")"):
                return True

        return False

    def C4():
        global i
        if(set[i][0]== "(" or set[i][0] == "AOP" or set[i][0] == "UOP"):

            if(set[i][0]== "("):
                if(F_call()):
                    return True
            elif(set[i][0] == "AOP"):
                i+=1
                if(OE()):
                    return True
            elif(set[i][0] == "UOP"):
                i+=1
                return True

        return False

    def If():
        global i
        if(set[i][0]== "if"):
            i+=1
            if(set[i][0]== "("):
                i+= 1
                if(OE()):
                    if(set[i][0]== ")"):
                        i+=1
                        if(Body()):
                            if(Else()):
                                return True
        return False

    def Else():
        global i
        if(set[i][0]== "else" or set[i][0] == "DT" or set[i][0] == "ID" or set[i][0] == "UOP" or set[i][0] == "static" or set[i][0] == "virtual" or set[i][0] == "const" or set[i][0] == "class" or set[i][0] == "while" or set[i][0] == "for" or set[i][0] == "$" or set[i][0] == "if" or set[i][0] == "switch" or set[i][0] == "break" or set[i][0] == "continue" or set[i][0] == "return" or set[i][0] ==  "}" ):

            if(set[i][0] == "else"):
                i+= 1
                if(Else1()):
                    return True
            elif(set[i] == "DT" or set[i][0] == "ID" or set[i][0] == "inc_dec" or set[i][0] == "static" or set[i][0] == "virtual" or set[i][0] == "const" or set[i][0] == "class" or set[i][0] == "while" or set[i][0] == "for" or set[i][0] == "$" or set[i][0] == "if" or set[i][0] == "switch" or set[i][0] == "break" or set[i][0] == "continue" or set[i][0] == "return" or set[i][0] ==  "}" ):
                return True

        return False

    def Else1():
        global i
        if(set[i][0]== "if" or set[i][0]== "{" or set[i][0]== ","):
            if(If()):
                return True
            elif(Body()):
                return True
        return False

    def Switch():
        global i
        if(set[i][0]== "switch"):
            i+= 1
            if(set[i][0]== "("):
                i+= 1
                if(OE()):
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
                if(OE()):
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
                i+= 1
                if(OE()):
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
                if(OE()):
                    return True
            elif(set[i][0] == ";"):
                return True

        return False

    def OE():
        global i
        if ( set[i][0]== "ID" or set[i][0] == "UOP" or set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const" or set[i][0] == "(" or set[i][0] == "!" or set[i][0] == "this" ):
            if(AE()):
                if(OE_()):
                    return True
        return False

    def OE_():
        global i
        if(set[i][0]== "||" or set[i][0] == "]" or set[i][0] == "AOP" or set[i][0] == ";" or set[i][0] == ")" or set[i][0] == ":" or set[i][0] == "}" or  set[i][0] == ","):

            if(set[i][0] == "||"):
                i+= 1
                if(AE()):
                    if(OE_()):
                        return True
            elif(set[i][0] == "]" or set[i][0] == "AOP" or set[i][0] == ";" or set[i][0] == ")" or set[i][0] == ":" or set[i][0] == "}" or  set[i][0] == ","):
                return True

        return False

    def AE():
        global i
        if( set[i][0]== "ID" or set[i][0] == "UOP" or set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const" or set[i][0] == "(" or set[i][0] == "UOP" or set[i][0] == "this" ):
            if(ROP()):
                if(AE_()):
                    return True
        return False

    def AE_():
        global i
        if(set[i][0] == "&&" or set[i][0] == "||" or set[i][0] == "]" or set[i][0] == "AOP" or set[i][0] == ";" or set[i][0] == ")" or set[i][0] == ":" or set[i][0] == "}" or  set[i][0] == ","):

            if(set[i][0]== "&&"):
                i+= 1
                if(ROP()):
                    if(AE_()):
                        return True
            elif(set[i][0] == "||" or set[i][0] == "]" or set[i][0] == "AOP" or set[i][0] == ";" or set[i][0] == ")" or set[i][0] == ":" or set[i][0] == "}" or  set[i][0] == ","):
                return True

        return False

    def ROP():
        global i
        if( set[i][0]== "ID" or set[i][0] == "UOP" or set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const" or set[i][0] == "(" or set[i][0] == "UOP" or set[i][0] == "this"):
            if (PM()):
                if (ROP_()):
                    return True
        return False

    def ROP_():
        global i
        if(set[i][0] == "ROP" or set[i][0] == "&&" or set[i][0] == "||" or set[i][0] == "]" or set[i][0] == "AOP" or set[i][0] == ";" or set[i][0] == ")" or set[i][0] == ":" or set[i][0] == "}" or  set[i][0] == ","):

            if (set[i][0] == "ROP"):
                i+=1
                if(PM()):
                    if(ROP_()):
                        return True
            elif (set[i][0] == "&&" or set[i][0] == "||" or set[i][0] == "]" or set[i][0] == "AOP" or set[i][0] == ";" or set[i][0] == ")" or set[i][0] == ":" or set[i][0] == "}" or  set[i][0] == ","):
                return True

        return False

    def PM():
        global i
        if( set[i][0]== "ID" or set[i][0] == "UOP" or set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const" or set[i][0] == "(" or set[i][0] == "!" or set[i][0] == "this"):
            if (MDM()):
                if (PM_()):
                    return True
        return False

    def PM_():
        global i
        if(set[i][0]== "PM" or set[i][0] == "ROP" or set[i][0] == "&&" or set[i][0] == "||" or set[i][0] == "]" or set[i][0] == "AOP" or set[i][0] == ";" or set[i][0] == ")" or set[i][0] == ":" or set[i][0] == "}" or  set[i][0] == ","):

            if(set[i][0] == "PM"):
                i += 1
                if(MDM()):
                    if(PM_()):
                        return True
            elif(set[i][0] == "ROP" or set[i][0] == "&&" or set[i][0] == "||" or set[i][0] == "]" or set[i][0] == "AOP" or set[i][0] == ";" or set[i][0] == ")" or set[i][0] == ":" or set[i][0] == "}" or  set[i][0] == ","):
                return True

        return False

    def MDM():
        global i
        if( set[i][0]== "ID" or set[i][0] == "UOP" or set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const" or set[i][0] == "(" or set[i][0] == "!" or set[i][0] == "this"):
            if (T()):
                if (MDM_()):
                    return True
        return False

    def MDM_():
        global i
        if (set[i][0]== "MDM" or set[i][0]== "PM" or set[i][0] == "ROP" or set[i][0] == "&&" or set[i][0] == "||" or set[i][0] == "]" or set[i][0] == "AOP" or set[i][0] == ";" or set[i][0] == ")" or set[i][0] == ":" or set[i][0] == "}" or  set[i][0] == ","):

            if(set[i][0] == "MDM" ):
                i += 1
                if(T()):
                    if(MDM_()):
                        return True
            elif(set[i][0]== "PM" or set[i][0] == "ROP" or set[i][0] == "&&" or set[i][0] == "||" or set[i][0] == "]" or set[i][0] == "AOP" or set[i][0] == ";" or set[i][0] == ")" or set[i][0] == ":" or set[i][0] == "}" or  set[i][0] == ","):
                return True

        return False

    def T():
        global i
        if(set[i][0]== "ID" or set[i][0] == "UOP" or set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const" or set[i][0] == "(" or set[i][0] == "this" or set[i][0] == "!"):

            if(set[i][0]== "ID"):
                i+= 1
                if(Array()):
                    if(T1()):
                        if(T2()):
                            return True
            elif(set[i][0] == "UOP"):
                if(Inc_dec()):
                    if(set[i][0] == ";"):
                        i+=1
                        return True
            elif(set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const"):
                if(Const()):
                    return True
            elif(set[i][0]== "("):
                i+= 1
                if(OE()):
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

    def T1():
        global i
        if(set[i][0]== "[" or set[i][0] == "." or set[i][0] == "(" or set[i][0] == "UOP" or set[i][0]== "MDM" or set[i][0]== "PM" or set[i][0] == "ROP" or set[i][0] == "&&" or set[i][0] == "||" or set[i][0] == "]" or set[i][0] == "AOP" or set[i][0] == ";" or set[i][0] == ")" or set[i][0] == ":" or set[i][0] == "}" or  set[i][0] == ","):

            if(set[i][0] == "."):
                    i+=1
                    if(set[i][0] == "ID"):
                        i+=1;
                        if(Array()):
                            if(T1()):
                                return True
            elif(set[i][0] == "(" or set[i][0] == "UOP" or set[i][0]== "MDM" or set[i][0]== "PM" or set[i][0] == "ROP" or set[i][0] == "&&" or set[i][0] == "||" or set[i][0] == "]" or set[i][0] == "AOP" or set[i][0] == ";" or set[i][0] == ")" or set[i][0] == ":" or set[i][0] == "}" or  set[i][0] == ","):
                return True

        return False

    def T2():
        global i
        if(set[i][0] == "(" or set[i][0] == "UOP" or set[i][0]== "MDM" or set[i][0]== "PM" or set[i][0] == "ROP" or set[i][0] == "&&" or set[i][0] == "||" or set[i][0] == "]" or set[i][0] == "AOP" or set[i][0] == ";" or set[i][0] == ")" or set[i][0] == ":" or set[i][0] == "}" or  set[i][0] == ","):

            if(set[i][0]== "("):
                if(F_call1()):
                    return True
            elif(set[i][0] == "UOP"):
                i+=1;
                return True
            elif(set[i][0]== "MDM" or set[i][0]== "PM" or set[i][0] == "ROP" or set[i][0] == "&&" or set[i][0] == "||" or set[i][0] == "]" or set[i][0] == "AOP" or set[i][0] == ";" or set[i][0] == ")" or set[i][0] == ":" or set[i][0] == "}" or  set[i][0] == ","):
                return True

        return False

    def Class():
        global i
        if(set[i][0]== "class"):
            if(set[i][0]== "class"):
                # T = set[i][1]
                i+= 1
                if(set[i][0]== "ID"):
                    # N = set[i][1]
                    i+= 1
                    # P = parameter
                    # AM = parameter
                    if(Inher()):#P , AM
                        if(set[i][0]== "{"):
                    #         if(not insertDT(N,T, P.p, 0)):
                    #             print(N, T)
                    #             print("Redeclaration Error")
                    #             return False
                            i+= 1
                            if(C_body()):
                                if(set[i][0]== "}"):
                                    i+=1
                                    return True
        return False

    def Inher():#P, am
        global i
        if(set[i][0]== ":" or set[i][0] == "{"):

            if(set[i][0] == ":"):
                i+= 1
                if(AM()):#am
                    if(set[i][0]== "ID"):
                        # N = set[i][1]
                        # T = lookUpDT(N)
                        # if not T:
                        #     print(N , "Undeclared Error")
                        #     return False
                        # P.p = N
                        i+= 1
                        return True
            elif(set[i][0] == "{"):
                return True

        return False

    def C_body():
        global i
        if(set[i][0]== "AM" or set[i][0] == "static" or set[i][0] == "const" or set[i][0] == "virtual" or set[i][0] == "DT" or set[i][0] == "ID" or set[i][0] == "static" or set[i][0] == "virtual" or set[i][0] == "const" or set[i][0] == "}"):

            if(set[i][0] == "AM"):
                am = set[i][1]
                i+=1
                if(set[i][0]== ":"):
                    i+= 1
                    if(C_TM()):
                        if(C_body()):
                            return True
            elif(set[i][0] == "static" or set[i][0] == "const" or set[i][0] == "virtual" or set[i][0] == "DT" or set[i][0] == "ID" or set[i][0] == "static" or set[i][0] == "virtual" or set[i][0] == "const"):
                if(C_TM()):
                    if(C_body()):
                        return True
            elif(set[i][0]== "}"):
                return True

        return False

    def AM():#am
        global i
        if(set[i][0]== "AM" or set[i]=="ID"):
            if(set[i][0]== "AM"):
                # am.p = set[i][1]
                i+= 1
                return True
        elif(set[i][0]== "ID"):
            # am.p = "private"
            return True

        return False

    def C_TM():
        global i
        if (set[i][0] == "static" or set[i][0] == "const" or set[i][0] == "virtual" or set[i][0] == "DT" or set[i][0] == "ID" or set[i][0] == "static" or set[i][0] == "virtual" or set[i][0] == "const"):
            if(set[i][0] == "static" or set[i][0] == "const"):
              if(TM()):
                  return True
            elif(set[i][0] == "virtual"):
                i+=1
                if(F_TM()):
                    return True
            elif(set[i][0] == "DT" or set[i][0] == "ID"):
                if(Class1()):
                    return True

        return False

    def F_TM():
        global i
        if(set[i][0] == "DT" or set[i][0] == "ID"):

            if(set[i][0] == "DT"):
                i+=1
                if(Array_ret()):
                    if(set[i][0] == "ID"):
                        i+=1
                        if(F_dec()):
                            return True
            elif(set[i][0] == "ID"):
                i += 1
                if (Array_ret()):
                    if (set[i][0] == "ID"):
                        i += 1
                        if (F_dec()):
                            return True
        return False


    def Class1():
        global i
        if(set[i][0]== "DT" or set[i][0] == "ID"):

            if(set[i][0]== "DT"):
                i+= 1
                if(X2()):
                    return True
            elif(set[i][0]== "ID"):
                i+= 1
                if(Class3()):
                    return True
        return False

    def X2():
        global i
        if(set[i][0] == "ID" or  set[i][0] == "[" ):

            if(set[i][0]== "["):
                i+= 1
                if(set[i][0]== "]"):
                    i+=1
                    if(set[i][0]== "ID"):
                        i+= 1
                        if(F_dec()):
                            return True
            elif(set[i][0]== "ID"):
                i+= 1
                if(Class2()):
                    return True
        return False

    def Class2():
        global i
        if(set[i][0]== "AOP" or set[i][0] == "[" or set[i][0] == "," or  set[i][0] == "(" or set[i][0] == ";"):

            if (set[i][0] == "AOP" or set[i][0] == "[" or set[i][0] == "," or set[i][0] == ";"):
                if(Dec()):#T
                    return True
            elif(set[i][0] == "("):
                if(F_dec()):
                    return True
        return False

    def Class3():
        global i
        if(set[i][0]== "ID" or set[i][0] == "[" or set[i][0] == "("):

            if(set[i][0]== "ID"):
                i+= 1
                if(Z()):
                    return True
            elif(set[i][0] == "["):
                i+=1
                if(set[i][0] == "]"):
                    i+=1
                    if(set[i][0] == "ID"):
                        i+=1
                        if(F_dec()):
                            return True
            elif(set[i][0] == "("):
                if(Constructor()):
                    return True
        return False

    def Constructor():
        global i
        if(set[i][0]== "("):
            i+= 1
            if(F2()):
                if(set[i][0]== ")"):
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
                if(OE()):
                    if(set[i][0] == "]"):
                        i+=1
                        return True

            elif(set[i][0] == "." or set[i][0] == "(" or set[i][0] == "AOP" or set[i][0] == "UOP" or set[i][0] == ";" or set[i][0] == ")" or set[i][0] == "MDM" or set[i][0] == "PM" or set[i][0] == "ROP" or set[i][0] == "&&" or set[i][0] == "||" or set[i][0] == "]" or set[i][0] == ":" or set[i][0] == "," or set[i][0] == "}"):
                return True

        return False

    def E():
        global i
        if(set[i][0]== "ID" or set[i][0] == "UOP" or set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const" or set[i][0] == "(" or set[i][0] == "!" or set[i][0] == "this" or set[i][0] == "}" or set[i][0] == ")"):

            if (set[i][0] == "ID" or set[i][0] == "UOP" or set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const" or set[i][0] == "(" or set[i][0] == "!" or set[i][0] == "this"):
                if(OE()):
                    if(E1()):
                        return True
            elif(set[i][0] == "}" or set[i][0] ==  ")"):
                return True

        return False

    def E1():
        global i
        if(set[i][0]== "," or set[i][0] == "}" or set[i][0] == ")" ):

            if (set[i][0]== ","):
                i+= 1
                if(OE()):
                    if(E1()):
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

    def Const():
        global i
        if(set[i][0] == "int_const" or set[i][0] == "float_const" or set[i][0] == "string_const" or set[i][0] == "char_const" or set[i][0] == "bool_const"):

            if(set[i][0] == "int_const"):
                i += 1
                return True
            elif(set[i][0] == "float_const"):
                i += 1
                return True
            elif (set[i][0] == "string_const"):
                i += 1
                return True
            elif (set[i][0] == "char_const"):
                i += 1
                return True
            elif (set[i][0] == "bool_const"):
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
                        if (L1()):
                            if (L2()):
                                return True
        return False

    start = Start()
    print(start)
    if(start is False):
        print("Error Line No: " , set[i-1][2] , "\nAt: " , set[i][1])


ST = []
s_t = 0
def insertST(N, T, scope):
    global s_t
    if not ST:
        ST.append([])
        ST[s_t].append(N)       # 0---Name
        ST[s_t].append(T)       # 1---Type
        ST[s_t].append(scope)   # 2---Scope
        s_t += 1
        return True

    for z in range(s_t):
        if(ST[z][0] == N and ST[z][2] == scope):
            return False

    ST.append([])
    ST[s_t].append(N)  # 0---Name
    ST[s_t].append(T)  # 1---Type
    ST[s_t].append(scope)  # 2---Scope
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
        print("1")
        CDT.append([])
        CDT[c_d_t].append(C_name)
        CDT[c_d_t].append(C_info)
        c_d_t += 1
        return True

    else:
        for z in range(c_d_t):
            if (CDT[z][0] == C_name):
                CDT[z].append(C_info)
                return True

        CDT.append([])
        CDT[c_d_t].append(C_name)
        CDT[c_d_t].append(C_info)
        c_d_t += 1
        return True

def lookUpST(N):
    for z in range(s_t):
        if(ST[z][0] == N):
            return ST[z][1]

def lookUpDT(N):
    for z in range(d_t):
        if(DT[z][0] == N):
            return DT[z][1]


def compatibility(TL, TR, OP):
    print(TL,TR)


class parameter:
    p = ""

Lexical_Analyzer()
Syntax_Analyzer()
# print("ST",ST ,"\nDT", DT , "\nCDT", CDT)