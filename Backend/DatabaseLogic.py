from flask import session
import firebase_admin
from firebase_admin import credentials, firestore, auth
import requests
import random
import os

firebaseCredentials = credentials.Certificate(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'Credentials', 'firebaseCredentials.json'))
APIKey = 'AIzaSyCZmBaKVQJfx-ZF16BByk7Unt8K2LzDjK4'

firebase_admin.initialize_app(firebaseCredentials)
db = firestore.client()

class ExecutionAbort(Exception):
    pass

#Authentication Functionality

#returns user_id as string to frontend after signing in user
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
        return __verifyUserToken__(data["idToken"])
    else:
        print("[AUTH] Login unsuccessful, credentials are incorrect.")
        raise ExecutionAbort("[AUTH] Login failed, credentials are incorrect.")

#returns user_id as string to frontend after creating a user
def createUser(email, password):
    try:
        auth.get_user_by_email(email)
        raise ExecutionAbort("[AUTH] User already exists.")
    except firebase_admin.auth.UserNotFoundError:
        try:
            auth.create_user(email=email, password=password)
            user_id = signInUser(email, password)
            __createUserData__(email, user_id)
            print("[AUTH] Created new user with email:", email)
            return user_id
        except:
            raise ExecutionAbort("[AUTH] Failed to create user with provided email and password.")
    except ValueError:
        raise ExecutionAbort("[AUTH] Either email or password has invalid format/characters, try again.")

#deletes user account without returning anything
def deleteUser(user_id):
    if not user_id:
        raise ExecutionAbort("[AUTH] User is not signed in.")
    
    try:
        auth.delete_user(user_id)
        __deleteUserData__(user_id)
        print("[AUTH] Successfully deleted the user.")
    except:
        raise ExecutionAbort("[AUTH] Failed to delete user.")

#METHODS BELOW NOT FOR FRONTEND CALL
def __verifyUserToken__(userIDToken):
    try:
        decodedUserToken = auth.verify_id_token(userIDToken)
        print("[AUTH] Successfully verified user token.")
        return decodedUserToken["uid"]
    except:
        raise ExecutionAbort("[AUTH] Invalid token or verification failed.")
    
def __createUserData__(email, user_id):
    if not user_id:
        raise ExecutionAbort("[DATA] Cannot create data for user that is not signed in.")
    
    userData = {
        "userEmail" : email,
        "streak" : 1,
        "totalScore" : 0,
        "bestScore" : 0,
        "globalRanking" : len(db.collection("users").get()) + 1,
        "readArticles" : [],
        "readStatistics" : []
    }
    db.collection("users").document(user_id).set(userData)
    print("[DATA] Successfully created user data fields.")

def __deleteUserData__(user_id):
    if not user_id:
        raise ExecutionAbort("[DATA] Cannot delete data for user that is not signed in.")
    
    db.collection("users").document(user_id).delete()
    print("[DATA] Successfully deleted all user data.")



#User Profile Functionality

#registers new score to user profile without returning anything
def registerScore(user_id, score):
    if user_id is None:
        raise ExecutionAbort("[DATA] Cannot update score data for user that is not signed in.")
    
    try:
        currentTotalScore = getUserTotalScore(user_id)
        currentBestScore = getUserBestScore(user_id)
        
        db.collection("users").document(user_id).update({"totalScore": (currentTotalScore + score)})
        print("[DATA] Updated user's total score.")
        
        if score > currentBestScore:
            db.collection("users").document(user_id).update({"bestScore": score})
            print("[DATA] Updated user's best score.")
    except:
        raise ExecutionAbort("[DATA] Error while registering score to user.")

#returns integer value containing user's total score
def getUserTotalScore(user_id):
    if user_id is None:
        raise ExecutionAbort("[DATA] Cannot get score data for user that is not signed in.")

    try:
        userSnapshot = db.collection("users").document(user_id).get().to_dict()
        print("[DATA] Successfully fetched user's total score.")
        return userSnapshot.get("totalScore", 0)
    except:
        raise ExecutionAbort("[DATA] Error while fetching user's total score.")

