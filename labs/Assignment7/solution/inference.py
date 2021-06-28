import math

import torch
import torch.nn.functional as F

import myModel

# we load the model

filepath = "myNet.pt"
ann = myModel.Net(2,20,1)

ann.load_state_dict(torch.load(filepath))
ann.eval()

# visualise the parameters for the ann (aka weights and biases)
# for name, param in ann.named_parameters():
#     if param.requires_grad:
#         print (name, param.data)

x =float( input("x = "))
y =float( input("y = "))
pair = torch.tensor([x, y])
print(ann(pair).tolist())
print(torch.sin(torch.tensor(x) + torch.tensor(y)/math.pi))