from flask import Flask, render_template, request
import pandas as pd
import os
import math
app = Flask(__name__)
@app.route('/')
df = pd.read_pickle("1.pickle")
g = df.groupby('userID') 
df = g.filter(lambda x: len(x) > 25)
def index():
    # Template should be in templates/index.html
    return render_template('index2.html')

@app.route('/options')
def options():
    def similarity_score(person1,person2):
        item1 = set(df[df.userID==person1].artistID)
        item2 = set(df[df.userID==person2].artistID)
        common_items = set.intersection(*[item1, item2]) #算两个用户间，共同关注艺术家
        if len(common_items)==0:
            return 0
        sum_of_eclidean_distance = []
        for item in common_items: 
            freq1= float(df[(df.userID==person1)&(df.artistID==item)].freq) 
            freq2= float(df[(df.userID==person2)&(df.artistID==item)].freq) 
            sum_of_eclidean_distance.append(pow(freq1 - freq2,2)) #算共同关注艺术家之间的欧氏距离，作为两个人之间相似度的基准 
        sum_of_eclidean_distances = sum(sum_of_eclidean_distance)
        return 1/(1+math.sqrt(sum_of_eclidean_distances))

    def most_similar_users(person,number_of_users):
        scores_ = {other_person:similarity_score(person,other_person) for other_person in set(df.userID) if other_person != person}
        scores = sorted(scores_.items(), key=lambda d: d[1],reverse=True) #算相近的人 
        return scores[0:number_of_users]

    def user_recommend(person):
        recommend=[]
        similar_users = [i for i, j in most_similar_users(person,3)]
        item1 = set(df[df.userID==person].artistID)
        for other_user in similar_users:
            item2_ = set(df[df.userID==other_user].artistID)
            common_items_ = list(set.intersection(*[item1, item2_]))
            top_ = df[df.userID==other_user].sort_values('freq',ascending=False).artistID.tolist()
            top_2 = filter(lambda x: x not in common_items_ ,top_)
            top_2 = list(set(top_).difference(set(common_items_)))
            recommend.extend(top_2[0:4])
        recommends = list(set(recommend))
        return recommends

    query_new_user = request.args.get('query_new_user', '')
    query_new_user = int(query_new_user)
    df2 = df
    artist_name = df2.set_index('artistID')['name'].to_dict()
    '''
    query_new_user = int(query_new_user)
    query_1 = request.args.get('query_1', '')
    query_1 = int(query_1) 
    query_2 = request.args.get('query_2', '')
    query_first_score = int(query_2)/5
    query_3 = request.args.get('query_3', '')
    query_3 = int(query_3)
    query_4 = request.args.get('query_4', '')
    query_second_score = int(query_4)/5
    query_5 = request.args.get('query_5', '')
    query_5 = int(query_5)
    query_6 = request.args.get('query_6', '')
    query_third_score = int(query_6)/5
    new_data.update({query_1:query_first_score,query_3:query_second_score,query_5:query_third_score})

    newDF = pd.DataFrame()
    newDF['userID'] = [i for i in [int(query_new_user)]*3]
    newDF['artistID'] = [i for i in new_data.keys()]
    newDF['freq'] = [i for i in new_data.values()]
    df = df.append(newDF,ignore_index=True)
    '''
    your_recommend = user_recommend(int(query_new_user))
    list_test = []
    for i in your_recommend:
        list_test.append((artist_name.get(i),query_new_user))
    
    data = list_test
    #todo: compute some actual recommendations!
    options =  [(name,id) for (name,id) in data if id == int(query_new_user)]#if query in int(query)]
    return render_template('options.html', query=query_new_user, options=options)

@app.route('/recommend')
def recommend():
    item  = request.args.get('item', '')
    recommendations = ["Something based on {item}".format(**locals())]
    return render_template('recommend2.html', recommendations=recommendations)

if __name__ == "__main__":
    # This is only called if the script is run directly
    # This is the 'normal' way to control execution in python
    app.run(debug=True)


