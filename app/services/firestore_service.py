from google.cloud import firestore
import logging

logger = logging.getLogger(__name__)

import time

class FirestoreService:
    """
    Service to handle interactions with Google Cloud Firestore.
    Uses in-memory caching to reduce latency and API costs.
    """
    
    def __init__(self):
        self.db = firestore.Client()
        self._faq_cache = None
        self._last_fetch = 0
        self._cache_ttl = 600  # 10 minutes

    def get_faqs(self):
        """Fetches public FAQs with caching."""
        current_time = time.time()
        
        # Return cached version if still valid
        if self._faq_cache and (current_time - self._last_fetch < self._cache_ttl):
            return self._faq_cache

        try:
            faqs_ref = self.db.collection("faqs")
            docs = faqs_ref.stream()
            self._faq_cache = [doc.to_dict() for doc in docs]
            self._last_fetch = current_time
            return self._faq_cache
        except Exception:
            logger.error("Failed to fetch FAQs from Firestore")
            return self._faq_cache or []

# Singleton instance
firestore_service = FirestoreService()
