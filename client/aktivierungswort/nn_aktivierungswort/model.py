import torch
import torch.nn as nn
import torch.nn.functional as F

class Model(nn.Module):
    def __init__(self, hidden_units_1: int, hidden_units_2: int):
        super(Model, self).__init__()

        self.conv1 = nn.Conv2d(1, hidden_units_1, kernel_size=3, stride=1, padding=1)
        self.bn1 = nn.BatchNorm2d(hidden_units_1)
        self.conv2 = nn.Conv2d(hidden_units_1, hidden_units_2, kernel_size=3, stride=1, padding=1)
        self.bn2 = nn.BatchNorm2d(hidden_units_2)
        self.conv3 = nn.Conv2d(hidden_units_2, 128, kernel_size=3, stride=1, padding=1)
        self.bn3 = nn.BatchNorm2d(128)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)

        self.fc1 = nn.Linear(128 * (128 // 8) * (63 // 8), 512) # (128, 63)
        self.fc2 = nn.Linear(512, 128)
        self.fc3 = nn.Linear(128, 1)

        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        x = F.relu(self.bn1(self.conv1(x)))
        x = self.pool(x)
        x = F.relu(self.bn2(self.conv2(x)))
        x = self.pool(x)
        x = F.relu(self.bn3(self.conv3(x)))
        x = self.pool(x)

        x = x.view(x.size(0), -1)

        x = F.relu(self.fc1(x))
        x = self.dropout(x)
        x = F.relu(self.fc2(x))
        x = self.dropout(x)

        x = torch.sigmoid(self.fc3(x))
        return x