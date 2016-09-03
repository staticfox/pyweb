import pysrvx.srvx

from flask import g

def get_services(app):
    if not hasattr(g, 'services'):
        g.services = Services(app.config['GS_CONF']['qserver'])
    return g.services

class Services:
    def __init__(self, config):
        self.config = config
        self.srvx = None
        self.get_srvx()
        if self.srvx is None:
            raise Exception("Unable to connect to QServer")

        self.authserv = pysrvx.AuthServ(self.srvx)
        self.chanserv = pysrvx.ChanServ(self.srvx)

    def test_srvx(self):
        try:
            self.authserv.status()
        except (pysrvx.srvx.ConnectionError, pysrvx.srvx.NotConnected):
            self.get_srvx()

    def check_login(self, account, password):
        res = self.authserv.checkpass(account, password)
        return res

    def get_srvx(self):
        c = self.config

        try:
            self.srvx = pysrvx.SrvX(c['host'],
                c['port'], c['passsword'],
                c['authserv_username'],
                c['authserv_password'],
                c['bind'])
        except pysrvx.srvx.AuthenticationError as e:
            print("Unable to connect to SrvX {}".format(e))
        except pysrvx.srvx.ConnectionError as e:
            print("No SrvX connection found {}".format(e))
