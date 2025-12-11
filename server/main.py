from tutorial import Calculator
from tutorial.ttypes import InvalidOperation, Operation

from shared.ttypes import SharedStruct

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer


class CalculatorHandler(Calculator.Iface):
    def __init__(self):
        self.log = {}

    def ping(self):
        print("ping()")

    def add(self, num1, num2):
        print("add(%d,%d)" % (num1, num2))
        return num1 + num2

    def calculate(self, logid, w):
        print("calculate(%d, %r)" % (logid, w))

        if w.op == Operation.ADD:
            val = w.num1 + w.num2
        elif w.op == Operation.SUBTRACT:
            val = w.num1 - w.num2
        elif w.op == Operation.MULTIPLY:
            val = w.num1 * w.num2
        elif w.op == Operation.DIVIDE:
            if w.num2 == 0:
                raise InvalidOperation(w.op, "Cannot divide by 0")
            val = w.num1 / w.num2
        else:
            raise InvalidOperation(w.op, "Invalid operation")

        log = SharedStruct()
        log.key = logid
        log.value = "%d" % (val)
        self.log[logid] = log

        return val

    def getStruct(self, key):
        print("getStruct(%d)" % (key))
        return self.log[key]

    def zip(self):
        print("zip()")


if __name__ == "__main__":
    handler = CalculatorHandler()
    processor = Calculator.Processor(handler)
    transport = TSocket.TServerSocket(host="127.0.0.1", port=9090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

    # You could do one of these for a multithreaded server
    # server = TServer.TThreadedServer(
    #     processor, transport, tfactory, pfactory)
    # server = TServer.TThreadPoolServer(
    #     processor, transport, tfactory, pfactory)

    print("Starting the server...")
    server.serve()
    print("done.")
