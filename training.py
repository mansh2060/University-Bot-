from data_preparation import data_preparation
from torch.utils.data import Dataset,DataLoader
from model import NeuralNetwork
import torch
import torch.nn as nn


X_train,y_train,category_list,existing_word_list=data_preparation()
input_size=len(X_train[0])
hidden_size=8
output_size=len(category_list)
batch_size=8
num_iterations=1000
learning_rate=0.01
  
   
class DataBase(Dataset):
    def __init__(self):             # initializing input_data , output_data , num of samples 
        self.input_data=X_train
        self.output_data=y_train
        self.num_input=len(X_train)
        
    def __getitem__(self, index):
        return self.input_data[index] ,self.output_data[index]
        
    def __len__(self):
        return self.num_input

information=DataBase()
    
loading_data=DataLoader(dataset=information,shuffle=True,batch_size=batch_size,num_workers=0)

device=torch.device('cuda') if torch.cuda.is_available() else ('cpu')

model=NeuralNetwork(input_size,hidden_size,output_size).to(device)

loss_function=nn.CrossEntropyLoss()      #Loss Function

optimizer=torch.optim.Adam(model.parameters(),learning_rate)  #optimizer 

    
for epochs in range(num_iterations):
    for (tokens,category) in loading_data:
        tokens=tokens.to(device)                #moving input and output to the same device for computation in pytorch
        category=category.to(dtype=torch.long).to(device)  # dtype =long for crossentropyloss
            
            
        output=model(tokens)

        loss=loss_function(output,category)   #output = Y_predicted and category = Y

        optimizer.zero_grad()

        loss.backward()  # calculating gradients dL/dw

        optimizer.step()  # running backward propagation for updating the weights

         
    if (epochs+1) % 100 == 0:
        print (f'Epoch [{epochs+1}/{num_iterations}], Loss: {loss.item():.4f}')

    #gathering all the information from cleaning to training to process further for chat.py    
all_information={
           
        "model_state":  model.state_dict(),
        "input_size":   input_size,
        "hidden_size":  hidden_size,
        "output_size":  output_size,
        "existing_word_list" : existing_word_list,
        "category_list"     : category_list
}

filename="all_information.pth"
torch.save(all_information,filename)






   