#returns integer value containing user's best score
def getUserBestScore(user_id):
    if user_id is None:
        raise ExecutionAbort("[DATA] Cannot get best score data for user that is not signed in.")

    try:
        userSnapshot = db.collection("users").document(user_id).get().to_dict()
        print("[DATA] Successfully fetched user's best score.")
        return userSnapshot.get("bestScore", 0)
    except:
        raise ExecutionAbort("[DATA] Error while fetching user's best score.")
    
#sets users streak without returning anything
def setUserStreak(user_id, streak):
    if user_id is None:
        raise ExecutionAbort("[DATA] Cannot update streak data for user that is not signed in.")
    
    try:
        db.collection("users").document(user_id).update({"streak": streak})
        print("[DATA] Updated user's streak.")
    except:
        raise ExecutionAbort("[DATA] Error while updating user's streak.")

#returns integer value containing user's current streak
def getUserStreak(user_id):
    if user_id is None:
        raise ExecutionAbort("[DATA] Cannot get streak data for user that is not signed in.")
    
    try:
        userSnapshot = db.collection("users").document(user_id).get().to_dict()
        print("[DATA] Successfully fetched user's streak.")
        return userSnapshot.get("streak", 0)
    except:
        raise ExecutionAbort("[DATA] Error while fetching user's streak.")

#returns integer value containing user's global ranking
def getGlobalRanking(user_id):
    if user_id is None:
        raise ExecutionAbort("[DATA] Cannot get ranking data for user that is not signed in.")
    
    try:
        userSnapshot = db.collection("users").get()

        user_scores = []

        for doc in userSnapshot:
            data = doc.to_dict()
            if data is None:
                continue
            score = data.get("totalScore", 0)
            user_scores.append((doc.id, score))

        user_scores = sorted(user_scores, key = lambda x: x[1], reverse = True)

        for rank, (uid, score) in enumerate(user_scores, start = 1):
            if uid == user_id:
                return rank
            
        print("[DATA] Successfully fetched user's ranking.")
        
    except:
        raise ExecutionAbort("[DATA] Error while fetching user's ranking.")

def getUserEmail(user_id):
    if user_id is None:
        raise ExecutionAbort("[DATA] Cannot get email data for user that is not signed in.")
    
    try:
        userSnapshot = db.collection("users").document(user_id).get().to_dict()
        print("[DATA] Successfully fetched user's email.")
        return userSnapshot.get("userEmail", user_id)
    except:
        raise ExecutionAbort("[DATA] Error while fetching user's email.")

#Article and Statistics Functionality

#returns single article that user hasn't solved (if solved all, returns a random article) 
#as string as tuple of (title, content, link, answer), it also marks the returned article as read
#save answer return value to check against user answer.
def getArticleToSolve(user_id):
    if user_id is None:
        raise ExecutionAbort("[DATA] Cannot get article for user that is not signed in.")
     
    try:
        solvedArticleIDs = sorted(__getArticlesSolved__(user_id))

        allArticleIDs = sorted(__getAllArticles__())

        if solvedArticleIDs == allArticleIDs:
            return random.choice(allArticleIDs)

        availableArticles = [article for article in allArticleIDs if article not in solvedArticleIDs]
        
        articleToSolve = random.choice(availableArticles) 
     
        __addArticleAsSolved__(user_id, articleToSolve)

        return __getArticleByID__(articleToSolve)

    except:
        raise ExecutionAbort("[DATA] Error while fetching user's available article data.")
    
def getStatisticToSolve(user_id):
    if user_id is None:
        raise ExecutionAbort("[DATA] Cannot get statistic for user that is not signed in.")
     
    try:
        solvedStatisticIDs = sorted(__getStatisticsSolved__(user_id))

        allStatisticsIDs = sorted(__getAllStatistics__())

        if solvedStatisticIDs == allStatisticsIDs:
            return random.choice(allStatisticsIDs)

        availableStatistics = [article for article in allStatisticsIDs if article not in solvedStatisticIDs]
        
        statisticToSolve = random.choice(availableStatistics) 
     
        __addArticleAsSolved__(user_id, statisticToSolve)

        return __getStatisticByID__(statisticToSolve)

    except:
        raise ExecutionAbort("[DATA] Error while fetching user's available article data.")

