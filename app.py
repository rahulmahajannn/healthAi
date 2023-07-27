from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import random
from scipy.sparse import csr_matrix
from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt
import seaborn as sns
import app 
from localStoragePy import localStoragePy


# Reading CSV files
inputURL = "./csv//"

bf= pd.read_csv(inputURL + "breakfast.csv" , encoding= 'unicode_escape')
lunch= pd.read_csv(inputURL + "lunch.csv" , encoding= 'unicode_escape')
dinner= pd.read_csv(inputURL + "dinner.csv" , encoding= 'unicode_escape')
drinks= pd.read_csv(inputURL + "beverages.csv" , encoding= 'unicode_escape')
extras= pd.read_csv(inputURL + "dessert_snack.csv" , encoding= 'unicode_escape')
nonVeg= pd.read_csv(inputURL + "NonVeg.csv" , encoding= 'unicode_escape')
Exr= pd.read_csv(inputURL + "exercise.csv" , encoding= 'unicode_escape')

# AKM
def plot_points(points):
    x_coords = [point[0] for point in points]
    y_coords = [point[1] for point in points]
 
    plt.scatter(x_coords, y_coords)
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Points on a Plane')
    plt.show()
 
def calculate_threshold(points):
    total_distance = 0
    num_pairs = 0
 
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            distance = math.sqrt((points[i][0] - points[j][0]) ** 2 + (points[i][1] - points[j][1]) ** 2)
            total_distance += distance
            num_pairs += 1
 
    average_distance = total_distance / num_pairs
    return average_distance

def find_nearest_point(points, query_point):
    min_distance = math.inf
    nearest_point = None
 
    for point in points:
        distance = math.sqrt((point[0] - query_point[0]) ** 2 + (point[1] - query_point[1]) ** 2)
        if distance < min_distance:
            min_distance = distance
            nearest_point = point
 
    return nearest_point
 
# MKA


#A Gentle Water reminder and drinks offering function(just an Extra Part)
def Hydrated(age, gender):
    if(int(age)>=9 and int(age)<=13):
        if(gender=="male"):
            H2O="2." + str(random.randint(4, 8))
        else:
            H2O="2." + str(random.randint(0, 4))
    
    elif(int(age)>=14 and int(age)<=18):
        if(gender=="male"):
            H2O="3." + str(random.randint(2, 6))
        else:
            H2O="2." + str(random.randint(2, 6))
    elif(int(age)>=19 ):
        if(gender=="male"):
            H2O="3." + str(random.randint(5, 9))
        else:
            H2O="3." + str(random.randint(0, 2))

    return H2O



def Dk(dietType):
    if(dietType=="Weight Loss"):
        return "Sorry we recommend You to not drink for your current goal..."
    else:
        for i in range (0,len(drinks)):
            X=list(drinks.iloc[:,0])
        return ("You Got " + X[random.randint(0,16)] + " Enjoy! your drink")


def cheats(dietType):
    if(dietType=="Weight Gain"or dietType=="Healthy"):
        for i in range (0,len(extras)):
            Xtr=list(extras.iloc[:,0])
        return ("Your cheat meal for the day is " + Xtr[random.randint(0,40)] + " yuhooo!!")
    else:
        return "Sorry Buddy! we recommend You to not take cheat meals for your current goal..."


#main-function

