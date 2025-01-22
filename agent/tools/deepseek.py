import sys

from openai import OpenAI
import asyncio

key = "sk-a73fde8a79da4dabb6dff23c634d8383"



async def chatWithMessages(content,messages):
    messages.append(
        {"role": "user", "content": content}
    )
    client = OpenAI(api_key=key, base_url="https://api.deepseek.com")
    # print(messages)
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        stream=False,
        temperature=0.4,
        response_format = {
            'type': 'json_object'
        },
        max_tokens=8000
    )
    # print(response.choices[0].message.content)
    return response.choices[0].message.content


# 主程序执行
async def op(content,messages):
    try:
        # 创建一个任务来运行 chatWithMessages
        task = asyncio.create_task(chatWithMessages(content,messages))
        # 等待任务至多 2 分钟
        await asyncio.wait_for(task, timeout=120)  # 设置 120 秒超时
        return task
    except asyncio.TimeoutError:
        print("Timeout reached, continuing without waiting for chatWithMessages.")

    except Exception as e:  # 捕获其他所有异常
        print(f"An error occurred: {e}")