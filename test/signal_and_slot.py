"""
自定义信号和槽
1.  定义信号：在类中定义一个信号，使用PyQt的信号机制可以实现自定义信号。可以通过pyqtSignal()方法来创建一个信号对象。
2.  触发信号：在需要触发信号的地方，使用emit()方法来触发该信号。
3.  定义槽：在类中定义一个槽函数，使用@pyqtSlot()装饰器将该方法注册为槽函数。
4.  连接信号和槽：使用connect()方法将信号和槽连接起来。
"""
import sys
import threading
import time

from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QApplication


class MyObject(QObject):
    # 自定义信号
    my_signal = pyqtSignal(str)

    @pyqtSlot(str)
    def my_slot(self, data):
        print("槽函数被执行，在主线程更新UI:", threading.current_thread())
        print("主线程:", data)


def update_ui():
    global my_obj
    print("子线程发送信号:", threading.current_thread())
    data = "子线程发送信号"
    my_obj.my_signal.emit(data)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_obj = MyObject()
    my_obj.my_signal.connect(my_obj.my_slot)
    threading.Thread(target=update_ui).start()
    app.exit(app.exec_())
