from typing import List
from sqlalchemy.orm import Session
from ..models.buddy_match import BuddyPreferences, BuddyMatch
from ..models.user import UserDB

class BuddyMatcher:
    def __init__(self, db: Session):
        self.db = db

    def find_match(self, user_id: int) -> BuddyMatch:
        # Get user's preferences
        user_prefs = self.db.query(BuddyPreferences).filter(
            BuddyPreferences.user_id == user_id
        ).first()
        
        if not user_prefs:
            return None

        # Find potential matches based on preferences
        potential_matches = self.db.query(BuddyPreferences).filter(
            BuddyPreferences.user_id != user_id,
            BuddyPreferences.addiction_type == user_prefs.addiction_type,
            BuddyPreferences.recovery_stage == user_prefs.recovery_stage
        ).all()

        return potential_matches

    def find_matches(self, user_id: int, limit: int = 5) -> List[dict]:
        user_prefs = self.db.query(BuddyPreferences).filter(
            BuddyPreferences.user_id == user_id
        ).first()

        potential_matches = self.db.query(BuddyPreferences).filter(
            BuddyPreferences.user_id != user_id,
            BuddyPreferences.addiction_type == user_prefs.addiction_type,
            BuddyPreferences.recovery_stage == user_prefs.recovery_stage
        ).all()

        # Score and sort matches
        scored_matches = []
        for match in potential_matches:
            score = self._calculate_compatibility(user_prefs, match)
            scored_matches.append((score, match))

        return [match for _, match in sorted(scored_matches, reverse=True)[:limit]]

    def _calculate_compatibility(self, user_prefs: BuddyPreferences, 
                               potential_match: BuddyPreferences) -> float:
        score = 0.0
        if user_prefs.preferred_contact_frequency == potential_match.preferred_contact_frequency:
            score += 1.0
        if user_prefs.addiction_type == potential_match.addiction_type:
            score += 1.0
        if user_prefs.recovery_stage == potential_match.recovery_stage:
            score += 1.0
        return score
