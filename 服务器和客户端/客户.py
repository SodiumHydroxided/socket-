import socket
import threading


def send_date(socket_tcp_client):  # 发送数据
    while True:
        server_date = "客户端1的消息："+input()
        # 3.发送信息
        if server_date == "exit":  # 当输入exit时，断开于服务器的连接
            break
        else:
            socket_tcp_client.send(server_date.encode("utf-8"))  # 发数据,enconde为编码 utf-8为编码方式

    socket_tcp_client.close()  # 关闭套接字


def recv_date(socket_tcp_client):  # 接收数据

    while True:
        recv_date = socket_tcp_client.recv(1024)  # 接收信息，每次最大为1024

        print("接收到的数据为:", recv_date.decode("utf-8"))  # decode为解码，utf-8为解码方式
        print("请输入要发送的数据:", end=" ")


def main():
    socket_tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建一个套接字
    server_ip = "127.0.0.1"
    server_port = 1900
    print("请输入要发送的数据，输入exit退出会话:", end=" ")

    server_addr = (server_ip, server_port)
    socket_tcp_client.connect(server_addr)  # 2.绑定连接

    send_tcp_date = threading.Thread(target=send_date, args=(socket_tcp_client,))  # 定义两个线程，分别为发送和接收
    recv_tcp_date = threading.Thread(target=recv_date, args=(socket_tcp_client,))
    send_tcp_date.start()
    recv_tcp_date.start()  # 开启这两个线程


if __name__ == '__main__':
    main()