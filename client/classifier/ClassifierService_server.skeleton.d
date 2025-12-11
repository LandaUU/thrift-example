/*
 * This auto-generated skeleton file illustrates how to build a server. If you
 * intend to customize it, you should edit a copy with another file name to 
 * avoid overwriting it when running the generator again.
 */
module classifier.ClassifierService_server;

import std.stdio;
import thrift.codegen.processor;
import thrift.protocol.binary;
import thrift.server.simple;
import thrift.server.transport.socket;
import thrift.transport.buffered;
import thrift.util.hashset;

import classifier.ClassifierService;
import classifier.classificator_types;


class ClassifierServiceHandler : ClassifierService {
  this() {
    // Your initialization goes here.
  }

  void trainOnExample(double[] features, int result) {
    // Your implementation goes here.
    writeln("trainOnExample called");
  }

  double predictProba(double[] features) {
    // Your implementation goes here.
    writeln("predictProba called");
    return typeof(return).init;
  }

}

void main() {
  auto protocolFactory = new TBinaryProtocolFactory!();
  auto processor = new TServiceProcessor!ClassifierService(new ClassifierServiceHandler);
  auto serverTransport = new TServerSocket(9090);
  auto transportFactory = new TBufferedTransportFactory;
  auto server = new TSimpleServer(
    processor, serverTransport, transportFactory, protocolFactory);
  server.serve();
}
