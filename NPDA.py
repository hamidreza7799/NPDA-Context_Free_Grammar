class State:
    def __init__(self,name):
        self.Name=name
        #self.Final_State=False
        self.Nueighbor={}
class NPDA:
    def __init__(self,Alphabet,Count_States,Stack_Symbol,First_Stack_Symbol):
        #final state for npda
        self.Final_State=None
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
            
