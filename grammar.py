# (stmt-seq)' -> stmt-seq                           
# stmt-seq -> stmt-seq statement                        2
# stmt-seq -> statement                                 3
# statement -> repeat-stmt                              4
# statement ->  assign-stmt                             5
# repeat-stmt -> repeat stmt-seq until identifier       6
# assign-stmt -> identifier := factor ;                 7
# factor -> identifier                                  8
# factor -> number                                      9


    ##### DICTIONARY 1 #####

    #1 ---> (stmt-seq)'
    #2 ---> stmt-seq
    #3 ---> stmt-seq 
    #4 ---> statement
    #5 ---> statement
    #6 ---> repeat-stmt 
    #7 ---> assign-stmt 
    #8 ---> factor
    #9 ---> factor


    ##### DICTIONARY 2 #####
    #1 ---> stmt-seq
    #2 ---> stmt-seq statement 
    #3 ---> statement    
    #4 ---> repeat-stmt   
    #5 ---> assign-stmt 
    #6 ---> repeat stmt-seq until identifier  
    #7 ---> identifier := factor ;
    #8 ---> identifier
    #9 ---> number

import copy

class Grammar:
        
    In = []

    stack_table = []
    cnt =  1
    parseTable = {
        0: {
            'repeat': 's5',
            'identifier': 's6',
            'stmt-seq': '1',
            'statement': '2',
            'repeat-stmt': '3',
            'assign-stmt': '4'
        },
        1: {
            'repeat': 's5',
            'identifier': 's6',
            '$': 'acc',
            'statement': '7',
            'repeat-stmt': '3',
            'assign-stmt': '4'
        },
        2: {
            'repeat': 'r3',
            'until': 'r3',
            'identifier': 'r3',
            '$': 'r3'
        },
        3: {
            'repeat': 'r4',
            'until': 'r4',
            'identifier': 'r4',
            '$': 'r4'
        },  
        4: {
            'repeat': 'r5',
            'until': 'r5',
            'identifier': 'r5',
            '$': 'r5'
        },  
        5: {
            'repeat': 's5',
            'identifier': 's6',
            'stmt-seq'  : '8',
            'statement': '2',
            'repeat-stmt': '3',
            'assign-stmt': '4'
        },      
        6: {
            ':=': 's9'
        },            
        7: {
            'repeat': 'r2',
            'until': 'r2',
            'identifier': 'r2',
            '$'  : 'r2'
        },
        8: {
            'repeat': 's5',
            'until': 's10',
            'identifier': 's6',
            'statement': '7',
            'repeat-stmt': '3',
            'assign-stmt': '4'
        }, 
        9: {
            'identifier': 's12',
            'number': 's13',
            'factor': '11',
        },                 
        10: {
            'identifier': 's14',
        },                      
        11: {
            ';': 's15',
        },             
        12: {
            ';': 'r8',
        },
        13: {
            ';': 'r9',
        },   
        14: {
            'repeat': 'r6',
            'until': 'r6',
            'identifier': 'r6',
            '$': 'r6',    
        },     
        15: {
            'repeat': 'r7',
            'until': 'r7',
            'identifier': 'r7',
            '$': 'r7',    
        },                                  
        
    }


    leftOp_dict = {
        1: "(stmt-seq)'",
        2: "stmt-seq",
        3: "stmt-seq",
        4: "statement",
        5: "statement",
        6: "repeat-stmt",
        7: "assign-stmt",
        8: "factor",
        9: "factor"
    }


    rightOp_dict = {
        1: ["stmt-seq"],
        2: ["stmt-seq", "statement"],
        3: ['statement'],
        4: ["repeat-stmt"],
        5: ["assign-stmt"],
        6: ["repeat", "stmt-seq", "until", "identifier"],
        7: ["identifier", ":=", "factor", ';'],
        8: ["identifier"],
        9: ["number"]
    }

    stack, symbols = [0], []


    def changeTokens(self, types=[]):
        
        for token in types:
            if token == "ID":
                self.In.append("identifier")
            elif token == "NUM":
                self.In.append("number")
            elif token == "assign":
                self.In.append(":=")
            elif token == ";":
                self.In.append(";")
            elif token == "repeat":
                self.In.append("repeat")
            elif token == "until":
                self.In.append("until")








    #In = ["identifier", ":=", "number", ";","$"]



    def func(self, types=[]):
        
        self.changeTokens(types)
        self.In.append("$")
        
        while len(self.In) > 0:


            temp = []
            temp.append(self.cnt)
            self.cnt +=1
            stackCpy = copy.deepcopy(self.stack)
            symbolCpy = copy.deepcopy(self.symbols)
            inCpy = copy.deepcopy(self.In)
            temp.append(stackCpy)
            temp.append(symbolCpy)
            temp.append(inCpy)



            currInput = self.In[0]
            
            lastElement = self.stack[-1]

            action = ""

            if currInput in self.parseTable[lastElement].keys():
                action = self.parseTable[lastElement][currInput]
            else:
                print("not accepted")
                break
            
            temp.append(action)

            self.stack_table.append(temp)

            if action == "acc":
                print("accepted")
                break

            
            elif action[0] == 's':
                self.In.pop(0)
                self.stack.append(int(action[1:]))
                self.symbols.append(currInput)
            

            elif action[0] == 'r':
                state = int(action[1:])
                seq = self.rightOp_dict[state]
                
                subList = self.symbols[-len(seq):]

                if (subList == seq):
                    del self.symbols[-len(seq):]
                    leftOp = self.leftOp_dict[state]
                    self.symbols.append(leftOp)

                    del self.stack[-len(seq):]
                    lastElement = self.stack[-1]
                    element = self.parseTable[lastElement][self.symbols[-1]]

                    self.stack.append(int (element))
            
            else:
                print ("not accepted" )
                break

            #print(temp)

        for l in self.stack_table:
            print(l)


            


