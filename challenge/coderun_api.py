import requests,json,time
import base64



def coderun_api(code,language,input,timeout,expected_output):
    url = "https://judge0.p.rapidapi.com/submissions"
    headers = {
        'x-rapidapi-host': "judge0.p.rapidapi.com",
        'x-rapidapi-key': "cf4305d31bmsh82518687544739ep179fd2jsnf6d65d6ee270",
        'content-type': "application/json",
        'accept': "application/json"
        }
    querystring = {"base64_encoded":"true"}
    data = {
        "language_id" : language.id,
        "source_code": code,
        "stdin":"",
        "expected_output":"Sum of x+y = 35\n",
        "cpu_time_limit": 3
    }
    print (data)
    response = requests.post( url, data=json.dumps(data), headers=headers)
    token_url = url+"/"+json.loads(response.text)["token"]
    t=0.5
    response = requests.get(token_url, headers=headers, params=querystring)
    status  = json.loads(response.text)["status"]["description"]
    while status == "In Queue" or status ==  "Processing":
        time.sleep(t)
        response = requests.get(token_url, headers=headers, params=querystring)
        if "status" in json.loads(response.text):
            status = json.loads(response.text)["status"]["description"]
        else:
            break
        print(status)
        t+=0.2
    print("n\n\n\nn",response.text)
    res_dict = encode_response(json.loads(response.text),status)
    print(res_dict,"\n\n\n\n")
    return json.dumps(res_dict)

def encode_response(res_dict,status):
    if status== "Compilation Error":
        res_dict["compile_output"] = base64.b64decode(res_dict["compile_output"]).decode('utf-8')
    elif status == "Accepted" or status == "Wrong Answer":
        res_dict["stdout"] = base64.b64decode(res_dict["stdout"]).decode('utf-8')
    elif status == "Time Limit Exceeded":
        res_dict["message"] = base64.b64decode(res_dict["message"]).decode('utf-8')
    elif "Runtime Error" in status:
        res_dict["message"] = base64.b64decode(res_dict["message"]).decode('utf-8')
        res_dict["stderr"] = base64.b64decode(res_dict["stderr"]).decode('utf-8')
    return res_dict
    