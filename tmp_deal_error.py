import argparse
import json
import os
import subprocess
import time

from agent.second_agent.getSubContract import getSubContract
from agent.first_agent.deepseek_findblock_reachif import generateSequenceFromDeepseek, deal_findBlock, \
    deal_reachStatement_if
from agent.second_agent.deepseek_deal_result import deal_decode_error
from agent.tools.GPT2Seed import GPT2SmartianSeed
import json5


def test():
    filename = "2018-10706.sol"
    sequences = {"res": []}
    subContracts = getSubContract()
    for subContract in subContracts:
        if (subContract["sequences"].__len__() != 0):
            sequences["res"].append(subContract)
        else:
            messages = []
            result = generateSequenceFromDeepseek(tmpDir, filename, messages, mainContract)
            sequences["res"] += result["res"]
    return sequences

def generateSequenceForNewContract(student_message,newContract):
    start_time = time.time()
    ###这个agent会自动把deepseek的回答放在message聊天记录里面
    deal_findBlock(newContract, student_message,"")
    # summary(file_content,res1,stuMes)
    # func = dealJson(res1,"_sell")
    res2 = deal_reachStatement_if(student_message)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"{filename} execution time: {execution_time:.6f} seconds")
    # print(summary(file_content,res1,stuMes))
    ##TODO: 这个返回的结果应该可以去做去重
    return res2

def deal_second_agent(resSecondAgent,tmpDir,filename,datasetName):
    data = json.loads(resSecondAgent)
    if (data["reason"] == 'first'):
        ##做约减
        sequences = {"res": []}
        subContracts = getSubContract(tmpDir,filename,datasetName)
        for subContract in subContracts:
            try:
                if (subContract["sequences"].__len__() != 0):
                    sequences["res"].append(subContract)
                else:
                    messages = []
                    result = generateSequenceForNewContract(messages, subContract["newContract"])
                    try:
                        result = json.loads(result)
                    except Exception as e:
                        continue
                    sequences["res"] += result["res"]
            except Exception as e:
                continue
        return sequences
    elif (data["reason"] == 'second'):
        return data['result']


def read_err_file():
    file_path = "error2.txt"
    with open(file_path, "r") as file:
        log_content = file.read()  # 读取日志内容
        lines = log_content.splitlines()  # 获取第一行
    res = []
    for line in lines:
        if (line != ''):
            first_file = line.split()[0]  # 获取第一个单词（文件名）
            if (first_file.endswith("_seed.txt")):
                first_file = first_file.replace("_seed.txt", ".sol")
            res.append(first_file)
    return res


if __name__ == "__main__":
    # test()

    # parser = argparse.ArgumentParser(description="A script to process a file.")
    # # 添加 -filename 参数
    # parser.add_argument("-filename", type=str, required=True, help="The name of the file to process")
    # parser.add_argument("-datasetName", type=str, required=True, help="The name of the dataset")
    # parser.add_argument("-datasetPath", type=str, required=True, help="The system path dir of the dataset")
    # parser.add_argument("-outputDir", type=str, required=True, help="The output directory the smartian result output")
    # parser.add_argument("-timeLimit", type=str, required=True, help="The time limit that all the process needs")
    # parser.add_argument("-fuzzer", type=str, required=True, help="The ultilized fuzzer")

    # 解析参数
    # args = parser.parse_args()
    # 使用参数
    tmpDir = "B3"
    datasetName = "B3"
    res = read_err_file()
    for filename in res:
        messages = []
        filename = filename.replace("_seed.txt",".sol")
        if filename == "0xf7a6e15dfd5cdd9ef12711bd757a9b6021abf643.sol":
            mm = 1
        print(f"Processing file: {filename}")
        filename = filename
        assetsDir = os.path.join(tmpDir, "assets")
        assetsPath = os.path.join(assetsDir, datasetName + ".list")
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

        seedDir = os.path.join(os.path.abspath(tmpDir),"new_seed2")
        seedFile = filenameTag + "_seed.txt"
        if os.path.exists(os.path.join(seedDir,seedFile)):
            continue

        ###TODO: get normalFuncs 这个可以提前生成
        '''
        包含两个agent
        '''
        # result = generateSequenceFromDeepseek(os.path.abspath(tmpDir), filename, messages, mainContract)
        with open('0x1e2f.txt', 'r', encoding='utf-8') as file:
            result = file.read()

        # 使用 json5 解析
        # result = json5.loads(content)

        # print(data)
        # result = ""
        '''
        对结果做处理
        '''
        try:
            data = json5.loads(result)
        except json.JSONDecodeError as e:
            print("Error: Failed to decode JSON. Now turn to Agent to deal with the decode error.")
            if("Unterminated" in str(e) or "delimiter" in str(e)):
                resSecondAgent = '{"reason":"first"}'
            else:
                resSecondAgent = deal_decode_error(result)
            data = deal_second_agent(resSecondAgent,os.path.abspath(tmpDir), filename,datasetName)
        except Exception as e:
            resSecondAgent = '{"reason":"first"}'
            data = deal_second_agent(resSecondAgent, os.path.abspath(tmpDir), filename, datasetName)
        # print(f"An error occurred: {e}")
        # outputDir = args.outputDir
        # timeLimit = args.timeLimit
        # fuzzer = args.fuzzer
        # if (fuzzer == "smartian"):
        GPT2SmartianSeed(data, filename, tmpDir, mainContract)
            # deal_smartian_fuzzer(data, filename, tmpDir, mainContract, datasetName, outputDir, timeLimit, messages)
        # elif(fuzzer == "ityfuzz"):
        #     deal_ityfuzz_fuzzer()