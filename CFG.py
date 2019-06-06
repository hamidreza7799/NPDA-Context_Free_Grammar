class Stack:
    def __init__(self):
        self.Size=0
        self.Stack=[]
    def pop(self):
        if self.Size > 0:
            self.Size-=1
            Item=self.Stack[-1]
            del self.Stack[-1]
            return Item
    def push(self,Item):
        self.Size+=1
        self.Stack+=[Item]

#class CFG
class CFG:
    def __init__(self):
        self.Start_Variable=None
        self.Variables={}
    #remove lambda production
    def Remove_Lambda_Production(self):
        #find lambda productions
        Variables_with_lambda_production=[]
        for Var,Productions in self.Variables.items():
            if "_" in Productions:
                Variables_with_lambda_production+=[Var]
                Productions.remove("_")
        #remove all lambda production 
        for Var in  Variables_with_lambda_production:
            for Productions in self.Variables.values():
                for Pro in Productions:
                    if Var in Pro:
                        Productions+=[Pro.replace(Var,'')]
                    
            
    def Detection_String(self,String):
        #DFS travers for derivition tree
        String_Lentgh=len(String)
        S_Stack=Stack()
        S_Stack.push(self.Start_Variable)
        counter=0
        ####
        String_Map=[]
        while S_Stack.Size > 0 :
            if counter < String_Lentgh :
                try:#for errore for currrent_v = v[counter:7+counter]
                    v=S_Stack.pop()
                    String_Map+=[v]
                    #left most derivision
                    Left_Variable=v[counter:7+counter]
                    #find nueighbor start with string [counter] and add to nueighbor
                    Leafs=0#leafs of last variable
                    nueighbor=[]
                    for variable in self.Variables[Left_Variable]:
                        if variable[0] == String[counter]:
                            nueighbor+=[variable]
                            Leafs+=1
                    #push new_variable =left derivision last variable 
                    for variable in nueighbor:
                        S_Stack.push(v.replace(Left_Variable,variable))
                    #if nueighbor dosent element dont add counter
                    if len(nueighbor) > 0 :
                        counter+=1
                    else:
                        del String_Map[-1]
                        
                        
                except:
                    del String_Map[-1]
                    del String_Map[-1]
                    counter-=1

            else:
                for i in range(Leafs):
                    v=S_Stack.pop()
                    if v == String :
                        return String_Map
                counter-=1
                del String_Map[-1]
        return False
