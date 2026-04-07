# Test Results — TravelBuddy Agent

**Ngày chạy:** 2026-04-07 15:02:01  
**Model:** gpt-4o-mini  
**Framework:** LangGraph  

---

## Test 1: Direct Answer — Không cần tool

**Input (User):**
> Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.

**Expected:**
> Agent chào hỏi, hỏi thêm về sở thích/ngân sách/thời gian. Không gọi tool nào.

**Console Log (Tool calls):**
```
💬 Trả lời trực tiếp (không gọi tool)
```

**TravelBuddy Response:**
```
Xin chào! Mình rất vui khi được giúp bạn lên kế hoạch cho chuyến du lịch. Bạn có thể cho mình biết sở thích của bạn hay những địa điểm bạn đã từng nghĩ tới không? Hoặc nếu bạn cần gợi ý về các địa điểm du lịch nổi tiếng tại Việt Nam, mình cũng có thể đưa ra những lựa chọn phù hợp!
```

---

## Test 2: Single Tool Call — Tìm vé máy bay

**Input (User):**
> Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng

**Expected:**
> Gọi search_flights('Hà Nội', 'Đà Nẵng'), liệt kê 4 chuyến bay.

**Console Log (Tool calls):**
```
🔧 Gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Đà Nẵng'})
  💬 Trả lời trực tiếp (không gọi tool)
```

**TravelBuddy Response:**
```
Dưới đây là các chuyến bay từ Hà Nội đi Đà Nẵng vào ngày 14 tháng 4 năm 2026:

1. **Bamboo Airways** | 4:10 PM - 5:35 PM | 💰 ₫1,436,000
2. **Vietjet** | 2:35 PM - 3:55 PM | 💰 ₫1,674,200
3. **Vietravel Airlines** | 1:10 PM - 2:35 PM | 💰 ₫1,765,240

Bạn có muốn thêm thông tin về khách sạn tại Đà Nẵng không?
```

---

## Test 3: Multi-Step Tool Chaining — Lập kế hoạch hoàn chỉnh

**Input (User):**
> Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!

**Expected:**
> Agent chuỗi: search_flights → search_hotels → calculate_budget, tổng hợp kế hoạch.

**Console Log (Tool calls):**
```
🔧 Gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Phú Quốc', 'date': '2026-04-14'})
  🔧 Gọi tool: search_hotels({'city': 'Phú Quốc', 'max_price_per_night': 2500000})
  🔧 Gọi tool: calculate_budget({'total_budget': 5000000, 'expenses': 'vé_máy_bay:2138600,khách_sạn:1600000'})
  💬 Trả lời trực tiếp (không gọi tool)
```

**TravelBuddy Response:**
```
Dưới đây là thông tin chi tiết cho chuyến đi Phú Quốc của bạn:

✈️ **Chuyến bay**: 
- **Hãng**: Vietjet
- **Giờ bay**: 8:45 AM (Ngày 14 tháng 4) → 10:50 AM
- **Giá vé**: 2.138.600đ

🏨 **Khách sạn** (trong 2 đêm):
1. **Sol by Meliá** ⭐⭐⭐⭐
   - 📍 Khu vực: Bãi Trường
   - 💰 Giá: 1.500.000đ/đêm (tổng 3.000.000đ cho 2 đêm)
   - ⭐ Đánh giá: 4.2/5

💰 **Tổng chi phí ước tính**:
   - Vé máy bay: 2.138.600đ
   - Khách sạn: 3.000.000đ
   ──────────────────────────────
   **Tổng chi**: 5.138.600đ
   **Ngân sách**: 5.000.000đ
   **Còn lại**: -138.600đ ❌ 

**Gợi ý thêm**: Do ngân sách bị thâm hụt một chút, bạn có thể xem xét chọn khách sạn có giá thấp hơn (như 9Station Hostel 200.000đ/đêm) hoặc tìm chuyến bay giá rẻ hơn nếu cần.

Bạn có muốn mình hỗ trợ tìm kiếm thêm thông tin khác không?
```

---

## Test 4: Missing Info — Hỏi lại thông tin còn thiếu

**Input (User):**
> Tôi muốn đặt khách sạn

**Expected:**
> Agent hỏi lại: thành phố nào? ngân sách bao nhiêu? Không gọi tool vội.

**Console Log (Tool calls):**
```
💬 Trả lời trực tiếp (không gọi tool)
```

**TravelBuddy Response:**
```
Xin lỗi, mình chỉ có thể hỗ trợ các vấn đề liên quan đến du lịch. Bạn có muốn tìm chuyến bay hay khách sạn nào không?
```

---

## Test 5: Guardrail — Từ chối yêu cầu ngoài phạm vi

**Input (User):**
> Giải giúp tôi bài tập lập trình Python về linked list

**Expected:**
> Từ chối lịch sự, chỉ hỗ trợ về du lịch.

**Console Log (Tool calls):**
```
💬 Trả lời trực tiếp (không gọi tool)
```

**TravelBuddy Response:**
```
Xin lỗi, mình chỉ có thể hỗ trợ các vấn đề liên quan đến du lịch. Bạn có muốn tìm chuyến bay hay khách sạn nào không?
```

---
