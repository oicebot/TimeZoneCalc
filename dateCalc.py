#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# 
import time

def init_loop():
    global dates,current,dateStr
    dates = [None,None]
    current = 1
    dateStr = ''

def strToTime(inStr='1904-08-22'):
    inStr = inStr.strip()
    result = []
    temp = ''
    if not inStr[0].isdigit():
        return None
    for i in inStr:
        if i.isdigit():
            temp = temp + i
        else:
            if temp:
                result.append(int(temp))
                temp = ''
    else:
        if temp:
            result.append(int(temp))
            temp = ''

    length = len(result)
    
    if length <= 1:
        return None
    elif length == 2:
        result.append(1)
    elif length > 9:
        length = 9
        result = result[:9]

    length = 9 - length
    result.extend([0]*length)

    return time.mktime(tuple(result))

def dateBetween(date1='1904 8 22',date2='1997/002/019'):
    '''
    input 2 date string, 
    return float as date number
    return None if any string cannot be convert to date tuple
    '''
    d1 = strToTime(date1)
    d2 = strToTime(date2)

    if not all([d1,d2]):
        return None

    datesInSec = abs(d1 - d2)
    dateNumber = datesInSec/3600/24
    return dateNumber

def dateAdd(date1="1904 8 22",date2=33784,template=r"%Y-%m-%d"):
    '''
    input 1 date string and 1 int
    return date string
    '''
    d1 = strToTime(date1)
    d2 = date2 * 24 * 3600

    temp = str(template).strip()

    dateTuple = time.localtime(d1+d2)
    result = time.strftime(temp,dateTuple)

    return result

if __name__ == '__main__':
    '''
    print(strToTime())
    # -2062656000.0
    print(strToTime('1904.08 22'))
    print(strToTime('1904/08/22'))
    # 856281600.0
    print(strToTime('1997 2 19'))
    # 33784.0
    print(dateBetween())
    # 755
    print(dateBetween('2017-1-20',"2019 2 14 10 05"))

    # 2019-02-14
    print(dateAdd("2017 1 20",755))
    # 2017 1 20
    print(dateAdd("2019 2 14",-755))
    # 2017 Jan 20
    print(dateAdd("2019 2 14",-755,r"%Y %b %d"))
    # 2019 Feb 3, Sunday
    print(dateAdd("2019 2 4",-1,r"%Y %b %d, %A"))

    '''

    init_loop()

    while True:
        while(not all(dates)):
            try:
                if not dates[0]:
                    current = 1
                else:
                    current = 2
                dateStr = input("请输入第{}个日期：".format(current))
            except:
                # EOFError or KeyboardInterrupt
                print("\n感谢使用，再见。")
                exit()

            if dateStr:
                dates[current - 1] = dateStr
                current += 1
        
        datesFloat = dateBetween(dates[0],dates[1])
        if not datesFloat:
            print("输入有误，请重新输入。")
            init_loop()

        else:
            print("两个日期之间相差：{}天。".format(datesFloat))
            print('------')
            a = input('是否继续计算其他日期？[Y/n]：')
            if a.lower() == 'n':
                print("\n感谢使用，再见。")
                exit()
            else:
                init_loop()


            
            
            




    
