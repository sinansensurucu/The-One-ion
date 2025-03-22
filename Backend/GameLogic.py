import time
from datetime import datetime
import random
from Backend.DatabaseLogic import (
    getArticleToSolve, registerScore, getUserStreak, setUserStreak,
    getGlobalRanking, getUserTotalScore, getUserBestScore, getLeaderboard,
    getStatisticToSolve, getUserEmail
)

class GameLogic:
    def __init__(self, user_id):
        self.user_id = user_id
        self.start_time = time.time()  # starts timer when the game begins

    def calculate_score(self, is_correct): # is_correct should come from database
        """
        Calculate the user's score based on correctness and time taken.
        Score strts at 100 and -1 every second
        parameter "is_correct" needs to be sent into this method, boolean y/n if user guessed right
        :return: The calculated score.
        """
        end_time = time.time()
        elapsed_time = end_time - self.start_time
        base_score = 100 if is_correct else 0
        time_penalty = int(elapsed_time)  # Deduct 1 point per second
        final_score = max(base_score - time_penalty, 0)  # Ensure score doesn't go below 0
        return final_score

    def update_user_profile(self, is_correct, score): # is_correct should come from database
        """
        Update the user's profile with the new score and streak
        parameter "is_correct" boolean indicating if the user's answer was correct
        parameter "score" the score to add to the user's total score
        """
        registerScore(self.user_id, score)
        if is_correct:
            current_streak = getUserStreak(self.user_id)
            setUserStreak(self.user_id, current_streak + 1)
        else:
            setUserStreak(self.user_id, 0)  # Reset streak if incorrect

    def get_daily_challenge(self): # needs information from database, further work needed
        """
        fetch a daily challenge article for the user
        returns a tuple of (article, is_new_challenge)
        """
        last_challenge_date = self._get_last_challenge_date()
        today = datetime.now().date()

        if last_challenge_date != today:
            # fetch a new article for the daily challenge
            article = getArticleToSolve(self.user_id)
            self._update_last_challenge_date(today)
            return article, True
        else: # user alr done challenge
            return None, False
    