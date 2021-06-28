'''
1. Create the training database:
a. Create a distribution of 1000 random points in the domain [− 10, 10]2
b. Compute the value of the function f for each point
c. Create the pairs 𝑑 𝑖 = ((𝑥1𝑖, 𝑥2𝑖), 𝑓(𝑥1𝑖, 𝑥2𝑖)), 𝑖 = 1, 1000
Helping functions: torch.sin, torch.cos, torch.add, torch.rand, torch.full_like,
torch.addcmul, torch.column_stack, ...

2. Save the database into the file mydataset.dat
Help function: torch.save
'''
import torch
import math

input_tensor = (-20. * torch.rand(1000, 2) + 10.) #tensor(2D) with [-10, 10] elements
# print(input_tensor)

f_values = []
for i in range(1000):
    # print("x ", input_tensor[i][0], "y ", input_tensor[i][1])
    x_1 = input_tensor[i][0]
    x_2 = input_tensor[i][1]
    d = torch.sin(x_1 + x_2 / math.pi)
    # print("d: ", d)
    f_values.append(d)
# print(result)
f_values = torch.tensor(f_values)
result = torch.column_stack((input_tensor, f_values))
print(result)

torch.save(result, "mydataset.dat")