import socket
import threading

client_flag = 0  # 定义一个标志位


def client1(socket_tcp_server):  # 采用了多线程
    global client_flag  # 声明该变量可以在该方法使用

    # accept等待客户端连接
    # 如果有新的客户来连接服务器，那么就产生一个新的套接字连接客户端服务
    # new_client_socket用来为这个客户端服务
    # socket_tcp_server就可以省下专门等待其他客户连接

    new_client_socket, client_addr = socket_tcp_server.accept()  # 当服务器得到客户端请求连接时，client_flag=1
    client_flag = 1
    print("客户端连接成功", client_addr)

    while True:
        # 接收数据
        recv_date = new_client_socket.recv(1024)  # 当客户端断开连接时,recv_date的值为空

        if recv_date:  # 使服务器能一直收到信息，只有客户端断开时，才退出循环
            print("client" + str(client_addr[1] % 10000 % 1000 % 100 % 10) + ":接收到的数据为:",
                  recv_date.decode("utf-8"))
        else:
            break

        # 发送数据
        send_date = "收到"
        new_client_socket.send(send_date.encode("utf-8"))
    new_client_socket.close()  # 关闭这个套接字

    print("对方已经结束了会话，等待新的连接")


def main():
    global client_flag
    socket_tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 定义一个监听套接字
    socket_addr = ("127.0.0.1", 1900)
    socket_tcp_server.bind(socket_addr)  # 服务器绑定一个端口

    socket_tcp_server.listen(128)  # listen使套接字转变为被动连接，即类似等待客户端连接，而不是主动虚招客户端
    print("等待一个新客户端连接....")

    client1_threading = threading.Thread(target=client1, args=(socket_tcp_server,))
    client1_threading.start()

    while True:
        if client_flag:  # 当client_flag为1时，即服务器得到客户端请求连接时，开始一个新的线程

            client1_threading = threading.Thread(target=client1, args=(socket_tcp_server,))  # 新建一个线程
            client1_threading.start()  # 开启这个线程
            client_flag = 0  # 标志为，目的使线程不会一直增多，只有当服务器得到客户端请求连接时，才开始一个新的线程


if __name__ == '__main__':
    main()
