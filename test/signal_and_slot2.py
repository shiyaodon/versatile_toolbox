from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot


class Sender(QObject):
    my_signal = pyqtSignal(str)

    def send_data(self):
        data = "hello world"
        self.my_signal.emit(data)


class Receiver(QObject):

    @pyqtSlot(str)
    def my_solt(self, data):
        print("receiver: ", data)


sender = Sender()
receiver = Receiver()

sender.my_signal.connect(receiver.my_solt)

sender.send_data()
