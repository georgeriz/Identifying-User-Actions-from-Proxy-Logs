from myLogEntry import LogEntry
from os import listdir

# CONSTANTS
CHROME = 0 # 1 for Chrome, 0 for Firefox
ONLY_HTTP = True # true for no-connections
# this folder contains the client log files
# as captured by the browser extension
Logs = "C:/Users/George/Desktop/Logs/"

def ignore(log_entry):
    if log_entry.is_response() or log_entry.is_action():
        return True
    if ONLY_HTTP and log_entry.get_scheme() == "https":
        return True
    return False

def _make_client_action_bag(client_log, counterDict, counter):
    with open(client_log) as f:
        try:
            for line in f:
                log_entry = LogEntry(line)
                if not ignore(log_entry):
                    if log_entry.counter != None:
                        action_id = log_entry.counter + counter + CHROME
                    else:
                        action_id = 0
                    counterDict.setdefault(action_id, []).append(log_entry)
        except Exception:
            print "file:", client_log, "line:", line
            raise
    return sorted(counterDict.keys())[-1]

def make_client_action_bag():
    path = Logs
    counter = 0
    counterDict = {}
    logs = listdir(path)
    for log in logs:
        counter = _make_client_action_bag(path + log, counterDict, counter)
    return counterDict

def create_client_actions(filename, a_dict):
    with open(filename, 'w') as f:
        for k in a_dict:
            if k != 0:
                text = ""
                if not ONLY_HTTP:
                    text += str(a_dict[k][0].get_request_time()) + " "
                text += str(a_dict[k][0]) + '\n'
                f.write(text)

def main():
    counterDict = make_client_action_bag()
    create_client_actions("client_actions.txt", counterDict)

if __name__ == '__main__':
    main()