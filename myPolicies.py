# input:    list of lines from proxy log and which policies to be applied.
#           the N, R policies need a threshold != 0 to be applied,
#           the P policy should always be != 0,
#           filter should be either "Content" or "Url".
#           referer policy and other filters (text, size) exist, but are never applied.
# output:   dictionary with keys as suggested user actions according to policies

# there is also referer and some other filters (text, size):-> extra policies

def apply(proxy_list, previous_threshold, repetition_threshold, next_threshold, filter):
    customs = {}
    referer_list = []
    previous_time = 0
    look_for_alternatives = False
    counter = 0
    actions = {}

    for log_entry in proxy_list:
        # repetition policy
        path = log_entry.get_path()
        if path in customs:
            customs[path] += 1
        else:
            customs[path] = 1
        repetition_condition = True
        if repetition_threshold != 0 and customs[path] >= repetition_threshold:
            repetition_condition = False

        # referer policy
        referer_condition = True
##        referer = log_entry.referer
##        if referer != "-" and not (referer in referer_list):
##            referer_list.append(referer)
##            referer_condition = False

        current_time = log_entry.get_request_time()
        if current_time - previous_time < previous_threshold:
            if look_for_alternatives and referer_condition and check_candidate_filters(log_entry, filter) and repetition_condition:
                counter += 1
                actions[counter] = [log_entry]
                look_for_alternatives = False
            else:
                actions[counter].append(log_entry)
        else:
            if referer_condition and check_candidate_filters(log_entry, filter) and repetition_condition:
                counter += 1
                actions[counter] = [log_entry]
                look_for_alternatives = False
            else:
                actions[counter].append(log_entry)
                look_for_alternatives = True

        previous_time = current_time

    # next policy
    if next_threshold != 0:
        for key in actions.keys():
            if len(actions[key])>1:
                current = actions[key][0]
                next = actions[key][1]
                if next.get_request_time() - current.get_request_time() < next_threshold:
                    del actions[key]
    return actions

# FILTERS
def check_candidate_filters(log_entry, filter):
    if filter == "Content":
        if filterNonHtml(log_entry):
            return False
    elif filter == "Url":
        if filterBrowser(log_entry) or filterAds(log_entry) or filterScripts(log_entry):
            return False
    else:
        return True
    return True

def filterBrowser(log_entry):
    bad_words = ["favico", "ocsp", "symcd", ".ico"]
    for term in bad_words:
        if term in log_entry.get_path():
            return True
    return False

def filterAds(log_entry):
    ad_list = ["google-analytics", "doubleclick", "googlesyndication", "2o7"]
    ad_list.extend(["tacoda", "advertising", "adsonar", "yieldmanager", "quantserve", "2mdn"])
    for ad in ad_list:
        if ad in log_entry.get_hostname():
            return True
    return False

def filterScripts(log_entry):
    bad_types = ["javascript", "css"]
    for bad in bad_types:
        if bad in log_entry.content_type:
            return True
    return False

def filterNontext(log_entry):
    type = log_entry.content_type.split('/')[0]
    if type != "-" and type != "text":
        return True
    return False

def filterNonHtml(log_entry):
    type = log_entry.content_type
    if type != "-" and not ("text/html" in type):
        return True
    return False

def filterLength(log_entry):
    length = log_entry.get_length()
    if length == 0:
        return True
    return False