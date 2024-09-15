import tornado.web
import tornado.ioloop
from api.endpoints.report_handlers import ReportRequestHandler
from api.endpoints.account_handlers import AccountRequestHandler

class CrewInsightsServer():
    def __init__(self):
        self.app =  tornado.web.Application([
            (r"/api/flight-report", ReportRequestHandler),
            (r"/api/account/session", AccountRequestHandler),
        ])
    
    def listen(self, port):
        self.app.listen(port)

if __name__ == "__main__":
    server = CrewInsightsServer()
    server.listen(8888)
    print("CrewInsights Server http://localhost:8888/")
    tornado.ioloop.IOLoop.current().start()