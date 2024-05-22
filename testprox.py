import requests

def load_proxies(file_path):
    with open(file_path, 'r') as file:
        proxies = file.read().splitlines()
    return proxies

def save_proxies(file_path, proxies):
    with open(file_path, 'w') as file:
        for proxy in proxies:
            file.write(proxy + '\n')

def test_proxy(proxy):
    url = "http://httpbin.org/ip"
    proxies = {
        "http": f"http://{proxy}",
        "https": f"http://{proxy}",
    }
    try:
        response = requests.get(url, proxies=proxies, timeout=5)
        if response.status_code == 200:
            print(f"Proxy {proxy} is working.")
            return True
        else:
            print(f"Proxy {proxy} returned status code {response.status_code}.")
            return False
    except Exception as e:
        print(f"Proxy {proxy} failed. Error: {e}")
        return False

def main():
    input_file_path = 'proxies.txt'
    output_file_path = 'working_proxies.txt'

    proxy_list = load_proxies(input_file_path)
    working_proxies = []

    for proxy in proxy_list:
        if test_proxy(proxy):
            working_proxies.append(proxy)

    save_proxies(output_file_path, working_proxies)
    print(f"Saved {len(working_proxies)} working proxies to {output_file_path}.")

if __name__ == "__main__":
    main()
