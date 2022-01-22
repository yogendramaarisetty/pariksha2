from celery import shared_task
from .compile_run_processor import compile_run
from celery_progress.backend import ProgressRecorder
from .compile_run_entities import *
import uuid,json
@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y


@shared_task
def xsum(numbers):
    return sum(numbers)

@shared_task(bind=True)
def compile_run_task(self,request):
    progress_recorder = ProgressRecorder(self)
    cr_request_obj = CompileRunRequest(
                            Language[request['language']],
                            request['code'],
                            request['is_custom_input'],
                            request['stdin'],
                            uuid.UUID(request['guid'])
                        )
    response = compile_run(cr_request_obj,progress_recorder)
    return json.dumps(response.__dict__)

@shared_task(bind=True)
def candidate_question_compile_run_task(self,request,response):
    request["candidate_id"]
    request["question_id"]
    request[""]
    return response
