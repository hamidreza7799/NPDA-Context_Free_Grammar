from NPDA import *
from CFG import *                               
class App:
    def __init__(self,file_address,output):
        self.File_Address=file_address
        self.output=output
        self.NPDA=None
        self.CFG=None
        self.Alphabet=None
        #self.Start_Variable_CFG=None
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
        #set start variable for npda
        self.NPDA.Start_Variable=self.NPDA.States[int(Lines[4].split(',')[0].split('q')[1])-minimum]
        #complete npda"
        for line in range(4,len(Lines)):
            info=Lines[line].split(',')
            origin_index=int(info[0].split('q')[1])-minimum
            destination_index=int(info[4].replace('\n','').split('q')[1])-minimum
            self.NPDA.States[origin_index].Nueighbor[(info[1],info[2])]=self.NPDA.States[origin_index].Nueighbor.get((info[1],info[2]),[])+[(self.NPDA.States[destination_index],info[3])]
            #final states"
            if "*" in info[0]:
                self.NPDA.Final_State=self.NPDA.States[origin_index]
            if "*" in info[4]:
                self.NPDA.Final_State=self.NPDA.States[destination_index]

    def Creat_CFG(self):
        self.CFG=CFG()
        self.NPDA.Convert_NPDA_to_CFG(self.CFG)
        #set start variable
        self.CFG.Start_Variable="("+self.NPDA.Start_Variable.Name+self.NPDA.First_Stack_Symbol[0]+self.NPDA.Final_State.Name+")"
        #add start variable if it is not in cfg.variables
        if self.CFG.Start_Variable not in self.CFG.Variables:
            self.CFG.Variables[self.CFG.Start_Variable]=[]
    def Write_CFG(self):
        File=open(self.output,"w")
        for var,pro in self.CFG.Variables.items():
            result=var+'->'
            for p in pro:
                result+=('|'+p)
            File.write(result.replace('|',"",1)+'\n')
        File.close()
    def Detection_String(self,String):
        String_Map=self.CFG.Detection_String(String)
        File=open(self.output,"a")
        File.write("input :"+String+'\n')
        File.write("output :"+'\n')
        if String_Map == False:
            File.write("False"+'\n')
        else:
            File.write("True"+'\n')
            String_Map+=[String]
            result=''
            for i in range(len(String_Map)):
                result+="=>"+String_Map[i]
            File.write(result.replace("=>","",1)+'\n')
                
        File.close()
        
App=App("input.txt","output.txt")
App.Creat_NPDA()
App.Creat_CFG()
#remove lambda productions
App.CFG.Remove_Lambda_Production()
#write cfg with no lambda production
App.Write_CFG()
#detect input string
App.Detection_String("abba")
App.Detection_String("ba")
App.Detection_String("_")

