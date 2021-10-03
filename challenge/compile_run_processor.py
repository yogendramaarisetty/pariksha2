from challenge.compile_run_entities import Language
from . import compile_run_helper as crh
from .compile_run_entities import Extension
from .compile_run_entities import CompileRunResponse
import subprocess,os 
from subprocess import run, PIPE,STDOUT,Popen
from celery import shared_task

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def candidate_compile_run(request,progress_recorder):
    file_name = f'{str(request.guid)}.{Extension(request.language.name).value}'
    
    code_files_path = os.path.join(BASE_DIR,"code_files")
    crh.create_folder(code_files_path)

    candidate_folder_path = os.path.join(BASE_DIR,"code_files",f'{request.language.name}_files',str(request.guid))
    crh.create_folder(candidate_folder_path)   
    progress_recorder.set_progress(20, 100, description='created directories')
    
    file_name_with_path = os.path.join(candidate_folder_path,file_name)
    crh.write_code_file(file_name_with_path,request.code)
    progress_recorder.set_progress(40, 100, description='code written into file successfully')
    
    response = CompileRunResponse(request.language,request.code)
    response = crh.compile_code(language =request.language,fileName =file_name,workingDirectory=candidate_folder_path,response= response)
    progress_recorder.set_progress(70, 100, description='code compiled')
    
    if response.compile_success == True:
        crh.run_code(language =request.language,fileName =file_name,workingDirectory=candidate_folder_path,stdin=request.stdin,response= response)
        progress_recorder.set_progress(70, 100, description='code ran.')
    
    return response

    
