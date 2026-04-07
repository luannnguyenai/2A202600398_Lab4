from langchain_core.tools import tool
from datetime import datetime, timedelta
from fast_flights import FlightData, get_flights, Passengers

# ============================================================
# AIRPORT MAPPING — Ánh xạ tên thành phố sang mã IATA
# Hỗ trợ toàn bộ các sân bay dân dụng tại Việt Nam
# ============================================================
AIRPORT_MAP = {
    "hà nội": "HAN", "nội bài": "HAN",
    "hồ chí minh": "SGN", "sài gòn": "SGN", "tân sơn nhất": "SGN",
    "đà nẵng": "DAD",
    "nha trang": "CXR", "cam ranh": "CXR",
    "phú quốc": "PQC",
    "hải phòng": "HPH", "cát bi": "HPH",
    "huế": "HUI", "phú bài": "HUI",
    "cần thơ": "VCA",
    "vinh": "VII",
    "vân đồn": "VDO", "quảng ninh": "VDO",
    "đà lạt": "DLI", "liên khương": "DLI",
    "buôn ma thuột": "BMV",
    "cà mau": "CAH",
    "côn đảo": "VCS",
    "chu lai": "VCL", "tam kỳ": "VCL",
    "điện biên phủ": "DIN",
    "đồng hới": "VDH",
    "pleiku": "PXU",
    "quy nhơn": "UIH", "phù cát": "UIH",
    "rạch giá": "VKG",
    "thanh hóa": "THD", "thọ xuân": "THD",
    "tuy hòa": "TBB"
}

HOTELS_DB = {
    "Đà Nẵng": [
        {"name": "Mường Thanh Luxury",   "stars": 5, "price_per_night": 1_800_000, "area": "Mỹ Khê",    "rating": 4.5},
        {"name": "Sala Danang Beach",    "stars": 4, "price_per_night": 1_200_000, "area": "Mỹ Khê",    "rating": 4.3},
        {"name": "Fivitel Danang",       "stars": 3, "price_per_night": 650_000,   "area": "Sơn Trà",   "rating": 4.1},
        {"name": "Memory Hostel",        "stars": 2, "price_per_night": 250_000,   "area": "Hải Châu",  "rating": 4.6},
        {"name": "Christina's Homestay", "stars": 2, "price_per_night": 350_000,   "area": "An Thượng", "rating": 4.7},
    ],
    "Phú Quốc": [
        {"name": "Vinpearl Resort",      "stars": 5, "price_per_night": 3_500_000, "area": "Bãi Dài",    "rating": 4.4},
        {"name": "Sol by Meliá",         "stars": 4, "price_per_night": 1_500_000, "area": "Bãi Trường", "rating": 4.2},
        {"name": "Lahana Resort",        "stars": 3, "price_per_night": 800_000,   "area": "Dương Đông", "rating": 4.0},
        {"name": "9Station Hostel",      "stars": 2, "price_per_night": 200_000,   "area": "Dương Đông", "rating": 4.5},
    ],
    "Hồ Chí Minh": [
        {"name": "Rex Hotel",            "stars": 5, "price_per_night": 2_800_000, "area": "Quận 1", "rating": 4.3},
        {"name": "Liberty Central",      "stars": 4, "price_per_night": 1_400_000, "area": "Quận 1", "rating": 4.1},
        {"name": "Cochin Zen Hotel",     "stars": 3, "price_per_night": 550_000,   "area": "Quận 3", "rating": 4.4},
        {"name": "The Common Room",      "stars": 2, "price_per_night": 180_000,   "area": "Quận 1", "rating": 4.6},
    ],
}


