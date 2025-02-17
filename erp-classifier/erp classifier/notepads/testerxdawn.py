import matplotlib.pyplot as plt
import joblib
import numpy as np
from sklearn.metrics import roc_curve, auc, accuracy_score
from scipy import interp
import mne
import utils

def plot_prediction_results(prediction_proba, labels_test):
    fprs = np.linspace(0, 1, 100)

    # ROC curve for fold i
    # https://scikit-learn.org/stable/auto_examples/model_selection/plot_roc_crossval.html
    fpr, tpr, thresholds = roc_curve(labels_test, prediction_proba[:, 1])
    tprs = interp(fprs, fpr, tpr)
    tprs[0] = 0.0
    tprs[-1] = 1.0
    roc_auc = auc(fprs, tprs)
    std_auc = np.std(roc_auc)

    plt.figure(figsize=(20, 10))
    plt.plot(fprs, tprs, color='b', label=r'ROC (AUC = %0.2f $\pm$ %0.2f)' % (roc_auc, std_auc),
             lw=2, alpha=.8)

    # Chance line
    plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='r', label='Chance', alpha=.8)

    plt.title('ROC curve')
    plt.xlabel('False positive rate')
    plt.xlim([-0.05, 1.05])
    plt.ylabel('True positive rate')
    plt.ylim([-0.05, 1.05])
    plt.legend(loc="best")
    plt.show()


def test_classifier(classifier_path, test_experiences, n):

    epochs = mne.concatenate_epochs(test_experiences)


    testing_labels_aux = epochs.events[:, -1]


    further_label = 10002
    closer_label = 10001
    testing_labels = np.array([1 if x == further_label else 0 if x == closer_label else x for x in testing_labels_aux])


    print(testing_labels)

    classifier = joblib.load(classifier_path)
    prediction = classifier.predict(epochs)
    print("Accuracy: {}".format(accuracy_score(testing_labels, prediction)))

    prediction_proba = classifier.predict_proba(epochs)

    print(prediction_proba)


    further_label = 10002
    closer_label = 10001
    hit_epochs_labels= np.array([1 if x == further_label else 0 if x == closer_label else x for x in testing_labels])

    plot_prediction_results(prediction_proba, hit_epochs_labels)
    return prediction

def get_classifier(classifier_path):
    return joblib.load(classifier_path)