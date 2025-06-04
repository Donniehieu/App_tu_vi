// an12cung.js - Tiện ích an 12 cung, nạp can chi các cung theo can năm sinh (Tử vi Bắc phái)

// Danh sách thiên can và địa chi
const CAN = ["Giáp", "Ất", "Bính", "Đinh", "Mậu", "Kỷ", "Canh", "Tân", "Nhâm", "Quý"];
const CHI = ["Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"];
// Địa chi 12 cung trên bàn lá số Bắc phái, bắt đầu từ Dần (cung 13)
const CHI_CUNG_BAN = ["Dần", "Mão", "Thìn", "Tỵ", "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi", "Tý", "Sửu"];
// Tên đầy đủ 12 cung tử vi
const CUNG_TUVI = [
    "Mệnh", "Phụ Mẫu", "Phúc Đức", "Điền Trạch", "Quan Lộc", "Nô Bộc",
    "Thiên Di", "Tật Ách", "Tài Bạch", "Tử Tức", "Phu Thê", "Huynh Đệ"
];

// Bảng khởi can tháng giêng (Dần) theo can năm
const START_CAN_THANG = {
    "Giáp": 2, // Bính
    "Kỷ": 2,   // Bính
    "Ất": 4,   // Mậu
    "Canh": 4, // Mậu
    "Bính": 6, // Canh
    "Tân": 6,  // Canh
    "Đinh": 8, // Nhâm
    "Nhâm": 8, // Nhâm
    "Mậu": 0,  // Giáp
    "Quý": 0   // Giáp
};

/**
 * An 12 cung từ vị trí cung Mệnh (index trên bàn CHI_CUNG_BAN), trả về mảng đối tượng {cung, chi}
 * @param {number} menhIdx - vị trí cung Mệnh trên bàn CHI_CUNG_BAN (0 = Dần, 1 = Mão,...)
 * @returns {Array<{cung, chi}>}
 */
function an12Cung(menhIdx) {
    let arr = [];
    for (let i = 0; i < 12; ++i) {
        let chi = CHI_CUNG_BAN[(menhIdx + i) % 12];
        arr.push({
            cung: CUNG_TUVI[i],
            chi: chi
        });
    }
    return arr;
}

/**
 * Lấy mảng Can 12 cung, khởi đầu từ can tháng giêng (Dần) theo can năm âm lịch
 * @param {string} canNam - Thiên can năm sinh (vd: "Giáp", "Kỷ",...)
 * @returns {Array<string>} - Mảng 12 can cho 12 cung (Dần, Mão, ..., Sửu)
 */
function getCanThangArray(canNam) {
    let startIdx = START_CAN_THANG[canNam];
    if (typeof startIdx === "undefined") return [];
    let arr = [];
    for (let i = 0; i < 12; ++i) {
        arr.push(CAN[(startIdx + i) % 10]);
    }
    return arr;
}

/**
 * Nạp can chi cho 12 cung theo can năm sinh
 * @param {string} canNam - Thiên can năm sinh (vd: "Giáp", "Kỷ",...)
 * @returns {Array<{can, chi, label}>}
 */
function getCungCanChiArray(canNam) {
    let canArr = getCanThangArray(canNam);
    let arr = [];
    for (let i = 0; i < 12; ++i) {
        arr.push({
            can: canArr[i],
            chi: CHI_CUNG_BAN[i],
            label: canArr[i] + " " + CHI_CUNG_BAN[i]
        });
    }
    return arr;
}

/**
 * Hiển thị tên cung + can chi lên bàn lá số theo vị trí cung Mệnh
 * @param {number} menhIdx - vị trí cung Mệnh trên bàn (Dần=0, Mão=1,...)
 * @param {string} canNam - can năm sinh
 */
function hienThiCungCanChiLaso(menhIdx, canNam) {
    let cungArr = an12Cung(menhIdx);
    let canChiArr = getCungCanChiArray(canNam);
    // Mapping chi->cell html
    const chi2cell = {
        "Dần": 13, "Mão": 9, "Thìn": 5, "Tỵ": 1, "Ngọ": 2, "Mùi": 3,
        "Thân": 4, "Dậu": 8, "Tuất": 12, "Hợi": 16, "Tý": 15, "Sửu": 14
    };
    for (let i = 0; i < 12; ++i) {
        let chi = cungArr[i].chi;
        let cellNum = chi2cell[chi];
        let cell = document.querySelector('.cell' + cellNum);
        if (cell) {
            cell.innerHTML = `<div style="font-weight:bold;text-align:center;width:100%;position:absolute;top:2px;left:0;right:0;font-size:1.05em;color:#a66300;">
                ${CUNG_TUVI[i]}</div>
                <div style="margin-top:1.6em;text-align:center;width:100%">${canChiArr[i].label}</div>`;
        }
    }
}

// ----- Export hàm cho file index.html dễ gọi -----
window.an12Cung = an12Cung;
window.getCungCanChiArray = getCungCanChiArray;
window.hienThiCungCanChiLaso = hienThiCungCanChiLaso;