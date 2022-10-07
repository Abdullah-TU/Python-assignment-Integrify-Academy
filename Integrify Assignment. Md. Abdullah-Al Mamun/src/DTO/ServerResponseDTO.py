# Method creates one response of whole api here.
# status =  1 means request is successfull.
# msg is if user have to send msg to user.
# data if any data is need to be send to user.
def get_server_response(status=1 , msg="" , data=[]):
    return {"status":status , "msg":msg , "data":data}