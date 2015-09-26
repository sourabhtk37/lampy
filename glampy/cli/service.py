import subprocess


class Service(object):
    def __init__(self):
        pass

    @staticmethod
    def control(service, command, prefix=""):
        system = 'systemctl'
        p = subprocess.Popen(" ".join([prefix, system, command, service]), stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        return out

    @staticmethod
    def status(service):
        status = Service.control(service, 'status')
        if "Loaded: loaded" not in status:
            return False
        if "Active: inactive" in status:
            return False
        if "Active: active" in status:
            return True

    @staticmethod
    def start(service):
        return Service.control(service, 'start', 'gksu')

    @staticmethod
    def stop(service):
        return Service.control(service, 'start', 'gksu')

    @staticmethod
    def toggle(service):
        pass
