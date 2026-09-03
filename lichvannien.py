import datetime
import math
import wx

CAN = ['Giáp', 'Ất', 'Bính', 'Đinh', 'Mậu', 'Kỷ', 'Canh', 'Tân', 'Nhâm', 'Quý']
CHI = ['Tý', 'Sửu', 'Dần', 'Mão', 'Thìn', 'Tỵ', 'Ngọ', 'Mùi', 'Thân', 'Dậu', 'Tuất', 'Hợi']
THANG_AM = ['Giêng', 'Hai', 'Ba', 'Tư', 'Năm', 'Sáu', 'Bảy', 'Tám', 'Chín', 'Mười', 'Mười Một', 'Chạp']
THU_VN = ['Thứ Hai', 'Thứ Ba', 'Thứ Tư', 'Thứ Năm', 'Thứ Sáu', 'Thứ Bảy', 'Chủ Nhật']

def _INT(d):
    return int(math.floor(d))

def jdFromDate(dd, mm, yy):
    if yy < 0: 
        yy += 1
    if mm <= 2:
        yy -= 1
        mm += 12
    A = int(yy / 100)
    B = int(A / 4)
    C = int(2 - A + B)
    E = int(365.25 * (yy + 4716))
    F = int(30.6001 * (mm + 1))
    return int(C + dd + E + F - 1524.5)

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
    C1 -= 0.4068 * math.sin(Mpr * dr) + 0.0161 * math.sin(2 * Mpr * dr)
    C1 -= 0.0004 * math.sin(3 * Mpr * dr)
    C1 += 0.0104 * math.sin(2 * F * dr) - 0.0051 * math.sin((M + Mpr) * dr)
    C1 -= 0.0074 * math.sin((M - Mpr) * dr) + 0.0004 * math.sin((2 * F + M) * dr)
    C1 -= 0.0004 * math.sin((2 * F - M) * dr) - 0.0006 * math.sin((2 * F + Mpr) * dr)
    C1 += 0.0010 * math.sin((2 * F - Mpr) * dr) + 0.0005 * math.sin((M + 2 * Mpr) * dr)
    if T < -11:
        deltaT = 0.001 + 0.00054 * math.cos((166.56 + 132.87 * T) * dr)
    else:
        deltaT = (T * T) * 0.0000278 + 0.000216
    JdNew = Jd1 + C1 - deltaT
    return _INT(JdNew + 0.5 + timeZone / 24.0)

def getSunLongitude(jdn, timeZone):
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
    return _INT(L / 30)

def getLunarMonth11(yy, timeZone):
    off = jdFromDate(31, 12, yy) - 2415020
    k = _INT(off / 29.53058867)
    nm = getNewMoonDay(k, timeZone)
    sunLong = getSunLongitude(nm, timeZone)
    if sunLong >= 9:
        k -= 1
        nm = getNewMoonDay(k, timeZone)
    return nm

def getLeapMonthOffset(a11, timeZone):
    k = _INT((a11 - 2415020.75933) / 29.53058867 + 0.5)
    i = 1
    arc = getSunLongitude(getNewMoonDay(k, timeZone), timeZone)
    while True:
        k += 1
        nm = getNewMoonDay(k, timeZone)
        sunLong = getSunLongitude(nm, timeZone)
        if sunLong == arc:
            return i
        arc = sunLong
        i += 1
        if i >= 14:
            break
    return 0

def convert_solar_to_lunar(dd, mm, yy):
    timeZone = 7.0
    dayNumber = jdFromDate(dd, mm, yy)
    k = _INT((dayNumber - 2415020.75933) / 29.53058867)
    nm = getNewMoonDay(k, timeZone)
    if nm > dayNumber:
        k -= 1
        nm = getNewMoonDay(k, timeZone)
    
    lunarDay = dayNumber - nm + 1
    a11 = getLunarMonth11(yy, timeZone)
    b11 = a11
    if a11 >= nm:
        a11 = getLunarMonth11(yy - 1, timeZone)
    else:
        b11 = getLunarMonth11(yy + 1, timeZone)
        
    k_a11 = _INT((a11 - 2415020.75933) / 29.53058867 + 0.5)
    off = k - k_a11
    
    is_leap = False
    leapMonth = 0
    if b11 - a11 > 365:
        leapMonth = getLeapMonthOffset(a11, timeZone)
        
    if leapMonth > 0:
        if off == leapMonth:
            is_leap = True
            lunarMonth = off + 10
        elif off > leapMonth:
            lunarMonth = off + 10
        else:
            lunarMonth = off + 11
    else:
        lunarMonth = off + 11
        
    if lunarMonth > 12:
        lunarMonth -= 12

    lunarYear = yy
    if lunarMonth >= 11 and mm < 6:
        lunarYear = yy - 1
    elif lunarMonth < 3 and mm > 10:
        lunarYear = yy + 1
    else:
        lunarYear = yy if a11 < nm else yy - 1

    return int(lunarDay), int(lunarMonth), int(lunarYear), is_leap, dayNumber

