import http.client
import urllib.parse
import time
import argparse
import random
from threading import Thread


def load_proxies(file_path):
    with open(file_path, 'r') as file:
        proxies = file.read().splitlines()
    return proxies


def send_request(url, data, thread_id, proxy):
    parsed_url = urllib.parse.urlparse(url)
    try:
        if proxy:
            proxy_ip, proxy_port = proxy.split(":")
            conn = http.client.HTTPSConnection(proxy_ip, int(proxy_port))
            conn.set_tunnel(parsed_url.netloc, 443)
        else:
            conn = http.client.HTTPSConnection(parsed_url.netloc)

        headers = {'Content-type': 'application/x-www-form-urlencoded'}
        params = urllib.parse.urlencode(data)

        conn.request('POST', parsed_url.path, params, headers)
        response = conn.getresponse()
        if response.status == 200:
            print(f"Thread {thread_id}: Request sent successfully through proxy {proxy}.")
        else:
            print(f"Thread {thread_id}: Request failed with status code {response.status}. Proxy: {proxy}")
    except Exception as e:
        print(f"Thread {thread_id}: Request failed. Error: {e}. Proxy: {proxy}")
    finally:
        conn.close()


def spam_google_form(url, data, num_requests, num_threads, delay, proxies):
    threads = []

    for i in range(num_requests):
        proxy = random.choice(proxies) if proxies else None
        thread = Thread(target=send_request, args=(url, data, i, proxy))
        threads.append(thread)
        thread.start()

        # Delay between starting each thread
        if delay > 0:
            time.sleep(delay / num_threads)

    for thread in threads:
        thread.join()


def main():
    parser = argparse.ArgumentParser(description="Google Form Spammer with Proxy Support")
    parser.add_argument("-r", "--requests", type=int, help="Number of requests to send", required=True)
    parser.add_argument("-t", "--threads", type=int, help="Number of threads to use", required=True)
    parser.add_argument("-d", "--delay", type=float, help="Total delay between requests in seconds", required=True)
    parser.add_argument("-p", "--proxies", type=str, help="Path to file with list of proxies", required=True)
    args = parser.parse_args()

    google_form_url = "Google form here"

    # You need to inspect the Google Form and find out the entry numbers for the fields.
    # The data dictionary should be modified to include the appropriate entry numbers and values.
    data = {
        "entry.839170109": "Test", # use network inspect form response to find entries
        "entry.610229885": "Test"
        # Add more entries here as needed.
    }

    proxies = load_proxies(args.proxies)

    spam_google_form(google_form_url, data, args.requests, args.threads, args.delay, proxies)


if __name__ == "__main__":
    main()
