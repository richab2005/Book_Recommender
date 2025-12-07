from flask import Flask,render_template,request
import pickle
import numpy as np
from fuzzywuzzy import process
popular_df=pickle.load(open('popular.pkl','rb'))
pt=pickle.load(open('pt.pkl','rb'))
books=pickle.load(open('books.pkl','rb'))
similarity_score=pickle.load(open('similarity_score.pkl','rb'))
app =Flask(__name__)
@app.route('/')
def index():
    return render_template('index.html'
                           ,book_name=list(popular_df['Book-Title'].values),
                           author=list(popular_df['Book-Author'].values),
                           image=list(popular_df['Image-URL-M'].values),
                           votes=list(popular_df['Number of Rates'].values),
                           rating=list(popular_df['Average-Rating'].values)
    )



@app.route('/recommend')
def recommend():
    return render_template('recommend.html')


@app.route('/search_books', methods=['POST'])
def search_books():
    user_input = request.form.get('user_input')

    # find closest match
    best_match = process.extractOne(user_input, pt.index)[0]

    # now use the same recommend logic
    index = np.where(pt.index == best_match)[0][0]
    similar_items = sorted(list(enumerate(similarity_score[index])),
                           key=lambda x: x[1], reverse=True)[1:8]

    data = []
    for i in similar_items:
        item = []
        temp_df = books[books['Book-Title'] == pt.index[i[0]]].drop_duplicates('Book-Title')
        item.append(temp_df['Book-Title'].values[0])
        item.append(temp_df['Book-Author'].values[0])
        item.append(temp_df['Image-URL-M'].values[0])
        data.append(item)

    return render_template('recommend.html', data=data)


@app.route('/recommend_books',methods=['POST']) 
def recommend_books():
    book_name = request.form.get('book_name')
    index=np.where(pt.index==book_name)[0][0]
    similar_items=sorted(list(enumerate(similarity_score[index])),key=lambda x:x[1] ,reverse=True)[1:8]

    data=[]
    for i in similar_items:
        item=[]
        temp_df=books[books['Book-Title']==pt.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))

        data.append(item)

    print(data)
    

    return render_template('recommend.html',data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
