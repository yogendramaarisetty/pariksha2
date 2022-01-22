from challenge.compile_run_entities import Language, RequestType
from . import compile_run_helper as crh
from .compile_run_entities import CompileRunRequest, Extension
from .compile_run_entities import CompileRunResponse
import subprocess,os 
from subprocess import run, PIPE,STDOUT,Popen
from celery import shared_task
from .models import *

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def compile_run(request,progress_recorder):
    
    response = CompileRunResponse(request.language,request.code)
    file_name = f'{str(request.guid)}.{Extension(request.language.name).value}'
    
    try:
        #creating code files path
        code_files_path = os.path.join(BASE_DIR,"code_files")
        crh.create_folder(code_files_path)

        #creating guid folder path
        guid_folder_path = os.path.join(BASE_DIR,"code_files",f'{request.language.name}_files',str(request.guid))
        crh.create_folder(guid_folder_path)   
        
        #Task progress recorder
        progress_recorder.set_progress(20, 100, description='created directories')
        
        #Writing the file
        file_name_with_path = os.path.join(guid_folder_path,file_name)
        crh.write_code_file(file_name_with_path,request.code)
        
        #Task progress recorder
        progress_recorder.set_progress(40, 100, description='code written into file successfully')
        
        #compile the Code
        response = crh.compile_code(language =request.language,fileName =file_name,workingDirectory=guid_folder_path,response= response)
        
        #Task progress recorder
        progress_recorder.set_progress(70, 100, description='code compiled')
        
        #Run code if compilation is successful
        if response.compile_success == True:
            crh.run_code(language =request.language,fileName =file_name,workingDirectory=guid_folder_path,stdin=request.stdin,response= response)
            
            #Task progress recorder
            progress_recorder.set_progress(70, 100, description='code ran.')
        return response
    except Exception as e:
        response.status['message'] = "Code failed to run."
        response.error["type"] = "Unknown Exception occured while running the code."
        response.std_output = str(e)
        return response

def candidate_question_compile_run(request,progress_recorder):
    cid = request['candidate_id']
    qid = request['question_id']
    chid = request['challenge_id']
    is_completed = CandidateChallenge.objects.filter(candidate = cid).filter(challenge = cid).first()
    if is_completed:
        return {'message':"Your test is completed"}
    else:
        rtype = RequestType(request['type'])
        cr_request_obj = CompileRunRequest(
                            Language[request['language']],
                            request['code'],
                            request['is_custom_input'],
                            request['stdin'],
                            uuid.UUID(request['guid'])
                        )

        try:
            final_response = {}
            if rtype == RequestType.custom_input:
                response = compile_run(cr_request_obj,progress_recorder)
                final_response = response
            elif rtype == RequestType.run:
                sample_testcases = TestCase.objects.filter(sample = True)
                response = []
                for testcase in sample_testcases:
                    cr_request_obj.stdin = crh.getTestCaseInput(testcase)
                    r = compile_run(cr_request_obj,progress_recorder)
                    response.append(r)
                response = crh.validte_testcases(testcase,response)
                final_response = response
            elif rtype == RequestType.submit:
                all_testcases = TestCase.objects.all()
                response = []
                for testcase in all_testcases:
                    cr_request_obj.stdin = crh.getTestCaseInput(testcase)
                    r = compile_run(cr_request_obj,progress_recorder)
                    response.append(r)
                response = crh.validte_testcases(testcase,response)
                #Todo save task id as well in submission
                final_response = crh.save_submission(testcase,response,request)
            return final_response
        except Exception as e:
            return {'message':"Unknown exception has occured",'error':str(e)}