@tool
def search_flights(origin: str, destination: str, date: str = None) -> str:
    """
    Tìm kiếm các chuyến bay thực tế giữa hai thành phố bằng fast_flights.
    Tham số:
    - origin: tên thành phố/sân bay khởi hành (VD: 'Hà Nội', 'Nội Bài', 'Sài Gòn')
    - destination: tên thành phố/sân bay đến (VD: 'Cam Ranh', 'Đà Lạt', 'Phú Quốc')
    - date: ngày bay định dạng 'YYYY-MM-DD'. Nếu không có, mặc định là 7 ngày sau.
    """
    try:
        # Lấy mã IATA từ bảng ánh xạ
        from_code = AIRPORT_MAP.get(origin.lower().strip())
        to_code = AIRPORT_MAP.get(destination.lower().strip())

        if not from_code or not to_code:
            return f"⚠️ Xin lỗi, hệ thống hiện chưa hỗ trợ tuyến bay từ '{origin}' đến '{destination}'."

        # Xử lý ngày tháng (Hỗ trợ cả YYYY-MM-DD và dd-mm-yyyy)
        if not date:
            target_date = datetime.now() + timedelta(days=7)
            date = target_date.strftime("%Y-%m-%d")
        else:
            # Nếu người dùng nhập dd-mm-yyyy, quy đổi về YYYY-MM-DD
            if "-" in date:
                parts = date.split("-")
                if len(parts[0]) == 2: # Trường hợp dd-mm-yyyy
                    try:
                        temp_date = datetime.strptime(date, "%d-%m-%Y")
                        date = temp_date.strftime("%Y-%m-%d")
                    except ValueError:
                        pass # Để try-except phía sau xử lý lỗi định dạng chung

        # Kiểm tra ngày tháng và logic ngày quá khứ (Hôm nay: 2026-04-07)
        try:
            req_date = datetime.strptime(date, "%Y-%m-%d")
            if req_date.date() < datetime.now().date():
                return "❌ Ngày bạn chọn đã qua, vui lòng chọn ngày khác."
        except ValueError:
            return "Hệ thống bị lỗi, vui lòng bảo trì hệ thống"

        # Gọi fast_flights API
        passengers = Passengers(adults=1, children=0, infants_in_seat=0, infants_on_lap=0)
        fd = FlightData(date=date, from_airport=from_code, to_airport=to_code)

        result = get_flights(flight_data=[fd], trip='one-way', passengers=passengers, seat='economy')

        if not result or not result.flights:
            return "Hệ thống bị lỗi, vui lòng bảo trì hệ thống"

        # Format danh sách chuyến bay thực tế - Rút gọn tối đa để tránh lỗi 400
        lines = [f"✈️ Kết quả bay {origin} → {destination} ({date}):\n"]
        
        # Chỉ lấy 2-3 chuyến quan trọng nhất
        for i, f in enumerate(result.flights[:3], 1):
            price_val = f.price if hasattr(f, 'price') else "N/A"
            airline = f.name if hasattr(f, 'name') else "N/A"
            dep = f.departure if hasattr(f, 'departure') else "N/A"
            arr = f.arrival if hasattr(f, 'arrival') else "N/A"
            time = f"{dep}→{arr}"
            
            # price_val đã có sẵn định dạng (VD: ₫1.450.000), không cần format thêm
            lines.append(f"  {i}. {airline} | {time} | 💰 {price_val}")

        return "\n".join(lines)

    except Exception as e:
        print(f"DEBUG: Lỗi API: {str(e)}")
        return "Hệ thống bị lỗi, vui lòng bảo trì hệ thống"


