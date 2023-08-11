import socket


def decode_bytes(data: bytes) -> str:
    try:
        return data.decode("utf-8")
    except:
        return data.decode("GBK")


def get_local_ip():
    """
    获取本机所有IP
    :return: IP列表
    """
    local_ips = ["127.0.0.1"]
    __hostname = socket.gethostname()
    for ip in socket.gethostbyname_ex(__hostname)[2]:
        local_ips.append(ip)

    local_ips.sort(reverse=True)
    return local_ips


if __name__ == '__main__':
    print(get_local_ip())
