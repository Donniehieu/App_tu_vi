#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Vietnamese Astrology Complete Calculator
Tính An Mạng, An Thân và 12 cung theo phương pháp tử vi cổ truyền

Created by: Donniehieu
Date: 2025-05-26 04:10:53 UTC
"""

from typing import Dict, List, Tuple, Optional
import json

# Constants - Hằng số
EARTHLY_BRANCHES = [
    "Tý", "Sửu", "Dần", "Mão", "Thìn", "Tỵ",
    "Ngọ", "Mùi", "Thân", "Dậu", "Tuất", "Hợi"
]

TWELVE_PALACES = [
    "Mạng", "Phụ", "Phúc", "Điền", "Quan", "Nô",
    "Thiên", "Tật", "Tài", "Tử", "Phối", "Bào"
]

PALACE_FULL_NAMES = {
    "Mạng": "Mệnh",
    "Phụ": "Phụ Mẫu", 
    "Phúc": "Phúc Đức",
    "Điền": "Điền Trạch",
    "Quan": "Quan Lộc",
    "Nô": "Nô Bộc",
    "Thiên": "Thiên Di",
    "Tật": "Tật Ách",
    "Tài": "Tài Bạch",
    "Tử": "Tử Tức",
    "Phối": "Phu Thê",
    "Bào": "Huynh Đệ"
}

MONTH_NAMES_VN = {
    1: "Giêng", 2: "Hai", 3: "Ba", 4: "Tư", 5: "Năm", 6: "Sáu",
    7: "Bảy", 8: "Tám", 9: "Chín", 10: "Mười", 11: "Mười Một", 12: "Mười Hai"
}

# === BỔ SUNG CAN CHI THÁNG ÂM LỊCH 12 CUNG ===
CAN_LIST = ["Giáp","Ất","Bính","Đinh","Mậu","Kỷ","Canh","Tân","Nhâm","Quý"]
CHI_LIST = ["Tý","Sửu","Dần","Mão","Thìn","Tỵ","Ngọ","Mùi","Thân","Dậu","Tuất","Hợi"]
CHI_THANG_LIST = ["Dần","Mão","Thìn","Tỵ","Ngọ","Mùi","Thân","Dậu","Tuất","Hợi","Tý","Sửu"]
# Bảng khởi Can tháng 1 theo Can năm
START_CAN_THANG = {
    "Giáp": 2, # Bính
    "Kỷ": 2,   # Bính
    "Ất": 4,   # Mậu
    "Canh": 4, # Mậu
    "Bính": 6, # Canh
    "Tân": 6,  # Canh
    "Đinh": 8, # Nhâm
    "Nhâm": 8, # Nhâm
    "Mậu": 0,  # Giáp
    "Quý": 0   # Giáp
}

def get_can_chi_nam(nam_am: int) -> Tuple[str, str]:
    can = CAN_LIST[(nam_am - 4) % 10]
    chi = CHI_LIST[(nam_am - 4) % 12]
    return can, chi

def get_can_thang(nam_am: int, thang_am: int) -> str:
    """
    Trả về thiên can của tháng âm lịch (thang_am: 1-12)
    """
    can_nam = CAN_LIST[(nam_am - 4) % 10]
    start_can_idx = START_CAN_THANG[can_nam]
    idx = (start_can_idx + (thang_am - 1)) % 10
    return CAN_LIST[idx]

def get_12_cung_can_chi(nam_am: int) -> List[Dict[str, str]]:
    """
    Trả về danh sách 12 cung với can tháng và chi theo quy tắc Tử vi
    Địa chi bắt đầu từ Dần (cung 13, index 2), thuận kim đồng hồ
    Thiên can tháng xác định theo năm âm lịch và thứ tự tháng âm (1-12)
    """
    palaces = []
    for i in range(12):
        thang_am = i + 1  # tháng âm lịch 1-12 ứng với cung Dần, Mão, ...
        can = get_can_thang(nam_am, thang_am)
        chi = CHI_THANG_LIST[(i) % 12]  # Dần bắt đầu
        palace_name = TWELVE_PALACES[i]
        palaces.append({
            "palace": palace_name,
            "palace_full": PALACE_FULL_NAMES[palace_name],
            "can": can,
            "chi": chi,
            "canchi": f"{can}.{chi}",
            "month_am": thang_am
        })
    return palaces

def convert_hour_to_branch(hour: int) -> str:
    """
    Chuyển đổi giờ (0-23) thành địa chi
    
    Args:
        hour (int): Giờ trong ngày (0-23)
        
    Returns:
        str: Địa chi tương ứng
        
    Example:
        >>> convert_hour_to_branch(10)
        'Tỵ'
    """
    if hour in [23, 0, 1]:
        return "Tý"
    elif hour in [2, 3]:
        return "Sửu"
    elif hour in [4, 5]:
        return "Dần"
    elif hour in [6, 7]:
        return "Mão"
    elif hour in [8, 9]:
        return "Thìn"
    elif hour in [10, 11]:
        return "Tỵ"
    elif hour in [12, 13]:
        return "Ngọ"
    elif hour in [14, 15]:
        return "Mùi"
    elif hour in [16, 17]:
        return "Thân"
    elif hour in [18, 19]:
        return "Dậu"
    elif hour in [20, 21]:
        return "Tuất"
    elif hour == 22:
        return "Hợi"
    else:
        return "Tý"  # Default

def find_month_palace(birth_month: int) -> Tuple[str, int]:
    """
    Tìm cung tương ứng với tháng sinh
    Từ cung Dần kể là tháng Giêng, đếm thuận đến tháng sinh
    
    Args:
        birth_month (int): Tháng sinh (1-12)
        
    Returns:
        Tuple[str, int]: (tên_cung, vị_trí_index)
        
    Example:
        >>> find_month_palace(11)
        ('Tý', 0)
    """
    if not 1 <= birth_month <= 12:
        raise ValueError("Tháng sinh phải từ 1 đến 12")
    
    # Dần (index 2) = tháng Giêng (1)
    dan_index = 2
    month_palace_index = (dan_index + birth_month - 1) % 12
    month_palace = EARTHLY_BRANCHES[month_palace_index]
    
    return month_palace, month_palace_index

def calculate_an_mang(birth_month: int, birth_hour: int) -> Tuple[str, int]:
    """
    Tính An Mạng (đếm ngược từ Tý đến giờ sinh)
    
    Quy tắc: Từ cung Dần kể là tháng Giêng, đếm thuận từ cung đến tháng sinh 
    rồi từ đó kể là Tý, đếm ngược từng cung đến giờ sinh: An Mạng
    
    Args:
        birth_month (int): Tháng sinh (1-12) 
        birth_hour (int): Giờ sinh (0-23)
        
    Returns:
        Tuple[str, int]: (địa_chi_cung_mạng, vị_trí_index)
        
    Example:
        >>> calculate_an_mang(11, 10)
        ('Mùi', 7)
    """
    # Bước 1: Tìm cung tháng sinh
    month_palace, month_palace_index = find_month_palace(birth_month)
    
    # Bước 2: Chuyển giờ thành địa chi
    hour_branch = convert_hour_to_branch(birth_hour)
    hour_branch_index = EARTHLY_BRANCHES.index(hour_branch)
    
    # Bước 3: Từ cung tháng sinh (coi như Tý), đếm ngược đến giờ sinh
    # month_palace_index là vị trí Tý (index 0 trong chu kỳ đếm ngược)
    ty_index = 0
    steps_backward = (ty_index - hour_branch_index) % 12
    an_mang_index = (month_palace_index - steps_backward) % 12
    an_mang_branch = EARTHLY_BRANCHES[an_mang_index]
    
    return an_mang_branch, an_mang_index

def calculate_an_than(birth_month: int, birth_hour: int) -> Tuple[str, int]:
    """
    Tính An Thân (đếm thuận từ Tý đến giờ sinh)
    
    Quy tắc: Từ cung Dần kể là tháng Giêng, đếm thuận từ cung đến tháng sinh
    rồi từ đó kể là Tý, đếm thuận từng cung đến giờ sinh: An Thân
    
    Args:
        birth_month (int): Tháng sinh (1-12)
        birth_hour (int): Giờ sinh (0-23)
        
    Returns:
        Tuple[str, int]: (địa_chi_cung_thân, vị_trí_index)
        
    Example:
        >>> calculate_an_than(11, 10)
        ('Tỵ', 5)
    """
    # Bước 1: Tìm cung tháng sinh
    month_palace, month_palace_index = find_month_palace(birth_month)
    
    # Bước 2: Chuyển giờ thành địa chi
    hour_branch = convert_hour_to_branch(birth_hour)
    hour_branch_index = EARTHLY_BRANCHES.index(hour_branch)
    
    # Bước 3: Từ cung tháng sinh (coi như Tý), đếm thuận đến giờ sinh
    ty_index = 0
    steps_forward = (hour_branch_index - ty_index) % 12
    an_than_index = (month_palace_index + steps_forward) % 12
    an_than_branch = EARTHLY_BRANCHES[an_than_index]
    
    return an_than_branch, an_than_index

def calculate_twelve_palaces(an_mang_index: int) -> Dict[str, str]:
    """
    Tính 12 cung từ cung Mạng
    Viết theo chiều thuận: Mạng, Phụ, Phúc, Điền, Quan, Nô, Thiên, Tật, Tài, Tử, Phối, Bào
    
    Args:
        an_mang_index (int): Vị trí index của cung Mạng
        
    Returns:
        Dict[str, str]: Dictionary các cung và địa chi tương ứng
        
    Example:
        >>> calculate_twelve_palaces(7)  # Mùi index = 7
        {'Mạng': 'Mùi', 'Phụ': 'Thân', ...}
    """
    twelve_palaces = {}
    for i, palace_name in enumerate(TWELVE_PALACES):
        palace_index = (an_mang_index + i) % 12
        palace_branch = EARTHLY_BRANCHES[palace_index]
        twelve_palaces[palace_name] = palace_branch
    
    return twelve_palaces

def complete_astrology_calculation(birth_month: int, birth_hour: int, nam_am: Optional[int]=None) -> Dict:
    """
    Tính toán hoàn chỉnh lá số tử vi: An Mạng, An Thân và 12 cung
    Nếu truyền thêm nam_am: sẽ trả về thêm mảng 12 cung có can chi tháng âm
    
    Args:
        birth_month (int): Tháng sinh âm lịch (1-12)
        birth_hour (int): Giờ sinh (0-23)
        nam_am (int, optional): Năm sinh âm lịch để xác định can chi 12 cung
        
    Returns:
        Dict: Kết quả đầy đủ bao gồm An Mạng, An Thân, 12 cung và chi tiết tính toán
    """
    # Validate input
    if not 1 <= birth_month <= 12:
        raise ValueError("Tháng sinh phải từ 1 đến 12")
    if not 0 <= birth_hour <= 23:
        raise ValueError("Giờ sinh phải từ 0 đến 23")
    
    # Tính An Mạng
    an_mang_branch, an_mang_index = calculate_an_mang(birth_month, birth_hour)
    
    # Tính An Thân  
    an_than_branch, an_than_index = calculate_an_than(birth_month, birth_hour)
    
    # Tính 12 cung từ cung Mạng
    twelve_palaces = calculate_twelve_palaces(an_mang_index)
    
    # Thông tin chi tiết
    month_palace, month_palace_index = find_month_palace(birth_month)
    hour_branch = convert_hour_to_branch(birth_hour)

    # 12 cung ngoài với can chi tháng âm (nếu có năm âm)
    twelve_palaces_can_chi = []
    if nam_am is not None:
        twelve_palaces_can_chi = get_12_cung_can_chi(nam_am)

    result = {
        'birth_info': {
            'birth_month': birth_month,
            'birth_hour': birth_hour,
            'birth_month_name': MONTH_NAMES_VN[birth_month],
            'hour_branch': hour_branch,
            'nam_am': nam_am
        },
        'an_mang': an_mang_branch,
        'an_than': an_than_branch,
        'twelve_palaces': twelve_palaces,
        'twelve_palaces_can_chi': twelve_palaces_can_chi,
        'calculation_details': {
            'month_palace': month_palace,
            'month_palace_index': month_palace_index,
            'an_mang_index': an_mang_index,
            'an_than_index': an_than_index,
            'hour_branch': hour_branch
        }
    }
    
    return result

def format_birth_info(birth_month: int, birth_hour: int) -> str:
    """Định dạng thông tin sinh"""
    month_name = MONTH_NAMES_VN.get(birth_month, str(birth_month))
    hour_branch = convert_hour_to_branch(birth_hour)
    return f"Tháng {month_name} âm lịch ({birth_month}), Giờ {hour_branch} ({birth_hour:02d}:00)"

def print_calculation_steps(result: Dict) -> None:
    """In các bước tính toán chi tiết"""
    details = result['calculation_details']
    birth_info = result['birth_info']
    
    print("=== CÁCH TÍNH AN MẠNG VÀ AN THÂN ===")
    print(f"Sinh: {format_birth_info(birth_info['birth_month'], birth_info['birth_hour'])}")
    print()
    
    print("Bước 1: Từ cung Dần kể là tháng Giêng")
    print(f"- Đếm thuận đến tháng {birth_info['birth_month']}: Cung {details['month_palace']}")
    print()
    
    print("Bước 2A: An Mạng (đếm ngược)")
    print(f"- Cung {details['month_palace']} = Tý")
    print(f"- Giờ sinh: {details['hour_branch']}")
    print(f"- Đếm ngược từ Tý đến {details['hour_branch']}")
    print(f"- An Mạng: {result['an_mang']}")
    print()
    
    print("Bước 2B: An Thân (đếm thuận)")
    print(f"- Cung {details['month_palace']} = Tý") 
    print(f"- Giờ sinh: {details['hour_branch']}")
    print(f"- Đếm thuận từ Tý đến {details['hour_branch']}")
    print(f"- An Thân: {result['an_than']}")

def print_twelve_palaces(twelve_palaces: Dict[str, str]) -> None:
    """In 12 cung theo định dạng bảng"""
    print("\n=== MƯỜI HAI CUNG ===")
    for i, (palace_short, branch) in enumerate(twelve_palaces.items(), 1):
        palace_full = PALACE_FULL_NAMES[palace_short]
        print(f"{i:2d}. {palace_short} ({palace_full:<10}) : {branch}")

def print_twelve_palaces_can_chi(twelve_palaces_can_chi: List[Dict[str, str]]) -> None:
    """In 12 cung với can chi tháng âm lịch"""
    print("\n=== 12 CUNG VỚI CAN CHI THÁNG ÂM LỊCH ===")
    for i, pc in enumerate(twelve_palaces_can_chi, 1):
        print(f"{i:2d}. {pc['palace']} ({pc['palace_full']:<10}) : {pc['canchi']} (Tháng {pc['month_am']:>2d} âm)")

def export_to_json(result: Dict, filename: str = None) -> str:
    """Xuất kết quả ra file JSON"""
    if filename is None:
        birth_month = result['birth_info']['birth_month']
        birth_hour = result['birth_info']['birth_hour']
        filename = f"astrology_result_T{birth_month}_H{birth_hour}.json"
    
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    
    return filename

def validate_input(birth_month: int, birth_hour: int) -> bool:
    """Kiểm tra tính hợp lệ của input"""
    return (1 <= birth_month <= 12) and (0 <= birth_hour <= 23)

# Test với dữ liệu của Donniehieu
def test_donniehieu_data():
    """Test với dữ liệu của Donniehieu: tháng 11 âm lịch, 10 giờ sáng, năm 2008 âm lịch"""
    print("=== TEST VỚI DỮ LIỆU CỦA DONNIEHIEU ===")
    
    birth_month = 11
    birth_hour = 10
    nam_am = 2008  # ví dụ
    
    result = complete_astrology_calculation(birth_month, birth_hour, nam_am=nam_am)
    
    print_calculation_steps(result)
    print_twelve_palaces(result['twelve_palaces'])
    if result['twelve_palaces_can_chi']:
        print_twelve_palaces_can_chi(result['twelve_palaces_can_chi'])
    
    print(f"\n>>> KẾT QUẢ <<<")
    print(f"An Mạng: {result['an_mang']}")
    print(f"An Thân: {result['an_than']}")
    
    # Xuất file JSON
    json_file = export_to_json(result)
    print(f"\nĐã xuất kết quả ra file: {json_file}")
    
    return result

def main():
    """Hàm chính - chế độ tương tác"""
    print("=== CHƯƠNG TRÌNH TÍNH AN MẠNG, AN THÂN VÀ 12 CUNG ===")
    print(f"Created by: Donniehieu")
    print(f"Date: 2025-05-26 04:10:53 UTC")
    print()
    
    # Test với dữ liệu của Donniehieu
    test_donniehieu_data()
    
    # Chế độ tương tác
    print("\n" + "="*60)
    print("=== CHẾ ĐỘ TƯƠNG TÁC ===")
    
    while True:
        try:
            print("\nNhập thông tin sinh (âm lịch):")
            birth_month = int(input("Tháng sinh (1-12): "))
            birth_hour = int(input("Giờ sinh (0-23): "))
            nam_am = int(input("Năm sinh âm lịch (vd: 2008, hoặc Enter bỏ qua): ") or 0)
            if not validate_input(birth_month, birth_hour):
                print("Dữ liệu không hợp lệ! Vui lòng nhập lại.")
                continue
            
            # Tính toán
            if nam_am > 0:
                result = complete_astrology_calculation(birth_month, birth_hour, nam_am=nam_am)
            else:
                result = complete_astrology_calculation(birth_month, birth_hour)
            
            print("\n" + "="*50)
            print_calculation_steps(result)
            print_twelve_palaces(result['twelve_palaces'])
            if result['twelve_palaces_can_chi']:
                print_twelve_palaces_can_chi(result['twelve_palaces_can_chi'])
            
            print(f"\n>>> KẾT QUẢ <<<")
            print(f"An Mạng: {result['an_mang']}")
            print(f"An Thân: {result['an_than']}")
            
            # Hỏi có muốn xuất file không
            export_choice = input("\nXuất kết quả ra file JSON? (y/n): ").lower()
            if export_choice in ['y', 'yes', 'có']:
                json_file = export_to_json(result)
                print(f"Đã xuất ra file: {json_file}")
            
            # Tiếp tục?
            if input("\nTính tiếp? (y/n): ").lower() not in ['y', 'yes', 'có']:
                break
                
        except ValueError:
            print("Vui lòng nhập số hợp lệ!")
        except KeyboardInterrupt:
            print("\nTạm biệt!")
            break

if __name__ == "__main__":
    main()