@tool
def search_hotels(city: str, max_price_per_night: int = 99_999_999) -> str:
    """
    Tìm kiếm khách sạn tại một thành phố, có thể lọc theo giá tối đa mỗi đêm.
    Tham số:
    - city: tên thành phố (VD: 'Đà Nẵng', 'Phú Quốc', 'Hồ Chí Minh')
    - max_price_per_night: giá tối đa mỗi đêm (VNĐ), mặc định không giới hạn
    Trả về danh sách khách sạn phù hợp với tên, số sao, giá, khu vực, rating.
    """
    try:
        hotels = HOTELS_DB.get(city)

        if hotels is None:
            return f"❌ Không tìm thấy thông tin khách sạn tại {city}. Hệ thống hiện hỗ trợ: {', '.join(HOTELS_DB.keys())}."

        # Lọc theo giá tối đa
        filtered = [h for h in hotels if h["price_per_night"] <= max_price_per_night]

        if not filtered:
            budget_fmt = f"{max_price_per_night:,.0f}".replace(",", ".")
            return (
                f"❌ Không tìm thấy khách sạn tại {city} với giá dưới {budget_fmt}đ/đêm.\n"
                f"Hãy thử tăng ngân sách hoặc chọn địa điểm khác."
            )

        # Sắp xếp theo rating giảm dần
        filtered_sorted = sorted(filtered, key=lambda x: x["rating"], reverse=True)

        max_price_fmt = f"{max_price_per_night:,.0f}".replace(",", ".")
        lines = [f"🏨 Khách sạn tại {city} (giá ≤ {max_price_fmt}đ/đêm) — {len(filtered_sorted)} kết quả:\n"]

        for i, h in enumerate(filtered_sorted, 1):
            price_fmt = f"{h['price_per_night']:,.0f}".replace(",", ".")
            stars = "⭐" * h["stars"]
            lines.append(
                f"  {i}. {h['name']} {stars}\n"
                f"     📍 {h['area']} | 💰 {price_fmt}đ/đêm | ⭐ Rating: {h['rating']}/5"
            )

        return "\n".join(lines)

    except Exception as e:
        return f"❌ Lỗi khi tìm kiếm khách sạn: {str(e)}"


@tool
def calculate_budget(total_budget: int, expenses: str) -> str:
    """
    Tính toán ngân sách còn lại sau khi trừ các khoản chi phí.
    Tham số:
    - total_budget: tổng ngân sách ban đầu (VNĐ, tối đa 10 tỷ)
    - expenses: định dạng 'tên_khoản:số_tiền' (VD: 'vé_máy_bay:890000,khách_sạn:650000')
    """
    try:
        # Giới hạn số tiền tối đa (10 tỷ)
        if total_budget > 10_000_000_000 or total_budget < 0:
            return "❌ Ngân sách không hợp lệ (Phải từ 0 đến 10 tỷ VNĐ)."

        expense_dict = {}
        if not expenses or not expenses.strip():
            return "❌ Vui lòng cung cấp danh sách chi phí."

        items = expenses.strip().split(",")
        for item in items:
            if ":" not in item:
                return "Hệ thống bị lỗi, vui lòng bảo trì hệ thống"
            
            parts = item.split(":", 1)
            name = parts[0].strip().replace("_", " ").capitalize()
            try:
                # Chặn SQL Injection/Overflow thô sơ bằng cách check độ dài và kiểu dữ liệu
                if len(name) > 50: return "❌ Tên khoản chi quá dài."
                amount = int(float(parts[1].strip()))
                if amount < 0 or amount > 10_000_000_000:
                    return "❌ Số tiền chi phí không hợp lệ."
                expense_dict[name] = amount
            except (ValueError, TypeError):
                return "Hệ thống bị lỗi, vui lòng bảo trì hệ thống"

        total_expense = sum(expense_dict.values())
        budget_fmt = f"{total_budget:,.0f}".replace(",", ".")
        total_expense_fmt = f"{total_expense:,.0f}".replace(",", ".")

        lines = ["💰 Bảng chi phí:\n"]
        for name, amount in expense_dict.items():
            lines.append(f"   - {name}: {f'{amount:,.0f}'.replace(',', '.')}đ")
        lines.append("   " + "─" * 30)
        lines.append(f"   Tổng chi:  {total_expense_fmt}đ\n   Ngân sách: {budget_fmt}đ")

        remaining = total_budget - total_expense
        remaining_fmt = f"{abs(remaining):,.0f}".replace(",", ".")
        if remaining >= 0:
            lines.append(f"   Còn lại:   {remaining_fmt}đ ✅")
        else:
            lines.append(f"   Thiếu:     {remaining_fmt}đ ⚠️")
        
        return "\n".join(lines)

    except Exception:
        return "Hệ thống bị lỗi, vui lòng bảo trì hệ thống"
