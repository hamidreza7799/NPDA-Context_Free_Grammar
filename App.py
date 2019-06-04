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

        
class State:
    def __init__(self,name):
        self.Name=name
        self.Final_State=False
        self.Nueighbor={}

        
class NPDA:
    def __init__(self,Alphabet,Count_States,Stack_Symbol,First_Stack_Symbol):
        #Alphabet for stack
        self.Stack_Symbol=Stack_Symbol
        self.First_Stack_Symbol=First_Stack_Symbol
        #stack of npda
        #self.Stack=Stack
        #alphabt for npda
        self.Alphabet=Alphabet
        #count of states
        self.Count_States=Count_States
        #start variable for npda
        self.Start_Variable=None
        #state's list of npda
        self.States=[]
        #creat States for npda and add to self.states
        for count in range(Count_States):
            name_of_state='q'+str(count)
            new_state=State(name_of_state)
            self.States+=[new_state]

    def Convert_NPDA_to_CFG(self,CFG):
        for state in self.States:
            #key = (input-alphabet,top_stack)
            # value = list of (destination,push stack)
            for key,value in state.Nueighbor.items():
                for transition in value:
                    if transition[1]!="_":
                        # check every qk and qj 
                        for k in range(self.Count_States):
                            for l in range(self.Count_States):
                                variable="("+state.Name+key[1]+"q"+str(k)+")"
                                product=key[0]+"("+transition[0].Name+transition[1][0]+"q"+str(l)+")"+"("+"q"+str(l)+transition[1][1]+"q"+str(k)+")"
                                CFG.Variables[variable]=CFG.Variables.get(variable,[])+[product]
                                
                    else:
                        variable='('+state.Name+key[1]+transition[0].Name+')'
                        product=key[0]
                        #insert production to CFG
                        CFG.Variables[variable]=CFG.Variables.get(variable,[])+[product]
            


#class CFG
class CFG:
    def __init__(self):
        self.Start_Variable=None
        self.Variables={}
    def Detection_String(self,String):
        #DFS travers for derivition tree
        pass
        
            
class App:
    def __init__(self,file_address):
        self.File_Address=file_address
        self.NPDA=None
        self.CFG=None
        self.Alphabet=None
    def Creat_NPDA(self):
        #read file
        File=open(self.File_Address,'r')
        Lines=File.readlines()
        File.close()
        self.Alphabet=Lines[1].replace('\n','').split(',')
        #add lambda to alphabet for npda
        NPDA_Alphabet=self.Alphabet+["_"]
        # split stack symbol and first stack symbol
        Stack_Symbol=Lines[2].replace('\n','').split(',')
        First_Stack_Symbol=Lines[3].replace('\n','').split(',')
        #creat base noda
        self.NPDA=NPDA(NPDA_Alphabet,int(Lines[0]),Stack_Symbol,First_Stack_Symbol)
        #reduce state numbert to start at zero
        minimum=int(Lines[4].split(',')[0].split('q')[1])
        for line in range(4,len(Lines)):
            info=Lines[line].split(',')
            origin_index=int(info[0].split('q')[1])
            if origin_index < minimum:
                minimum=origin_index
            destination_index=int(info[4].replace('\n','').split('q')[1])
            if destination_index < minimum:
                minimum=destination_index
        #set start variable
        self.NPDA.Start_Variable=self.NPDA.States[int(Lines[4].split(',')[0].split('q')[1])-minimum]
        #complete npda"
        for line in range(4,len(Lines)):
            info=Lines[line].split(',')
            origin_index=int(info[0].split('q')[1])-minimum
            destination_index=int(info[4].replace('\n','').split('q')[1])-minimum
            self.NPDA.States[origin_index].Nueighbor[(info[1],info[2])]=self.NPDA.States[origin_index].Nueighbor.get((info[1],info[2]),[])+[(self.NPDA.States[destination_index],info[3])]
            #final states"
            if "*" in info[0]:
                self.NPDA.States[origin_index].Final_State=True
            if "*" in info[2]:
                self.NPDA.States[destination_index].Final_State=True

    def Creat_CFG(self):
        self.CFG=CFG()
        self.NPDA.Convert_NPDA_to_CFG(self.CFG)

App=App("input.txt")
App.Creat_NPDA()
App.Creat_CFG()
for state in App.NPDA.States:
    print(state.Nueighbor)
print(App.CFG.Variables)
