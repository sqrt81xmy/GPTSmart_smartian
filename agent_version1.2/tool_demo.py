from openai import OpenAI

# 定义函数
def get_current_weather(location: str):
    """
    获取指定地点的当前天气。

    参数:
        location (str): 地点名称

    返回:
        str: 天气信息
    """
    # 这里模拟调用天气 API
    if location == "Beijing":
        return "Sunny, 25°C"
    elif location == "Shanghai":
        return "Cloudy, 22°C"
    else:
        return "Unknown location"

def send_messages(messages):
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=tools
    )
    return response.choices[0].message

client = OpenAI(
    api_key="sk-325c7b2d26bb448283e36709e2f94b4a",
    base_url="https://api.deepseek.com",
)

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get weather of an location, the user shoud supply a location first",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    }
                },
                "required": ["location"]
            },
        }
    },
]

messages = [{"role": "user", "content": "How's the weather in Hangzhou?"}]
message = send_messages(messages)
print(f"User>\t {messages[0]['content']}")

tool = message.tool_calls[0]
messages.append(message)

messages.append({"role": "tool", "tool_call_id": tool.id, "content": "24℃"})
message = send_messages(messages)
print(f"Model>\t {message.content}")