"""
SoundCloud API client module for fetching user followings.
Uses the public/undocumented SoundCloud API v2 endpoints.
"""

import requests
import time
from typing import List, Dict, Optional


class SoundCloudAPI:
    """Client for interacting with SoundCloud's public API."""

    BASE_URL = "https://api-v2.soundcloud.com"
    WEB_BASE_URL = "https://soundcloud.com"

    def __init__(self, client_id: Optional[str] = None):
        """
        Initialize the SoundCloud API client.

        Args:
            client_id: Optional client ID. If not provided, will extract from web page.
        """
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        self.client_id = client_id
        self.rate_limit_delay = 0.5  # seconds between requests

    def _get_client_id(self) -> str:
        """Extract client_id from SoundCloud's web page."""
        if self.client_id:
            return self.client_id

        try:
            response = self.session.get(self.WEB_BASE_URL)
            response.raise_for_status()

            # Look for script tags containing client_id
            import re
            scripts = re.findall(r'<script[^>]+src="([^"]+)"', response.text)

            for script_url in scripts:
                if 'sndcdn.com' in script_url:
                    try:
                        script_response = self.session.get(script_url)
                        match = re.search(r'client_id[=:]"([a-zA-Z0-9]+)"', script_response.text)
                        if match:
                            self.client_id = match.group(1)
                            return self.client_id
                    except:
                        continue

        except Exception as e:
            raise RuntimeError(f"Failed to extract client_id: {e}")

        raise RuntimeError("Could not find client_id")

    def resolve_user(self, username: str) -> Dict:
        """
        Resolve a username to get user ID and details.

        Args:
            username: SoundCloud username/permalink

        Returns:
            User data dictionary
        """
        client_id = self._get_client_id()
        url = f"{self.BASE_URL}/resolve"
        params = {
            'url': f'{self.WEB_BASE_URL}/{username}',
            'client_id': client_id
        }

        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_followings(self, user_id: int, limit: int = 200) -> List[Dict]:
        """
        Get all users that a user follows.

        Args:
            user_id: SoundCloud user ID
            limit: Number of results per page (max 200)

        Returns:
            List of user dictionaries
        """
        client_id = self._get_client_id()
        all_followings = []
        next_href = f"{self.BASE_URL}/users/{user_id}/followings"

        while next_href:
            params = {
                'client_id': client_id,
                'limit': limit
            }

            # If next_href already contains params, don't add them again
            if '?' in next_href:
                response = self.session.get(next_href)
            else:
                response = self.session.get(next_href, params=params)

            response.raise_for_status()
            data = response.json()

            collection = data.get('collection', [])
            all_followings.extend(collection)

            # Check for next page
            next_href = data.get('next_href')

            if next_href:
                time.sleep(self.rate_limit_delay)

            print(f"Fetched {len(all_followings)} followings so far...")

        return all_followings

    def get_user_followings_by_username(self, username: str) -> List[Dict]:
        """
        Get all followings for a user by their username.

        Args:
            username: SoundCloud username/permalink

        Returns:
            List of user dictionaries
        """
        user_data = self.resolve_user(username)
        user_id = user_data['id']
        return self.get_followings(user_id)
