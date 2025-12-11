
namespace py classifier
namespace d classifier

service ClassifierService {
    /**
     * One online-training update using sgd.
     */
    void trainOnExample(1: list<double> features, 2: i32 result),

    /**
     * Predict probability for class=1
     */
    double predictProba(1: list<double> features)
}
