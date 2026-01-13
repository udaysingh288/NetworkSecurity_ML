import sys
from networksecurity.logging import logger
class NetworkSecurityException(Exception):
    def __init__(self,error_message,error_detais:sys):
        self.error_message= error_message
        _,_,exc_tb = error_detais.exc_info()

        self.lineno=exc_tb.tb_lineno
        self.filename= exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return f"Error occured in script: {self.filename} at line number: {self.lineno} with message: {self.error_message}"
    
# if __name__=="__main__":
#     try:
#         logger.logging.info("Testing NetworkSecurityException")
#         a=1/0
#     except Exception as e:
#         raise NetworkSecurityException(e,sys)