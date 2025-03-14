from flask import session
import firebase_admin
from firebase_admin import credentials, firestore, auth
import requests
import os

firebaseCredentials = credentials.Certificate(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Credentials', 'firebaseCredentials.json'))
APIKey = 'AIzaSyCZmBaKVQJfx-ZF16BByk7Unt8K2LzDjK4'

firebase_admin.initialize_app(firebaseCredentials)
db = firestore.client()

class ExecutionAbort(Exception):
    pass

def verifyUserToken(userIDToken):
    try:
        decodedUserToken = auth.verify_id_token(userIDToken)
        print("[AUTH] Successfully verified user token.")
        return decodedUserToken["uid"]
    except Exception as e:
        raise ExecutionAbort("[AUTH] Invalid token or verification failed.") from e

def signInUser(email, password):
    signInURL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={APIKey}"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    
    response = requests.post(signInURL, json=payload)
    data = response.json()
    
    if "idToken" in data:
        print("[AUTH] Login successful.")
        return verifyUserToken(data["idToken"])
    else:
        print("[AUTH] Login unsuccessful, credentials are incorrect.")
        raise ExecutionAbort("[AUTH] Login failed, credentials are incorrect.")

def createUser(email, password):
    try:
        auth.get_user_by_email(email)
        raise ExecutionAbort("[AUTH] User already exists.")
    except firebase_admin.auth.UserNotFoundError:
        try:
            auth.create_user(email=email, password=password)
            user_id = signInUser(email, password)
            createUserData(email, user_id)
            print("[AUTH] Created new user with email:", email)
            return user_id
        except Exception as e:
            raise ExecutionAbort("[AUTH] Failed to create user with provided email and password.") from e
    except ValueError:
        raise ExecutionAbort("[AUTH] Either email or password has invalid format/characters, try again.")

def deleteUser(user_id):
    if not user_id:
        raise ExecutionAbort("[AUTH] User is not signed in.")
    
    try:
        auth.delete_user(user_id)
        deleteUserData(user_id)
        print("[AUTH] Successfully deleted the user.")
    except Exception as e:
        raise ExecutionAbort("[AUTH] Failed to delete user.") from e

def createUserData(email, user_id):
    if not user_id:
        raise ExecutionAbort("[DATA] Cannot create data for user that is not signed in.")
    
    userData = {
        "userEmail": email,
        "streak": 1,
        "totalScore": 0,
        "bestScore": 0,
        "globalRanking": len(db.collection("users").get()) + 1
    }
    db.collection("users").document(user_id).set(userData)
    print("[DATA] Successfully created user data fields.")

def deleteUserData(user_id):
    if not user_id:
        raise ExecutionAbort("[DATA] Cannot delete data for user that is not signed in.")
    
    db.collection("users").document(user_id).delete()
    print("[DATA] Successfully deleted all user data.")
    

def registerScore(roundScore):
    user_id = session.get("user_id")

    if user_id is None:
        raise ExecutionAbort("[DATA] Cannot update score data for user that is not signed in.")
    
    userSnapshot = db.collection("users").document(user_id).get().to_dict()
    currentTotalScore = getUserTotalScore(user_id)
    currentBestScore = getUserBestScore(user_id)
    
    db.collection("users").document(user_id).update({"totalScore": (currentTotalScore + roundScore)})
    print("[DATA] Updated user's total score.")
    
    if roundScore > currentBestScore:
        db.collection("users").document(user_id).update({"bestScore": roundScore})
        print("[DATA] Updated user's best score.")

def getUserTotalScore():
    user_id = session.get("user_id")

    if user_id is None:
        raise ExecutionAbort("[DATA] Cannot get score data for user that is not signed in.")

    try:
        userSnapshot = db.collection("users").document(user_id).get().to_dict()
        print("[DATA] Successfully fetched user's total score.")
        return userSnapshot.get("totalScore", 0)
    except Exception as e:
        raise ExecutionAbort("[DATA] Error while fetching user's total score.")

def getUserBestScore():
    user_id = session.get("user_id")

    if user_id is None:
        raise ExecutionAbort("[DATA] Cannot get best score data for user that is not signed in.")

    try:
        userSnapshot = db.collection("users").document(user_id).get().to_dict()
        print("[DATA] Successfully fetched user's best score.")
        return userSnapshot.get("bestScore", 0)
    except Exception as e:
        raise ExecutionAbort("[DATA] Error while fetching user's best score.")