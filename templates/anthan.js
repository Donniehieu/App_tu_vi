// Thứ tự 12 cung ngoài Bắc phái (bắt đầu từ Dần là tháng 1)
const CUNG_CELLS = [
    {cell: 13, chi: "Dần"},
    {cell: 9,  chi: "Mão"},
    {cell: 5,  chi: "Thìn"},
    {cell: 1,  chi: "Tỵ"},
    {cell: 2,  chi: "Ngọ"},
    {cell: 3,  chi: "Mùi"},
    {cell: 4,  chi: "Thân"},
    {cell: 8,  chi: "Dậu"},
    {cell: 12, chi: "Tuất"},
    {cell: 16, chi: "Hợi"},
    {cell: 15, chi: "Tý"},
    {cell: 14, chi: "Sửu"}
];
const CHI12 = ["Tý","Sửu","Dần","Mão","Thìn","Tỵ","Ngọ","Mùi","Thân","Dậu","Tuất","Hợi"];

/** 
 * Hàm xác định cung Thân đúng Bắc phái: 
 * - thang_am: tháng sinh âm (1-12)
 * - gio_chi: tên chi giờ sinh, vd "Tý", "Sửu"...
 */
function getThanCell(thang_am, gio_chi) {
    // Bước 1: Xác định vị trí index cung tháng sinh (Dần là tháng 1, index 0)
    let cungThangIdx = (thang_am - 1) % 12; // tháng 1 = Dần = 0
    // Bước 2: Đếm số bước từ Tý tới giờ sinh (gồm cả điểm đầu, nên +1)
    let soBuoc = CHI12.indexOf(gio_chi) + 1;
    // Bước 3: Đếm thuận từ cung tháng sinh, bước sốBuoc-1 bước (vì tính vị trí bắt đầu là Tý)
    let cungThanIdx = (cungThangIdx + soBuoc - 1) % 12;
    return CUNG_CELLS[cungThanIdx];
}