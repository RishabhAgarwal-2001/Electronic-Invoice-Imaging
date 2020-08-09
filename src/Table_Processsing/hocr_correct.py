def hocr_correct():
    file = open(r'../results/hocr_opt3.html', "r")

    lines = file.readlines()
    x = len(lines)
    # print(x)

    i = 0
    while(i<x-1):
        a = i
        lines[i]=lines[i].strip()
        if(lines[i].startswith('<span')):
            lines[i+1] = lines[i+1].rstrip()
            lines[i+1] = lines[i+1].lstrip()
            while(i<x-1 and not lines[i+1].startswith('</span')):
                lines[a] = lines[a].replace("\n", " ")
                lines[a] = lines[a] + lines[i+1]
                lines[i+1] = ""
                i = i + 1
                lines[i+1] = lines[i+1].rstrip()
                lines[i+1] = lines[i+1].lstrip()
            # print(lines[i+1])
        i = i + 1
    # print(lines)

    file.close()
    file = open('../results/opt.html', "w+")
    for i in lines:
        if(i!=""):
            i = i.lstrip()
            i = i.rstrip()
            file.write(i+"\n")

    file.close()

# hocr_correct()