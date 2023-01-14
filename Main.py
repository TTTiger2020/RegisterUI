# 这是UI 界面的主要配置函数
import PySimpleGUI as sg
import NumberConverter as nc
import swd

# 初始定义
# SVDName或者完整路径
SVDNamePath = 'STM32G474xx.svd'
BUTTONSIZE = 20

# 从SVD中提取到ListConfiguration列表

# 从每一行中提取相关元素
def InfExtract( para ):
    for i in range(len(para)):
        if('>' == para[i]):
            j = i+1
        if('<' == para[i]):
            if('/' == para[i+1]):
                k = i
                break
    return para[j:k]



# 提取每一个外设的SVD文件所有行集合
def PerpSvdExtract(PName):
    with open('%s'%SVDNamePath,'r') as f:
        ConfigTxt = f.read()
        ConfigLine = ConfigTxt.split('\n')
        ListMeta = []
        for i in range(len(ConfigLine)):
            if( '<name>%s</name>'%PName in ConfigLine[i] ):
                baseaddr = InfExtract(ConfigLine[i+3])
                j = i+1
                ListMeta.append(ConfigLine[i])
                for j in range(j, len(ConfigLine)):
                    ListMeta.append(ConfigLine[j])
                    if('</peripheral>' in ConfigLine[j]):
                        break                    
                break
            else:
                pass
        return ListMeta, baseaddr

# 根据寄存器值生成Bit值
def BitValueMake( listp, listr, rnum, bnum):
    if int(listr[bnum][3])<4:
        bvalue = (int(listp[rnum][5],16)>>int(listr[bnum][2]))&(0xffffffff>>(32-int(listr[bnum][3])))
    else:
        bvalue = hex((int(listp[rnum][5],16)>>int(listr[bnum][2]))&(0xffffffff>>(32-int(listr[bnum][3]))))
    return bvalue

# 生成外设的所有信息(目前六条信息): 0.外设的寄存器名，1.寄存器对应的地址，2.寄存器的读写属性，3.寄存器在ListMeta上的起始行， 4.寄存器在ListMeta上的结束行，5. 寄存器目前的值
def ListPerpMake( PName, ListMeta ):

    ListP = []
    ListTMP = []
    for i in range(len(ListMeta)):
        if( '<register>' in ListMeta[i] ):
            j = i+1
            ListTMP.append(InfExtract(ListMeta[j]))
            ListTMP.append(InfExtract(ListMeta[j+3]))
            ListTMP.append(InfExtract(ListMeta[j+5]))
            ListTMP.append(i)
            for j in range(j, len(ListMeta)):
                if('</register>' in ListMeta[j]):
                    ListTMP.append(j)
                    ListTMP.append(0)
                    break
            ListP.append(ListTMP)
            ListTMP = []                    
        else:
            pass
    return ListP



# 生成寄存器列表(目前四条信息)：0.Bit名字，1.Bit描述，2.Bit偏移地址，3.Bit 宽度
def ListRegiMake( RNum, ListP, ListMeta ):
    ListR = []
    ListTMP = []
    BitValue = []
    for i in range(ListP[RNum][3],ListP[RNum][4]):
        if( '<field>' in ListMeta[i] ):
            j = i+1
            ListTMP.append(InfExtract(ListMeta[j]))
            ListTMP.append(InfExtract(ListMeta[j+1]))
            ListTMP.append(InfExtract(ListMeta[j+2]))
            ListTMP.append(InfExtract(ListMeta[j+3]))
            ListR.append(ListTMP)
            ListTMP = []                    
        else:
            pass
    return ListR



# Windows Peripheral外设的窗口, 两列：第一列为寄存器名，第二列为寄存器值
def WindowPMake(ListP,Pname):
    layout = []
    for i in range(len(ListP)):
        layout.append([sg.Button('%s'%ListP[i][0],key='RegisterName'+'%s'%i,size=BUTTONSIZE),sg.Button('%s'%ListP[i][5],key='RegisterValue'+'%s'%i,size=BUTTONSIZE)])
    return sg.Window(Pname, layout)


