import firebase_admin
from firebase_admin import credentials, firestore, auth
import requests
import sys

class ExecutionAbort(Exception):
    pass

# FIREBASE SETUP
firebaseCredentials = credentials.Certificate("/Users/sinansensurucu/Desktop/the-one-ion-firebase-adminsdk-fbsvc-4767ae4f28.json")
APIKey = "AIzaSyCZmBaKVQJfx-ZF16BByk7Unt8K2LzDjK4"

firebase_admin.initialize_app(firebaseCredentials)
db = firestore.client()
userID = None

# USER AUTHENTICATION METHODS
def verifyUserToken(userIDToken):
    try:
        decodedUserToken = auth.verify_id_token(userIDToken)
        print("[AUTH] Successfully verified user token.")
        global userID
        userID = decodedUserToken["uid"]
    except Exception as e:
        raise ExecutionAbort("[AUTH] Invalid token or verification failed.") from e

def createUser(userEmail, userPassword):
    try:
        auth.get_user_by_email(userEmail)
        raise ExecutionAbort("[AUTH] User already exists.")
    except firebase_admin.auth.UserNotFoundError:
        try:
            auth.create_user(email=userEmail, password=userPassword)
            signInUser(userEmail, userPassword)
            createUserData(userEmail)
            print("[AUTH] Created new user with email:", userEmail)
        except Exception as e:
            raise ExecutionAbort("[AUTH] Failed to create user with provided email and password.") from e
    except ValueError:
        raise ExecutionAbort("[AUTH] Either email or password has invalid format/characters, try again.")
    except ExecutionAbort as e:
        raise ExecutionAbort(str(e))

def signInUser(userEmail, userPassword):
    if userID is not None:
        raise ExecutionAbort("[AUTH] User is already signed in. Sign out and try again.")

    signInURL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={APIKey}"
    payload = {
        "email": userEmail,
        "password": userPassword,
        "returnSecureToken": True
    }
    
    response = requests.post(signInURL, json=payload)
    data = response.json()
    
    if "idToken" in data:
        print("[AUTH] Login successful.")
        verifyUserToken(data["idToken"])
    else:
        raise ExecutionAbort("[AUTH] Login failed, credentials are incorrect.")

def deleteUser():
    if userID is None:
        raise ExecutionAbort("[AUTH] User is not signed in.")
    
    try:
        auth.delete_user(userID)
        deleteUserData()
        print("[AUTH] Successfully deleted the user that is currently signed in.")
        signOutUser()
    except Exception as e:
        raise ExecutionAbort("[AUTH] Failed to delete user.") from e

def signOutUser():
    global userID
    userID = None
    print("[AUTH] User signed out.")

#USER DATA METHODS
def createUserData(userEmail):
    if userID is None:
        raise ExecutionAbort("[DATA] Cannot create data for user that is not signed in.")

    userData = {
        "userEmail" : userEmail,
        "streak" : 1,
        "totalScore" : 0,
        "bestScore" : 0,
        "globalRanking" : len(db.collection("users").get()) + 1
    }

    db.collection("users").document(userID).set(userData)
    print("[AUTH] Successfully created user data fields.")


def deleteUserData():
    if userID is None:
        raise ExecutionAbort("[DATA] Cannot delete data for user that is not signed in.")
    
    db.collection("users").document(userID).delete()
    print("[DATA] Successfully deleted all user data.")

def registerScore(roundScore):
    if userID is None:
        raise ExecutionAbort("[DATA] Cannot update score data for user that is not signed in.")
    
    userSnapshot = db.collection("users").document(userID).get().to_dict()
    currentTotalScore = getUserTotalScore()
    currentBestScore = getUserBestScore()
    
    db.collection("users").document(userID).update({"totalScore": (currentTotalScore + roundScore)})
    print("[DATA] Updated user's total score.")

    if roundScore > currentBestScore:
        db.collection("users").document(userID).update({"bestScore": roundScore})
        print("[DATA] Updated user's best score.")

def getUserTotalScore():
    try:
        userSnapshot = db.collection("users").document(userID).get().to_dict()
        print("[DATA] Successfully fetched user's total score.")
        return userSnapshot.get("totalScore", 0)
    except Exception as e:
        raise ExecutionAbort("[DATA] Error while fetching user's total score.")

def getUserBestScore():
    try:
        userSnapshot = db.collection("users").document(userID).get().to_dict()
        print("[DATA] Successfully fetched user's best score.")
        return userSnapshot.get("bestScore", 0)
    except Exception as e:
        raise ExecutionAbort("[DATA] Error while fetching user's best score.")






while True:
    try:
        exec(input("--> "))
    except Exception as e:
        print(str(e))
