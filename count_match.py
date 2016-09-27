def count_match_connections(client_list, proxy_list):
    match_counter = 0
    for cl_line in client_list:
        if cl_line[1].startswith("http://"):
            for pr_line in proxy_list:
                if pr_line[1].startswith("http://"):
                    if cl_line[1] == pr_line[1]:
                        match_counter += 1
                        proxy_list.remove(pr_line)
                        break
        else:
            import urlparse
            h_cl = urlparse.urlsplit(cl_line[1]).hostname
            for pr_line in proxy_list:
                h_pr = urlparse.urlsplit(pr_line[1]).hostname
                if h_cl == h_pr and pr_line[0] >= cl_line[0] and pr_line[0] <= cl_line[0] + 500:
                    match_counter += 1
                    proxy_list.remove(pr_line)
                    break
    return match_counter

def count_match_HTTP(client_list, proxy_list):
    match_counter = 0
    for cl_line in client_list:
        for pr_line in proxy_list:
            if cl_line == pr_line:
                match_counter += 1
                proxy_list.remove(pr_line)
                break
    return match_counter

def create_list(filename, ONLY_HTTP):
    a_list = []
    with open(filename) as f:
        for line in f:
            if ONLY_HTTP:
                a_list.append(line.strip().split("#")[0])
            else:
                items = line.strip().split()
                a_list.append((int(items[0]), items[1]))
    return a_list

def main(ONLY_HTTP):
    client_list = create_list("client_actions.txt", ONLY_HTTP)
    proxy_list = create_list("proxy_actions.txt", ONLY_HTTP)
    proxy_list_length = len(proxy_list)
    if ONLY_HTTP:
        print count_match_HTTP(client_list, proxy_list),
    else:
        print count_match_connections(client_list, proxy_list),
    print proxy_list_length

if __name__ == "__main__":
    ONLY_HTTP_user_input = raw_input("Only HTTP?")
    if ONLY_HTTP_user_input in ["y", "Y", "yes", "Yes", "YES"]:
        ONLY_HTTP = True
    else:
        ONLY_HTTP = False
    main(ONLY_HTTP)