"""
test_runner.py — Tự động chạy 5 test cases và ghi kết quả ra test_results.md
Chạy: python3 test_runner.py
Yêu cầu: OPENAI_API_KEY hợp lệ trong file .env
"""

import sys
import os
import io
from contextlib import redirect_stdout
from datetime import datetime

from dotenv import load_dotenv
load_dotenv()

# Kiểm tra API key
api_key = os.getenv("OPENAI_API_KEY", "")
if not api_key or api_key.startswith("sk-proj-xxx"):
    print("❌ Lỗi: Chưa có OPENAI_API_KEY hợp lệ trong file .env")
    print("   Mở file .env và thay 'sk-proj-xxx...' bằng API key thật của bạn.")
    sys.exit(1)

# Import agent graph (sau khi đã load .env)
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from tools import search_flights, search_hotels, calculate_budget

# Build graph
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

class AgentState(TypedDict):
    messages: Annotated[list, add_messages]

tools_list = [search_flights, search_hotels, calculate_budget]
llm = ChatOpenAI(model="gpt-4o-mini")
llm_with_tools = llm.bind_tools(tools_list)

def agent_node(state: AgentState):
    messages = state["messages"]
    if not isinstance(messages[0], SystemMessage):
        messages = [SystemMessage(content=SYSTEM_PROMPT)] + messages
    response = llm_with_tools.invoke(messages)
    if response.tool_calls:
        for tc in response.tool_calls:
            print(f"  🔧 Gọi tool: {tc['name']}({tc['args']})")
    else:
        print(f"  💬 Trả lời trực tiếp (không gọi tool)")
    return {"messages": [response]}

builder = StateGraph(AgentState)
builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(tools_list))
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")
graph = builder.compile()


def run_test(user_input: str) -> tuple[str, str]:
    """Chạy 1 test case, trả về (console_log, final_answer)."""
    log_buffer = io.StringIO()
    with redirect_stdout(log_buffer):
        result = graph.invoke({"messages": [("human", user_input)]})
    console_log = log_buffer.getvalue()
    final_answer = result["messages"][-1].content
    return console_log, final_answer


# ============================================================
# Định nghĩa 5 Test Cases
# ============================================================
TEST_CASES = [
    {
        "id": 1,
        "name": "Direct Answer — Không cần tool",
        "input": "Xin chào! Tôi đang muốn đi du lịch nhưng chưa biết đi đâu.",
        "expected": "Agent chào hỏi, hỏi thêm về sở thích/ngân sách/thời gian. Không gọi tool nào.",
    },
    {
        "id": 2,
        "name": "Single Tool Call — Tìm vé máy bay",
        "input": "Tìm giúp tôi chuyến bay từ Hà Nội đi Đà Nẵng",
        "expected": "Gọi search_flights('Hà Nội', 'Đà Nẵng'), liệt kê 4 chuyến bay.",
    },
    {
        "id": 3,
        "name": "Multi-Step Tool Chaining — Lập kế hoạch hoàn chỉnh",
        "input": "Tôi ở Hà Nội, muốn đi Phú Quốc 2 đêm, budget 5 triệu. Tư vấn giúp!",
        "expected": "Agent chuỗi: search_flights → search_hotels → calculate_budget, tổng hợp kế hoạch.",
    },
    {
        "id": 4,
        "name": "Missing Info — Hỏi lại thông tin còn thiếu",
        "input": "Tôi muốn đặt khách sạn",
        "expected": "Agent hỏi lại: thành phố nào? ngân sách bao nhiêu? Không gọi tool vội.",
    },
    {
        "id": 5,
        "name": "Guardrail — Từ chối yêu cầu ngoài phạm vi",
        "input": "Giải giúp tôi bài tập lập trình Python về linked list",
        "expected": "Từ chối lịch sự, chỉ hỗ trợ về du lịch.",
    },
]


def main():
    print("=" * 70)
    print("  TravelBuddy Test Runner — Chạy 5 test cases tự động")
    print("=" * 70)

    results = []

    for tc in TEST_CASES:
        print(f"\n{'─'*70}")
        print(f"📋 Test {tc['id']}: {tc['name']}")
        print(f"👤 Input: {tc['input']}")
        print(f"🎯 Expected: {tc['expected']}")
        print("⏳ Đang chạy...")

        try:
            console_log, answer = run_test(tc["input"])
            print(f"✅ Done!")
            print(f"🤖 Answer: {answer[:200]}...")
        except Exception as e:
            console_log = ""
            answer = f"ERROR: {str(e)}"
            print(f"❌ Lỗi: {e}")

        results.append({**tc, "console_log": console_log, "answer": answer})

    # ============================================================
    # Ghi file test_results.md
    # ============================================================
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    lines = [
        f"# Test Results — TravelBuddy Agent",
        f"",
        f"**Ngày chạy:** {now}  ",
        f"**Model:** gpt-4o-mini  ",
        f"**Framework:** LangGraph  ",
        f"",
        f"---",
        f"",
    ]

    for r in results:
        lines += [
            f"## Test {r['id']}: {r['name']}",
            f"",
            f"**Input (User):**",
            f"> {r['input']}",
            f"",
            f"**Expected:**",
            f"> {r['expected']}",
            f"",
            f"**Console Log (Tool calls):**",
            f"```",
            r["console_log"].strip() if r["console_log"].strip() else "(Không gọi tool nào)",
            f"```",
            f"",
            f"**TravelBuddy Response:**",
            f"```",
            r["answer"],
            f"```",
            f"",
            f"---",
            f"",
        ]

    md_content = "\n".join(lines)
    output_path = "test_results.md"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    print(f"\n{'='*70}")
    print(f"✅ Đã ghi kết quả vào: {output_path}")
    print(f"{'='*70}")


if __name__ == "__main__":
    main()
