from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server.TServer import TSimpleServer

from benchmark import BenchService


class BenchHandler:
    def ping(self, msg):
        return msg


def run_server():
    handler = BenchHandler()
    processor = BenchService.Processor(handler)

    transport = TSocket.TServerSocket(host="127.0.0.1", port=9090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TSimpleServer(processor, transport, tfactory, pfactory)
    print("TSocket server listening on port 9090")
    server.serve()


if __name__ == "__main__":
    run_server()
