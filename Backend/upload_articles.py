import json
import firebase_admin
from firebase_admin import credentials, firestore
import os

# Initialize Firebase
current_dir = os.path.dirname(os.path.abspath(__file__))
cred = credentials.Certificate('/Users/rithwikchokkalingam/Desktop/The-One-ion/Backend/Credentials/FirebaseCredentials.json')
firebase_admin.initialize_app(cred)
db = firestore.client()

def upload_articles():

    data_dir = os.path.join(current_dir, 'Articles')
    
    article_types = {
        'real': os.path.join(data_dir, 'RealArticles.json'),
        'fake': os.path.join(data_dir, 'FakeArticles.json'),
        'onion': os.path.join(data_dir, 'OnionArticles.json')
    }

    for article_type, json_file in article_types.items():
        with open(json_file, 'r') as f:
            articles = json.load(f)
        
        for article_id, article_data in articles.items():
            # creates the id so its like real-1 and stuff
            doc_id = f"{article_type}_{article_id.split('_')[-1]}"
            
            # this column is for answer 
            article_data['answer'] = article_type.capitalize()  # "Real", "Fake" or "Onion"
            
            # upload to database
            db.collection('articles').document(doc_id).set(article_data)
            print(f"Uploaded {doc_id}")

if __name__ == "__main__":
    upload_articles()
    print("done")