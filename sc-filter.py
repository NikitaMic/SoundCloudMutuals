#!/usr/bin/env python3
"""
SoundCloud Location Filter - Simple CLI Tool
Find SoundCloud users by location from a user's followings.
"""

import argparse
import sys
from soundcloud_api import SoundCloudAPI


def filter_by_location(users, location):
    """Filter users by location string."""
    location_lower = location.lower().strip()
    matched = []

    for user in users:
        user_location = user.get('location') or ''
        if location_lower in user_location.lower():
            matched.append(user)

    return matched


def display_results(users, location):
    """Display results in console."""
    if not users:
        print(f"\n❌ No users found in '{location}'\n")
        return

    print(f"\n{'=' * 80}")
    print(f"✅ Found {len(users)} users in '{location}':")
    print(f"{'=' * 80}\n")

    for i, user in enumerate(users, 1):
        username = user.get('permalink', 'N/A')
        full_name = user.get('full_name', '')
        location = user.get('location', 'N/A')
        followers = user.get('followers_count', 0)
        profile_url = user.get('permalink_url', 'N/A')

        print(f"{i}. {username}")
        if full_name:
            print(f"   Name: {full_name}")
        print(f"   Location: {location}")
        print(f"   Followers: {followers:,}")
        print(f"   URL: {profile_url}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description='🎵 Find SoundCloud users by location',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s gloomweaver777 Tbilisi
  %(prog)s gloomweaver777 Berlin
  %(prog)s gloomweaver777 "New York"
        """
    )

    parser.add_argument('username', help='SoundCloud username to analyze')
    parser.add_argument('location', help='Location to filter (e.g., "Berlin", "Georgia")')
    parser.add_argument('--quiet', action='store_true', help='Minimal output')

    args = parser.parse_args()

    if not args.quiet:
        print(f"\n{'=' * 80}")
        print(f"🎵 SoundCloud Location Filter")
        print(f"{'=' * 80}")
        print(f"User: {args.username}")
        print(f"Location: {args.location}")
        print(f"{'=' * 80}\n")

    # Fetch followings
    if not args.quiet:
        print("⏳ Fetching followings from SoundCloud API...")

    try:
        api = SoundCloudAPI()
        followings = api.get_user_followings_by_username(args.username)

        if not args.quiet:
            print(f"✓ Found {len(followings)} followings\n")
    except Exception as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        sys.exit(1)

    # Add location data from API
    if not args.quiet:
        print("⏳ Processing location data...")

    users_with_location = 0
    for user in followings:
        if user.get('city'):
            user['location'] = user['city']
            if user.get('country_code'):
                user['location'] += f", {user['country_code']}"
            users_with_location += 1
        else:
            user['location'] = None

    if not args.quiet:
        print(f"✓ {users_with_location}/{len(followings)} users have location data\n")

    # Filter by location
    if not args.quiet:
        print(f"⏳ Filtering for '{args.location}'...")

    filtered = filter_by_location(followings, args.location)

    if not args.quiet:
        print(f"✓ Found {len(filtered)} matches\n")

    # Display results
    display_results(filtered, args.location)

    sys.exit(0 if filtered else 1)


if __name__ == '__main__':
    main()
