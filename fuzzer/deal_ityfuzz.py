import json
import os
import shutil
from agent.tools.GPT2Seed import getTransactionFromBigData
from agent.tools.GPT2Seed import getNameFromLeftPara
from agent.tools.GPT2Seed import setParams


def deal_ityfuzz_fuzzer(data,
                        datasetName,
                        filename):
    work_dir = "/home/test/tools/GPT_smartian"
    dataset_dir = os.path.join(work_dir, datasetName)
    abi_dir = os.path.join(dataset_dir, "abi")
    abi_file = filename.replace(".sol", ".abi")
    abi_path = os.path.join(abi_dir, abi_file)
    bin_dir = os.path.join(dataset_dir, "bin")
    bin_file = filename.replace(".sol", ".bin")
    bin_path = os.path.join(bin_dir, bin_file)
    filename_tag = filename.replace(".sol", "")
    dataset_path = os.path.join(work_dir, filename_tag)
    os.mkdir(dataset_path)
    shutil.copy(abi_path, dataset_path)
    shutil.copy(bin_path, dataset_path)
    normalFuncsDir = os.path.join(dataset_dir, "normalFuncs")
    normalFuncsFile = filename_tag + "_normalFuncs.txt"
    normalFuncs_path = os.path.join(normalFuncsDir, normalFuncsFile)
    with open(normalFuncs_path) as file:
        content = file.read()
        standard = json.loads(content)

    for obj in data:
        sequence_str = ""
        for sequence in obj["sequences"]:
            functionName = getNameFromLeftPara(sequence["functionName"])
            sequence_str += functionName + ":"
            std = getTransactionFromBigData(standard, functionName)
            types = []
            for param in std["FuncSpec"]["ArgSpecs"]:
                typeStr = param["TypeStr"]
                types.append(typeStr)
            params = setParams(functionName, std)
            for i in range(types.__len__()):
                if types[i] == "address":
                    params[i] = "0x" + params[i]
                sequence_str += types[i]
                sequence_str += ":"
                sequence_str += params[i]
                if(i != types.__len__() -1):
                    sequence_str += ","
                sequence_str += "\n"
            sequence_str += "\n"

