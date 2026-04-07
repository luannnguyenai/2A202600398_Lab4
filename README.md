# TravelBuddy — AI Agent Tư vấn Du lịch Thông minh 🌴

Dự án **TravelBuddy** là một AI Agent tiên tiến được xây dựng bằng **LangGraph** (LangChain Framework), giúp người dùng lập kế hoạch chuyến đi toàn diện thông qua trao đổi ngôn ngữ tự nhiên. 

### 🌟 Tính năng nổi bật
-   **Dữ liệu thật (Real-time Flights)**: Tra cứu chuyến bay trực thực tế từ Google Flights cho tất cả sân bay tại Việt Nam.
-   **Bộ nhớ phiên (Session Memory)**: Ghi nhớ thông tin từ các câu nói trước đó, tạo cảm giác trò chuyện liền mạch.
-   **Persona Chuyên gia**: Phong thái tư vấn điềm tĩnh, ấm áp và luôn chủ động đưa ra các lời khuyên chuyên sâu.
-   **Bảo mật nâng cao**: Lớp phòng thủ đa tầng chống các cuộc tấn công Prompt Injection và Jailbreak.

---

### 📂 Cấu trúc Repository (Lab 4 Standard)
-   `agent.py`: Chứa logic điều khiển chính (LangGraph: Nodes, Edges, State).
-   `tools.py`: Các công cụ tra cứu chuyến bay, khách sạn và quản lý ngân sách.
-   `system_prompt.txt`: "Não bộ" quy định persona và các quy tắc hành xử của Agent.
-   `test_results.md`: Báo cáo kết quả kiểm thử cho 5 kịch bản bắt buộc.
-   `test_results_security.md`: Báo cáo các kiểm thử bảo mật nâng cao.
-   `requirements.txt`: Danh sách các thư viện cần thiết.

---

### ⚙️ Hướng dẫn cài đặt
1.  **Cài đặt thư viện**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Cấu hình API Key**: Tạo file `.env` và thêm khóa OpenAI của bạn:
    ```env
    OPENAI_API_KEY=sk-xxxx...
    ```
3.  **Chạy Agent**:
    ```bash
    python3 agent.py
    ```

---

### 🧪 Hệ thống Kiểm thử Tự động
Dự án đi kèm với hai bộ test tự động để đảm bảo tính ổn định:
-   **Test Lab 4**: `python3 test_runner.py` (Xác minh 5 kịch bản yêu cầu của Lab).
-   **Test Bảo mật**: `python3 security_test_runner.py` (Xác minh 9 kịch bản Edge Case & Security).

---

© 2026 TravelBuddy Project - Lab 4: Building Your First AI Agent with LangGraph.
