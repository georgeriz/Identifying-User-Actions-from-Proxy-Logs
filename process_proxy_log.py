from myLogEntry import LogEntry

# CONSTANTS
ONLY_HTTP = True # true for no-connections
# this is the file that contains the proxy log
proxy_log = "example.txt"
# this is the file that will contain the processed proxy log
# (it used to be called alternative.txt)
processed_proxy_log = "processed_proxy_log.txt"

# PROXY
def make_proxy_list(proxy_log):
    aList = []
    connections = {}
    with open(proxy_log) as f:
        if ONLY_HTTP:
            for line in f:
                log_entry = LogEntry(line, True)
                if log_entry.method != "CONNECT":
                    aList.append(log_entry)
        else:
            for line in f:
                log_entry = LogEntry(line, True)
                if log_entry.dest_IP != "-":
                    connection_details = (log_entry.source_port, log_entry.dest_IP)
                    if not (connection_details in connections):
                        connections[connection_details] = log_entry
            for keys in connections:
                aList.append(connections[keys])
    aList = sorted(aList, key = LogEntry.get_request_time)
    return aList

def create_alternative(proxy_list):
    with open(processed_proxy_log, 'w') as f:
        for log_entry in proxy_list:
            text = log_entry.original_resp_t + " "
            text += log_entry.original_duration + " 127 "
            text += log_entry.method + " "
            text += log_entry.url + " "
            text += log_entry.referer + " "
            text += log_entry.length + " - "
            if ONLY_HTTP:
                text += log_entry.content_type + "\n"
            else:
                text += log_entry.content_type + " "
                text += log_entry.source_port + " "
                text += log_entry.dest_IP + "\n"
            f.write(text)

def main():
    proxy_list = make_proxy_list(proxy_log)
    create_alternative(proxy_list)

if __name__ == '__main__':
    main()