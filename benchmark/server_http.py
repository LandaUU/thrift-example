from flask import Flask, request, Response
from thrift.protocol import TBinaryProtocol
from thrift.transport import TTransport
from benchmark import BenchService

app = Flask(__name__)

handler = BenchService.Iface()


class BenchHandler:
    def ping(self, msg):
        return msg


processor = BenchService.Processor(BenchHandler())


@app.route("/thrift", methods=["POST"])
def thrift_endpoint():
    input_transport = TTransport.TMemoryBuffer(request.data)
    output_transport = TTransport.TMemoryBuffer()

    in_proto = TBinaryProtocol.TBinaryProtocol(input_transport)
    out_proto = TBinaryProtocol.TBinaryProtocol(output_transport)

    processor.process(in_proto, out_proto)
    return Response(
        output_transport.getvalue(), content_type="application/octet-stream"
    )


if __name__ == "__main__":
    app.run(port=8080)
