// amlich-convert.js - Đổi dương lịch sang âm lịch, lấy Can Chi năm/tháng/ngày/giờ
// Can tháng tính đúng theo bảng khởi Can truyền thống Việt Nam

const CAN = ["G.","Ấ.","B.","Đ.","M.","K.","C.","T.","N.","Q."];
const CHI = ["Tý","Sửu","Dần","Mão","Thìn","Tỵ","Ngọ","Mùi","Thân","Dậu","Tuất","Hợi"];
const CHI_THANG = ["Dần","Mão","Thìn","Tỵ","Ngọ","Mùi","Thân","Dậu","Tuất","Hợi","Tý","Sửu"];

// Bảng khởi Can tháng 1 theo Can năm
const START_CAN_THANG = {
    "G.": 2, // Bính
    "K.": 2,   // Bính
    "Ấ.": 4,   // Mậu
    "C.": 4, // Mậu
    "B.": 6, // Canh
    "T.": 6,  // Canh
    "Đ.": 8, // Nhâm
    "N.": 8, // Nhâm
    "M.": 0,  // Giáp
    "Q.": 0   // Giáp
};

// Đổi ngày dương sang số ngày Julius
function INT(d) { return Math.floor(d); }
function jdFromDate(dd, mm, yy) {
    var a = INT((14 - mm) / 12);
    var y = yy + 4800 - a;
    var m = mm + 12 * a - 3;
    var jd = dd + INT((153 * m + 2) / 5) + 365 * y + INT(y / 4) - INT(y / 100) + INT(y / 400) - 32045;
    if (jd < 2299161) {
        jd = dd + INT((153 * m + 2) / 5) + 365 * y + INT(y / 4) - 32083;
    }
    return jd;
}

function getNewMoonDay(k, timeZone) {
    var T = k / 1236.85,
        T2 = T * T,
        T3 = T2 * T,
        dr = Math.PI / 180;
    var Jd1 = 2415020.75933 + 29.53058868 * k
        + 0.0001178 * T2
        - 0.000000155 * T3
        + 0.00033 * Math.sin((166.56 + 132.87 * T - 0.009173 * T2) * dr);
    var M = 359.2242 + 29.10535608 * k - 0.0000333 * T2 - 0.00000347 * T3;
    var Mpr = 306.0253 + 385.81691806 * k + 0.0107306 * T2 + 0.00001236 * T3;
    var F = 21.2964 + 390.67050646 * k - 0.0016528 * T2 - 0.00000239 * T3;
    var C1 = (0.1734 - 0.000393 * T) * Math.sin(M * dr)
        + 0.0021 * Math.sin(2 * dr * M)
        - 0.4068 * Math.sin(Mpr * dr)
        + 0.0161 * Math.sin(dr * 2 * Mpr)
        - 0.0004 * Math.sin(dr * 3 * Mpr)
        + 0.0104 * Math.sin(dr * 2 * F)
        - 0.0051 * Math.sin(dr * (M + Mpr))
        - 0.0074 * Math.sin(dr * (M - Mpr))
        + 0.0004 * Math.sin(dr * (2 * F + M))
        - 0.0004 * Math.sin(dr * (2 * F - M))
        - 0.0006 * Math.sin(dr * (2 * F + Mpr))
        + 0.0010 * Math.sin(dr * (2 * F - Mpr))
        + 0.0005 * Math.sin(dr * (2 * Mpr + M));
    var deltat = 0;
    if (T < -11) {
        deltat = 0.001 + 0.000839 * T + 0.0002261 * T2 - 0.00000845 * T3 - 0.000000081 * T * T3;
    }
    else {
        deltat = -0.000278 + 0.000265 * T + 0.000262 * T2;
    }
    var JdNew = Jd1 + C1 - deltat;
    return INT(JdNew + 0.5 + timeZone / 24);
}

function getSunLongitude(jdn, timeZone) {
    var T = (jdn - 2451545.5 - timeZone / 24) / 36525,
        T2 = T * T,
        dr = Math.PI / 180;
    var M = 357.52910 + 35999.05030 * T - 0.0001559 * T2 - 0.00000048 * T * T2;
    var L0 = 280.46645 + 36000.76983 * T + 0.0003032 * T2;
    var DL = (1.914600 - 0.004817 * T - 0.000014 * T2) * Math.sin(dr * M)
        + (0.019993 - 0.000101 * T) * Math.sin(dr * 2 * M)
        + 0.000290 * Math.sin(dr * 3 * M);
    var L = L0 + DL;
    L = L % 360;
    return INT(L / 30);
}

function getLunarMonth11(yy, timeZone) {
    var off = jdFromDate(31, 12, yy) - 2415021,
        k = INT(off / 29.530588853),
        nm = getNewMoonDay(k, timeZone),
        sunLong = getSunLongitude(nm, timeZone);
    if (sunLong >= 9) {
        nm = getNewMoonDay(k - 1, timeZone);
    }
    return nm;
}

