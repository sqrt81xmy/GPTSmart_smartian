import ast
import copy
import json
import os
import re

from sympy import false

addressMap = {
    "NormalUser1": "0x118a2c24808934116e6ab4c00ff48145d23b09e1",
    "NormalUser2": "0x226cc61b3eac93cc2cc9d6cb8d61856670d50fad",
    "NormalUser3": "0x33b808a5ae24c410e8739b5ca2d5ef3931d3e09f",
    "TARG_CONTRACT": "0x6b773032d99fb9aad6fc267651c446fa7f9301af"
}

msgSender = ["NormalUser1", "NormalUser2", "NormalUser3", "TargetOwner"]

def read_last_line(file_path):
    with open(file_path, 'rb') as file:
        file.seek(0, os.SEEK_END)  # 移动到文件的末尾
        position = file.tell()      # 获取当前位置
        while position >= 0:
            file.seek(position)      # 移动到当前位置
            char = file.read(1)      # 读取一个字符
            if char == b'\n' and position != (os.path.getsize(file_path) - 1):
                return file.readline().decode().strip()  # 返回最后一行
            position -= 1
    return None  # 如果文件为空，返回 None

import json

# 读取 JSON 文件的函数



def read_json_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)  # 返回解析后的 JSON 数据
    except Exception as e:
        # 捕获异常并记录到 error_rec 文件中
        # with open(err_rec, 'a', encoding='utf-8') as error_file:
        #     error_file.write(f"{file_path}\n")
        print("an error occured in read_json_file in GPT2SeedFile at line 44")
        return None  # 或者返回任何适合的值

# 设置基本目录
# baseDir = "./B3/outputcc"  # 请替换为实际的基本目录路径
# seedDir = "./B3/seed1"
# normalFunsDir = "./B3/normalFuncs"



def getNameFromLeftPara(input_string):

    print(input_string)
    # 查找左括号的位置
    left_parenthesis_index = input_string.find('(')

    # 提取左括号前面的内容
    if left_parenthesis_index != -1:  # 确保找到了左括号
        return input_string[:left_parenthesis_index]  # 使用切片获取内容
    else:
        return input_string  # 如果没有括号，则返回原字符串

def getTransactionFromBigData(data,Name):
    for i in range(data['Transactions'].__len__()):
        if data['Transactions'][i]['FuncSpec']['Name'] == Name:
            return copy.deepcopy(data['Transactions'][i])

def to_little_endian_bytes(value, byte_size):
    """
    将整数转换为小端序的字节数组。
    :param value: 整数值
    :param byte_size: 字节数组的长度
    :return: 小端序的字节数组
    """


    if value < 0:
         # 对于负数，使用补码表示
         value = (1 << (byte_size * 8)) + value

    return value.to_bytes(byte_size, byteorder='little')

def dealHexParam(normalFuncsT,value,i,elemInd=None):
    address = value  # 地址
    str = address[2:]
    if str in addressMap.keys():  ##GPT有时出错
        str = addressMap[str]
        str = str[2:]
    # print(str)
    if (str.__len__() % 2 == 1):
        str = "0" + str
    address_bytes = bytes.fromhex(str)  # 去掉 0x 前缀并转换为字节数组
    address_bytes = address_bytes[::-1]
    for j in range(normalFuncsT['Args'][i + 1]['Elems'][0]['ByteVals'].__len__()):
        if j >= address_bytes.__len__():
            break
        # print(i,j,normalFuncsT['Args'][i+1]['Elems'][0]['ByteVals'].__len__(),address_bytes.__len__())
        # 把第一个位置给空出来
        if (elemInd != None):
            normalFuncsT['Args'][i + 1]['Elems'][elemInd]['ByteVals'][j]['Fields'][0] = address_bytes[j]
            # print(amount_bytes.__len__(), normalFuncsT['Args'][i + 1]['Elems'][0]['ByteVals'][j]['Fields'].__len__(),j,i,amount_bytes[j],normalFuncsT['Args'][i+1]['Elems'][0]['ByteVals'][j]['Fields'][0])
        else:
            normalFuncsT['Args'][i + 1]['Elems'][0]['ByteVals'][j]['Fields'][0] = address_bytes[j]

def dealIntegerParam(normalFuncsT,value,i,elemInd=None):
    if (value == 'true'):
        amount = 1
    elif (value == 'false'):
        amount = 0
    else:
        try:
            amount = int(value)  # 数量
        except Exception as e:
            amount = 0
    amount_bytes = to_little_endian_bytes(amount, normalFuncsT['Args'][i + 1]['Elems'][0][
        'ByteVals'].__len__())  # 转换为 32 字节的小端序字节数组

    for j in range(amount_bytes.__len__()):
        if (elemInd != None):
            normalFuncsT['Args'][i + 1]['Elems'][elemInd]['ByteVals'][j]['Fields'][0] = amount_bytes[j]
        else:
            normalFuncsT['Args'][i + 1]['Elems'][0]['ByteVals'][j]['Fields'][0] = amount_bytes[j]

