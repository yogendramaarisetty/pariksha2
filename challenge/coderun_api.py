import requests, json, time
import base64
from .models import TestCase,JudgeApiKey
from pariksha.settings import *

current_env = JudgeApiKey.objects.filter(active=True).first()
def coderun_api(code, language, input, expected_output, timeout):
    print(current_env.key,current_env.name)
    url = "https://judge0.p.rapidapi.com/submissions"
    headers = {
        'x-rapidapi-host': "judge0.p.rapidapi.com",
        'x-rapidapi-key': current_env.key,
        'content-type': "application/json",
        'accept': "application/json"
    }
    querystring = {"base64_encoded": "true"}
    data = {
        "language_id": language.id,
        "source_code": code,
        "stdin": input,
        "expected_output": expected_output,
        "cpu_time_limit": timeout
    }
    # print(data)
    response = requests.post(url, data=json.dumps(data), headers=headers)
    token_url = url + "/" + json.loads(response.text)["token"]
    t = 0.5
    response = requests.get(token_url, headers=headers, params=querystring)
    status = json.loads(response.text)["status"]["description"]
    while status == "In Queue" or status == "Processing":
        time.sleep(t)
        response = requests.get(token_url, headers=headers, params=querystring)
        if "status" in json.loads(response.text):
            status = json.loads(response.text)["status"]["description"]
        else:
            break
        print(status)
        t += 0.2
    print("n\n\n\nn", response.text)
    res_dict = encode_response(json.loads(response.text), status)
    # print(res_dict, "\n\n\n\n")
    return res_dict


def encode_response(res_dict, status):
    print(res_dict)
    res_dict["class"] = "WRONG"
    if status == "Compilation Error":
        if res_dict["compile_output"] is not None:
            res_dict["compile_output"] = res_dict["msg"] = base64.b64decode(res_dict["compile_output"]).decode('utf-8')
            res_dict["class"] = "CE"
    elif status == "Accepted":
        if res_dict["stdout"] is not None:
            res_dict["stdout"] = res_dict["msg"] = base64.b64decode(res_dict["stdout"]).decode('utf-8')
            res_dict["class"] = "SUCCESS"
    elif status == "Wrong Answer":
        if res_dict["stdout"] is not None:
            res_dict["stdout"] = res_dict["msg"] = base64.b64decode(res_dict["stdout"]).decode('utf-8')
            res_dict["class"] = "WRONG"
    elif status == "Time Limit Exceeded":
        if res_dict["message"] is not None and res_dict["stdout"] is not None:
            res_dict["message"] = base64.b64decode(res_dict["message"]).decode('utf-8')
            res_dict["stdout"] = res_dict["msg"] = base64.b64decode(res_dict["stdout"]).decode('utf-8')
            res_dict["msg"] += f'\n{res_dict["message"]}'
            res_dict["class"] = "TLE"
    elif "Runtime Error" in status:
        if res_dict["message"] is not None and res_dict["stderr"] is not None:
            res_dict["message"] = base64.b64decode(res_dict["message"]).decode('utf-8')
            res_dict["stderr"] = res_dict["msg"] = base64.b64decode(res_dict["stderr"]).decode('utf-8')
            res_dict["msg"] += f'\n{res_dict["message"]}'
            res_dict["class"] = "RE"
    return res_dict


def run_sample(code, language, question):
    sample_testcases = TestCase.objects.filter(question=question).filter(sample=True)
    print(sample_testcases)
    result = []
    for st in sample_testcases:
        response = coderun_api(code, language, st.tinput, st.toutput, st.timeout)
        response["testcase"] = st.hint
        response["expected"] = st.toutput
        response["input"] = st.tinput
        result.append(response)
        if response["status"]["description"] != "Accepted":
            return result
    return result
