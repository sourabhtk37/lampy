import subprocess


class Service(object):
    def __init__(self):
        self.system = 'systemctl'

    def control(self, service, argument, prefix=""):
        command = {
            'systemctl': [prefix, self.system, argument, service],
            'service': [prefix, self.system, service, argument]
        }
        p = subprocess.Popen(" ".join(command[self.system]), stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        return out

    def status(self, service):
        status = Service.control(service, 'status')
        if "Loaded: loaded" not in status:
            return False
        if "Active: inactive" in status:
            return False
        if "Active: active" in status:
            return True

    def start(self, service):
        return Service.control(service, 'start', 'gksu')

    def stop(self, service):
        return Service.control(service, 'start', 'gksu')

    def toggle(self, service):
        pass
