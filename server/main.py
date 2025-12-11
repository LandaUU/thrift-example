# server.py
import numpy as np
from sklearn.linear_model import SGDClassifier

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from classifier import ClassifierService


class ClassifierHandler(ClassifierService.Iface):
    """
    Онлайн-классификатор: SGDClassifier (логистическая регрессия)
    с partial_fit шагом при каждом запросе trainOnExample.
    """

    def __init__(self, n_features: int):
        self.n_features = n_features

        self.model = SGDClassifier(
            loss="log_loss", learning_rate="optimal", penalty="l2"
        )

        self.is_initialized = False

    def _ensure_init(self):
        if not self.is_initialized:
            X0 = np.zeros((1, self.n_features))
            y0 = np.array([0])
            self.model.partial_fit(X0, y0, classes=np.array([0, 1]))
            self.is_initialized = True

    def trainOnExample(self, features, result):
        self._ensure_init()

        X = np.array([features], dtype=float)
        y_arr = np.array([result], dtype=int)

        self.model.partial_fit(X, y_arr)

    def predictProba(self, features) -> float:
        self._ensure_init()
        X = np.array([features], dtype=float)

        p = self.model.predict_proba(X)[0][1]
        return float(p)


def main():
    n_features = 2

    handler = ClassifierHandler(n_features)
    processor = ClassifierService.Processor(handler)

    transport = TSocket.TServerSocket(host="0.0.0.0", port=9090)
    tfactory = TTransport.TBufferedTransportFactory()
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()

    server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

    print("Starting Python sklearn ClassifierService on port 9090...")
    server.serve()


if __name__ == "__main__":
    main()
