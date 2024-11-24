import tornado.web
import tornado.ioloop
from api.endpoints.report_handlers import ReportRequestHandler
from api.endpoints.account_handlers import AccountRequestHandler
from api.endpoints.crewbot_handlers import CrewBotRequestHandler
from api.endpoints.dashboard_handlers import DashboardRequestHandler
from api.endpoints.searchbot_handlers import SearchBotRequestHandler
from os import system

class CrewInsightsServer():
    def __init__(self):
        self.app =  tornado.web.Application([
            (r"/api/account/session", AccountRequestHandler),
            (r"/api/crewbot/(.*)", CrewBotRequestHandler),
            (r"/api/crewbot/user/([0-9a-fA-F]{24})", CrewBotRequestHandler),
            (r"/api/crewbot/user/([0-9a-fA-F]{24})/chat/([0-9a-fA-F]{24})", CrewBotRequestHandler),
            (r"/api/flight-report", ReportRequestHandler),
            (r"/api/dashboard/user/([0-9a-fA-F]{24})", DashboardRequestHandler),
            (r"/api/searchbot", SearchBotRequestHandler),
        ])
    
    def listen(self, port):
        self.app.listen(port)

if __name__ == "__main__":
    server = CrewInsightsServer()
    server.listen(8888)
    system("cls")
    print("CrewInsights Server http://192.168.0.19:8888/")
    tornado.ioloop.IOLoop.current().start()