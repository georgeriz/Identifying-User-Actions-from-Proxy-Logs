from myLogEntry import LogEntry
import myPolicies

# parameters
proxy_log = "C:/Users/George/Desktop/processed_proxy_log.txt"
Previous = 2000 #in ms, should not be deactivated
Next = 20 # in ms, 0 for deactivation
Repetition = 5 # 0 for deactivation
Filter = "-" # "Url" or "Content" or anything else for deactivation
ONLY_HTTP = True # False for connection-based

# input:    txt of proxy log (processed)
# output:   list with lines from the proxy log
def make_proxy_list(proxy_log):
    aList = []
    with open(proxy_log) as f:
        for line in f:
            log_entry = LogEntry(line, True)
            aList.append(log_entry)
    return aList

# input:    list of lines from the proxy log
# output:   dictionary with suggested user actions
#           according to the applied policies
def apply_policies(proxy_list):
    return myPolicies.apply(proxy_list,Previous, Repetition, Next, Filter)

# input:    dictionary of suggested user actions
# output:   txt with suggested user actions
def write_to_file(filename, proxy_actions_dictionary):
    with open(filename, 'w') as f:
        for k in proxy_actions_dictionary:
            text = ""
            if not ONLY_HTTP:
                text += str(proxy_actions_dictionary[k][0].get_request_time()) + " "
            text += str(proxy_actions_dictionary[k][0]) + '\n'
            f.write(text)

def main():
    proxy_list = make_proxy_list(proxy_log)
    proxy_dictionary = apply_policies(proxy_list)
    write_to_file("proxy_actions.txt", proxy_dictionary)

if __name__ == '__main__':
    main()