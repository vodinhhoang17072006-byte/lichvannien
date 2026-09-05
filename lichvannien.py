import datetime
import math
import wx
import wx.adv

CAN = ['Giáp', 'Ất', 'Bính', 'Đinh', 'Mậu', 'Kỷ', 'Canh', 'Tân', 'Nhâm', 'Quý']
CHI = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']
THANG_AM = ['Giêng', 'Hai', 'Ba', 'Tư', 'Năm', 'Sáu', 'Bảy', 'Tám', 'Chín', 'Mười', 'Mười Một', 'Chạp']
THU_VN = ['Thứ Hai', 'Thứ Ba', 'Thứ Tư', 'Thứ Năm', 'Thứ Sáu', 'Thứ Bảy', 'Chủ Nhật']

TIET_KHI = [
    "Xuân phân", "Thanh minh", "Cốc vũ", "Lập hạ", "Tiểu mãn", "Mang chủng",
    "Hạ chí", "Tiểu thử", "Đại thử", "Lập thu", "Xử thử", "Bạch lộ",
    "Thu phân", "Hàn lộ", "Sương giáng", "Lập đông", "Tiểu tuyết", "Đại tuyết",
    "Đông chí", "Tiểu hàn", "Đại hàn", "Lập xuân", "Vũ thủy", "Kinh trập"
]

CHI_VOI_GIO = [
    "Tý (23-1)", "Sửu (1-3)", "Dần (3-5)", "Mão (5-7)",
    "Thìn (7-9)", "Tỵ (9-11)", "Ngọ (11-13)", "Mùi (13-15)",
    "Thân (15-17)", "Dậu (17-19)", "Tuất (19-21)", "Hợi (21-23)"
]

HOANG_DAO_MAP = {
    0: [0, 1, 3, 6, 8, 9],
    1: [2, 3, 5, 8, 9, 11],
    2: [0, 1, 4, 5, 7, 10],
    3: [0, 2, 3, 6, 7, 9],
    4: [2, 4, 5, 8, 9, 11],
    5: [1, 4, 6, 7, 10, 11],
    6: [0, 1, 3, 6, 8, 9],
    7: [2, 3, 5, 8, 9, 11],
    8: [0, 1, 4, 5, 7, 10],
    9: [0, 2, 3, 6, 7, 9],
    10: [2, 4, 5, 8, 9, 11],
    11: [1, 4, 6, 7, 10, 11]
}

def _INT(d):
    return int(math.floor(d))

