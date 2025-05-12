import os
import sys
import logging



class TradingException(Exception):
    """Base class for all trading-related exceptions."""
    def __init__(self,error_message,error_deails:sys):
        self.error_message=error_message
        _,_,exc_tb=error_deails.exc_info()

        self.lineno=exc_tb.tb_lineno
        self.filename=exc_tb.tb_frame.f_code.co_filename

    def __str__(self):
        return "Error occured in python script name [{0}] line number [{1}] error message [{2}]".format(
            self.filename,self.lineno,str(self.error_message)
        )


if __name__=="__main__":
    try:
        a=1/0
        print("This will not be printed",a)
    except Exception as e:
        logging.info("Divide by zero error")
        raise TradingException(e,sys) from e