import tornado.web
import tornado.ioloop
from api.endpoints.report_handlers import ReportRequestHandler
from api.endpoints.account_handlers import AccountRequestHandler
from api.endpoints.crewbot_handlers import CrewBotRequestHandler
from os import system

class CrewInsightsServer():
    def __init__(self):
        self.app =  tornado.web.Application([
            (r"/api/flight-report", ReportRequestHandler),
            (r"/api/account/session", AccountRequestHandler),
            (r"/api/crewbot/(.*)", CrewBotRequestHandler),
        ])
    
    def listen(self, port):
        self.app.listen(port)

if __name__ == "__main__":
    server = CrewInsightsServer()
    server.listen(8888)
    system("cls")
    print("CrewInsights Server http://localhost:8888/")
    tornado.ioloop.IOLoop.current().start()