function getLeapMonthOffset(a11, timeZone) {
    var k = INT(0.5 + (a11 - 2415021.076998695) / 29.530588853),
        last = 0, i = 1,
        arc = getSunLongitude(getNewMoonDay(k + i, timeZone), timeZone);
    do {
        last = arc;
        i++;
        arc = getSunLongitude(getNewMoonDay(k + i, timeZone), timeZone);
    } while (arc != last && i < 14);
    return i - 1;
}

function convertSolar2Lunar(dd, mm, yy, timeZone) {
    var dayNumber = jdFromDate(dd, mm, yy),
        k = INT((dayNumber - 2415021.076998695) / 29.530588853),
        monthStart = getNewMoonDay(k + 1, timeZone);
    if (monthStart > dayNumber) {
        monthStart = getNewMoonDay(k, timeZone);
    }
    var a11 = getLunarMonth11(yy, timeZone),
        b11 = a11;
    var lunarYear;
    if (a11 >= monthStart) {
        lunarYear = yy;
        a11 = getLunarMonth11(yy - 1, timeZone);
    }
    else {
        lunarYear = yy + 1;
        b11 = getLunarMonth11(yy + 1, timeZone);
    }
    var lunarDay = dayNumber - monthStart + 1,
        diff = INT((monthStart - a11) / 29),
        lunarLeap = 0,
        lunarMonth = diff + 11,
        leapMonthDiff = b11 - a11;
    if (leapMonthDiff > 365) {
        var leapMonth = getLeapMonthOffset(a11, timeZone);
        if (diff >= leapMonth) {
            lunarMonth = diff + 10;
            if (diff == leapMonth) lunarLeap = 1;
        }
    }
    if (lunarMonth > 12) lunarMonth -= 12;
    if (lunarMonth >= 11 && diff < 4) lunarYear -= 1;
    return [lunarDay, lunarMonth, lunarYear, lunarLeap];
}

// Can chi năm âm lịch
function getCanChiNam(yearLunar) {
    return CAN[(yearLunar - 4) % 10] + " " + CHI[(yearLunar - 4) % 12];
}

// Can tháng truyền thống: tra theo bảng khởi Can năm
function getCanChiThang(yearLunar, monthLunar) {
    // Xác định can năm
    const canNamIdx = (yearLunar - 4) % 10;
    const canNam = CAN[canNamIdx];
    const startCanThang = START_CAN_THANG[canNam];
    // Can tháng = can bắt đầu + (tháng âm - 1) theo vòng 10
    const canThangIdx = (startCanThang + (monthLunar - 1)) % 10;
    const chiThangIdx = (monthLunar - 1) % 12;
    return CAN[canThangIdx] + " " + CHI_THANG[chiThangIdx];
}

// Can chi ngày - tính theo số ngày Julius
function getCanChiNgay(jd) {
    const canNgayIdx = (jd + 9) % 10;
    const chiNgayIdx = (jd + 1) % 12;
    return CAN[canNgayIdx] + " " + CHI[chiNgayIdx];
}

// Can chi giờ - truyền vào can ngày (dạng số) và chi giờ (chuỗi)
function getCanChiGio(canNgayIdx, chiGio) {
    const chiIdx = CHI.indexOf(chiGio);
    const canGioIdx = (canNgayIdx * 2 + chiIdx) % 10;
    return CAN[canGioIdx] + " " + chiGio;
}

// Hàm trả về đầy đủ can chi năm/tháng/ngày/giờ và ngày âm
function getCanChiFull(dd, mm, yy, gioChi) {
    const timeZone = 7;
    const [lunarDay, lunarMonth, lunarYear, lunarLeap] = convertSolar2Lunar(dd, mm, yy, timeZone);
    const canchiNam = getCanChiNam(lunarYear);
    const canchiThang = getCanChiThang(lunarYear, lunarMonth);
    const jd = jdFromDate(dd, mm, yy);
    const canchiNgay = getCanChiNgay(jd);
    const canNgayIdx = (jd + 9) % 10;
    const canchiGio = getCanChiGio(canNgayIdx, gioChi);
    return {
        amlich: { ngay: lunarDay, thang: lunarMonth, nam: lunarYear, nhuan: lunarLeap },
        canchi: {
            nam: canchiNam,
            thang: canchiThang,
            ngay: canchiNgay,
            gio: canchiGio
        }
    };
}

// Ví dụ sử dụng:
// const kq = getCanChiFull(8,8,2008,"Thân");
// console.log(kq);
// Tháng 7 âm 2008 là "Kỷ Thân" (Can tháng theo bảng khởi Can truyền thống)