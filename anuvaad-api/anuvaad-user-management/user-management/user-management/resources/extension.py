from flask_restful import Resource
from repositories import ExtensionRepositories
from models import CustomResponse, Status
from utilities import MODULE_CONTEXT
from anuvaad_auditor.loghandler import log_info, log_exception
from flask import request
from anuvaad_auditor.errorhandler import post_error
import config

exRepo    =   ExtensionRepositories()

class GenerateIdToken(Resource):

    def post(self):
        body = request.get_json()
        if 'requestID' not in body or not body['requestID']:
            return post_error("Data Missing", "requestID not found", None), 400

        request_id = body["requestID"]

        log_info(f"token request for requestID : {request_id}, from web extension", MODULE_CONTEXT)  
        try:
            result = exRepo.register_request(request_id)
            if "errorID" in result:
                log_info(f"token request for {request_id} failed | {result}", MODULE_CONTEXT)
                return result, 400   
            else:
                res = CustomResponse(Status.SUCCESS.value, result)
                log_info(f"token request for {request_id} successful", MODULE_CONTEXT)
                return res.getresjson(), 200
        except Exception as e:
            log_exception("Exception while token request for web extension user: " +
                          str(e), MODULE_CONTEXT, e)
            return post_error("Exception occurred", "Exception while token request for web extension user:{}".format(str(e)), None), 400