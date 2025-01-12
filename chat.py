from nlp import tokenize,bag_of_words
from model import NeuralNetwork
import torch
import json
import random
import warnings
import numpy as np
warnings.filterwarnings('ignore')
with open('context.json','r') as file:
    texts=json.load(file)


filename="all_information.pth"
all_information=torch.load(filename)

input_size=all_information['input_size']
hidden_size=all_information['hidden_size']
output_size=all_information['output_size']
existing_words_list=all_information['existing_word_list']
category_list=all_information['category_list']
model_state=all_information['model_state']


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = NeuralNetwork(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()
bot_name = "Assistant"

def get_response(sentence):
    tokens=tokenize(sentence)
    vectors=bag_of_words(existing_words_list,tokens)
    vectors=np.array(vectors)                       #converting vectors to numpy array
    vectors = vectors.reshape(1, -1)            #original shape of vector was (83,) and now (1,83)
    vectors=torch.from_numpy(vectors).to(device)
    output=model(vectors)

    _,prediction=torch.max(output,dim=1)  #calculating the category index from the model

    category=category_list[prediction.item()] #calculating category class
    
    probability=torch.softmax(output,dim=1)  #list of probabilities for all 25 different classes

    probability_percentage=probability[0][prediction.item()]
    if probability_percentage.item() > 0.75:
        for element in texts['chatbot_responses']:
            if category==element['category']:
                return random.choice(element['response'])
        
    return "I do not understand"


if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        # sentence = "do you use credit cards?"
        sentence = input("You           : ")
        if sentence == "quit":
            break

        response = get_response(sentence)
        print(f"Assistant     :{response}")
     