#returns a list of tuples containing (rank, userEmail, and userScore) for the ranks
def getLeaderboard():
    try:
        userSnapshot = db.collection("users").get()

        user_scores = []

        for doc in userSnapshot:
            data = doc.to_dict()
            if data is None:
                continue
            score = data.get("totalScore", 0)
            user_scores.append((doc.id, score))

        user_scores = sorted(user_scores, key = lambda x: x[1], reverse = True)

        results = [(rank, getUserEmail(uid), score) for rank, (uid, score) in enumerate(user_scores, start = 1)]

        print("[DATA] Successfully fetched user's ranking.")

        return results
            
    except:
        print("[DATA] Error while fetching leaderboard.")

#METHODS BELOW ARE NOT FOR FRONTEND CALLS
def __getAllArticles__():
    articlesSnapshot = db.collection("articles").get()

    return [a.id for a in articlesSnapshot]

def __getArticleByID__(article_id):
    if article_id is None:
        raise ExecutionAbort("[DATA] Cannot get article for non-existent article id.")

    articleSnapshot = db.collection("articles").document(article_id).get().to_dict()

    articleTitle = articleSnapshot.get("title")
    articleContent = articleSnapshot.get("content")
    articleLink = articleSnapshot.get("link")
    articleAnswer = articleSnapshot.get("answer")

    return articleTitle, articleContent, articleLink, articleAnswer

def __getArticlesSolved__(user_id):
    if user_id is None:
        raise ExecutionAbort("[DATA] Cannot get article data for user that is not signed in.")
    
    try:
        userSnapshot = db.collection("users").document(user_id).get().to_dict()
        print("[DATA] Successfully fetched user's read articles.")

        return userSnapshot.get("readArticles", [])
    except:
        raise ExecutionAbort("[DATA] Error while fetching user's article data.")
    
def __addArticleAsSolved__(user_id, article_id):
    if user_id is None:
        raise ExecutionAbort("[DATA] Cannot get article data for user that is not signed in.")
    
    try:
        db.collection("users").document(user_id).update({"readArticles": (__getArticlesSolved__(user_id) + [article_id])})
        print("[DATA] Successfully updated user's read articles.")

    except:
        raise ExecutionAbort("[DATA] Error while fetching user's article data.")
    
def __getAllStatistics__():
    statisticsSnapshot = db.collection("statistics").get()

    return [s.id for s in statisticsSnapshot]

def __getStatisticByID__(statistic_id):
    if statistic_id is None:
        raise ExecutionAbort("[DATA] Cannot get statistic for non-existent article id.")

    statisticSnapshot = db.collection("articles").document(statistic_id).get().to_dict()

    statisticContent = statisticSnapshot.get("content")
    statisticLink = statisticSnapshot.get("link")
    statisticAnswer = statisticSnapshot.get("answer")

    return statisticContent, statisticLink, statisticAnswer

def __getStatisticsSolved__(user_id):
    if user_id is None:
        raise ExecutionAbort("[DATA] Cannot get statistic data for user that is not signed in.")
    
    try:
        userSnapshot = db.collection("users").document(user_id).get().to_dict()
        print("[DATA] Successfully fetched user's read statistics.")

        return userSnapshot.get("readStatistics", [])
    except:
        raise ExecutionAbort("[DATA] Error while fetching user's statistics data.")
    
def __addStatisticAsSolved__(user_id, statistic_id):
    if user_id is None:
        raise ExecutionAbort("[DATA] Cannot get statistic data for user that is not signed in.")
    
    try:
        db.collection("users").document(user_id).update({"readStatistics": (__getStatisticsSolved__(user_id) + [statistic_id])})
        print("[DATA] Successfully updated user's read statistics.")

    except:
        raise ExecutionAbort("[DATA] Error while fetching user's statistics data.")