import make_client_actions
import process_proxy_log
import make_proxy_actions
import count_match

CHROME = 0 # 1 for Chrome, 0 for Firefox
ONLY_HTTP = True # False for connection-based
Logs = "C:/Users/George/Desktop/Logs/"
proxy_log = "C:/Users/George/Desktop/example.txt"
processed_proxy_log = "C:/Users/George/Desktop/processed_proxy_log.txt"
Previous = 2000 # no deactivation
Next = 20 #in ms, 0 for deactivation
Repetition = 5 # 0 for deactivation
Filter = "Url" # "Url" or "Content" or anything else for deactivation

make_client_actions.CHROME = CHROME
make_client_actions.Logs = Logs
make_client_actions.ONLY_HTTP = ONLY_HTTP

process_proxy_log.ONLY_HTTP = ONLY_HTTP
process_proxy_log.proxy_log = proxy_log
process_proxy_log.processed_proxy_log = processed_proxy_log

make_proxy_actions.proxy_log = processed_proxy_log
make_proxy_actions.Previous = Previous
make_proxy_actions.Next = Next
make_proxy_actions.Repetition = Repetition
make_proxy_actions.Filter = Filter
make_proxy_actions.ONLY_HTTP = ONLY_HTTP

if CHROME:
    print "Simulation with Chrome"
else:
    print "Simulation with Firefox"
if ONLY_HTTP:
    print "Only HTTP traffic"
else:
    print "Connections"

# run all
##make_client_actions.main()
##process_proxy_log.main()
##make_proxy_actions.main()
##count_match.main(ONLY_HTTP)

### run preparation
##make_client_actions.main()
##process_proxy_log.main()

# run main course
make_proxy_actions.main()
count_match.main(ONLY_HTTP)

log_scale = [1, 2, 4.6, 10, 20, 46, 100, 200, 460, 1000, 2000, 4600, 10000, 20000, 46000, 100000]

def run(p, n, r):
    make_proxy_actions.Previous = p
    make_proxy_actions.Next = n
    make_proxy_actions.Repetition = r
    make_proxy_actions.main()
    count_match.main(ONLY_HTTP)

##for previous_threshold in range(500, 10500, 500):
##    run(previous_threshold, 20, 5)
##print("----------")
##
##for next_threshold in log_scale[3:]:
##    next_threshold /= 100
##    run(2000, next_threshold, 5)
##print("----------")
##
##for repetition_threshold in log_scale[1:10]:
##    run(2000, 20, repetition_threshold)