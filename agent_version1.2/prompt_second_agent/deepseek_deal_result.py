import json
from deepseek_findblock_reachif import chatWithDeespseek

def deal_decode_error(messages):

    with open("prompt_check_decodeError_result.txt") as file:
        prompt = file.read()
    resStudent = chatWithDeespseek(prompt, messages)
    return resStudent

