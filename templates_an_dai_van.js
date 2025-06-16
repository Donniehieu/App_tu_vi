/**
 * Tính đại vận cho 12 cung lá số tử vi Bắc phái.
 * @param {number} menhIdx - Chỉ số cung Mệnh (0-11, bắt đầu từ Dần thuận chiều kim đồng hồ)
 * @param {number} cucSo - Số của Cục (2~6)
 * @param {string} amduong - Chuỗi: "Dương Nam", "Dương Nữ", "Âm Nam", "Âm Nữ"
 * @returns {Array<number>} - Mảng 12 số đại vận ứng với 12 cung, index 0 là cung Mệnh, tiếp đến các cung xung quanh.
 */
function tinhDaiVan(menhIdx, cucSo, amduong) {
    // Số đại vận cho 12 cung, khởi tạo
    let daiVanArr = Array(12).fill(0);
    // Xác định chiều: thuận = +1, ngược = -1
    let isThuan = (amduong === "Dương Nam" || amduong === "Âm Nữ");
    // Đặt số cục tại cung Mệnh
    let idx = menhIdx;
    for (let i = 0; i < 12; ++i) {
        daiVanArr[idx] = cucSo + i * 10;
        // Tính chỉ số cung tiếp theo
        idx = (idx + (isThuan ? 1 : -1) + 12) % 12;
    }
    return daiVanArr;
}

/**
 * Ví dụ sử dụng:
 * menhIdx = 8 (cung Tuất), cucSo = 5 (Thổ ngũ cục), amduong = "Dương Nam"
 * ==> tinhDaiVan(8, 5, "Dương Nam")
 * Kết quả: [ , , , , , , , , 5, 15, 25, 35, 45 ] (5 tại Tuất, 15 tại Hợi, 25 tại Tý...)
 */