import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

class ValueNetwork(nn.Module):
    def __init__(self):
        super(ValueNetwork, self).__init__()
        self.conv1 = nn.Conv2d(1, 128, kernel_size=2, stride=1, padding=1)
        self.conv2 = nn.Conv2d(128, 128, kernel_size=2, stride=1, padding=0)
        self.fc1 = nn.Linear(128 * 4 * 4, 256)
        self.fc2 = nn.Linear(256, 1)

    def forward(self, x):
        x = torch.relu(self.conv1(x))
        x = torch.relu(self.conv2(x))
        x = x.view(x.size(0), -1)
        x = torch.relu(self.fc1(x))
        x = self.fc2(x)
        return x

def load_training_data(file_path="training_data.npy"):
    data = np.load(file_path, allow_pickle=True)
    states, values = zip(*data)
    states = np.array(states, dtype=np.float32).reshape(-1, 1, 4, 4)
    values = np.array(values, dtype=np.float32).reshape(-1, 1)
    return torch.tensor(states), torch.tensor(values)

def train_value_network():
    X_train, y_train = load_training_data()

    model = ValueNetwork()
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    epochs = 10
    batch_size = 32
    dataset = torch.utils.data.TensorDataset(X_train, y_train)
    dataloader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=True)

    for epoch in range(epochs):
        total_loss = 0
        for batch in dataloader:
            states, values = batch
            optimizer.zero_grad()
            predictions = model(states)
            loss = criterion(predictions, values)
            loss.backward()
            optimizer.step()
            total_loss += loss.item()

        print(f"Epoch {epoch + 1}/{epochs}, Loss: {total_loss / len(dataloader):.4f}")

    torch.save(model.state_dict(), "value_network.pth")
    print("Modelo treinado salvo como 'value_network.pth'.")

if __name__ == "__main__":
    train_value_network()