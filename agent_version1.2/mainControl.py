import argparse
import json
import os

from agent_version1.2/prompt_first_agent.deepseek_findblock_reachif import generateSequenceFromDeepseek
from deepseek_deal_result import deal_decode_error
from agent.tools.GPT2Seed import GPT2SmartianSeed

def deal_second_agent(resSecondAgent):
    data = json.loads(resSecondAgent)
    if(data["reason"] == 'first'):
        ##做约减

    elif(data["reason"] == 'second'):
        return data['result']

if __name__ == "__main__":
    messages = []
    parser = argparse.ArgumentParser(description="A script to process a file.")
    # 添加 -filename 参数
    parser.add_argument("-filename", type=str, required=True, help="The name of the file to process")
    # 解析参数
    args = parser.parse_args()
    # 使用参数
    print(f"Processing file: {args.filename}")
    filename = args.filename
    tmpDir = "../B1"
    assetsDir = os.path.join(tmpDir, "assets")
    assetsPath = os.path.join(assetsDir, "B1.list")
    with open(assetsPath) as file:
        lines = file.readlines()
        # 创建一个空字典
    mainContract_map = {}

    # 遍历每一行，将键值对添加到字典中
    for line in lines:
        key, value = line.strip().split(",")
        mainContract_map[key] = value
    filenameTag = filename.replace(".sol", "")
    mainContract = mainContract_map[filenameTag]
    ###TODO: get normalFuncs 这个可以提前生成

    '''
    包含两个agent
    '''
    result = generateSequenceFromDeepseek(tmpDir,filename,messages,mainContract)
    '''
    对结果做处理
    '''
    try:
        data = json.loads(result)
        GPT2SmartianSeed(data,filename,tmpDir)
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON. Now turn to Agent to deal with the decode error.")
        resSecondAgent = deal_decode_error(messages)
        deal_second_agent(resSecondAgent)
    except Exception as e:
        print(f"An error occurred: {e}")