import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F

# Prepare samples
samples_inp = torch.tensor([[1,2,3],[1,1,1],[4,4,4],[9,9,9],[3,2,1],[0,0,1],[0,0,0]],dtype=torch.float)
samples_out = torch.tensor([[123],[111],[444],[999],[321],[1],[0]],dtype=torch.float)

class Perceptron(nn.Module):
    # initialization
    def __init__(self, num_inputs, num_hiddens, num_outputs):
        super().__init__()
        self.layer1 = nn.Linear(num_inputs, num_hiddens)
        self.layer2 = nn.Linear(num_hiddens, num_outputs)
    # forward
    def forward(self, x):
        return self.layer2(self.layer1(x))

# Define model 
model = Perceptron(3,10,1)

# Define loss function
loss_function = nn.MSELoss(reduction='sum')

# Define optimizer
optimizer = optim.Adam(model.parameters())

# Training
num_epochs = 35000

for t in range(num_epochs):

    # Forward pass
    out = model(samples_inp)
    loss = loss_function(out, samples_out)
    if t % 10 == 0:
        print(t, loss.item())

    # Reset gradients
    optimizer.zero_grad()

    # Backward pass
    loss.backward()

    # Update model parameters (weights)
    optimizer.step()

# Saving 
torch.save(model.state_dict(), 'perceptron.pth') # weights only
torch.save(model,'perceptron.pt') # whole model 

# Print weighs
for param in model.parameters():
    print(param.data)

# test
result = model(torch.tensor([[7,7,7]],dtype=torch.float))
print('test result',result[0].item())

#quit()
