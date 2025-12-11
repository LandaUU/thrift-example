import time
from thrift.transport import TSocket, THttpClient, TTransport
from thrift.protocol import TBinaryProtocol

from benchmark import BenchService


def measure(label, client_factory, iterations=5000):
    client = client_factory()

    # warm-up
    for _ in range(100):
        client.ping("warmup")

    start = time.perf_counter()
    for _ in range(iterations):
        client.ping("hello")
    end = time.perf_counter()

    total = end - start
    print(f"{label}:")
    print(f"  Total time: {total:.4f} s")
    print(f"  Avg latency: {total / iterations * 1000:.4f} ms")
    print(f"  Throughput: {iterations / total:.2f} req/s")
    print()


def make_socket_client():
    transport = TSocket.TSocket("127.0.0.1", 9090)
    transport = TTransport.TBufferedTransport(transport)
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = BenchService.Client(protocol)
    transport.open()
    return client


def make_http_client():
    transport = THttpClient.THttpClient("http://127.0.0.1:8080")
    protocol = TBinaryProtocol.TBinaryProtocol(transport)
    client = BenchService.Client(protocol)
    transport.open()
    return client


if __name__ == "__main__":
    ITER = 5000

    print("Starting Thrift transport benchmark...\n")
    measure("TSocket (binary)", make_socket_client, ITER)
    measure("THttpClient (HTTP/1.1)", make_http_client, ITER)
