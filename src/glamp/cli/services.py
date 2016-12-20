import os
import subprocess
from gi.repository import GObject, Polkit, Gio


class Service(object):
    def __init__(self):
        pass

    def control(self, service, argument, prefix=""):
        p = subprocess.Popen(" ".join([prefix, 'service', service, argument]), stdout=subprocess.PIPE, shell=True)
        out, err = p.communicate()
        return out

    def status(self, service):
        status = self.control(service, 'status', 'pkexec')
        if "Loaded: loaded" not in status:
            return False
        if "Active: inactive" in status:
            return False
        if "Active: active" in status:
            return True

    def start(self, service):
        return Service.control(service, 'start', 'pkexec')

    def stop(self, service):
        return Service.control(service, 'start', 'pkexec')

    def toggle(self, service):
        pass


# @todo
class Auth(object):
    def __init__(self):
        self.action_id = "org.freedesktop.policykit.exec"
        self.mainloop = GObject.MainLoop()
        self.authority = Polkit.Authority.get()
        self.cancellable = Gio.Cancellable()
        self.subject = Polkit.UnixProcess.new(os.getppid())

        # lockbutton = Gtk.LockButton()
        # lockbutton.connect("clicked", self.check_authorization)

        self.check_authorization()
        self.mainloop.run()

    def check_authorization(self):
        self.authority.check_authorization(self.subject, self.action_id, None,
                                           Polkit.CheckAuthorizationFlags.ALLOW_USER_INTERACTION, self.cancellable,
                                           self.check_authorization_cb, self.mainloop)

    def check_authorization_cb(self, authority, res, loop):
        try:
            result = authority.check_authorization_finish(res)
            if result.get_is_authorized():
                print("Authorized")
            elif result.get_is_challenge():
                print("Challenge")
            else:
                print("Not authorized")
        except GObject.GError as error:
            print("Error checking authorization: %s" % error.message)
