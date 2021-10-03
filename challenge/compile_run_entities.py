import enum,platform,json
os_env = platform.system()

class CompileRunRequest:
    def __init__(self,language,code,custom_input,stdin,guid):
        self.language = language
        self.code = code
        self.stdin = stdin
        self.is_custom_input = custom_input
        self.guid = guid
    def toJSON(self):
        return json.dumps(self, default=lambda o: o._asdict, 
            sort_keys=True, indent=4)
    
class CompileRunResponse:
    def __init__(self,language,code):
        self.language = language
        self.code = code
        self.status = { 'status':None, 'message':None}
        self.std_input = None
        self.std_output = None
        self.expected_output = None
        self.compile_success = None
        self.run_success = None
        self.error = {'type':None,'stderr':None}
        self.time = None
        self.return_code = None
        
    def toJSON(self):
        return json.dumps(self, default=lambda o: o._asdict, 
        sort_keys=True, indent=4)

class Language(str,enum.Enum):
    c = 101
    cpp = 102
    java = 103
    python = 104

class Extension(enum.Enum):
    c = "c"
    cpp = "cpp"
    java = "java"
    python = "py" if os_env == "Windows" else "python"

class Status(enum.Enum):
    accepted = 1
    wrong_output = 2
    hidden_testcase = 3
    compile_success = 4
    run_success = 5
    compile_failed = 6
    run_failed = 7


class ErrorType(enum.Enum):
    run_time_error = 401
    compile_time_error = 501
    time_limit_exceeded = 601
    syntax_error = 701 # for python error code