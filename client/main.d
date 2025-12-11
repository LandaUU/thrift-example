module client;

import std.stdio;
import thrift.base;
import thrift.codegen.client;
import thrift.protocol.binary;
import thrift.transport.buffered;
import thrift.transport.socket;

import tutorial.Calculator;
import tutorial.tutorial_types;

void main()
{
	auto socket = new TSocket("localhost", 9090);
	auto transport = new TBufferedTransport(socket);
	auto protocol = tBinaryProtocol(transport);
	auto client = tClient!Calculator(protocol);

	transport.open();

	client.ping();
	writeln("ping()");

	int sum = client.add(1, 1);
	writefln("1 + 1 = %s", sum);

	auto work = Work();
	work.op = Operation.DIVIDE;
	work.num1 = 1;
	work.num2 = 0;
	try
	{
		int quotient = client.calculate(1, work);
		writeln("Whoa we can divide by 0");
	}
	catch (InvalidOperation io)
	{
		writeln("Invalid operation: " ~ io.why);
	}

	work.op = Operation.SUBTRACT;
	work.num1 = 15;
	work.num2 = 10;
	int diff = client.calculate(1, work);
	writefln("15 - 10 = %s", diff);

	auto log = client.getStruct(1);
	writefln("Check log: %s", log.value);
}
