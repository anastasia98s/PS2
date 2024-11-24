from torchmetrics import ConfusionMatrix
from mlxtend.plotting import plot_confusion_matrix
import matplotlib.pyplot as plt
import torch

def calculate_accuracy(vorhersage_array, loesung_array):
    vorhersage_tensor = torch.tensor(vorhersage_array)
    loesung_tensor = torch.tensor(loesung_array)
    genauigkeit = (vorhersage_tensor == loesung_tensor).sum().item() / len(loesung_tensor)
    return round(genauigkeit * 100, 1)

def show_conf_matrix(vorhersage_array, loesung_array, label, title, binary=False, plot=False):
    if len(label) > 1:
        title = title + "\nGenauigkeit: " + str(calculate_accuracy(vorhersage_array, loesung_array)) + "%"
        print("\nConfusion matrix " + title)
        if binary:
            confmat_metric = ConfusionMatrix(task='binary', num_classes=2)
        else:
            confmat_metric = ConfusionMatrix(task='multiclass', num_classes=len(label))
        conf_matrix = confmat_metric(torch.tensor(vorhersage_array), torch.tensor(loesung_array))
        print(conf_matrix)

        if plot:
            conf_matrix_np = conf_matrix.cpu().numpy()
            fig, ax = plot_confusion_matrix(conf_mat=conf_matrix_np, class_names=label, figsize=(8, 8), cmap="Blues")
            plt.tight_layout(pad=3.0)
            plt.title(title)
            plt.xlabel("Vorhersage")
            plt.ylabel("Lösung")
            plt.show()

def to_yhat(logits):
    logits = logits.view(-1, logits.shape[-1]).cpu().detach()
    probs = torch.softmax(logits, dim=1)
    y_hat = torch.argmax(probs, dim=1)
    return probs.numpy(), y_hat.numpy()