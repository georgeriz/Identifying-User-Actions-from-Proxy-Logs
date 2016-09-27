import urlparse

#CLASSES
class LogEntry:
    def __init__(self, entry, proxy=False):
        try:
            items = entry.split()
            if not proxy:
                self.timestamp = int(items[0])
                self.type = items[1]
                self.url = items[2]
                # handle lines without counter
                if self.is_action() or items[3] == "N":
                    self.counter = None
                else:
                    self.counter = int(items[3])
            else:
                # check if the proxy log has info about connections
                connectionsON = False
                if len(items) == 15:
                    connectionsON = True
                #
                self.original_resp_t = items[0]
                self.original_duration = items[1]
                resp_t = int(float(items[0])*1000)
                self.timestamp = resp_t - int(items[1])
                self.resp_t = resp_t
                self.type = "P"
                self.method = items[3]
                if self.method == "CONNECT" and not items[4].startswith("http"):
                    foo = items[4].split(":")
                    self.url = "https://" + foo[0]
                    if connectionsON:
                        self.dest_port = foo[1]
                else:
                    self.url = items[4]
                    if connectionsON:
                        self.dest_port = items[14]
                self.counter = None
                self.referer = items[5]
                self.length = items[6]
                self.content_type = items[8]
                if connectionsON:
                    self.source_port = items[9]
                    self.proxy_IP = items [10] # always 127.0.0.1
                    self.proxy_port = items[11] # always 3128 (squid)
                    self.dest_IP = items[12]
                    self.local_IP = items [13] # always "-"
        except Exception:
            print "LogEntryException:", entry
            raise

    def __repr__(self):
        return self.url

    def is_request(self):
        if self.type == "Q":
            return True
        return False

    def is_response(self):
        if self.type == "R":
            return True
        return False

    def get_hostname(self):
        foo = urlparse.urlsplit(self.url)
        return foo.hostname

    def get_scheme(self):
        foo = urlparse.urlsplit(self.url)
        return foo.scheme

    def is_action(self):
        action_ids = ["T", "C", "M", "L", "X", "H", "B", "F", "U", "P"]
        if self.type in action_ids:
            return True
        return False

    def is_N(self):
        if self.counter == None:
            return True
        return False

    def get_counter(self):
        return self.counter

    def get_length(self):
        if self.length == "-":
            return -1
        return int(self.length)

    def get_referer(self):
        if self.referer == "-":
            return None
        return self.referer

    def get_request_time(self):
        return self.timestamp

    def get_response_time(self):
        return self.resp_t

    def get_path(self):
        foo = urlparse.urlsplit(self.url)
        goo = foo.scheme+"://"+foo.hostname+foo.path
        return goo
