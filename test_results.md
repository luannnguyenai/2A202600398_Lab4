# Test Results — TravelBuddy Agent

**Ngày chạy:** 2026-04-07 14:18:07  
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
Chào bạn! 😊 Có rất nhiều điểm du lịch thú vị ở Việt Nam. Bạn muốn trải nghiệm vẻ đẹp thiên nhiên, khám phá di sản văn hóa hay tìm một chốn nghỉ ngơi thư giãn? Mình có thể gợi ý cho bạn một số địa điểm như Đà Nẵng, Hội An, Phú Quốc hay Nha Trang. Bạn thích đi đâu hơn?
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
Đây là một số chuyến bay từ Hà Nội đi Đà Nẵng cho bạn:

✈️ **Chuyến bay**:
1. **Vietnam Airlines** | **06:00 → 07:20** | Economy | 💰 **1.450.000đ**
2. **Vietnam Airlines** | **14:00 → 15:20** | Business | 💰 **2.800.000đ**
3. **VietJet Air** | **08:30 → 09:50** | Economy | 💰 **890.000đ**  (Vé rẻ nhất)
4. **Bamboo Airways** | **11:00 → 12:20** | Economy | 💰 **1.200.000đ**

Nếu bạn cần hỗ trợ tìm khách sạn hoặc thông tin gì thêm, đừng ngần ngại hỏi nhé! 😊
```

---

## Test 3: Multi-Step Tool Chaining — Lập kế hoạch hoàn chỉnh

**Input (User):**
> Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!

**Expected:**
> Agent chuỗi: search_flights → search_hotels → calculate_budget, tổng hợp kế hoạch.

**Console Log (Tool calls):**
```
🔧 Gọi tool: search_flights({'origin': 'Hà Nội', 'destination': 'Phú Quốc'})
  🔧 Gọi tool: search_hotels({'city': 'Phú Quốc', 'max_price_per_night': 2500000})
  🔧 Gọi tool: calculate_budget({'total_budget': 5000000, 'expenses': 'vé_máy_bay:1100000,khách_sạn:1600000'})
  💬 Trả lời trực tiếp (không gọi tool)
```

**TravelBuddy Response:**
```
Dưới đây là kế hoạch chi tiết cho chuyến đi của bạn từ Hà Nội đến Phú Quốc trong 2 đêm:

✈️ **Chuyến bay**:
- **Vietnam Airlines** | 07:00 → 09:15 | Economy | 💰 **2.100.000đ**
- **VietJet Air** | 10:00 → 12:15 | Economy | 💰 **1.350.000đ**
- **VietJet Air** | 16:00 → 18:15 | Economy | 💰 **1.100.000đ** (Vé rẻ nhất)

🏨 **Khách sạn**:
1. **9Station Hostel** ⭐⭐
   - 📍 Dương Đông | 💰 **200.000đ/đêm** | ⭐ Rating: 4.5/5
2. **Sol by Meliá** ⭐⭐⭐⭐
   - 📍 Bãi Trường | 💰 **1.500.000đ/đêm** | ⭐ Rating: 4.2/5
3. **Lahana Resort** ⭐⭐⭐
   - 📍 Dương Đông | 💰 **800.000đ/đêm** | ⭐ Rating: 4.0/5

💰 **Tổng chi phí ước tính**:
- Vé máy bay: 1.100.000đ
- Khách sạn (2 đêm tại 9Station Hostel): 2.600.000đ (200.000đ * 2 đêm)
- ──────────────────────────────
- **Tổng chi**: 2.700.000đ
- **Ngân sách**: 5.000.000đ
- **Còn lại**: 2.300.000đ ✅

🎉 Bạn vẫn còn 2.300.000đ để chi cho ăn uống, tham quan và mua sắm!

💡 **Gợi ý thêm**: 
- Đừng quên thưởng thức hải sản tươi ngon tại Phú Quốc nhé!
- Thử tham quan Vinpearl Land hoặc đi khám phá các bãi biển đẹp như Bãi Sao hay Bãi Dài.

Nếu bạn cần thêm thông tin gì khác hoặc giúp đỡ trong việc đặt vé và khách sạn, cứ cho mình biết nhé! 😊
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
Bạn có thể cho mình biết bạn muốn đặt khách sạn ở đâu và ngân sách mỗi đêm của bạn là bao nhiêu không? 😊
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
Mình chỉ có thể hỗ trợ về du lịch thôi bạn nhé! Bạn có kế hoạch đi đâu không? 😊
```

---
