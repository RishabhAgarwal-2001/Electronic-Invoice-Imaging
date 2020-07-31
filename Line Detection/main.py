from oct2py import Oct2Py
oc = Oct2Py()

def Main(c):
    if (c == 'h'):
        script = ""
        with open("EdgeDetectionH.m","r") as f:
            f.read(script)
        print (script)
        #oc.myScript(7)
    elif (c == 'v'):
        script = ""
        with open("EdgeDetectionV.m","r") as f:
            f.read(script)
        print (script)
    elif (c == 'b'):
        script = ""
        with open("EdgeDetectionAll.m","r") as f:
            f.read(script)
        print (script)
    else:
        print("Wrong value of argument passed. Valid arguments values are h, v and b only")