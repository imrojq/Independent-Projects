from random import *
totallines=0
tabspace=0
iterator='i'
operatorlist=["+","-","*",">>","<<","++","--","func1","func2","func3"]
conditionlist=[">","<","==","<=",">="]
f=open('code.cpp','w+')
def decide():
    if random() <0.65 :
        operator()
    else :
        conditional()
def selectoperator():
    a=random()
    if a<0.25:
        return "+"
    elif a<0.45:
        return "-"
    elif a<0.60:
        return "*"
    elif a<0.66:
        return ">>"
    elif a<0.73:
        return "<<"
    elif a<0.80:
        return "++"
    elif a<0.85:
        return "--"
    elif a<0.92:
        return "func1"
    elif a<0.97:
        return "func2"
    else:
        return "func3"

def conditional():
    global iterator,tabspace
    toss=random()
    if toss <=0.5:
        f.write(" "*(4*tabspace)+"for("+iterator+"=0;"+iterator+" < "+str(randint(1,100))+" ;"+iterator+"++)\n"+" "*(4*tabspace)+"{\n")
        iterator=chr(ord(iterator)+1)
        tabspace+=1
        decide()
        tabspace-=1
        iterator=chr(ord(iterator)-1)
        f.write(" "*(4*tabspace)+"}\n")
    else:
        condition=choice(conditionlist)
        f.write(" "*(4*tabspace)+"if ("+variable(0.25)+" "+condition+" "+variable()+")\n"+" "*(4*tabspace)+"{\n")
        tabspace+=1
        decide()
        tabspace-=1
        f.write(" "*(4*tabspace)+"}\n")
        f.write(" "*(4*tabspace)+"else\n"+""*(4*tabspace)+"{\n")
        tabspace+=1
        decide()
        tabspace-=1
        f.write(" "*(4*tabspace)+"}\n")
        
        
    
def variable(x=0):
    a=random()
    a+=x
    if a<0.25:
        ans=str(int(normalvariate(1000,500)))[:6]
    elif a>=0.25 and a<0.50:
        ans=" array"+str(choice(range(1,5)))+"["+str(choice(range(50)))+"] "
    else :
        ans=" var"+str(choice(range(1,41)))+" "
    if ans ==0:
        ans=variable(x)
    return ans
        
def operator():
    global totallines,tabspace
    no_of_lines=randint(5,15)
    totallines+=no_of_lines
    for i in range(no_of_lines):
        op=selectoperator()
        if op == "+" or op == "-" or op == "*" or op == "/" or op == "%" :
            f.write(" "*(4*tabspace)+variable(0.25)+" = "+variable()+op+" "+variable()+";\n")
        elif op==">>" or op=="<<":
            f.write(" "*(4*tabspace)+variable(0.25)+" = "+variable()+op +str(choice(range(4)))+";\n")
        elif op=="func1":
            f.write(" "*(4*tabspace)+variable(0.25)+" = "+op+"("+variable()+");\n")
        elif op=="func2":
            f.write(" "*(4*tabspace)+variable(0.25)+" = "+op+"("+variable()+","+variable()+");\n")
        elif op=="func3":
            f.write(" "*(4*tabspace)+variable(0.25)+" = "+op+"("+variable()+","+variable()+","+variable()+");\n")
        else :
            f.write(" "*(4*tabspace)+variable(0.25)+op+";\n")
            
    
f.write("#include <iostream.h>\n")
f.write("#include <conio.h>\n")
f.write("#include <stdio.h>\n")
f.write("using namespace std;\n")
f.write("int func1(int a){\n")
#writerandom(tab=1,line=10)
f.write("return (a-89);\n}\n")
f.write("int func2(int a, int b){\n")
f.write("return a-b;\n}\n")
f.write("int func3(int a, int b,int c){\n")
f.write("return a-b+c;\n}\n")
f.write("int main(){\n")
for i in range(40):
    f.write("int var"+str(i+1)+"="+str(randint(1,10000))+";\n")
for i in range(15):
    f.write("int "+str(chr(ord('i')+i))+";\n")
    

"""#f.write("float ")
for i in range(20,30):
    f.write("float var"+str(i+1)+"="+str(randint(1,10000))+"."+str(randint(1,100))+";\n")
#f.write("var"+str(i+1)+";\n")

#f.write("double ")
for i in range(30,40):
    f.write("double var"+str(i+1)+"="+str(randint(1,10000))+"."+str(randint(1,10000))+";\n")
#f.write("var"+str(i+1)+";\n")"""

for i in range(4):
    f.write("int "+"array"+str(i+1)+"[50];\n")

f.write("for (i=0;i<50;i++){\n")
tabspace+=1
for i in range(4):
    f.write(" "*(4*tabspace)+"array"+str(i+1)+"[i]="+str(i+1)+";\n")
f.write("}\n")
tabspace-=1
num_lines=input("Enter the number of lines you want in the code :")
while (totallines < num_lines):
    decide()
for i in range(40):
    f.write("printf(\"The value of variable var"+str(i+1)+" is :%d\\n\",var"+str(i+1)+");\n")
  #  f.write("printf(\"\\n\");\n")
f.write("getch();\n }\n")


    



f.close()

