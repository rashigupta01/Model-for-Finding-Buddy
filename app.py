from flask import Flask, request
import pickle

songs_data = pickle.load(open('songs_data.pkl','rb'))
similarity_matrix = pickle.load(open('similarity_matrix.pkl','rb'))

app = Flask(__name__)

def sort_by_score (val) : 
    return val['score']
@app.route('/') 
def home():
    return "hello world"

@app.route('/findBuddy', methods=['post'])
def recommend():
    json_data = request.json
    userId = json_data['currentUserId']
    user_favourites = json_data['user_favourites']

    for user_idx in range(len(user_favourites)):
        if user_favourites[user_idx]['id'] == userId : break

    users_match_list = []

    for user in user_favourites :
        if user['id'] == userId : continue
        
        score = 0
        for favourite in user_favourites[user_idx]['favourites'] :
            index1 = songs_data.index[songs_data['title'] == favourite].values[0]
            
            similarity = 0
            for current_user_fav in user['favourites'] :
                index2 = songs_data.index[songs_data['title'] == current_user_fav].values[0]
                similarity = max(similarity, similarity_matrix[index1][index2])
            
            score += similarity
        
        percent_score = ((score/len(user_favourites[user_idx]['favourites']))*100)
        users_match_list.append({'username': user['id'], 'score' : percent_score })

    users_match_list.sort(key=sort_by_score, reverse=True)
    return users_match_list

if __name__ == '__main__':
    app.run(debug=True)