import asyncio
import multiprocessing
import os
import re
import time
import json

from agent.tools.deepseek import chatWithMessages




def read_file(filePath):
    with open(filePath, "r", encoding='utf-8') as file:
        content = file.read()
        content += "\n\n\n"
    return content


def chatWithDeespseek(promptStudent, student_message):
    try:
        resStudent = asyncio.run(chatWithMessages(promptStudent, student_message))  # 启动主程序
        # print(resStudent)
        student_message.append({"role": "assistant", "content": resStudent})
        return resStudent
    except Exception as e:
        print(f"An error occurred during execution: {e}")  # 捕获并输出主程序的错误


def deal_findBlock(file_content, student_message,mainContract):
    promptStudent = read_file("prompt._findblock.txt")
    promptStudent = re.sub(r'`solidityFile`', file_content, promptStudent)
    promptStudent = re.sub(r'`mainContract`', mainContract, promptStudent)
    # print(promptStudent.__len__(), file_path)
    resStudent = chatWithDeespseek(promptStudent, student_message)
    return resStudent


def deal_reachStatement_if(student_message):
    promptStudent = read_file("prompt_reach_statement_if.txt")
    # promptStudent = re.sub(r'`\$\{solidityFile\}`', file_content, promptStudent)
    # promptStudent = re.sub(r'`\$\{statementArray\}`', findBlockRes, promptStudent)
    # promptStudent = re.sub(r'`\$\{functionName\}`', functionName, promptStudent)
    # print(promptStudent.__len__(), file_path)
    resStudent = chatWithDeespseek(promptStudent, student_message)
    return resStudent

def deal_reachStatement_function(student_message):
    promptStudent = read_file("prompt_reach_statement_function.txt")
    # promptStudent = re.sub(r'`\$\{solidityFile\}`', file_content, promptStudent)
    # promptStudent = re.sub(r'`\$\{statementArray\}`', findBlockRes, promptStudent)
    # promptStudent = re.sub(r'`\$\{functionName\}`', functionName, promptStudent)
    # print(promptStudent.__len__(), file_path)
    resStudent = chatWithDeespseek(promptStudent, student_message)
    return resStudent


def dealJson(jsonRes, funcName):
    content = jsonRes.replace("```json", "").replace("```", "").strip()
    data = json.loads(content)
    for i in range(data.__len__()):
        if (data[i]["functionName"] == funcName):
            return data[i].__str__()
    return None


def deal_return_array_form_data(jsonRes):
    content = jsonRes.replace("```json", "").replace("```", "").strip()
    data = json.loads(content)
    return data


def deal_return_specific_length(data, ind, len):
    ##TODO
    ### 返回从索引ind开始的len长度的子数组
    return data[ind:ind + len]


def deal_split_array(data):
    ##TODO:返回一个字典数组，每个元素的组成是{data,functionName}
    res = []
    length = 3
    for i in range(len(data) - length):
        datax = deal_return_specific_length(data, i, length)
        res.append({"data": datax, "functionName": data[i]["functionName"]})
    startInd = len(data) - length
    datax = deal_return_specific_length(data, startInd, length)
    for j in range(length):
        res.append({"data": datax, "functionName": data[startInd]["functionName"]})
    return res


def extract_wrapped_content(input_string):
    # 定义正则表达式，匹配被 ```json 和 ``` 包裹的内容
    pattern = r'```json\s+(.*?)\s+```'
    match = re.search(pattern, input_string, re.DOTALL)  # 使用 re.DOTALL 匹配多行内容

    # 如果匹配成功，返回提取的内容
    if match:
        return match.group(1).strip()  # 去除首尾空白字符
    else:
        return None  # 如果没有匹配到，返回 None


def deal_match_json_content(content):
    ## TODO:把识别出来的内容直接按照json格式读入然后返回一个数组
    modifiedContent = extract_wrapped_content(content)
    dataArray = json.loads(modifiedContent)
    return dataArray


def worker(args):
    file_content, stuMes, res1 = args
    print("res1414", res1)
    return deal_reachStatement_if(file_content, stuMes, res1["data"], res1["functionName"])


def deal_subprocess_deepseek(file_content, splitArray, stuMes):
    ## TODO:返回多线程访问deepseek的所有结果,每次最多开PC的核心数个
    m = multiprocessing.cpu_count()
    max_workers = max(1, m - 2)  # 最多开 m-2 个线程
    tasks = [(file_content, stuMes, res1) for res1 in splitArray]

    # 分批处理任务
    batch_size = max_workers  # 每批的任务数等于最大工作进程数
    res2_list = []

    with multiprocessing.Pool(processes=max_workers) as pool:
        for i in range(0, len(tasks), batch_size):
            batch = tasks[i:i + batch_size]  # 获取当前批次的子任务
            print(f"Processing batch: {i}")
            batch_results = pool.map(worker, batch)  # 处理当前批次
            res2_list.extend([result[0] for result in batch_results])  # 收集结果

    # 打印所有 res2 结果
    print("All res2 results:", res2_list)
    ##TODO: res是每一个多线程的结果
    subprocess_res = []
    for i in range(len(res2_list)):
        subprocess_res.append(deal_match_json_content(res2_list[i]))
    return subprocess_res


