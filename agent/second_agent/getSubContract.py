import os

from slither import Slither
from agent.second_agent.split_ifUse_define_set import getSetfromSolidity


# # 安装 Solidity 编译器
# install_solc('0.8.0')
#
# # 编译 Solidity 代码并生成 AST
# source_code = """
# pragma solidity ^0.8.0;
#
# contract SimpleStorage {
#     uint256 storedData;
#
#     function set(uint256 x) public {
#         storedData = x;
#     }
#
#     function get() public view returns (uint256) {
#         return storedData;
#     }
# }
# """

def find_function(contract, functionName):
    functions = []
    # 提取函数定义
    for function in contract.functions:
        if function.name == functionName:
            # print(f"Function '{target_function}' definition found:")
            # print()
            functions.append(function)
    if functions.__len__() == 1:
        return functions[0]
    elif functions.__len__() > 1:
        for function in functions:
            if (function.is_implemented == True and function.is_override == False):
                return function
        return functions[-1]
    else:
        return None


def find_variable(contract, variName):
    for variable in contract.state_variables:
        if variable.name == variName:
            # print(f"State variable '{target_variable}' definition found:")
            # print(variable.source_mapping.content)
            return variable.source_mapping.lines
        else:
            for contract in contract.inheritance:
                find_function(contract, variName)
    return None


# compiled = compile_source(source_code, output_values=["ast"], optimize=False)

# 获取 AST
# ast = compiled['<stdin>:DSPXToken']['ast']['children'][-1]

# functionSets = [
#     [{'fName': 'deal', 'vari': ['games', 'maxBet', 'minBet']}, {'fName': 'getPlayerCard', 'vari': ['games']},
#      {'fName': 'getHouseCard', 'vari': ['games']}, {'fName': 'getGameState', 'vari': ['games']}],
#     [{'fName': 'valueOf', 'vari': []}], [{'fName': 'isAce', 'vari': []}], [{'fName': 'isTen', 'vari': []}],
#     [{'fName': 'BlackJack', 'vari': []}], [{'fName': 'fallback', 'vari': []}], [{'fName': 'hit', 'vari': []}],
#     [{'fName': 'stand', 'vari': []}], [{'fName': 'checkGameResult', 'vari': ['BLACKJACK']}],
#     [{'fName': 'calculateScore', 'vari': []}], [{'fName': 'getPlayerCardsNumber', 'vari': []}],
#     [{'fName': 'getHouseCardsNumber', 'vari': []}], [{'fName': 'slitherConstructorVariables', 'vari': []}]]


def getSubContract(tmpDir,file_name,datasetName):

    """
        数据集的初始化
        dataset initialize
    """
    # datasetDir = "../B1"
    datasetDir = tmpDir
    solDir = os.path.join(datasetDir, "sol")
    assetsDir = os.path.join(datasetDir, "assets")
    assetsPath = os.path.join(assetsDir, datasetName + ".list")
    mainContract_map = {}
    with open(assetsPath) as file:
        lines = file.readlines()
        # 遍历每一行，将键值对添加到字典中
    for line in lines:
        key, value = line.strip().split(",")
        mainContract_map[key] = value
    """
        some data initialize that will be used later
    """
    solcs = []
    # file_name = "2018-10706.sol"
    solc_path = os.path.join(solDir, file_name)
    slither = Slither(solc_path)
    with open(solc_path) as file:
        source_code = file.read()
    filenameTag = file_name.replace(".sol", "")
    mainContract = mainContract_map[filenameTag]
    tarContract = None
    for contract in slither.contracts:
        if contract.name == mainContract:
            tarContract = contract
    xxvv = [function.name for function in tarContract.functions]
    """
        主线任务开始，为每个函数找到在文件中所在的位置
    """
    functionSets = getSetfromSolidity(solc_path, tarContract)
    for set in functionSets:
        funs = []  ##函数名称集合
        varis = []  ##变量名称集合
        for obj in set:
            ##收集函数名称
            funcName = obj["fName"]
            funs.append(funcName)
            ###收集变量名称
            variArray = obj["vari"]
            for vari in variArray:
                if (vari not in varis):
                    varis.append(vari)
        ###收集函数在文件中的位置
        tmp_solc = []
        for func in funs:
            function = find_function(tarContract, func)
            tmp_solc.append(function)
            ##把内部直接调用先放进去
            for internal_call in function.internal_calls:
                if internal_call not in tmp_solc:
                    tmp_solc.append(internal_call)
            ##然后把节点的间接调用(表达式、返回值)放进去
            for node in function.nodes:
                # 检查节点是否有内部调用
                for internal_call in node.internal_calls:
                    if internal_call not in tmp_solc:
                        tmp_solc.append(internal_call)
                    # 递归提取内部调用的函数
        solc = []
        if (tmp_solc.__len__() != 1):
            for function in tmp_solc:
                if function.source_mapping is not None:
                    solc.append(function.source_mapping.lines)
        else:  ##这个时候说明他只有一个函数
            sequence_single_function = tmp_solc[0]
            if (sequence_single_function.is_constructor == False
                    and sequence_single_function.is_implemented == True
                    and sequence_single_function.is_override == False

            ):   ##我只认为在没有参数的时候才应该用这种方式直接存放而不经过GPT
                # parameter_str = ""
                # parameters = sequence_single_function.parameters
                # address_array = ["NormalUser1","NormalUser2","NormalUser3","TARG_CONTRACT"]
                # for i in range(len(parameters)):
                #     parameter = parameters[i]
                #     if(parameter.type.name == "address"):
                if sequence_single_function.parameters.__len__() == 0:
                    solc.append({
                        "functionName": sequence_single_function.name,
                        "sequences": [
                            [
                                {
                                    "functionName": "constructor()",
                                    "msgValue": 0,
                                    "msgSender": "TargetOwner"
                                },
                                {
                                    "functionName": sequence_single_function.name + "()",
                                    "msgValue": 0,
                                    "msgSender": "TargetOwner"
                                }
                            ]
                        ]
                    })
                else:
                    if sequence_single_function.source_mapping is not None:
                        solc.append(sequence_single_function.source_mapping.lines)
        ###收集变量在文件中的位置
        for vari in varis:
            source_code = find_variable(tarContract, vari)
            solc.append(source_code)
        solcs.append(solc)
    # print(solc)
    # print(functionSets)
    '''
    找到函数位置之后再把函数包好
    '''
    contractPrefix = "contract " + mainContract + "{"
    contractSuffix = "}"
    with open(solc_path, 'r') as file:
        lines = file.readlines()
    setFunctions = []
    for solc in solcs:
        if solc.__len__() != 1 or type(solc[0]) == list:
            str = ""
            for funcOrvari in solc:
                for numberLine in funcOrvari:
                    try:
                        str += lines[numberLine - 1]
                    except Exception as e:
                        continue
            setFunctions.append({
                "newContract": contractPrefix + str + contractSuffix,
                "functionLength": solc.__len__(),
                "sequences": []
            })
        else:
            setFunctions.append(solc[0])
            '''
                solc应该具有以下的格式：
                {
                    "functionName":{},
                    "sequences":[] 
                }
            '''
    return setFunctions
    print(setFunctions)
