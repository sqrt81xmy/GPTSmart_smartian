import json
import re
import sys
import pprint

from solidity_parser import parser
from slither.slither import Slither

# sol_path = "B2/sol/0xbaa3de6504690efb064420d89e871c27065cdd52.sol"
# sol_path = "../../../Users/SQRT81/Desktop/ftclLab/if_sub/B1/sol/2018-10706.sol"
# sourceUnit = parser.parse_file(sol_path, loc=False) # loc=True -> add location information to ast nodes
# # pprint.pprint(sourceUnit)
# content = sourceUnit.__str__()
# valid_json_string = content.replace("'", '"')
# # 使用正则表达式替换 True 和 False
# output_string = re.sub(r'\bFalse\b', '"False"', valid_json_string)
# output_string = re.sub(r'\bTrue\b', '"True"', output_string)
# output_string = re.sub(r'\bNone\b', '"None"', output_string)
# data = json.loads(output_string)
mm = 1


#
# def dfs(condition,names):
#     if('left' in condition.keys()):
#         dfs(condition['left'],names)
#     if('right' in condition.keys()):
#         dfs(condition['right'],names)
#     if(condition['type'] == 'Identifier'):
#         names.append(condition['name'])
#     if(condition['type'] == 'MemberAccess'):
#         names.append(condition['expression']['name'])
#     if(condition['type'] == 'IndexAccess'):
#         dfs(condition['base'], names)
#         dfs(condition['index'], names)

# def operate(contract):
#     res = []
#     for i in range(contract['subNodes'].__len__()):
#         con1 = contract['subNodes'][i]['type'] == "FunctionDefinition"
#         if not con1:
#             continue
#         names = []
#         for j in range(contract['subNodes'][i]['body']['statements'].__len__()):
#             con2 = contract['subNodes'][i]['body']['statements'][j]['type'] == "IfStatement"
#             if not con2:
#                 continue
#             condition = contract['subNodes'][i]['body']['statements'][j]['condition']
#             dfs(condition,names)
#         res.append({'functionName':contract['subNodes'][i]['name'],
#                     'ifVariable': list(set(names))
#                     })
#     return res

def operate1(contract):
    res = []
    for function in contract.functions:
        names = []
        for read_variables in function.state_variables_read:
            if function.is_reading_in_conditional_node(read_variables) or function.is_reading_in_require_or_assert(
                    read_variables):
                names.append(read_variables.name)
        res.append({'functionName': function.name,
                    'ifVariable': list(set(names))
                    })
    return res


def getSetfromSolidity(solc_path, mainContract):
    # slither = Slither("B2/sol/0xbaa3de6504690efb064420d89e871c27065cdd52.sol")
    slither = Slither(solc_path)
    write_variable_table = []

    for function in mainContract.functions:
        write_variable_table.append({'functionName': function.name,
                                     'writeVariable': [v.name for v in function.state_variables_written]})

    if_variable_table_ress = []

    for contract in slither.contracts:
        # print('Contract: ' + contract.name)
        if contract.name == mainContract:
            if_variable_table_ress = operate1(contract)
            break

    variMap = {}  # 函数名邻接数组
    vvvMap = {}  # 变量名预处理数组
    funcFlagMap = {}

    for function in write_variable_table:
        variMap[function['functionName']] = []
        funcFlagMap[function['functionName']] = 0
        for vv in function['writeVariable']:
            if vv not in vvvMap.keys():
                vvvMap[vv] = [function['functionName']]
            else:
                vvvMap[vv].append(function['functionName'])

    def addToList(lst, fName, vari):
        for obj in lst:
            if obj["fName"] == fName:
                obj["vari"].append(vari)
                obj["vari"] = list(set(obj["vari"]))
                return
        lst.append({"fName": fName, "vari": [variable]})

    for if_function in if_variable_table_ress:
        # print(if_function)
        fName = if_function['functionName']
        if fName not in variMap.keys():
            continue
        for variable in if_function['ifVariable']:
            if variable in vvvMap.keys():
                for adj_name in vvvMap[variable]:
                    # variMap[adj_name].append({"fName":fName,"vari":[variable]})
                    # variMap[adj_name] = listSet(variMap[adj_name])
                    # variMap[fName].append({"fName":fName,"vari":[variable]})
                    # variMap[fName] = listSet(variMap[fName])
                    addToList(variMap[adj_name], fName, variable)
                    # variMap[adj_name]["vari"] = list(set(variMap[adj_name]["vari"]))
                    addToList(variMap[fName], fName, variable)
                    # variMap[fName]["vari"] = list(set(variMap[fName]["vari"]))

    print(variMap)

    def listSet(lst):
        res = []
        map = {}
        for x in lst:
            if (x["fName"] in map.keys()):
                continue
            else:
                map[x["fName"]] = 1
                res.append(x)
        return res

    def dfs(funcName, res, variMap, funcFlagMap):
        # res.append(variMap[funcName])

        for adj_name in variMap[funcName]:
            if funcFlagMap[adj_name["fName"]] == 0:
                funcFlagMap[adj_name["fName"]] = 1
                res.append(adj_name)
                # res = listSet(res)
                dfs(adj_name["fName"], res, variMap, funcFlagMap)

    ress = []
    for func in funcFlagMap.keys():
        res = []
        if (funcFlagMap[func] == 0):
            flag = 0
            dfs(func, res, variMap, funcFlagMap)
            if (res.__len__() != 0):
                # res = list(set(res))
                res = listSet(res)
                ress.append(res)
                # print("xxx",res)
            else:
                res = [{'fName': func, 'vari': []}]
                ress.append(res)
                # print(res)
    return ress
    print(ress)