def is_leap_year_solar(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

def jdFromDate(dd, mm, yy):
    a = _INT((14 - mm) / 12)
    y = yy + 4800 - a
    m = mm + 12 * a - 3
    jd = dd + _INT((153 * m + 2) / 5) + 365 * y + _INT(y / 4) - _INT(y / 100) + _INT(y / 400) - 32045
    if jd < 2299161:
        jd = dd + _INT((153 * m + 2) / 5) + 365 * y + _INT(y / 4) - 32083
    return jd

def jdToDate(jd):
    if jd > 2299160:
        a = jd + 32044
        b = _INT((4 * a + 3) / 146097)
        c = a - _INT((b * 146097) / 4)
    else:
        b = 0
        c = jd + 32082
    d = _INT((4 * c + 3) / 1461)
    e = c - _INT((1461 * d) / 4)
    m = _INT((5 * e + 2) / 153)
    day = e - _INT((153 * m + 2) / 5) + 1
    month = m + 3 - 12 * _INT(m / 10)
    year = b * 100 + d - 4800 + _INT(m / 10)
    return int(day), int(month), int(year)

def getNewMoonDay(k, timeZone):
    T = k / 1236.85
    T2 = T * T
    T3 = T2 * T
    dr = math.pi / 180.0
    Jd1 = 2415020.75933 + 29.53058868 * k + 0.0001178 * T2 - 0.000000155 * T3
    Jd1 += 0.00033 * math.sin((166.56 + 132.87 * T - 0.009173 * T2) * dr)
    M = 359.2242 + 29.10535608 * k - 0.0000333 * T2 - 0.00000347 * T3
    Mpr = 306.0253 + 385.81691806 * k + 0.0107306 * T2 + 0.00001236 * T3
    F = 21.2964 + 390.67050646 * k - 0.0016528 * T2 - 0.00000239 * T3
    C1 = (0.1734 - 0.000393 * T) * math.sin(M * dr) + 0.0021 * math.sin(2 * M * dr)
    C1 -= 0.4068 * math.sin(Mpr * dr) - 0.0161 * math.sin(2 * Mpr * dr)
    C1 -= 0.0004 * math.sin(3 * Mpr * dr)
    C1 += 0.0104 * math.sin(2 * F * dr) - 0.0051 * math.sin((M + Mpr) * dr)
    C1 -= 0.0074 * math.sin((M - Mpr) * dr) - 0.0004 * math.sin((2 * F + M) * dr)
    C1 -= 0.0004 * math.sin((2 * F - M) * dr) + 0.0006 * math.sin((2 * F + Mpr) * dr)
    C1 += 0.0010 * math.sin((2 * F - Mpr) * dr) + 0.0005 * math.sin((M + 2 * Mpr) * dr)
    if T < -11:
        deltaT = 0.001 + 0.000839 * T + 0.0002261 * T2 - 0.00000845 * T3 - 0.000000081 * T * T3
    else:
        deltaT = -0.000278 + 0.000265 * T + 0.000262 * T2
    JdNew = Jd1 + C1 - deltaT
    return _INT(JdNew + 0.5 + timeZone / 24.0)

def getSunLongitude(jdn, timeZone):
    T = (jdn - 2451545.5 - timeZone / 24.0) / 36525.0
    T2 = T * T
    dr = math.pi / 180.0
    M = 357.52910 + 35999.05030 * T - 0.0001559 * T2 - 0.00000048 * T * T2
    L0 = 280.46645 + 36000.76983 * T + 0.0003032 * T2
    DL = (1.914600 - 0.004817 * T - 0.000014 * T2) * math.sin(dr * M)
    DL += (0.019993 - 0.000101 * T) * math.sin(dr * 2 * M) + 0.000290 * math.sin(dr * 3 * M)
    L = L0 + DL
    L = L * dr
    L = L - math.pi * 2 * _INT(L / (math.pi * 2))
    return _INT(L / math.pi * 6)

def getSunLongitudeExact(jdn, timeZone):
    T = (jdn - 2451545.0 - timeZone / 24.0) / 36525.0
    T2 = T * T
    dr = math.pi / 180.0
    L0 = 280.46646 + 36000.76983 * T + 0.0003032 * T2
    M = 357.52911 + 35999.05029 * T - 0.0001537 * T2
    C = (1.914602 - 0.004817 * T - 0.000014 * T2) * math.sin(M * dr)
    C += (0.019993 - 0.000101 * T) * math.sin(2 * M * dr) + 0.000289 * math.sin(3 * M * dr)
    L = L0 + C
    L = L % 360
    if L < 0: 
        L += 360
    return L

def get_tiet_khi(jd):
    long_deg = getSunLongitudeExact(jd, 7.0)
    index = int(long_deg / 15) % 24
    return TIET_KHI[index]

def getLunarMonth11(yy, timeZone):
    off = jdFromDate(31, 12, yy) - 2415021.076998695
    k = _INT(off / 29.530588853)
    nm = getNewMoonDay(k, timeZone)
    sunLong = getSunLongitude(nm, timeZone)
    if sunLong >= 9:
        nm = getNewMoonDay(k - 1, timeZone)
    return nm

def getLeapMonthOffset(a11, timeZone):
    k = _INT((a11 - 2415021.076998695) / 29.530588853 + 0.5)
    i = 1
    arc = getSunLongitude(getNewMoonDay(k + i, timeZone), timeZone)
    while True:
        last = arc
        i += 1
        arc = getSunLongitude(getNewMoonDay(k + i, timeZone), timeZone)
        if not (arc != last and i < 14):
            break
    return i - 1

def get_lunar_year_leap_info(lunarYear):
    timeZone = 7.0
    a11_prev = getLunarMonth11(lunarYear - 1, timeZone)
    a11_curr = getLunarMonth11(lunarYear, timeZone)
    if a11_curr - a11_prev > 365:
        leap_off = getLeapMonthOffset(a11_prev, timeZone)
        leap_m = leap_off - 2
        if leap_m <= 0:
            leap_m += 12
        return True, leap_m
    return False, 0

def convert_solar_to_lunar(dd, mm, yy):
    timeZone = 7.0
    dayNumber = jdFromDate(dd, mm, yy)
    k = _INT((dayNumber - 2415021.076998695) / 29.530588853)
    monthStart = getNewMoonDay(k + 1, timeZone)
    if monthStart > dayNumber:
        monthStart = getNewMoonDay(k, timeZone)

    a11 = getLunarMonth11(yy, timeZone)
    b11 = a11
    if a11 >= monthStart:
        lunarYear = yy
        a11 = getLunarMonth11(yy - 1, timeZone)
    else:
        lunarYear = yy + 1
        b11 = getLunarMonth11(yy + 1, timeZone)

    lunarDay = dayNumber - monthStart + 1
    diff = _INT((monthStart - a11) / 29)

    is_leap = False
    lunarMonth = diff + 11
    if b11 - a11 > 365:
        leapMonthDiff = getLeapMonthOffset(a11, timeZone)
        if diff >= leapMonthDiff:
            lunarMonth = diff + 10
            if diff == leapMonthDiff:
                is_leap = True

    if lunarMonth > 12:
        lunarMonth -= 12
    if lunarMonth >= 11 and diff < 4:
        lunarYear -= 1

    return int(lunarDay), int(lunarMonth), int(lunarYear), is_leap, dayNumber

def convert_lunar_to_solar(lunarDay, lunarMonth, lunarYear, isLeap):
    timeZone = 7.0
    if lunarMonth < 11:
        a11 = getLunarMonth11(lunarYear - 1, timeZone)
        b11 = getLunarMonth11(lunarYear, timeZone)
    else:
        a11 = getLunarMonth11(lunarYear, timeZone)
        b11 = getLunarMonth11(lunarYear + 1, timeZone)

    off = lunarMonth - 11
    if off < 0:
        off += 12

    if b11 - a11 > 365:
        leapOff = getLeapMonthOffset(a11, timeZone)
        if isLeap or off >= leapOff:
            off += 1

    k = _INT(0.5 + (a11 - 2415021.076998695) / 29.530588853) + off
    nm = getNewMoonDay(k, timeZone)
    jd = nm + lunarDay - 1
    return jdToDate(jd)

def get_can_chi_nam(year):
    if year < 0: 
        year += 1 
    return f"{CAN[(year + 6) % 10]} {CHI[(year + 8) % 12]}"

def get_can_chi_ngay(jd):
    can_ngay = CAN[(jd + 9) % 10]
    chi_ngay = CHI[(jd + 1) % 12]
    return f"{can_ngay} {chi_ngay}"

def get_can_chi_thang(lunar_month, lunar_year):
    can_nam_idx = (lunar_year + 6) % 10
    can_thang_gieng = (can_nam_idx * 2 + 2) % 10
    can_thang = (can_thang_gieng + lunar_month - 1) % 10
    
    chi_thang = (lunar_month + 1) % 12
    return f"{CAN[can_thang]} {CHI[chi_thang]}"

def get_gio_hoang_dao(jd):
    chi_ngay_idx = (jd + 1) % 12
    indices = HOANG_DAO_MAP[chi_ngay_idx]
    res = [CHI_VOI_GIO[i] for i in indices]
    return ", ".join(res)

def get_khong_minh_xuat_hanh(lunar_day, lunar_month):
    """Tính ngày xuất hành theo Khổng Minh dựa trên ngày và tháng Âm lịch."""
    group_1 = [1, 4, 7, 10]
    group_2 = [2, 5, 8, 11]
    group_3 = [3, 6, 9, 12]

    if lunar_month in group_1:
        mapping = {
            1: ("Đường Phong", "Rất tốt, xuất hành thuận lợi, cầu tài được như ý muốn, gặp quý nhân phù trợ."),
            7: ("Đường Phong", "Rất tốt, xuất hành thuận lợi, cầu tài được như ý muốn, gặp quý nhân phù trợ."),
            13: ("Đường Phong", "Rất tốt, xuất hành thuận lợi, cầu tài được như ý muốn, gặp quý nhân phù trợ."),
            19: ("Đường Phong", "Rất tốt, xuất hành thuận lợi, cầu tài được như ý muốn, gặp quý nhân phù trợ."),
            25: ("Đường Phong", "Rất tốt, xuất hành thuận lợi, cầu tài được như ý muốn, gặp quý nhân phù trợ."),
            2: ("Kim Thổ", "Ra đi nhỡ tàu, nhỡ xe, cầu tài không được, trên đường đi mất của, bất lợi."),
            8: ("Kim Thổ", "Ra đi nhỡ tàu, nhỡ xe, cầu tài không được, trên đường đi mất của, bất lợi."),
            14: ("Kim Thổ", "Ra đi nhỡ tàu, nhỡ xe, cầu tài không được, trên đường đi mất của, bất lợi."),
            20: ("Kim Thổ", "Ra đi nhỡ tàu, nhỡ xe, cầu tài không được, trên đường đi mất của, bất lợi."),
            26: ("Kim Thổ", "Ra đi nhỡ tàu, nhỡ xe, cầu tài không được, trên đường đi mất của, bất lợi."),
            3: ("Kim Dương", "Xuất hành tốt, có quý nhân phù trợ, tài lộc thông suốt, thưa kiện có nhiều lý phải."),
            9: ("Kim Dương", "Xuất hành tốt, có quý nhân phù trợ, tài lộc thông suốt, thưa kiện có nhiều lý phải."),
            15: ("Kim Dương", "Xuất hành tốt, có quý nhân phù trợ, tài lộc thông suốt, thưa kiện có nhiều lý phải."),
            21: ("Kim Dương", "Xuất hành tốt, có quý nhân phù trợ, tài lộc thông suốt, thưa kiện có nhiều lý phải."),
            27: ("Kim Dương", "Xuất hành tốt, có quý nhân phù trợ, tài lộc thông suốt, thưa kiện có nhiều lý phải."),
            4: ("Thuần Dương", "Xuất hành tốt, lúc về cũng tốt, nhiều thuận lợi, được người tốt giúp đỡ, cầu tài được như ý muốn."),
            10: ("Thuần Dương", "Xuất hành tốt, lúc về cũng tốt, nhiều thuận lợi, được người tốt giúp đỡ, cầu tài được như ý muốn."),
            16: ("Thuần Dương", "Xuất hành tốt, lúc về cũng tốt, nhiều thuận lợi, được người tốt giúp đỡ, cầu tài được như ý muốn."),
            22: ("Thuần Dương", "Xuất hành tốt, lúc về cũng tốt, nhiều thuận lợi, được người tốt giúp đỡ, cầu tài được như ý muốn."),
            28: ("Thuần Dương", "Xuất hành tốt, lúc về cũng tốt, nhiều thuận lợi, được người tốt giúp đỡ, cầu tài được như ý muốn."),
            5: ("Đạo Tặc", "Rất xấu, xuất hành bị hại, mất của, nhiều bất lợi."),
            11: ("Đạo Tặc", "Rất xấu, xuất hành bị hại, mất của, nhiều bất lợi."),
            17: ("Đạo Tặc", "Rất xấu, xuất hành bị hại, mất của, nhiều bất lợi."),
            23: ("Đạo Tặc", "Rất xấu, xuất hành bị hại, mất của, nhiều bất lợi."),
            29: ("Đạo Tặc", "Rất xấu, xuất hành bị hại, mất của, nhiều bất lợi."),
            6: ("Hảo Thương", "Xuất hành thuận lợi, gặp quý nhân phù trợ, làm mọi việc vừa lòng, như ý muốn, áo phẩm vinh quy."),
            12: ("Hảo Thương", "Xuất hành thuận lợi, gặp quý nhân phù trợ, làm mọi việc vừa lòng, như ý muốn, áo phẩm vinh quy."),
            18: ("Hảo Thương", "Xuất hành thuận lợi, gặp quý nhân phù trợ, làm mọi việc vừa lòng, như ý muốn, áo phẩm vinh quy."),
            24: ("Hảo Thương", "Xuất hành thuận lợi, gặp quý nhân phù trợ, làm mọi việc vừa lòng, như ý muốn, áo phẩm vinh quy."),
            30: ("Hảo Thương", "Xuất hành thuận lợi, gặp quý nhân phù trợ, làm mọi việc vừa lòng, như ý muốn, áo phẩm vinh quy.")
        }
    elif lunar_month in group_2:
        mapping = {
            1: ("Thiên Đạo", "Xuất hành cầu tài nên tránh, dù được cũng rất tốn kém, thất lý mà thua."),
            9: ("Thiên Đạo", "Xuất hành cầu tài nên tránh, dù được cũng rất tốn kém, thất lý mà thua."),
            17: ("Thiên Đạo", "Xuất hành cầu tài nên tránh, dù được cũng rất tốn kém, thất lý mà thua."),
            25: ("Thiên Đạo", "Xuất hành cầu tài nên tránh, dù được cũng rất tốn kém, thất lý mà thua."),
            2: ("Thiên Môn", "Xuất hành làm mọi việc đều vừa ý, cầu được ước thấy, mọi việc đều thành đạt."),
            10: ("Thiên Môn", "Xuất hành làm mọi việc đều vừa ý, cầu được ước thấy, mọi việc đều thành đạt."),
            18: ("Thiên Môn", "Xuất hành làm mọi việc đều vừa ý, cầu được ước thấy, mọi việc đều thành đạt."),
            26: ("Thiên Môn", "Xuất hành làm mọi việc đều vừa ý, cầu được ước thấy, mọi việc đều thành đạt."),
            3: ("Thiên Đường", "Xuất hành tốt, quý nhân phù trợ, buôn bán may mắn, mọi việc đều như ý."),
            11: ("Thiên Đường", "Xuất hành tốt, quý nhân phù trợ, buôn bán may mắn, mọi việc đều như ý."),
            19: ("Thiên Đường", "Xuất hành tốt, quý nhân phù trợ, buôn bán may mắn, mọi việc đều như ý."),
            27: ("Thiên Đường", "Xuất hành tốt, quý nhân phù trợ, buôn bán may mắn, mọi việc đều như ý."),
            4: ("Thiên Tài", "Nên xuất hành, cầu tài thắng lợi, được người tốt giúp đỡ, mọi việc đều thuận."),
            12: ("Thiên Tài", "Nên xuất hành, cầu tài thắng lợi, được người tốt giúp đỡ, mọi việc đều thuận."),
            20: ("Thiên Tài", "Nên xuất hành, cầu tài thắng lợi, được người tốt giúp đỡ, mọi việc đều thuận."),
            28: ("Thiên Tài", "Nên xuất hành, cầu tài thắng lợi, được người tốt giúp đỡ, mọi việc đều thuận."),
            5: ("Thiên Tặc", "Xuất hành xấu, cầu tài không được, đi đường dễ mất cắp, mọi việc đều rất xấu."),
            13: ("Thiên Tặc", "Xuất hành xấu, cầu tài không được, đi đường dễ mất cắp, mọi việc đều rất xấu."),
            21: ("Thiên Tặc", "Xuất hành xấu, cầu tài không được, đi đường dễ mất cắp, mọi việc đều rất xấu."),
            29: ("Thiên Tặc", "Xuất hành xấu, cầu tài không được, đi đường dễ mất cắp, mọi việc đều rất xấu."),
            6: ("Thiên Dương", "Xuất hành tốt, cầu tài được tài, hỏi vợ được vợ, mọi việc đều như ý muốn."),
            14: ("Thiên Dương", "Xuất hành tốt, cầu tài được tài, hỏi vợ được vợ, mọi việc đều như ý muốn."),
            22: ("Thiên Dương", "Xuất hành tốt, cầu tài được tài, hỏi vợ được vợ, mọi việc đều như ý muốn."),
            30: ("Thiên Dương", "Xuất hành tốt, cầu tài được tài, hỏi vợ được vợ, mọi việc đều như ý muốn."),
            7: ("Thiên Hầu", "Xuất hành dù ít hay nhiều cũng cãi cọ, phải tránh xảy ra tai nạn chảy máu."),
            15: ("Thiên Hầu", "Xuất hành dù ít hay nhiều cũng cãi cọ, phải tránh xảy ra tai nạn chảy máu."),
            23: ("Thiên Hầu", "Xuất hành dù ít hay nhiều cũng cãi cọ, phải tránh xảy ra tai nạn chảy máu."),
            8: ("Thiên Thương", "Xuất hành gặp cấp trên thì tuyệt vời, cầu tài thì được tài, mọi việc đều thuận lợi."),
            16: ("Thiên Thương", "Xuất hành gặp cấp trên thì tuyệt vời, cầu tài thì được tài, mọi việc đều thuận lợi."),
            24: ("Thiên Thương", "Xuất hành gặp cấp trên thì tuyệt vời, cầu tài thì được tài, mọi việc đều thuận lợi.")
        }
    else:
        mapping = {
            1: ("Chu Tước", "Xuất hành, cầu tài đều xấu, hay mất của, kiện cáo thua vì đuối lý."),
            9: ("Chu Tước", "Xuất hành, cầu tài đều xấu, hay mất của, kiện cáo thua vì đuối lý."),
            17: ("Chu Tước", "Xuất hành, cầu tài đều xấu, hay mất của, kiện cáo thua vì đuối lý."),
            25: ("Chu Tước", "Xuất hành, cầu tài đều xấu, hay mất của, kiện cáo thua vì đuối lý."),
            2: ("Bạch Hổ Đầu", "Xuất hành, cầu tài đều được, đi đâu đều thông đạt cả."),
            10: ("Bạch Hổ Đầu", "Xuất hành, cầu tài đều được, đi đâu đều thông đạt cả."),
            18: ("Bạch Hổ Đầu", "Xuất hành, cầu tài đều được, đi đâu đều thông đạt cả."),
            26: ("Bạch Hổ Đầu", "Xuất hành, cầu tài đều được, đi đâu đều thông đạt cả."),
            3: ("Bạch Hổ Kiếp", "Xuất hành, cầu tài được như ý muốn, đi hướng Nam và Bắc rất thuận lợi."),
            11: ("Bạch Hổ Kiếp", "Xuất hành, cầu tài được như ý muốn, đi hướng Nam và Bắc rất thuận lợi."),
            19: ("Bạch Hổ Kiếp", "Xuất hành, cầu tài được như ý muốn, đi hướng Nam và Bắc rất thuận lợi."),
            27: ("Bạch Hổ Kiếp", "Xuất hành, cầu tài được như ý muốn, đi hướng Nam và Bắc rất thuận lợi."),
            4: ("Bạch Hổ Túc", "Cấm đi xa, làm việc gì cũng không thành công, rất xấu trong mọi việc."),
            12: ("Bạch Hổ Túc", "Cấm đi xa, làm việc gì cũng không thành công, rất xấu trong mọi việc."),
            20: ("Bạch Hổ Túc", "Cấm đi xa, làm việc gì cũng không thành công, rất xấu trong mọi việc."),
            28: ("Bạch Hổ Túc", "Cấm đi xa, làm việc gì cũng không thành công, rất xấu trong mọi việc."),
            5: ("Huyền Vũ", "Xuất hành thường gặp cãi cọ, gặp việc xấu, không nên đi."),
            13: ("Huyền Vũ", "Xuất hành thường gặp cãi cọ, gặp việc xấu, không nên đi."),
            21: ("Huyền Vũ", "Xuất hành thường gặp cãi cọ, gặp việc xấu, không nên đi."),
            29: ("Huyền Vũ", "Xuất hành thường gặp cãi cọ, gặp việc xấu, không nên đi."),
            6: ("Thanh Long Đầu", "Xuất hành nên đi vào sáng sớm, cầu tài thắng lợi, mọi việc như ý."),
            14: ("Thanh Long Đầu", "Xuất hành nên đi vào sáng sớm, cầu tài thắng lợi, mọi việc như ý."),
            22: ("Thanh Long Đầu", "Xuất hành nên đi vào sáng sớm, cầu tài thắng lợi, mọi việc như ý."),
            30: ("Thanh Long Đầu", "Xuất hành nên đi vào sáng sớm, cầu tài thắng lợi, mọi việc như ý."),
            7: ("Thanh Long Kiếp", "Xuất hành 4 phương 8 hướng đều tốt, trăm sự được như ý."),
            15: ("Thanh Long Kiếp", "Xuất hành 4 phương 8 hướng đều tốt, trăm sự được như ý."),
            23: ("Thanh Long Kiếp", "Xuất hành 4 phương 8 hướng đều tốt, trăm sự được như ý."),
            8: ("Thanh Long Túc", "Đi xa không nên, xuất hành xấu, tài lộc không có, kiện cáo đuối lý."),
            16: ("Thanh Long Túc", "Đi xa không nên, xuất hành xấu, tài lộc không có, kiện cáo đuối lý."),
            24: ("Thanh Long Túc", "Đi xa không nên, xuất hành xấu, tài lộc không có, kiện cáo đuối lý.")
        }

    res = mapping.get(lunar_day, ("Không xác định", "Không có thông tin"))
    return f"Ngày {res[0]}: {res[1]}"

class CalendarFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Tra Cứu Lịch Âm Dương", size=(650, 620))
        
        self.sound_flip = wx.adv.Sound("flip_calendar.wav")

        panel = wx.Panel(self)
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        lbl_title = wx.StaticText(panel, label="TRA CỨU LỊCH ÂM DƯƠNG")
        font_title = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        lbl_title.SetFont(font_title)
        main_sizer.Add(lbl_title, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 15)

        input_box = wx.StaticBox(panel, label="Nhập ngày tháng năm")
        input_sizer = wx.StaticBoxSizer(input_box, wx.HORIZONTAL)

        lbl_day = wx.StaticText(panel, label="Ngày:")
        self.txt_day = wx.TextCtrl(panel, size=(50, -1), style=wx.TE_PROCESS_ENTER)
        self.txt_day.SetName("Ngày")
        
        lbl_month = wx.StaticText(panel, label="Tháng:")
        self.txt_month = wx.TextCtrl(panel, size=(50, -1), style=wx.TE_PROCESS_ENTER)
        self.txt_month.SetName("Tháng")

        lbl_year = wx.StaticText(panel, label="Năm:")
        self.txt_year = wx.TextCtrl(panel, size=(70, -1), style=wx.TE_PROCESS_ENTER)
        self.txt_year.SetName("Năm")

        input_sizer.Add(lbl_day, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 5)
        input_sizer.Add(self.txt_day, 0, wx.ALL, 5)
        input_sizer.Add(lbl_month, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)
        input_sizer.Add(self.txt_month, 0, wx.ALL, 5)
        input_sizer.Add(lbl_year, 0, wx.ALIGN_CENTER_VERTICAL | wx.LEFT, 10)
        input_sizer.Add(self.txt_year, 0, wx.ALL, 5)

        main_sizer.Add(input_sizer, 0, wx.EXPAND | wx.LEFT | wx.RIGHT, 15)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self.btn_prev = wx.Button(panel, label="Xem  lịch ngày hôm &trước")
        self.btn_today = wx.Button(panel, label="&Xem lịch ngày hôm nay")
        self.btn_next = wx.Button(panel, label=" Xem lịch ngày hôm &sau")
        self.btn_search_solar = wx.Button(panel, label="Tra cứu &lịch dương")
        self.btn_search_lunar = wx.Button(panel, label="Tra cứu lịc&h âm")

        btn_sizer.Add(self.btn_prev, 0, wx.RIGHT, 5)
        btn_sizer.Add(self.btn_today, 0, wx.RIGHT, 5)
        btn_sizer.Add(self.btn_next, 0, wx.RIGHT, 5)
        btn_sizer.Add(self.btn_search_solar, 0, wx.RIGHT, 5)
        btn_sizer.Add(self.btn_search_lunar, 0, wx.LEFT, 5)

        main_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP | wx.BOTTOM, 15)

        res_box = wx.StaticBox(panel, label="Thông tin Lịch Âm Dương")
        res_sizer = wx.StaticBoxSizer(res_box, wx.VERTICAL)

        result_inner_sizer = wx.BoxSizer(wx.HORIZONTAL)

        self.txt_result = wx.TextCtrl(
            panel, 
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_DONTWRAP, 
            size=(-1, 280)
        )
        self.txt_result.SetName("Kết quả lịch")
        font_res = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.txt_result.SetFont(font_res)

        self.btn_copy = wx.Button(panel, label="sao chép vào &bộ nhớ tạm")

        result_inner_sizer.Add(self.txt_result, 1, wx.EXPAND | wx.RIGHT, 5)
        result_inner_sizer.Add(self.btn_copy, 0, wx.ALIGN_TOP)

        res_sizer.Add(result_inner_sizer, 1, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(res_sizer, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)

        panel.SetSizer(main_sizer)

        self.btn_prev.Bind(wx.EVT_BUTTON, self.on_prev_day)
        self.btn_today.Bind(wx.EVT_BUTTON, self.on_show_today)
        self.btn_next.Bind(wx.EVT_BUTTON, self.on_next_day)
        self.btn_search_solar.Bind(wx.EVT_BUTTON, self.on_search_solar)
        self.btn_search_lunar.Bind(wx.EVT_BUTTON, self.on_search_lunar)
        self.btn_copy.Bind(wx.EVT_BUTTON, self.on_copy_clipboard)
        
        self.txt_day.Bind(wx.EVT_TEXT_ENTER, self.on_search_solar)
        self.txt_month.Bind(wx.EVT_TEXT_ENTER, self.on_search_solar)
        self.txt_year.Bind(wx.EVT_TEXT_ENTER, self.on_search_solar)

        self.Center()
        self.on_show_today(None)

    def update_calendar(self, d, m, y):
        try:
            dt = datetime.date(y, m, d)
        except ValueError:
            wx.MessageBox("Ngày tháng năm không hợp lệ!", "Lỗi nhập liệu", wx.OK | wx.ICON_ERROR)
            return

        thu_str = THU_VN[dt.weekday()]
        ld, lm, ly, is_leap, jd = convert_solar_to_lunar(d, m, y)
        can_chi_nam = get_can_chi_nam(ly)
        can_chi_ngay = get_can_chi_ngay(jd)
        can_chi_thang = get_can_chi_thang(lm, ly)
        nhuan_str = " (Nhuận)" if is_leap else ""

        if is_leap_year_solar(y):
            solar_leap_info = f"Năm {y} là năm nhuận Dương lịch (có 29 ngày vào tháng 2)."
        else:
            solar_leap_info = f"Năm {y} là năm không nhuận Dương lịch."

        has_lunar_leap, leap_month = get_lunar_year_leap_info(ly)
        if has_lunar_leap:
            lunar_leap_info = f"Năm Âm lịch nhuận tháng {leap_month}"
        else:
            lunar_leap_info = f"Năm Âm lịch này không phải năm nhuận"

        tiet_khi_str = get_tiet_khi(jd)
        gio_hoang_dao_str = get_gio_hoang_dao(jd)
        khong_minh_str = get_khong_minh_xuat_hanh(ld, lm)

        output_text = (
            f"Thứ: {thu_str}\n"
            f"Dương lịch: Ngày {d} tháng {m} năm {y}\n"
            f"Âm lịch: Ngày {ld} tháng {lm}{nhuan_str} năm {ly}\n"
            f"Ngày: {can_chi_ngay}\n"
            f"Tháng: {can_chi_thang} (Tháng {THANG_AM[lm-1]})\n"
            f"Năm: {can_chi_nam} ({ly})\n"
            f"✦ Thông tin Nhuận Dương Lịch: {solar_leap_info}\n"
            f"✦ Thông tin Nhuận Âm Lịch: {lunar_leap_info}\n"
            f"✦ Tiết khí: {tiet_khi_str}\n"
            f"✦ Giờ Hoàng Đạo: {gio_hoang_dao_str}\n"
            f"✦ Lịch Xuất Hành Khổng Minh: {khong_minh_str}"
        )

        self.txt_day.SetValue(str(d))
        self.txt_month.SetValue(str(m))
        self.txt_year.SetValue(str(y))

        self.txt_result.SetValue(output_text)
        self.txt_result.SetFocus()

    def on_show_today(self, event):
        if self.sound_flip.IsOk():
            self.sound_flip.Play(wx.adv.SOUND_ASYNC)
        now = datetime.datetime.now()
        self.update_calendar(now.day, now.month, now.year)

    def on_prev_day(self, event):
        if self.sound_flip.IsOk():
            self.sound_flip.Play(wx.adv.SOUND_ASYNC)

        try:
            d = int(self.txt_day.GetValue().strip())
            m = int(self.txt_month.GetValue().strip())
            y = int(self.txt_year.GetValue().strip())
            current_date = datetime.date(y, m, d)
            prev_date = current_date - datetime.timedelta(days=1)
            self.update_calendar(prev_date.day, prev_date.month, prev_date.year)
        except ValueError:
            wx.MessageBox("Vui lòng nhập ngày tháng năm hợp lệ trước khi chuyển ngày!", "Lỗi nhập liệu", wx.OK | wx.ICON_ERROR)

    def on_next_day(self, event):
        if self.sound_flip.IsOk():
            self.sound_flip.Play(wx.adv.SOUND_ASYNC)

        try:
            d = int(self.txt_day.GetValue().strip())
            m = int(self.txt_month.GetValue().strip())
            y = int(self.txt_year.GetValue().strip())
            current_date = datetime.date(y, m, d)
            next_date = current_date + datetime.timedelta(days=1)
            self.update_calendar(next_date.day, next_date.month, next_date.year)
        except ValueError:
            wx.MessageBox("Vui lòng nhập ngày tháng năm hợp lệ trước khi chuyển ngày!", "Lỗi nhập liệu", wx.OK | wx.ICON_ERROR)

    def on_search_solar(self, event):
        try:
            d = int(self.txt_day.GetValue().strip())
            m = int(self.txt_month.GetValue().strip())
            y = int(self.txt_year.GetValue().strip())
            self.update_calendar(d, m, y)
        except ValueError:
            wx.MessageBox("Vui lòng nhập số hợp lệ vào các ô Ngày, Tháng, Năm!", "Lỗi nhập liệu", wx.OK | wx.ICON_ERROR)

    def on_search_lunar(self, event):
        try:
            ld = int(self.txt_day.GetValue().strip())
            lm = int(self.txt_month.GetValue().strip())
            ly = int(self.txt_year.GetValue().strip())
            
            sd, sm, sy = convert_lunar_to_solar(ld, lm, ly, False)
            self.update_calendar(sd, sm, sy)
        except ValueError:
            wx.MessageBox("Vui lòng nhập ngày tháng năm Âm lịch hợp lệ!", "Lỗi nhập liệu", wx.OK | wx.ICON_ERROR)

    def on_copy_clipboard(self, event):
        text_to_copy = self.txt_result.GetValue()
        if text_to_copy:
            if wx.TheClipboard.Open():
                wx.TheClipboard.SetData(wx.TextDataObject(text_to_copy))
                wx.TheClipboard.Close()
                wx.MessageBox("Đã sao chép thông tin lịch vào bộ nhớ tạm!", "Thông báo", wx.OK | wx.ICON_INFORMATION)
            else:
                wx.MessageBox("Không thể mở bộ nhớ!", "Lỗi", wx.OK | wx.ICON_ERROR)

if __name__ == "__main__":
    app = wx.App(False)
    frame = CalendarFrame()
    frame.Show()
    app.MainLoop()