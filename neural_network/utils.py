from torchmetrics import ConfusionMatrix
from mlxtend.plotting import plot_confusion_matrix
import matplotlib.pyplot as plt
import torch

def show_conf_matrix(antwort_array, loesung_array, label, title, binary=False, plot=False):
    if len(label) > 1:
        if binary:
            confmat_metric = ConfusionMatrix(task='binary', num_classes=2)
        else:
            confmat_metric = ConfusionMatrix(task='multiclass', num_classes=len(label))
        conf_matrix = confmat_metric(torch.tensor(antwort_array), torch.tensor(loesung_array))
        print(conf_matrix)

        if plot:
            conf_matrix_np = conf_matrix.cpu().numpy()
            fig, ax = plot_confusion_matrix(conf_mat=conf_matrix_np, class_names=label, figsize=(6, 6), cmap="Blues")
            plt.title(title)
            plt.xlabel("Antwort")
            plt.ylabel("Lösung")
            plt.show()

def to_yhat(logits):
    logits = logits.view(-1, logits.shape[-1]).cpu().detach()
    probs = torch.softmax(logits, dim=1)
    y_hat = torch.argmax(probs, dim=1)
    return probs.numpy(), y_hat.numpy()