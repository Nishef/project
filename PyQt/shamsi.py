import datetime


def gLeapYear(y):
    if (y % 4 == 0) and ((y % 100 != 0) or (y % 400 == 0)):
        return True
    else:
        return False


def sLeapYear(y):
    ary = [1, 5, 9, 13, 17, 22, 26, 30]
    result = False
    b = y % 33
    if b in ary:
        result = True
    return result


def shamsiDate(gyear, gmonth, gday):
    _gl = [0, 31, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
    _g = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]

    deydiffjan = 10
    if gLeapYear(gyear - 1):
        deydiffjan = 11
    if gLeapYear(gyear):
        gd = _gl[gmonth - 1] + gday
    else:
        gd = _g[gmonth - 1] + gday

    if gd > 79:
        sy = gyear - 621
        gd = gd - 79
        if gd <= 186:
            gmod = gd % 31
            if gmod == 0:
                sd = 31
                sm = int(gd / 31)
            else:
                sd = gmod
                sm = int(gd / 31) + 1
        else:
            gd = gd - 186
            gmod = gd % 30
            if gmod == 0:
                sd = 30
                sm = int(gd / 30) + 6
            else:
                sd = gmod
                sm = int(gd / 30) + 7
    else:
        sy = gyear - 622
        gd = gd + deydiffjan
        gmod = gd % 30
        if gmod == 0:
            sd = 30
            sm = int(gd / 30) + 9
        else:
            sd = gmod;
            sm = int(gd / 30) + 10

    result = [sy, sm, sd]
    return result


shamsidata = shamsiDate(datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day)
# shamsidata=shamsidata
shamsi_data = str(shamsidata[0])
shamsi_data += '/'
shamsi_data += str(shamsidata[1])
shamsi_data += '/'
shamsi_data += str(shamsidata[2])

print(shamsi_data)
