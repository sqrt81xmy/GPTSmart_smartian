import os

def read_err_file():
    file_path = "error1.txt"
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

res = read_err_file()
tmpDir = "B3"
datasetName = "B3"
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

for filename in res:
    filenameTag = filename.replace(".sol", "")
    mainContract = mainContract_map[filenameTag]
    with open("B3.list","a") as file:
        file.writelines(filenameTag+","+mainContract+"\n")

