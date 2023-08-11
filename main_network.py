"""做一个TCP客户端、TCP服务器、UDP
    1. 导入模块
    2. 创建自定义QMainWindow类
    3. main初始化 PyQt、自定义类
"""
import threading

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from common.utils import decode_bytes
from ui.Ui_network_main_window import Ui_mainWindow
import sys
import socket

RECV_BUFSIZE = 2048


class NetWorkMainWindow(QMainWindow):
    def __init__(self):
        super().__init__(None)
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.init_ui()

    def connect_and_recv(self, target_ip, target_port):
        tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcp_client.connect((target_ip, int(target_port)))
        self.statusBar().showMessage("连接服务器成功 {}:{}".format(target_ip, target_port))
        local_ip, local_port = tcp_client.getsockname()
        self.ui.edit_local_ip.clear()
        self.ui.edit_local_ip.addItem(local_ip)
        self.ui.edit_local_port.setText(str(local_port))

        try:
            while True:
                recv_bytes = tcp_client.recv(RECV_BUFSIZE)
                if not recv_bytes:
                    break
                recv_data = decode_bytes(recv_bytes)
                print("接收到数据: {}".format(recv_data))
                self.ui.edit_recv.appendPlainText(recv_data)
        except Exception as e:
            print(e)
        finally:
            tcp_client.close()

    def on_btn_connect_click(self):
        target_ip = self.ui.edit_target_ip.text()
        target_port = self.ui.edit_target_port.text()
        print("连接目标服务器 {}:{}".format(target_ip, target_port))

        # 为获取消息函数开启一个线程，防止主线程因无法收到数据进入死循环
        t = threading.Thread(target=self.connect_and_recv, args=(target_ip, target_port))
        t.daemon = True
        t.start()

    def init_ui(self):
        self.ui.edit_target_ip.setText("127.0.0.1")
        self.ui.edit_target_port.setText("8888")
        self.ui.btn_connect.clicked.connect(self.on_btn_connect_click)


def main():
    app = QApplication(sys.argv)
    window = NetWorkMainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