def food_recommendation(wt, ht, age, gender, dietType, dietTime, Category ):
    n=14
    #getting the amount of calorie needed with RMR value
    if(gender=="male"):
        calNeed= 5 + (99*int(wt)) + (6*int(ht))-(5*int(age))
    else :
        calNeed=  (10*int(wt)) + (6*int(ht))-(5*int(age))-161


    #Checking the required Diet Calories
    if(dietType=="Weight Gain"):
        p=2
        if(gender=="male"):
            calNeed= calNeed + 1000
        else :
            calNeed= calNeed +750

    elif(dietType=="Weight Loss"):
        p=6
        
        if(gender=="male"):
            calNeed= calNeed-300
        else :
            calNeed= calNeed-500
    else:
        p=4

    # print(calNeed)

    calNeed= calNeed/3
    
    #checking the dietTime and Category of User
    print('dietTime', dietTime)
    if(dietTime=="Breakfast"):
        print('?', bf)
        calories=bf

    elif(dietTime=="Lunch"):
        calories=lunch
        if(Category=="NonVeg"):
            calories=nonVeg

    elif(dietTime=="Dinner"):
        calories=dinner
        if(Category=="NonVeg"):
            calories=nonVeg   

    print('>>>>>>>>>>>>>>>>>>')
    calNeed= calNeed/p

    #giving required neighbors value
    neigh = KNeighborsClassifier(n_neighbors=14)

    lenCal=len(calories)

    #getting values for X and Y from dataset
    i=0
    X=[]  
    for i in range(0,lenCal):
        j=list(calories.iloc[i,[1]])
        X.insert(i,j)
        y=list(calories.iloc[:,0])


    X=np.array(X)
    y=np.array(y)

    #removing NaN 
    y = y[~np.isnan(X).reshape(-1)]
    X=X[~np.isnan(X)]
    X=X.reshape(-1,1)

    neigh.fit(X, y)

    #Preping the required calories
    j=np.array(calNeed)
    j=j.reshape(-1,1)



    #getting the indexes of k nearest neighbors for value j
    ans=neigh.kneighbors(j, return_distance=False)
    ans=ans[0]

    #giving Name of the dishes recommended for user
    food=[]
    for i in range (0,len(ans)):
        c=ans[i]
        c=y[c]
        food.insert(i,c)

    return food
        


    



#Exercise Recommendation engine

def Exercise_recommendation(wt, ht, age, gender, Target):

    if(gender=="male"):
        calNeed= 5 + (99*int(wt)) + (6*int(ht))-(5*int(age))+1500
    else :
        calNeed=  (10*int(wt)) + (6*int(ht))-(5*int(age))-161+1000


    if(Target=="Weight Loss"):
        calNeed= (50/100)*calNeed
    elif(Target=="Healthy"):
        calNeed= (30/100)*calNeed
    else:
        calNeed=(20/100)*calNeed


    calNeed/=6

    neigh = KNeighborsClassifier(n_neighbors=15)

    length= len(Exr)



    i=0
    X=[]
    for i in range(0, length):
        j=list(Exr.iloc[i,[1]])
        X.insert(i,j)
        y=list(Exr.iloc[:,0])

    X=np.array(X)
    y=np.array(y)


    y = y[~np.isnan(X).reshape(-1)]
    X=X[~np.isnan(X)]
    X=X.reshape(-1,1)

    neigh.fit(X, y)


    
    #Preping the required calories to burnt
    j=np.array(calNeed)
    j=j.reshape(-1,1)

    #getting the indexes of k nearest neighbors for value j
    ans=neigh.kneighbors(j, return_distance=False)
    ans=ans[0]


    #giving Name of the Exercise recommended for user
    
    Exercise=[]
    for i in range (0,len(ans)):
        c=ans[i]
        c=y[c]
        Exercise.insert(i,c)

    return Exercise







app = Flask(__name__)
app._static_folder = './static/'

@app.route('/')
def entry():
    return render_template("login.html")

@app.route('/', methods=['POST', 'GET'])
def getentry():
    if 'form2' in request.form:
        name = request.form['name']
    email = request.form['Email']
    password = request.form['password']
    return render_template('dietexr.html')


@app.route('/info')
def info():
    return render_template("dietexr.html")

@app.route('/info', methods=['POST', 'GET'])
def getInfo():
    t=False
    water=0
    ext=""
    drink=""
    msg = "Hey FireBall!!  Just do 5 to 6 of these exercise, for 10 min each :"
    wt = request.form['weight']
    ht = request.form['height']
    age = request.form['age']
    gender = request.form['gender']
    diettype = request.form['dietType']
    diettime = ''
    category = ''
    if 'form1' in request.form:
        t=True
        msg = "Hey Buddy, we recommend you to eat 3-4 of these suggest dishes :"
        diettime = request.form['dietTime']
        # print(dietTime)
        category = request.form['category']
        rec = food_recommendation(wt,ht,age,gender, diettype,diettime,category)
        water= Hydrated(age, gender)
        ext=cheats(diettype)
        drink= Dk(diettype)
    else:
        rec = Exercise_recommendation(wt,ht,age,gender,diettype)
    return render_template('main.html', rec=rec, msg=msg, check=t, water=water , ext=ext, drink= drink )


@app.route('/main')
def main():
    render_template("main.html")
    


if __name__ == "__main__":
    app.run(port=6969,debug=True)
