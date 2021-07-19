#This is a Smart ChatBot Program

#Required Libraries
from newspaper import Article
import random
import string
import nltk
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy
import warnings
warnings.filterwarnings('ignore')

#Download the punkt package
nltk.download('punkt',quiet=True)

#Get the Article
article=Article('https://www.mayoclinic.org/diseases-conditions/chronic-kidney-disease/symptoms-causes/syc-20354521')
article.download()
article.parse()
article.nlp()
corpus=article.text

#Print the Articles text
#print(corpus)

#Tokenization
text=corpus
sentence_list=nltk.sent_tokenize(text) # A list of sentences

#Print the list of sentences
#print(sentence_list)

#Greeting Function
def greeting_response(text):
    text=text.lower()

    #Bots greeting
    bot_greeting=['Hi','Hey','Hello','Hi there!!']
    #Users greeting
    user_greeting=['hi','hey','hello','greetings']

    for word in text.split():
        if word in user_greeting:
            return random.choice(bot_greeting)

#Sort index
def index_sort(list_var):
    length=len(list_var)
    list_index=list(range(0,length))
    x=list_var
    for i in range (length):
        for j in range (length):
            if x[list_index[i]]>x[list_index[j]]:
                temp=list_index[i]
                list_index[i]=list_index[j]
                list_index[j]=temp
    return list_index

#Create the Bots response
def bots_response(user_input):
    user_input=user_input.lower()
    sentence_list.append(user_input)
    bot_response=''
    cm=CountVectorizer().fit_transform(sentence_list)
    similarity_scores=cosine_similarity(cm[-1],cm)
    similarity_scores_list=similarity_scores.flatten()
    index=index_sort(similarity_scores_list)
    index=index[1:]
    response_flag=0

    j=0
    for i in range (len(index)):
        if similarity_scores_list[index[i]]>0.0:
            bot_response=bot_response+' '+sentence_list[index[i]]
            response_flag=1
            j=j+1
        if j>2:
            break
    if response_flag==0:
        bot_response=bot_response+' '+"I apologize, I don't understand"
    sentence_list.remove(user_input)
    return bot_response

#Start the Chat
print("Doc Bot: Hello I am Doc Bot. If you want to exit, type 'Bye'")
exit_list=['exit','bye','quit']
while(True):
    user_input=input()
    if user_input.lower() in exit_list:
        print("Doc Bot: Have a Good Day")
        break
    else:
        if greeting_response(user_input) != None:
            print('Doc Bot: '+greeting_response(user_input))
        else:
            print('Doc Bot: '+bots_response(user_input))
