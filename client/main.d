module client;

import std.stdio;
import thrift.base;
import thrift.codegen.client;
import thrift.protocol.binary;
import thrift.transport.buffered;
import thrift.transport.socket;

import classifier.ClassifierService;

void main()
{
	auto socket = new TSocket("localhost", 9090);
	auto transport = new TBufferedTransport(socket);
	auto protocol = tBinaryProtocol(transport);
	auto client = tClient!ClassifierService(protocol);

	transport.open();

	double[][] trainX = [
		[0.0, 0.1],
		[0.2, -0.1],
		[-0.1, 0.2],
		[1.0, 1.1],
		[1.2, 0.9],
		[0.8, 1.3],
	];

	int[] trainY = [0, 0, 0, 1, 1, 1];

	writeln("Training...");
	foreach (i, x; trainX)
	{
		client.trainOnExample(x, trainY[i]);
	}

	writeln("Testing predictions...");

	double[][] testX = [
		[0.0, 0.0],
		[1.0, 1.0],
		[0.5, 0.4],
	];

	foreach (x; testX)
	{
		double p = client.predictProba(x);
		writeln("x=", x, " → P(y=1)=", p);
	}

	transport.close();
}
