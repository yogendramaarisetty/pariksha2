from os import error
from .compile_run_commands import *
from .compile_run_entities import *
import subprocess, traceback,os
os_env = platform.system()
shell_value = False if os_env == "Windows" else True
def compile_code(language,fileName,workingDirectory,response):
    print(fileName,workingDirectory)    
    compile_code = subprocess.run(CompileCommands[language.name].format(fileName),
                                  check=True,encoding='ascii',cwd=workingDirectory,
                                  shell=shell_value, timeout=3,capture_output=True)
    compile_errors = compile_code.stderr
    has_compile_errors = compile_code.returncode == 1 #Popen doesnt give returncode
    if has_compile_errors:
        response.compile_success = False
        response.status['status'] = Status.compile_failed.name
        response.status['message'] = "Code has compilation errors. Please correct the syntax."
        response.error["type"] = ErrorType.compile_time_error.name
        errors = get_error_info(compile_errors,language)
        response.error["stderr"] = errors
    else:
        response.compile_success = True
    return response

def run_code(language,fileName,stdin,workingDirectory,response):
    
    response.status['status'] = Status.run_failed
    response.run_success = False
    response.stdin = stdin
    try:
        run_code = subprocess.run(RunCommands[language.name].format(fileName),
                                  check=True,input=stdin,encoding='ascii',cwd=workingDirectory,
                                  shell=shell_value, timeout=3,capture_output=True)
        response.status['status'] = Status.run_success.name
        response.status['message'] = "Code ran successfully."
        response.run_success = True
        response.return_code = run_code.returncode
        #ToDo write input/output to a file instead of storing it in memoery
        response.stdout  = run_code.stdout

    except subprocess.TimeoutExpired as tle:
        response.status['message'] = "Code failed to run."
        response.error["type"] = ErrorType.time_limit_exceeded.name
        response.std_output = tle.output
        response.error["stderr"] = "timed out after {tle.timeout} seconds"
        response.return_code = tle.returncode
    except subprocess.CalledProcessError as re:
        response.status['message'] = "Code failed to run."
        response.error["type"] = ErrorType.time_limit_exceeded.name
        response.std_output = re.output
        response.error["stderr"] = re.stderr
        response.return_code = re.returncode
    except Exception as e:
        response.status['message'] = "Unknown Exception occured while running the code."
        response.error["stderr"] = traceback.format_exc()
    
    #if there are no compile
       
    return

def write_code_file(fileName,code):
    code_file = open(fileName,'w')
    code_file.flush()
    code_file.write(code)
    code_file.close()

def write_output_file(fileName,stdout):
    pass


def get_error_info(errors,language):
    if language is Language.python:

        pass
        # b'  File "D:\\Projects\\pariksha\\pariksha\\pariksha\\code_files\\python_codes\\1yogi1\\1yogi1.py", line 3\r\n'
        # b'    print(i)\r\n'
        # b'    ^\r\n'
        # b'IndentationError: expected an indented block\r\n'
    elif language is Language.java:
        pass
    elif language is Language.cpp:
        pass

        #[b"filename.cpp: In function 'int main()':\n",
        # b"filrname.cpp:7:18: error: expected ';' before '}' token\n", 
        # b'    7 |     cout<<"kalam"\n', b'      |                  ^\n', 
        # b'      |                  ;\n', b'    8 | }\n', b'      | ~                 \n']
    
    elif language is Language.c:
        pass

    # errors = f''.join(e.decode('utf-8') for e in errors)
    return errors

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path) 

