import json
import os
import subprocess

from agent.second_agent.deepseek_deal_result import deal_decode_error
from agent.tools.GPT2Seed import GPT2SmartianSeed


def deal_smartian_fuzzer(data,filename,tmpDir,mainContract,datasetName,outputDir,timeLimit,messages):

        GPT2SmartianSeed(data, filename, tmpDir, mainContract)
        seedDir = os.path.join(tmpDir, "new_seed2")
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


