import torch
import torch.nn as nn

""" class Model(nn.Module):
    def __init__(self, hidden_units_1: int, hidden_units_2: int):
        super(Model, self).__init__()
        # o = ((i + 2*p - k)/s)+1
        self.conv1 = nn.Conv1d(in_channels=1, out_channels=hidden_units_1, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv1d(in_channels=hidden_units_1, out_channels=hidden_units_2, kernel_size=3, stride=1, padding=1)
        self.pool1 = nn.MaxPool1d(kernel_size=2)
        self.conv3 = nn.Conv1d(in_channels=hidden_units_2, out_channels=hidden_units_1, kernel_size=3, stride=1, padding=1)
        self.conv4 = nn.Conv1d(in_channels=hidden_units_1, out_channels=hidden_units_2, kernel_size=3, stride=1, padding=1)
        self.pool2 = nn.MaxPool1d(kernel_size=2)
        self.fc1 = nn.Linear(hidden_units_2*48, hidden_units_1)
        self.fc2 = nn.Linear(hidden_units_1, 1)

    def forward(self, x):
        x = x.unsqueeze(1)

        x = self.conv1(x)
        x = torch.relu(x)
        x = self.conv2(x)
        x = torch.relu(x)
        x = self.pool1(x)

        x = self.conv3(x)
        x = torch.relu(x)
        x = self.conv4(x)
        x = torch.relu(x)
        x = self.pool2(x)

        x = x.view(x.size(0), -1)
        x = self.fc1(x)
        x = torch.relu(x)
        x = self.fc2(x)
        x = x.squeeze()
        x = torch.sigmoid(x) 
        return x """

class Model(nn.Module):
    def __init__(self, hidden_units_1: int, hidden_units_2: int, lstm_units=100):
        super(Model, self).__init__()
        self.conv1 = nn.Conv1d(in_channels=1, out_channels=hidden_units_1, kernel_size=3, stride=1, padding=1)
        self.conv2 = nn.Conv1d(in_channels=hidden_units_1, out_channels=hidden_units_2, kernel_size=3, stride=1, padding=1)
        self.pool1 = nn.MaxPool1d(kernel_size=2)
        self.conv3 = nn.Conv1d(in_channels=hidden_units_2, out_channels=hidden_units_1, kernel_size=3, stride=1, padding=1)
        self.conv4 = nn.Conv1d(in_channels=hidden_units_1, out_channels=hidden_units_2, kernel_size=3, stride=1, padding=1)
        self.pool2 = nn.MaxPool1d(kernel_size=2)
        self.lstm = nn.LSTM(input_size=hidden_units_2, hidden_size=lstm_units, batch_first=True)
        self.fc1 = nn.Linear(lstm_units, hidden_units_1)
        self.fc2 = nn.Linear(hidden_units_1, 1)

    def forward(self, x):
        x = x.unsqueeze(1)
        x = self.conv1(x)
        x = torch.relu(x)
        x = self.conv2(x)
        x = torch.relu(x)
        x = self.pool1(x)
        x = self.conv3(x)
        x = torch.relu(x)
        x = self.conv4(x)
        x = torch.relu(x)
        x = self.pool2(x)
        x = x.transpose(1, 2)
        x, _ = self.lstm(x)
        x = x[:, -1, :]
        x = self.fc1(x)
        x = torch.relu(x)
        x = self.fc2(x)
        x = x.squeeze()
        x = torch.sigmoid(x)
        return x