def setParams(input_str, normalFuncsT):
    # 使用正则表达式提取括号内的内容
    match = re.match(r'.*\((.*)\)', input_str['functionName'])
    if match:
        # 提取括号内的参数
        params_str = match.group(1)
        if(params_str == ""):
            return
        print("括号内的参数:", params_str)
    else:
        print("未匹配到参数")
        return
    # 拆分参数
    params = [param.strip() for param in re.split(r',\s*(?![^[]*\])', params_str)]

    # 将参数转换为小端序字节数组


    for i in range(len(normalFuncsT['Args'])-1):
        if(i>=params.__len__()):
            break
        if params[i] in addressMap.keys():
            params[i] = addressMap[params[i]]
        if params[i].startswith("0x"):
            # 处理地址
            dealHexParam(normalFuncsT,params[i],i)
        elif params[i].startswith("["):
            try:
                # 去掉方括号
                content = params[i].strip('[]')
                # 按逗号分割元素
                elements = [element.strip() for element in content.split(',')]
                for j in range(len(elements)):
                    tar = elements[j]
                    if tar in addressMap.keys():
                        tar = addressMap[tar]
                    if tar.startswith("0x"):
                        # 处理地址
                        dealHexParam(normalFuncsT, tar, i,j)
                    else:
                        dealIntegerParam(normalFuncsT, tar,i, j)
            except (ValueError, SyntaxError):
                print("Failed to parse the array string.")
        else:
            # 处理数量
            dealIntegerParam(normalFuncsT,params[i],i)
    if(input_str['msgSender'].startswith("0x")):
        # 去掉 "0x" 前缀
        address_without_prefix = input_str['msgSender'][2:]
        # 将所有大写字母转换为小写字母
        input_str['msgSender'] = address_without_prefix.lower()
        normalFuncsT['Sender']['Case'] = "CustomUser"
        normalFuncsT['Sender']['name'] = input_str['msgSender']
    ###处理msg.sender和msg.value
    else:
        if input_str['msgSender'] == "TARG_CONTRACT":
            input_str['msgSender'] = "TargetOwner"
        if input_str['msgSender'] not in msgSender:
            input_str['msgSender'] = "NormalUser1"
        normalFuncsT['Sender']['Case'] = input_str['msgSender']
    normalFuncsT['UseAgent'] = "false"
    try:
        amount = int(input_str['msgValue'])  # 数量
    except Exception as e:
        amount = 0
    amount_bytes = to_little_endian_bytes(amount, normalFuncsT['Args'][0]['Elems'][0][
        'ByteVals'].__len__())  # 转换为 32 字节的小端序字节数组
    for j in range(amount_bytes.__len__()):
        normalFuncsT['Args'][0]['Elems'][0]['ByteVals'][j]['Fields'][0] = amount_bytes[j]



def getSeedFromSeq(Seq,file_name,mainContract,normalFuncsDir):
    resultTx = []
    json_path = file_name.replace(".sol", "_normalFuncs.txt")
    json_path = os.path.join(normalFuncsDir,json_path)
    # json_path = 'a.json'  # 替换为实际的文件路径
    data = read_json_file(json_path)
    # print(file_name)
    if data == None:
        return None

    seed = {}
    flag = 0
    i = 0
    name = Seq[i]
    functionName = getNameFromLeftPara(name['functionName'])
    if functionName != mainContract and functionName != 'constructor' and functionName != 'Constructor':
        normalFuncsT = getTransactionFromBigData(data, 'constructor')
        resultTx.append(normalFuncsT)
    while i < len(Seq):
        name = Seq[i]
        functionName = getNameFromLeftPara(name['functionName'])
        if functionName == "batchTransfer":
            mm = 1
        if(functionName == mainContract):
            normalFuncsT = getTransactionFromBigData(data, 'constructor')
        elif(functionName == 'constructor'):
            normalFuncsT = getTransactionFromBigData(data, 'constructor')
        elif(functionName == 'Constructor'):
            normalFuncsT = getTransactionFromBigData(data, 'constructor')
            # resultTx.append(constructorT)
        else:
            if name['functionName'] == "()" or name['functionName'] == "":
                print("fallback")
                name['functionName'] = "fallback()"
            elif name['functionName'].startswith("()"):
                name['functionName'] = name['functionName'].replace("()", "fallback", 1)
            functionName = getNameFromLeftPara(name['functionName'])
            normalFuncsT = getTransactionFromBigData(data, functionName)
        if(normalFuncsT):
            setParams(name, normalFuncsT)
            resultTx.append(normalFuncsT)
        else:
            flag = 1
            if name != "address":
                print("alert!!danger!!",name, file_name)
            # return None
        i += 1
    # if flag == 1:
    #



    seed['Transactions'] = resultTx
    seed['TXCursor'] = 0
    return seed


