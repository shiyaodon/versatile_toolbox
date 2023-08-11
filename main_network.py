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
    # 定义信号，将子线程发送的数据传递给主线程槽函数去执行
    modify_ui_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__(None)
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.tcp_client: socket.socket = None

        # 信号与槽函数关联
        self.modify_ui_signal.connect(self.recv_data_solt)
        self.init_ui()

    @pyqtSlot(str)
    def recv_data_solt(self, data):
        # print("recv_data_solt: ", threading.current_thread())
        self.ui.edit_recv.appendPlainText(data)

    def connect_and_recv(self, target_ip, target_port):
        """
        当前函数在子线程执行
            1. 链接服务器
            2. 循环接收服务器发来的数据
        :param target_ip:
        :param target_port:
        :return:
        """
        print(threading.current_thread())
        try:
            while True:
                recv_bytes = self.tcp_client.recv(RECV_BUFSIZE)
                if not recv_bytes:
                    break
                recv_data = decode_bytes(recv_bytes)
                print("接收到数据: {}".format(recv_data))
                # 子线程发送信号，主线程关联信号之后在主线程中修改信号
                self.modify_ui_signal.emit(recv_data)
        except Exception as e:
            print("子线程捕获到异常：", e)
        finally:
            print("服务器已断开 {}:{}".format(target_ip, target_port))
            self.statusBar().showMessage("已服务器断开 {}:{}".format(target_ip, target_port))
            if self.tcp_client is not None:
                self.tcp_client.close()
                self.tcp_client = None
            self.modify_current_ui()

    def modify_current_ui(self):
        """
        连接与断开时更改UI页面中的连接按钮的图标和文字
        :return:
        """
        if self.tcp_client is None:
            self.ui.btn_connect.setIcon(QIcon(":/button/disconnect"))
            self.ui.btn_connect.setText("进行连接")
        else:
            self.ui.btn_connect.setIcon(QIcon(":/button/connect"))
            self.ui.btn_connect.setText("断开连接")

    def btn_connect_clicked(self):
        """ 定义标记
        1. 连接服务器
        2. 断开当前连接
        - 方式 1：
            self.tcp_client is None : 连接服务器
            self.tcp_client is not None: 断开连接
        :return:
        """
        if self.tcp_client is None:
            self.connect_server()
        else:
            self.tcp_client.close()
            self.tcp_client = None
        self.modify_current_ui()

    def connect_server(self):
        """
        连接服务器
        :return:
        """
        target_ip = self.ui.edit_target_ip.text()
        target_port = self.ui.edit_target_port.text()
        print("连接目标服务器 {}:{}".format(target_ip, target_port))
        # 创建 socket 对象
        self.tcp_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # 连接TCP服务器
            self.tcp_client.connect((target_ip, int(target_port)))
            self.statusBar().showMessage("连接服务器成功 {}:{}".format(target_ip, target_port))
            local_ip, local_port = self.tcp_client.getsockname()
            self.ui.edit_local_ip.clear()
            self.ui.edit_local_ip.addItem(local_ip)
            self.ui.edit_local_port.setText(str(local_port))

            # 为获取消息函数开启一个线程，防止主线程因无法收到数据进入死循环
            t = threading.Thread(target=self.connect_and_recv, args=(target_ip, target_port))
            t.daemon = True
            t.start()
            self.modify_current_ui()
        except socket.timeout as e:
            self.statusBar().showMessage("连接服务器超时")
            self.tcp_client.close()
            self.tcp_client = None
        except Exception as e:
            self.statusBar().showMessage("连接服务器异常，检查服务器是否正常")
            self.tcp_client.close()
            self.tcp_client = None

    def btn_send_clicked(self):
        text = self.ui.edit_send.toPlainText()
        if text == "":
            self.statusBar().showMessage("请输入内容")
            return
        if self.tcp_client is None:
            self.statusBar().showMessage("服务器未连接")
            return

        self.tcp_client.send(f"{text}\r\n".encode())

    def init_ui(self):
        self.ui.edit_target_ip.setText("127.0.0.1")
        self.ui.edit_target_port.setText("8888")
        self.ui.btn_connect.clicked.connect(self.btn_connect_clicked)
        self.ui.btn_send.clicked.connect(self.btn_send_clicked)


def main():
    app = QApplication(sys.argv)
    window = NetWorkMainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
