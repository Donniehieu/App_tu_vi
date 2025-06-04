async function convertSolarToLunar(day, month, year) {
    // Gọi API chuyển đổi trên backend Flask
    let res = await fetch('http://localhost:5000/api/convert_solar_to_lunar', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({day, month, year})
    });
    let lunar = await res.json();
    return lunar; // {day, month, year, leap}
}

document.getElementById('form_tuvi').addEventListener('input', async function() {
    let loailich = document.querySelector('input[name="loailich"]:checked').value;
    let day = document.getElementById('ngay').value;
    let month = document.getElementById('thang').value;
    let year = document.getElementById('nam').value;
    let btn = document.getElementById('btn_xemtuvi');
    if (loailich === 'duong' && day && month && year) {
        let lunar = await convertSolarToLunar(day, month, year);
        document.getElementById('amlich').innerText = 
            `Âm lịch: ${lunar.day}/${lunar.month}${lunar.leap ? ' (Nhuận)' : ''}/${lunar.year}`;
        btn.disabled = false;
    } else if (loailich === 'am') {
        document.getElementById('amlich').innerText = '';
        btn.disabled = false;
    } else {
        btn.disabled = true;
    }
});