##这个位置没有做去重
def deal_return_set_res(data):
    ##TODO:把GPT的所有结果都返回成一个数组，然后做成set
    res = []
    map = {}
    for i in range(len(data)):
        for j in range(len(data[i])):
            functionName = data[i][j]["functionName"]
            if (not (functionName in map.keys())):
                map[functionName] = []
            sequences = data[i][j]["sequences"]
            for k in range(len(sequences)):
                map[functionName].append(sequences[k])
    keys = data.keys
    for key in keys:
        ## key是functionName
        functionName = key
        sequences = map[key]
        res.append({
            functionName: functionName,
            sequences: sequences
        })
    return res


def summary(file_content, res1, stuMes):
    data = deal_return_array_form_data(res1)
    splitArray = deal_split_array(data)

    deepseekRes = deal_subprocess_deepseek(file_content, splitArray, stuMes)
    setRes = deal_return_set_res(deepseekRes)
    return setRes


def setList(lst):
    res = []
    resMap = {}
    for i in range(lst.__len__()):
        str = ""
        for j in range(lst[i].__len__()):
            str += lst[i][j]['functionName']
        if (str in resMap.keys()):
            continue
        else:
            res.append(lst[i])
            resMap[str] = 1
    return res


def generateSequenceFromDeepseek(tmpDir,filename,student_message,mainContract):
    # freeze_support()  # 在 Windows 或 macOS 上需要调用
    # 遍历 sol 文件夹，读取每个 .sol 文件的内容
    # tmpDir = "../B1/sol"

    # tmpSuffix = "_tmp.txt"
    # suc_rec = "./B3/suc_rec.txt"
    # error_rec = "./B3/error_rec.txt"
    output_directory = os.path.join(tmpDir, "output1")
    datasetDir = os.path.join(tmpDir,"sol")
    # if not os.path.exists(output_directory):
    #     os.mkdir(output_directory)
    # student_message = []



    if filename.endswith('.sol'):
        start_time = time.time()
        print(filename)
        file_path = os.path.join(datasetDir, filename)  # 获取每个文件的完整路径
        with open(file_path, 'r', encoding='utf-8') as file:
            file_content = file.read()  # 读取文件内容
        # student_message = []

        ###这个agent会自动把deepseek的回答放在message聊天记录里面
        deal_findBlock(file_content, student_message,mainContract)
        # summary(file_content,res1,stuMes)
        # func = dealJson(res1,"_sell")
        res2 = deal_reachStatement_if(student_message)
        # print(res2)
        # res3 = deal_reachStatement_function(student_message)
        ###把结果输出出去
        output_file = filename.replace(".sol","_output.txt")
        output = os.path.join(output_directory,output_file)
        # with open(output1,"w") as file:
        #     file.write(res2)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"{filename} execution time: {execution_time:.6f} seconds")
        # print(summary(file_content,res1,stuMes))
        ##TODO: 这个返回的结果应该可以去做去重
        return res2


def tmp_jioaben():
    tmpDir = "../../B3"
    solDir = os.path.join(tmpDir,"sol")
    assetsDir = os.path.join(tmpDir, "assets")
    assetsPath = os.path.join(assetsDir, "B3.list")
    with open(assetsPath) as file:
        lines = file.readlines()
        # 创建一个空字典
    mainContract_map = {}

    # 遍历每一行，将键值对添加到字典中
    for line in lines:
        key, value = line.strip().split(",")
        mainContract_map[key] = value

    for file_name in os.listdir(solDir):
        output_file = file_name.replace(".sol", "_output.txt")
        output_directory = os.path.join(tmpDir, "output")
        output = os.path.join(output_directory, output_file)
        if output_file in os.listdir(output_directory):
            continue  ##成功生成的不再生成
        messgaes = []
        filenameTag = file_name.replace(".sol", "")
        mainContract = mainContract_map[filenameTag]
        try:
            res = generateSequenceFromDeepseek(tmpDir,file_name,messgaes,mainContract)
        except Exception as e:
            with open(os.path.join(solDir,file_name))as file:
                content = file.read()
            print("error",file_name,e)
            continue
        with open(output,"w") as file:
            file.write(res)

tmp_jioaben()