# Windows Register寄存器详细每个bit位的窗口
def WindowRMake(ListR,Rname,BitValue):
    layout = []
    for i in range(len(ListR)):
        layout.append([sg.Button('%s'%ListR[i][0],key='BitName'+'%s'%i,size=BUTTONSIZE),sg.Button('%s'%BitValue[i],key='BitValue'+'%s'%i,size=BUTTONSIZE)])
    return sg.Window(Rname, layout)

def WindowALLMake(PerName):
    layout = []
    for name in PerName:
        layout.append([sg.Button('%s'%name)])    
    return sg.Window('ALL', layout)
# 写值窗口
def WindowBWMake( bvalue,  bname):
    layout = [[sg.InputText('%s'%bvalue,size=BUTTONSIZE),sg.Submit()]]
    return sg.Window( bname, layout )

def WindowRWMake( pvalue,  pname):
    layout = [[sg.InputText('%s'%pvalue,size=BUTTONSIZE),sg.Submit()]]
    return sg.Window( pname, layout )


# 某一个外设的窗口函数
# 可以直接对外设的值进行写的操作：窗口WindowPV，也可以按照bit位对外设进行写的操作
def DisAndCon(PName, session, target):
    ListMeta, BaseAddr = PerpSvdExtract( PName )
    ListP = ListPerpMake( PName, ListMeta )
    windowP = WindowPMake(ListP,PName)
    while True:
        eventP, valueP = windowP.read(timeout=50)
        # 寄存器数值更新
        for i in range(len(ListP)):
            ListP[i][5] = hex(swd.UlinkRead(nc.HexAdd(ListP[i][1],BaseAddr), target))
        if eventP == sg.WINDOW_CLOSED:
            break
        # 按钮查询
        for i in range(len(ListP)):
            # 更新数值
            windowP.FindElement('RegisterValue'+'%s'%i).update(ListP[i][5])
            # 按下寄存器名字
            if 'RegisterName'+'%s'%i == eventP:
                ListR = ListRegiMake(i, ListP, ListMeta)
                BitValue = []
                for ii in range(len(ListR)):
                    BitValue.append(BitValueMake( ListP, ListR, i, ii))
                windowR = WindowRMake(ListR, ListP[i][0], BitValue)
                while True:
                    eventR, valueR = windowR.read(timeout=50)
                    #寄存器bit位窗口的一些操作
                    if eventR == sg.WINDOW_CLOSED:
                        break
                    for j in range(len(ListR)):
                        # 寄存器的位值写入
                        if 'BitValue'+'%s'%j == eventR:
                            windowBW = WindowBWMake(BitValue[j], ListR[j][0])
                            eventBW, valueBW = windowBW.read()
                            if eventBW: 
                                # 错误输入
                                if nc.Str2Int(valueBW[0]) == -1:
                                    pass
                                # 正确输入
                                else:
                                    valueBWtmp = (int(ListP[i][5],16))&(0xffffffff-pow(2,int(ListR[j][2])+int(ListR[j][3]))+pow(2,int(ListR[j][2])))
                                    valueBWtmp |= nc.Str2Int(valueBW[0])<<int(ListR[j][2])
                                    swd.UlinkWrite(nc.HexAdd(ListP[i][1],BaseAddr), valueBWtmp, target)
                            windowBW.close()
                windowR.close()
            # 按下寄存器所存值
            if 'RegisterValue'+'%s'%i == eventP:
                windowRW = WindowRWMake(ListP[i][5], ListP[i][0])
                eventRW, valueRW= windowRW.read()
                # 寄存器的值写入
                if eventRW:
                    # 错误输入
                    if nc.Str2Int(valueRW[0]) == -1:
                        pass
                    else:
                        swd.UlinkWrite(nc.HexAdd(ListP[i][1],BaseAddr), nc.Str2Int(valueRW[0]), target)
                    windowRW.close()
    windowP.close()


session,target = swd.UlinkInit()
PerName = ['HRTIM_Master','HRTIM_TIMA','HRTIM_TIMB','HRTIM_TIMC','HRTIM_TIMD','HRTIM_TIME','HRTIM_TIMF','HRTIM_Common',]
windowall = WindowALLMake(PerName)
while True:
    eventall, valueall = windowall.read()
    if eventall == sg.WINDOW_CLOSED:
        break
    for ii in PerName:
        if eventall == ii:
            DisAndCon(ii, session, target)
swd.UlinkClose(session)

