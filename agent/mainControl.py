import argparse
import json
import os
import subprocess

from second_agent.getSubContract import getSubContract
from first_agent.deepseek_findblock_reachif import generateSequenceFromDeepseek
from second_agent.deepseek_deal_result import deal_decode_error
from tools.GPT2Seed import GPT2SmartianSeed


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


def deal_second_agent(resSecondAgent):
    data = json.loads(resSecondAgent)
    if (data["reason"] == 'first'):
        ##做约减
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
    elif (data["reason"] == 'second'):
        return data['result']


if __name__ == "__main__":
    # test()
    messages = []
    parser = argparse.ArgumentParser(description="A script to process a file.")
    # 添加 -filename 参数
    parser.add_argument("-filename", type=str, required=True, help="The name of the file to process")
    parser.add_argument("-datasetName", type=str, required=True, help="The name of the dataset")
    parser.add_argument("-datasetPath", type=str, required=True, help="The system path dir of the dataset")
    parser.add_argument("-outputDir", type=str, required=True, help="The output directory the smartian result output")
    parser.add_argument("-timeLimit", type=str, required=True, help="The time limit that all the process needs")

    # 解析参数
    args = parser.parse_args()
    # 使用参数
    print(f"Processing file: {args.filename}")
    filename = args.filename
    tmpDir = args.datasetPath
    datasetName = args.datasetName
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
    ###TODO: get normalFuncs 这个可以提前生成

    '''
    包含两个agent
    '''
    result = generateSequenceFromDeepseek(tmpDir, filename, messages, mainContract)
    '''
    对结果做处理
    '''
    try:
        data = json.loads(result)
        GPT2SmartianSeed(data, filename, tmpDir, mainContract)
        seedDir = os.path.join(tmpDir, "seed")
        seedDir = os.path.abspath(seedDir)
        # seed_filename = filename.replace(".sol", "_seed.txt")
        # seed_path = os.path.join(seedDir, seed_filename)
        # seed_path = os.path.abspath(seedDir)
        smartian_datasetDir = datasetName
        abiName = filename.replace(".sol", ".abi")
        abiDir = os.path.join(smartian_datasetDir,"abi")
        abiPath = os.path.join(abiDir,abiName)
        binName = filename.replace(".sol", ".bin")
        binDir = os.path.join(smartian_datasetDir,"bin")
        binPath = os.path.join(binDir,binName)
        outputDir = args.outputDir
        timeLimit = args.timeLimit
        cmd_str_build = "dotnet build Smartian/src/Smartian.fsproj"
        cmd_str_exec = "dotnet Smartian/src/bin/Debug/net8.0/Smartian.dll fuzz " \
                       " -p " + binPath + " -a " + abiPath + " -s " + seedDir + \
                       " -t " + timeLimit + " -o " + outputDir

        # 执行 build 命令
        try:
            print("Running build command...")
            result_build = subprocess.run(cmd_str_build, shell=True, check=True, text=True)
            print("Build completed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Build failed with error: {e}")
            exit(1)  # 如果 build 失败，退出程序

        # 执行 exec 命令
        try:
            print("Running exec command...")
            result_exec = subprocess.run(cmd_str_exec, shell=True, check=True, text=True)
            print("Exec completed successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Exec failed with error: {e}")

    except json.JSONDecodeError:
        print("Error: Failed to decode JSON. Now turn to Agent to deal with the decode error.")
        resSecondAgent = deal_decode_error(messages)
        deal_second_agent(resSecondAgent)
    except Exception as e:
        print(f"An error occurred: {e}")
