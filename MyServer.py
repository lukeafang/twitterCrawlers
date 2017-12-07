import http.server
import crawler
from pathlib import Path
from _codecs import encode
import codecs


class MyServer(http.server.BaseHTTPRequestHandler):
    def returnResponse(self,responseCode=200,responseMes='',paramStr=''):
        #success
        if responseCode==200: 
            #convert str to string
            if not isinstance(paramStr, str):
                paramStr=str(paramStr)
            paramStr=codecs.encode(paramStr)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(bytes(paramStr))
            self.wfile.flush() 
        else:
            self.send_error(responseCode, responseMes)


    
    #return html
    def returnResource(self,url):
        index=url.rfind('/')
        
        p=Path("../web"+url[index:])
        file=open(p)
        resourceStr=file.read()
        self.returnResponse(paramStr=resourceStr)
        
    
    #check urlpath requests a resource file or not
    @staticmethod    
    def isResource(self,urlPath):    
        resouceTypes=['.html','.js','.css']
        for resourceType in resouceTypes:
            if resourceType in urlPath:
                return True
        return False
        
    #get request
    def do_GET(self):
        #parse paramters in url
        
        
        urlPath=self.path
        #request html files
        if MyServer.isResource(self, urlPath):
            self.returnResource(urlPath)
            return
        if '?' in urlPath:
            paramsMap=dict();
            params=urlPath.split('?')[1]
            
            for param in params.split('&'):
                key=param.split('=')[0]
                value=param.split('=')[1]
                
                paramsMap[key]=value
            print(paramsMap)    
            #check params
            if not self.validate(paramsMap):
                self.returnResponse(400, 'Please ensure correct action transfered')
                return 
            
            action=Action()
            try: 
                actionMethod=getattr(action, paramsMap['action'])
              
            except AttributeError:
                print('method:'+paramsMap['action']+" is not exist")
                self.returnResponse(400, 'method:'+paramsMap['action']+" is not exist")
                return 
            else:
                responseJson=actionMethod(paramsMap)
                self.returnResponse(paramStr=responseJson)
                
    #send response result as json 
    
    
    
                
    #validate paramsMap contains action or not
    def validate(self,paramsMap):
        if not isinstance(paramsMap, dict):
            return False   
        if 'action' not in paramsMap:
            return False
        actionVale=paramsMap['action']    
        if  actionVale.replace(' ','')=='':
            return False
        return True   
    
#Action is to excute specific method to call crawler
class Action():
    def __init__(self):
        self.crawler=crawler.TweetCrawler()
    #?action=getUserInfo&userId=xxxxxx
    def getUserInfo(self,params):    
        print("This is getUserInfo")
        userId=params['userId']
        print(self.crawler.get_userProfile(userId)._json)
        return self.crawler.get_userProfile(userId)._json
        
        
if __name__ == '__main__':
    http_server=http.server.HTTPServer(('',8080),MyServer)
    http_server.serve_forever()
#     p=Path("../web/index.html")
#     file=open(p, "r", 1024)
#     str=file.read()
#     print(str)
    
    
    