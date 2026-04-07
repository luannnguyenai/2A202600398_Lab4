from langchain_core.tools import tool

# ============================================================
# MOCK DATA — Dữ liệu giả lập hệ thống du lịch
# Lưu ý: Giá cả có logic (VD: cuối tuần đắt hơn, hạng cao hơn đắt hơn)
# Sinh viên cần đọc hiểu data để debug test cases.
# ============================================================

FLIGHTS_DB = {
    ("Hà Nội", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "07:20", "price": 1_450_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "14:00", "arrival": "15:20", "price": 2_800_000, "class": "business"},
        {"airline": "VietJet Air",      "departure": "08:30", "arrival": "09:50", "price": 890_000,   "class": "economy"},
        {"airline": "Bamboo Airways",   "departure": "11:00", "arrival": "12:20", "price": 1_200_000, "class": "economy"},
    ],
    ("Hà Nội", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "07:00", "arrival": "09:15", "price": 2_100_000, "class": "economy"},
        {"airline": "VietJet Air",      "departure": "10:00", "arrival": "12:15", "price": 1_350_000, "class": "economy"},
        {"airline": "VietJet Air",      "departure": "16:00", "arrival": "18:15", "price": 1_100_000, "class": "economy"},
    ],
    ("Hà Nội", "Hồ Chí Minh"): [
        {"airline": "Vietnam Airlines", "departure": "06:00", "arrival": "08:10", "price": 1_600_000, "class": "economy"},
        {"airline": "VietJet Air",      "departure": "07:30", "arrival": "09:40", "price": 950_000,   "class": "economy"},
        {"airline": "Bamboo Airways",   "departure": "12:00", "arrival": "14:10", "price": 1_300_000, "class": "economy"},
        {"airline": "Vietnam Airlines", "departure": "18:00", "arrival": "20:10", "price": 3_200_000, "class": "business"},
    ],
    ("Hồ Chí Minh", "Đà Nẵng"): [
        {"airline": "Vietnam Airlines", "departure": "09:00", "arrival": "10:20", "price": 1_300_000, "class": "economy"},
        {"airline": "VietJet Air",      "departure": "13:00", "arrival": "14:20", "price": 780_000,   "class": "economy"},
    ],
    ("Hồ Chí Minh", "Phú Quốc"): [
        {"airline": "Vietnam Airlines", "departure": "08:00", "arrival": "09:00", "price": 1_100_000, "class": "economy"},
        {"airline": "VietJet Air",      "departure": "15:00", "arrival": "16:00", "price": 650_000,   "class": "economy"},
    ],
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
def search_flights(origin: str, destination: str) -> str:
    """
    Tìm kiếm các chuyến bay giữa hai thành phố.
    Tham số:
    - origin: thành phố khởi hành (VD: 'Hà Nội', 'Hồ Chí Minh')
    - destination: thành phố đến (VD: 'Đà Nẵng', 'Phú Quốc')
    Trả về danh sách chuyến bay với hãng, giờ bay, giá vé.
    Nếu không tìm thấy tuyến bay, trả về thông báo không có chuyến.
    """
    try:
        # Tra cứu chiều đi
        flights = FLIGHTS_DB.get((origin, destination))

        # Nếu không tìm thấy, thử tra ngược chiều
        if flights is None:
            flights = FLIGHTS_DB.get((destination, origin))
            if flights is not None:
                # Thông báo chỉ tìm thấy chiều ngược
                return (
                    f"⚠️ Không tìm thấy chuyến bay từ {origin} đến {destination}.\n"
                    f"Tuy nhiên có chuyến từ {destination} đến {origin} — "
                    f"bạn có muốn xem không?\n"
                    f"(Gọi lại với origin='{destination}', destination='{origin}')"
                )
            else:
                return f"❌ Không tìm thấy chuyến bay từ {origin} đến {destination}. Tuyến này hiện chưa có trong hệ thống."

        # Format danh sách chuyến bay
        lines = [f"✈️ Chuyến bay từ {origin} → {destination} ({len(flights)} chuyến):\n"]
        for i, f in enumerate(flights, 1):
            price_fmt = f"{f['price']:,.0f}".replace(",", ".")
            lines.append(
                f"  {i}. {f['airline']} | {f['departure']} → {f['arrival']} "
                f"| {f['class'].capitalize()} | 💰 {price_fmt}đ"
            )

        # Tìm vé rẻ nhất
        cheapest = min(flights, key=lambda x: x["price"])
        cheapest_price = f"{cheapest['price']:,.0f}".replace(",", ".")
        lines.append(f"\n💡 Vé rẻ nhất: {cheapest['airline']} lúc {cheapest['departure']} — {cheapest_price}đ")

        return "\n".join(lines)

    except Exception as e:
        return f"❌ Lỗi khi tìm kiếm chuyến bay: {str(e)}"


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
    - total_budget: tổng ngân sách ban đầu (VNĐ)
    - expenses: chuỗi mô tả các khoản chi, mỗi khoản cách nhau bởi dấu phẩy,
      định dạng 'tên_khoản:số_tiền' (VD: 'vé_máy_bay:890000,khách_sạn:650000')
    Trả về bảng chi tiết các khoản chi và số tiền còn lại.
    Nếu vượt ngân sách, cảnh báo rõ ràng số tiền thiếu.
    """
    try:
        # Parse chuỗi expenses thành dict {tên: số_tiền}
        expense_dict = {}
        if expenses.strip():
            items = expenses.strip().split(",")
            for item in items:
                item = item.strip()
                if ":" not in item:
                    return (
                        f"❌ Lỗi format: '{item}' không đúng định dạng 'tên_khoản:số_tiền'.\n"
                        f"Ví dụ đúng: 'vé_máy_bay:890000,khách_sạn:650000'"
                    )
                parts = item.split(":", 1)
                name = parts[0].strip().replace("_", " ").capitalize()
                try:
                    amount = int(float(parts[1].strip()))
                    if amount < 0:
                        return f"❌ Số tiền không được âm: '{parts[0]}' = {parts[1]}"
                    expense_dict[name] = amount
                except ValueError:
                    return (
                        f"❌ Lỗi format: '{parts[1]}' không phải số hợp lệ cho khoản '{parts[0]}'.\n"
                        f"Vui lòng nhập số nguyên (VD: 890000)."
                    )

        # Tính tổng chi phí
        total_expense = sum(expense_dict.values())

        # Format ngân sách
        budget_fmt = f"{total_budget:,.0f}".replace(",", ".")
        total_expense_fmt = f"{total_expense:,.0f}".replace(",", ".")

        # Tạo bảng chi tiết
        lines = ["💰 Bảng chi phí:\n"]
        for name, amount in expense_dict.items():
            amount_fmt = f"{amount:,.0f}".replace(",", ".")
            lines.append(f"   - {name}: {amount_fmt}đ")

        lines.append("   " + "─" * 30)
        lines.append(f"   Tổng chi:  {total_expense_fmt}đ")
        lines.append(f"   Ngân sách: {budget_fmt}đ")

        remaining = total_budget - total_expense
        if remaining >= 0:
            remaining_fmt = f"{remaining:,.0f}".replace(",", ".")
            lines.append(f"   Còn lại:   {remaining_fmt}đ ✅")
            if remaining > 0:
                lines.append(f"\n🎉 Bạn vẫn còn {remaining_fmt}đ để chi cho ăn uống, tham quan và mua sắm!")
        else:
            over_fmt = f"{abs(remaining):,.0f}".replace(",", ".")
            lines.append(f"   Còn lại:   -{over_fmt}đ ⚠️")
            lines.append(f"\n⚠️ Vượt ngân sách {over_fmt}đ! Cần điều chỉnh lại kế hoạch.")

        return "\n".join(lines)

    except Exception as e:
        return f"❌ Lỗi khi tính ngân sách: {str(e)}"
