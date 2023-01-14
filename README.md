# RegisterUI
A MCU peripheral register watcher.

## RegisterUI介绍
- 这是一个用于平替MCU寄存器操作界面的软件程序，Keil的外设监视窗口在单片机使用中设置或实时读取寄存器十分便利，但是由于闭源封装起来了，无法自由地添加一些功能，例如记录操作的过程。
- 基于Python语言以及PySimplegui、pyocd库
- 可以按字、按照功能位进行读取、写入 (目前按照功能位写入需回到字界面才能回读写入结果，后续将进行优化) 

## 安装环境
- Python 3.x
- PySimplegui 4.x
- pyocd 0.34.3
    - pyocd中需要安装arm内核或芯片型号相应的Pack包，参考Pyocd官方文档对Target目标芯片的说明 <https://pyocd.io/docs/target_support.html><br>
        例如使用CM4内核的芯片
        > pyocd pack find CM4

        会显示名为CMSDK_CM4_FP的Pack包，选择安装这个Pack包
        > pyocd pack install CMSDK_CM4_FP

        并在swd.py文件中将传入的target_override="CMSDK_CM4_FP"
## 使用方法
- 推荐直接使用VSCode将一整个工程文件夹打开，并在这个Debug中运行程序

## 效果一览
![总窗口界面及外设界面]( /PeripheralWindow.jpg "TIMD in STMG4 HRTimer")

## 碎碎念
- 其实Keil的各种相关功能都可以或者有机会通过Python实现，这样子或许能对单片机的操作拥有更高的自由度
    - 举一个例子，对于机械臂这种需要实时操作的情况来说，由于本身就需要上位机来进行控制，单片机端其实可以不用运行或者存在程序，或者说只需保存一些基础自保护程序即可，然后由电脑端下发指令，直接操作相关外设例如Timer的寄存器。省去在FLash上编写存储片上程序，进一步提升不同环境的可移植性，加快开发调试进度。
