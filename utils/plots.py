import os
from typing import List

import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import (accuracy_score, average_precision_score,
                             confusion_matrix, f1_score,
                             precision_recall_curve, precision_score,
                             recall_score, roc_auc_score, roc_curve)


def plot_confusion_matrix(preds: np.ndarray, 
                          labels: np. ndarray,
                          classes: List[str],
                          path: str=os.getcwd()) -> None:
    """
    Plots the Confusion Matrix.

    Parameters
    ----------
    preds : model's predictions

    labels : true labels as binary targets

    classes : a list of class names to use. The class names order 
    should exactly match the ordinality of the labels and predictions.

    path : where to save the plot image. Defaults to current directory.
    """
    cm = confusion_matrix(labels, preds)

    plt.imshow(cm, cmap=plt.cm.Blues)

    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes)
    plt.yticks(tick_marks, classes, rotation=90)

    thresh = cm.max() / 2
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            plt.text(j, i, cm[i, j],
                     horizontalalignment='center',
                     color='white' if cm[i, j] > thresh else 'black')
            
    plt.title('Confusion Matrix')
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.savefig(os.path.join(path,'confusion_matrix.png'), 
                dpi=300, 
                bbox_inches='tight')
    plt.close()


def plot_roc_curve(probs: np.ndarray, 
                   labels: np.ndarray,
                   path: str=os.getcwd()) -> None:
    """
    Plots the Receiver Operating Characteristic curve.

    Parameters
    ----------
    probs : probability of the positive class

    labels : true labels as binary targets

    path : where to save the plot image. Defaults to current directory.
    """
    fpr, tpr, _ = roc_curve(labels, probs)

    auc = roc_auc_score(labels, probs)

    plt.plot(fpr, tpr, label=f'AUC = {auc:.4f}')
    plt.title(f'ROC Curve')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Postive Rate')
    plt.legend()
    plt.savefig(os.path.join(path,'roc_curve.png'), 
                dpi=300, 
                bbox_inches='tight')
    plt.close()


def plot_pre_rec_curve(probs: np.ndarray,
                       labels: np.ndarray,
                       path: str=os.getcwd()) -> None:
    """
    Plots the Precision-Recall curve.

    Parameters
    ----------
    probs : probability of the positive class

    labels : true labels as binary targets

    path : where to save the plot image. Defaults to current directory.
    """
    precision, recall, _ = precision_recall_curve(labels, probs)

    ap = average_precision_score(labels, probs)
    
    plt.plot(recall, precision, label=f'AP = {ap:.4f}')
    plt.title(f'Precision-Recall Curve ')
    plt.xlabel('Recall')
    plt.ylabel('Precision')
    plt.legend()
    plt.savefig(os.path.join(path,'precision_recall_curve.png'), 
                dpi=300, 
                bbox_inches='tight')
    plt.close()


def plot_results_above_threshold(probs: np.ndarray,
                                 labels: np.ndarray,
                                 path: str=os.getcwd()) -> None:
    """
    Plots the Accuracy, Precision, Recall and F1 Score results
    by changing the probability threshold.

    Parameters
    ----------
    probs : probability of the positive class

    labels : true labels as binary targets

    path : where to save the plot image. Defaults to current directory.
    """
    metrics = {'Percentage of Samples': '', 
               'Accuracy': accuracy_score, 
               'Precision': precision_score, 
               'Recall': recall_score,
               'F1 Score': f1_score}

    threshold = np.arange(0.01, 1.00, 0.01)

    for key in metrics.keys():
        above_threshold = np.zeros(len(threshold))

        for i,thr in enumerate(threshold):
            preds = (probs > thr).astype(int)
            if key == 'Percentage of Samples':
                above_threshold[i] = sum(preds)/len(probs)
            elif key == 'Accuracy':
                above_threshold[i] = metrics[key](labels, preds)
            else:
                above_threshold[i] = metrics[key](labels, preds, zero_division=0)

            if thr == 0.5:
                result = above_threshold[i]

        nonzero = np.array(above_threshold) != 0
        plt.figure()
        plt.plot(threshold[nonzero], above_threshold[nonzero], label=f'{key} at 0.5 = {result:.4f}')
        plt.xlabel('Probability Threshold')
        plt.ylabel(key)
        plt.legend()
        plt.savefig(os.path.join(path,f'{key}.png'), 
                    dpi=300, 
                    bbox_inches='tight')
        plt.close()