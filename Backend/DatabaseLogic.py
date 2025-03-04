import firebase_admin
from firebase_admin import credentials, firestore, auth

import requests

firebaseCredentials = credentials.Certificate("/Users/sinansensurucu/Desktop/the-one-ion-firebase-adminsdk-fbsvc-4767ae4f28.json")
APIKey = "AIzaSyCZmBaKVQJfx-ZF16BByk7Unt8K2LzDjK4"

firebase_admin.initialize_app(firebaseCredentials)

db = firestore.client()

#USER AUTHENTICATION METHODS
def createUser(userEmail, userPassword):
    if checkUserExistence(userEmail):
        print("[DATABASE] User already exists, sign in instead.")

    try:
        user = auth.create_user(email = userEmail, password = userPassword)
    except:
        print("[DATABASE] Failed to create user with provided email and password.")
        return
    print("[DATABASE] Created new user with email:", userEmail)
    
    userIDToken = signInUser(userEmail, userPassword)
    decodedUserToken = verifyUserToken(userIDToken)

    userID = decodedUserToken["uid"]

    createUserData(userID)

def checkUserExistence(userEmail):
    try:
        user = auth.get_user_by_email(userEmail)
        return True
    except firebase_admin.auth.UserNotFoundError:
        return False


def signInUser(userEmail, userPassword):
    signInURL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={APIKey}"

    payload = {
        "email" : userEmail,
        "password" : userPassword,
        "returnSecureToken" : True
    }

    response = requests.post(signInURL, json = payload)

    data = response.json()
    
    if "idToken" in data:
        print("[DATABASE] Login successful")
        return data["idToken"]
    else:
        print("[DATABASE] Login failed, email or password might be incorrect.")
        return None

def verifyUserToken(userIDToken):
    try:
        decodedUserToken = auth.verify_id_token(userIDToken)
        print("[DATABASE] Successfully verified user token.")
        return decodedUserToken
    except:
        print("[DATABASE] Invalid token or verification failed.")
        return None

def deleteUser(userEmail, userPassword):
    userIDToken = signInUser(userEmail, userPassword)
    
    if userIDToken is None:
        print("[DATABASE] Failed to sign in user.")
        return
    
    decodedUserToken = verifyUserToken(userIDToken)

    if decodedUserToken is None:
        print("[DATABASE] Failed to verify userIDToken.")
    
    userID = decodedUserToken["uid"]
    
    auth.delete_user(userID)
    print("[DATABASE] Successfully deleted the user associated with the email:", userEmail)

#USER DATA METHODS
def createUserData(userID):
    data = {
        "streak" : 0,
        "totalScore" : 0,
        "bestScore" : 0,
        "globalRanking" : -9999
    }

    db.collection("users").document(userID).set(data)
    print("[DATABASE] Successfully created user data fields.")



createUser("sinansensurucu@gmail.com", "Sinan!")