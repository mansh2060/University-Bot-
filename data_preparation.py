import json
from nlp import tokenize,stem,bag_of_words
 


with open('context.json','r') as file:
    text=json.load(file)

def data_preparation():
    category_list=[]
    existing_word_list=[]
    category_word_list=[]
    for data in text['chatbot_responses']:
        category=data['category']
        category_list.append(category)
        for user_input in data['user_input']:
        #initiation of vocabulary
            tokens=tokenize(user_input)
          
        #collecting all the tokens in a single list so i will have single vector list in bag of words
            existing_word_list.extend(tokens) # 1st step of vocabulary
            category_word_list.append((category,tokens))
         

    
#collection of unique words + sorted
    ignored_list=['?',',','!','']
    existing_word_list=[stem(words) for words in existing_word_list if words not in ignored_list]
    existing_word_list=sorted(set(existing_word_list))   # vocabulary is created
    category_list=sorted(set(category_list))
#vectorization
    X_train=[]
    y_train=[]
    for (category,tokens) in category_word_list:
        vectors=bag_of_words(existing_word_list,tokens)
        X_train.append(vectors)
        index=category_list.index(category)
        y_train.append(index)
    return  X_train,y_train,category_list,existing_word_list

