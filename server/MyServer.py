import http.server
import crawler
from pathlib import Path
import codecs
import json
from socketserver import ThreadingMixIn
from http.server import HTTPServer


class MyServer(http.server.BaseHTTPRequestHandler):
    #initialize server  
    def __init__(self, request, client_address, server):
       
        
#         http.server.BaseHTTPRequestHandler.__init__(self,request, client_address, server)
        super(MyServer,self).__init__(request, client_address, server)
    def returnData(self,responseCode=200,responseMes="",paramStr="",resourceType="html"):
        paramStr=json.dumps(paramStr)
        print("*****"+paramStr) 
        self.returnResponse(responseCode, responseMes, paramStr, resourceType)
        
    
    def returnResponse(self,responseCode=200,responseMes="",paramStr="",resourceType="html"):
        #success
        if responseCode==200: 
            #convert str to string
            if not isinstance(paramStr, str):
                paramStr=str(paramStr)
           
             
            paramStr=codecs.encode(paramStr)

            self.send_response(200)
            self.send_header("Content-type", "text/"+resourceType)
            self.end_headers()
            self.wfile.write(bytes(paramStr))
            self.wfile.flush() 
        else:
            self.send_error(responseCode, responseMes)


    
    #return 
    def returnResource(self,url,resourceType):
        index=url.rfind('/')
        
        p=Path("../web"+url[index:])
        try:
            file=open(p)
            resourceStr=file.read()
        except:
            self.returnResponse(404)
        self.returnResponse(paramStr=resourceStr,resourceType=resourceType)
        
    
    #check urlpath requests a resource file or not
    @staticmethod    
    def isResource(self,urlPath):    
        resourceTypes=['.html','.js','.css','.png','.jpeg']
        for resourceType in resourceTypes:
            if resourceType in urlPath:
                if resourceType=='.html' or resourceType=='.js':
                    return 'html'
                else:
                    return resourceType[1:]
                
        return None
    
    def procecssReq(self,urlPath):
        
        #check resource
        resourceType=MyServer.isResource(self, urlPath)
        
        if resourceType is not None:#request resource files
            self.returnResource(urlPath,resourceType)
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
                print("ParamsMap is "+str(paramsMap))
                responseJson=actionMethod(paramsMap)
                self.returnData(paramStr=responseJson)
                
    #send response result as json 
        
    #get request
    def do_GET(self):
        self.procecssReq(self.path)
        
        
                
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
    #search user's profile with user's id
    def getUserInfo(self,params):    
        print("This is getUserInfo")
        userId=params['userId']
        #print(self.crawler.get_userProfile(userId)._json)
        result=self.crawler.get_userProfile(userId)
        print("****"+str(result))
        return result
    #search tweets with keyword
    def searchByKey(self, params):
        result=self.crawler.search_tweetsbyKeyword(params['keyword'], params['count'])
        
       
        return result
    #search tweets with location info
    def searchByLocation(self,params):
        longit=params['logit']
        lat=params['lat']
        range=params['range']
        result=self.crawler.search_tweetsbyRegion(longit, lat, range, 50)
        return result
#no block support            
class MyThreadedServer(ThreadingMixIn,HTTPServer):  
    pass      
if __name__ == '__main__':
    http_server=MyThreadedServer(('',8080),MyServer)
    http_server.serve_forever()

    
    
    