def get_can_chi_nam(year):
    if year < 0: 
        year += 1 
    return f"{CAN[(year + 6) % 10]} {CHI[(year + 8) % 12]}"

def get_can_chi_ngay(jd):
    can_ngay = CAN[(jd + 0) % 10]
    chi_ngay = CHI[(jd + 2) % 12]
    return f"{can_ngay} {chi_ngay}"

def get_can_chi_thang(lunar_month, lunar_year):
    can_nam_idx = (lunar_year + 6) % 10
    can_thang_gieng = (can_nam_idx * 2 + 2) % 10
    can_thang = (can_thang_gieng + lunar_month - 1) % 10
    
    chi_thang = (lunar_month + 1) % 12
    return f"{CAN[can_thang]} {CHI[chi_thang]}"

class CalendarFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Tra Cứu Lịch Âm Dương", size=(460, 480))
        
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
        
        self.btn_today = wx.Button(panel, label="&Xem lịch ngày hôm nay")
        self.btn_search = wx.Button(panel, label="&Tra cứu")

        btn_sizer.Add(self.btn_today, 0, wx.RIGHT, 10)
        btn_sizer.Add(self.btn_search, 0, wx.LEFT, 10)

        main_sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP | wx.BOTTOM, 15)

        res_box = wx.StaticBox(panel, label="Thông tin Lịch Âm Dương")
        res_sizer = wx.StaticBoxSizer(res_box, wx.VERTICAL)

        self.txt_result = wx.TextCtrl(
            panel, 
            style=wx.TE_MULTILINE | wx.TE_READONLY | wx.TE_DONTWRAP, 
            size=(-1, 160)
        )
        self.txt_result.SetName("Kết quả lịch")
        font_res = wx.Font(11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.txt_result.SetFont(font_res)

        res_sizer.Add(self.txt_result, 1, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(res_sizer, 1, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, 15)

        panel.SetSizer(main_sizer)

        self.btn_today.Bind(wx.EVT_BUTTON, self.on_show_today)
        self.btn_search.Bind(wx.EVT_BUTTON, self.on_search)
        
        self.txt_day.Bind(wx.EVT_TEXT_ENTER, self.on_search)
        self.txt_month.Bind(wx.EVT_TEXT_ENTER, self.on_search)
        self.txt_year.Bind(wx.EVT_TEXT_ENTER, self.on_search)

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

        output_text = (
            f"Thứ: {thu_str}\n"
            f"Dương lịch: Ngày {d} tháng {m} năm {y}\n"
            f"Âm lịch: Ngày {ld} tháng {lm}{nhuan_str} năm {ly}\n"
            f"Ngày: {can_chi_ngay}\n"
            f"Tháng: {can_chi_thang} (Tháng {THANG_AM[lm-1]})\n"
            f"Năm: {can_chi_nam}"
        )

        self.txt_result.SetValue(output_text)
        self.txt_result.SetFocus()

    def on_show_today(self, event):
        now = datetime.datetime.now()
        self.txt_day.SetValue(str(now.day))
        self.txt_month.SetValue(str(now.month))
        self.txt_year.SetValue(str(now.year))
        self.update_calendar(now.day, now.month, now.year)

    def on_search(self, event):
        try:
            d = int(self.txt_day.GetValue().strip())
            m = int(self.txt_month.GetValue().strip())
            y = int(self.txt_year.GetValue().strip())
            self.update_calendar(d, m, y)
        except ValueError:
            wx.MessageBox("Vui lòng nhập số hợp lệ vào các ô Ngày, Tháng, Năm!", "Lỗi nhập liệu", wx.OK | wx.ICON_ERROR)

if __name__ == "__main__":
    app = wx.App(False)
    frame = CalendarFrame()
    frame.Show()
    app.MainLoop()