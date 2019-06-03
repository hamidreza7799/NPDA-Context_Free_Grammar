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

    def Convert_NPDA_to_CFG(self):
        pass

class App:
    def __init__(self,file_address):
        self.File_Address=file_address
        self.NPDA=None
        self.CFG=None
        self.Alphabet=None
    def creat_NPDA(self):
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

App=App("input.txt")
App.creat_NPDA()
for state in App.NPDA.States:
    print(state.Nueighbor)
