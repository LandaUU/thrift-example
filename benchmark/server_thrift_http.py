from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server.THttpServer import THttpServer

from benchmark import BenchService


class BenchHandler:
    def ping(self, msg):
        return msg


def run_server():
    port = 8080
    handler = BenchHandler()
    processor = BenchService.Processor(handler)

    transport = TSocket.TServerSocket(host="127.0.0.1", port=port)
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = THttpServer(processor, ("127.0.0.1", port), pfactory, pfactory)
    print(f"THttpServer listening on port {port}")
    server.serve()


if __name__ == "__main__":
    run_server()
