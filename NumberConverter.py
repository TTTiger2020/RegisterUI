# 对于嵌入式指令或者各种交互窗口红常用的数据进行类型转化
def Str2Int(strin):
    if(len(strin)==0):
        return -1
    if(strin[-1]=='x'):
        return -1
    if(strin[0]=='x'):
        return -1
    if(len(strin)==1):
        return int(strin,16)
    else:
        if(strin[1] == 'x'):
            return int(strin[2:len(strin)],16)
        else:
            return int(strin)

def Str2Hex(strin):
    return hex(Str2Int(strin))


# 返回Int类型， swd写寄存器指令专用
def HexAdd(hexS1, hexS2):
    return (int(hexS1,16)+int(hexS2,16))

