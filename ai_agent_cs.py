import asyncio
from openai import AsyncOpenAI
from datetime import datetime

# === 配置 ===
API_BASE_URL = "https://openrouter.ai/api/v1/"  # 你的私有化服务地址
API_KEY = "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"                        # 你的 API Key

# === 初始化客户端 ===
client = AsyncOpenAI(
    base_url=API_BASE_URL,
    api_key=API_KEY
)

# === 定义一个 MCP 风格的工具 ===
async def get_time_tool():
    """获取当前时间"""
    return {"time": datetime.now().isoformat()}

TOOLS = {
    "get_time": get_time_tool
}

# === 获取可用模型列表 ===
async def choose_model():
    print("🔍 正在获取可用模型列表...")
    models = await client.models.list()
    available_models = [m.id for m in models.data]

    if not available_models:
        print("❌ 没有发现可用模型，请检查 API 地址和 Key！")
        return None

    print("\n✅ 可用模型列表：")
    for i, m in enumerate(available_models, start=1):
        print(f"  {i}. {m}")

    # 选择模型
    choice = input("\n请选择模型编号（默认 1）: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(available_models):
        return available_models[int(choice) - 1]
    else:
        print(f"默认选择第 1 个模型：{available_models[0]}")
        return available_models[0]

# === 核心智能体 ===
# 用于保存对话历史
conversation_history = [
    {"role": "system", "content": "你是一个友好的 AI 助手，可以聊天回答问题。"}
]


async def simple_agent(model_name: str, user_input: str):
    # 把用户输入添加到历史
    conversation_history.append({"role": "user", "content": user_input})

    # 调用 OpenAI 接口，带上完整历史
    response = await client.chat.completions.create(
        model=model_name,
        messages=conversation_history
    )

    # 取出 AI 回复
    ai_reply = response.choices[0].message.content

    # 把 AI 回复也加入历史
    conversation_history.append({"role": "assistant", "content": ai_reply})

    return ai_reply

# === 运行入口 ===
async def main():
    # 先列出可用模型并选择
    model_name = await choose_model()
    if not model_name:
        return

    print(f"\n🤖 智能体已启动！（使用模型：{model_name}）输入问题（q 退出）\n")

    while True:
        user_input = input("你：")
        if user_input.lower() in ["q", "quit", "exit"]:
            break
        answer = await simple_agent(model_name, user_input)
        print("智能体：", answer)

if __name__ == "__main__":
    asyncio.run(main())
