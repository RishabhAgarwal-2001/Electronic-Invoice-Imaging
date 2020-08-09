import xlwt 
from xlwt import Workbook 
import xlrd
  
def hocr2table():
    wb = Workbook() 
    sheet1 = wb.add_sheet('Sheet 1') 

    target=open("../results/Table_Processing_Data/IB1.txt","w")
    file=open("../results/hocr_opt.html","r")


    for line in file:
        l=len(line)
        for i in range (0,l):
            if line[i]!='<':
                continue
            if line[i+1]=='s' and line[i+2]=='p':
                target.write(line)
                break

    file.close()
    target.close()

    file = open("../results/Table_Processing_Data/IB1.txt", "r")
    target = open("../results/Table_Processing_Data/IB2.txt", "w")

    for line in file:
        l=len(line)
        for i in range (0,l):
            if line[i]!='>':
                continue
            f=0
            i=i+1
            while i<l-1 and line[i]!='<':
                if line[i]!=' ':
                    f=1
                    break
                i=i+1
            if f==1:
                target.write(line)
                break

    file.close()
    target.close()

    file = open("../results/Table_Processing_Data/IB2.txt", "r")
    target = open("../results/Table_Processing_Data/IB3.txt", "w")

    for line in file:
        size=len(line)
        s=""
        for i in range (0,size-4):
            if line[i]=='b' and line[i+1]=='b' and line[i+2]=='o' and line[i+3]=='x':
                l=""
                while i<size-4 and line[i]!=';':
                    l=l+line[i]
                    i=i+1
                l=l+" "
                s=s+l
            if line[i]=='>':
                l=""
                while i<size-4 and line[i]!='<':
                    l=l+line[i]
                    i=i+1
                if line[i+1]=='/':
                    l=l+" "
                    s=s+l
        s=s+"\n"
        target.write(s)

    file.close()
    target.close()

    file = open("../results/Table_Processing_Data/IB3.txt", "r")

    data=[]
    for linet in file:
        rowarr=linet.split(" ")
        rowarr[2]=int(rowarr[2])
        data.append(rowarr)


    data.sort(key = lambda x: x[2])
    print("Data:")

    file.close()
    d2=[]
    text=[]
    for j in range(len(data)):
        lijh=[]
        abcd=[]
        for i in range (len(data[j])):
            cl=str(data[j][i])
            if cl[0]!='>' or (cl[1]=='|' and len(cl)<4):
                continue
            abcd.append(cl)
            lijh.append(data[j][i-4])
            # print(data[j][i-4],end="  ")
        # print(lijh)
        d2.append(lijh)
        text.append(abcd)
        # print("\n\n")

    lmno=[]
    r_bounds=[]
    boun_itr=0
    while len(d2[boun_itr])<3:
        boun_itr+=1

    for i in range (len(data[boun_itr])):
        cl=str(data[boun_itr][i])
        if cl[0]!='>' or (cl[1]=='|' and len(cl)<4):
            continue
        lmno.append(cl)
        r_bounds.append(data[boun_itr][i-2])

    # print(d2)
    # print("Text")
    # print(text)
    boundaries=d2[boun_itr]
    print(boundaries)
    print(text[0])
    print("RRR:"+str(boun_itr))
    print(r_bounds)
    print(len(boundaries),len(text[0]),len(r_bounds))
    for itr in range (0,len(text[0])-1):
        if itr>=len(text[0])-1:
            break
        while int(boundaries[itr+1])-int(r_bounds[itr])<7:
            print("Merging "+str(text[0][itr])+" And "+str(text[0][itr+1]))
            text[0][itr]=text[0][itr]+" "+text[0].pop(itr+1)[1:]
            r_bounds.pop(itr)
            boundaries.pop(itr+1)
            for thisitr in range (1,len(text)-1):
                try:
                    if int(d2[thisitr][itr+1])-int(d2[thisitr][itr]) <10:
                        text[thisitr][itr]=text[thisitr][itr]+" ! "+text[thisitr].pop(itr+1)[1:]
                        d2[thisitr].pop(itr+1)
                        print("Merging "+str(text[thisitr][itr])+" And "+str(text[thisitr][itr+1]))
                except:
                    pass
            itr=itr-2
    print("RRR:")
    print(r_bounds)

    print(boundaries)
    print(text[0])


    print(text)

    i=0
    for itr in range (0,len(text[0])):
        sheet1.write(0,i,text[0][itr][1:])
        i=i+1

    # for j in range (1,len(d2)):
    #     # print(len(text[j]))
    #     # print(len(d2[j]))
    #     cele=0
    #     for arw in range (len(text[j])-1):
    #         if arw>=len(text[j])-1:
    #             break
    #         print("\n")
    #         print(arw)
    #         print(d2[j][arw+1])
    #         print(r_bounds[arw])
    #         print(text[j][arw])
    #         if int(d2[j][arw+1])<int(r_bounds[arw]):
    #             text[j][arw]=text[j][arw]+" "+text[j].pop(arw+1)[1:]
    #             d2[j].pop(arw+1)
    #             arw=arw-2
    #         print(arw)

    cellmax=len(boundaries)
    for j in range (1,len(d2)):
        cele=0
        # print(text[j][0])
        while True:
            # print(cele)
            if cele>=len(text[j])-2:
                break
            if cele<0:
                cele=0
            # print("\n")
            # print(cele)
            # print(d2[j][cele+1])
            # print(r_bounds[])
            # print(text[j][arw])
            if len(text[j])!=len(d2[j]) or len(text[j])!=len(r_bounds):
                print(len(text[j]))
                print(len(d2[j]))
                print(len(r_bounds))

            if int(d2[j][cele+1])<int(r_bounds[cele]):
                text[j][cele]=text[j][cele]+" "+text[j].pop(cele+1)[1:]
                d2[j].pop(cele+1)
                cele=cele-2
            cele=cele+1



    for j in range(1,len(d2)):
        cell=0
        cellmax=len(boundaries)
        print("\n\n")
        print(text[j])
        print(d2[j])

        for itr in range(len(text[j])):
            if cell>=len(boundaries)-1:
                try:
                    sheet1.write(j,cellmax,text[j][itr][1:])
                except:
                    cellmax+=1
                    sheet1.write(j,cellmax,text[j][itr][1:])
                continue
            while cell<len(boundaries)-1 and (int(d2[j][itr])>int(boundaries[cell+1]) or (int(d2[j][itr])==int(boundaries[cell+1])  and itr!=0)):
                cell=cell+1
            att=cell
            while True:
                try:
                    sheet1.write(j,att,text[j][itr][1:])
                    break
                except:
                    att+=1

    wb.save('../results/final_8.xlsx')


# cell=0
# while <cond>:
#     sheet1.write(row,cell,<text to be written>)
#     cell=cell+1


# top=10000
# lno=0
# i=0

# for line in file:
#     i=i+1    
#     arr=line.split(" ")
#     if top>int(arr[2]):
#         top=int(arr[2])
#         lno=i
# print(top,lno)
# file.close()
# file=open("IB3.txt","r")

# i=1
# for line in file:
#     if i!=lno:
#         i=i+1
#         continue
#     arr=line.split(" ")
#     print(arr)
#     break

# i=0

# for element in arr:
#     if element[0]=='>':
#         sheet1.write(0,i,element)
#         i=i+1

# wb.save('top_line.xls')
# file.close()
# file=open("IB3.txt","r")