def write_seeds(file_name,seeds,seedDir):
    seed_filename = file_name.replace(".sol", "_seed.txt")
    seed_path = os.path.join(seedDir, seed_filename)
    with open(seed_path, "w") as file:
        json.dump(seeds, file, indent=4, ensure_ascii=False)  # 写入文件
    # 从文件读取数据
    # 打印结果
    # print(seed1)  # 输出: ['a', 'b']
    mm = 1

def extract_wrapped_content(input_string):
    # 定义正则表达式，匹配被 ```json 和 ``` 包裹的内容
    # 定义正则表达式，匹配被 ```json 和 ``` 包裹的内容
    pattern = r'```json\s+(.*?)\s+```'
    matches = re.findall(pattern, input_string, re.DOTALL)  # 使用 re.DOTALL 匹配多行内容

    if matches:
        # 去除每个匹配内容的首尾空白字符，并返回数组
        return [match.strip() for match in matches]
    else:
        return None  # 如果没有匹配到，返回 None

def deal_json_obj(data):
    data = data["res"]
    res = []
    for xdata in data:
        if 'sequence' in xdata.keys():
            res.append(xdata['sequence'])
        elif 'sequences' in xdata.keys():
            res.append(xdata['sequences'])
    return res

def read_json(file_path):
    # if file_path == './B3/outputcc\\smart_billions_output.txt':
    #     m = 1;
    try:
        # 打开并读取 JSON 文件
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            data = json.loads(content)
            data = data["res"]
            res = []
            for xdata in data:
                if 'sequence' in xdata.keys():
                    res.append(xdata['sequence'])
                elif 'sequences' in xdata.keys():
                    res.append(xdata['sequences'])
            return res
            #  # 解析 JSON 数据为字典
            # content = file.read()
            # # 去掉前缀 ```json 和后缀 ```, 并去除多余空白
            # # content = content.replace("```json", "").replace("```", "").strip()
            # content = extract_wrapped_content(content)
            # if content.__len__() == 1:
            #     content = content[0]
            #     data = json.loads(content)
            # else:
            #     data = []
            #     for cont in content:
            #         datamm = json.loads(cont)
            #         data.append(datamm)
            #     return data
            # if not type(data) == list:
            #     if 'sequence' in data.keys():
            #         return data['sequence']
            #     elif 'sequences' in data.keys():
            #         return data['sequences']
            # else:
            #     res = []
            #     for xdata in data:
            #         if 'sequence' in xdata.keys():
            #             res.append(xdata['sequence'])
            #         elif 'sequences' in xdata.keys():
            #             res.append(xdata['sequences'])
            #     return res
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def setList(lst):
    res = []
    resMap = {}
    for i in range(lst.__len__()):
        str = ""
        for j in range(lst[i].__len__()):
            str += lst[i][j]['functionName']
        if(str in resMap.keys()):
            continue
        else:
            res.append(lst[i])
            resMap[str] = 1
    return res
def GPT2SmartianSeed(data,file_name,datasetDir,mainContract):
    # 读取文件名并处理
    # with open(suc_rec, "r") as file:
    # for file_name in os.listdir(solDir):
    #     print(file_name)
    #     ouput_name = file_name.replace(".sol","_output.txt")
    #     file_path = os.path.join(GPT_output_dir, ouput_name)
    #     try:
    #         array = read_json(file_path)
    #     except Exception as e:
    #         print(f"An error occurred: {e}")
    #         continue
    seedDir = os.path.join(datasetDir, "seed")
    normalFuncsDir = os.path.join(datasetDir, "normalFuncs")

    if os.path.exists(seedDir) == False:
        os.mkdir(seedDir)

    array = deal_json_obj(data)
    seeds = []
    # assetsDir = os.path.join(datasetDir, "assets")
    # assetsPath = os.path.join(assetsDir, "B1.list")
    # with open(assetsPath) as file:
    #     lines = file.readlines()
    # # 创建一个空字典
    # mainContract_map = {}
    #
    # # 遍历每一行，将键值对添加到字典中
    # for line in lines:
    #     key, value = line.strip().split(",")
    #     mainContract_map[key] = value
    # filenameTag = file_name.replace(".sol", "")
    # mainContract = mainContract_map[filenameTag]
    for i in range(array.__len__()):
        array[i] = setList(array[i])
        for seq in array[i]:
            seed = getSeedFromSeq(seq,file_name,mainContract,normalFuncsDir)
            # print(seed1['Transactions'].__len__())
            print(seed)
            if seed == None or seed['Transactions'].__len__() == 1:
                continue
            seeds.append(seed)
            ##把Seed写入文件中
    write_seeds(file_name, seeds,seedDir)
