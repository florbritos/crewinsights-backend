import os
import tornado.web
import tornado.ioloop
from api.endpoints.report_handlers import ReportRequestHandler
from api.endpoints.account_handlers import AccountRequestHandler
from api.endpoints.crewbot_handlers import CrewBotRequestHandler
from api.endpoints.dashboard_handlers import DashboardRequestHandler
from api.endpoints.searchbot_handlers import SearchBotRequestHandler
from api.endpoints.users_handlers import UsersRequestHandler
from api.endpoints.password_recovery_handlers import PasswordRecoveryRequestHandler

class CrewInsightsServer():
    def __init__(self):
        self.app =  tornado.web.Application([
            (r"/api/account/session", AccountRequestHandler),
            (r"/api/password-recovery", PasswordRecoveryRequestHandler),
            (r"/api/crewbot/(.*)", CrewBotRequestHandler),
            (r"/api/crewbot/user/([0-9a-fA-F]{24})", CrewBotRequestHandler),
            (r"/api/crewbot/user/([0-9a-fA-F]{24})/chat/([0-9a-fA-F]{24})", CrewBotRequestHandler),
            (r"/api/flight-report", ReportRequestHandler),
            (r"/api/dashboard/user/([0-9a-fA-F]{24})", DashboardRequestHandler),
            (r"/api/searchbot", SearchBotRequestHandler),
            (r"/api/users", UsersRequestHandler),
            (r"/api/users/([0-9a-fA-F]{24})", UsersRequestHandler),
        ])
    
    def listen(self, port):
        self.app.listen(port)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    server = CrewInsightsServer()
    server.listen(port)
    print(f"CrewInsights Server running on port {port}")
    tornado.ioloop.IOLoop.current().start()