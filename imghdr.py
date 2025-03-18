"""
Mock implementation of imghdr for Python 3.13+ compatibility with tweepy.

The imghdr module was deprecated in Python 3.11 and completely removed in Python 3.13.
This mock implementation provides the minimum functionality needed for tweepy to work.

Note: This mock only supports text-based tweets. Image posting will not work with this implementation.
If you need to post images, please use Python 3.11 or earlier, or wait for tweepy to update their library.
"""


def what(file, h=None):
    """
    Mock implementation that just returns None for all files.

    In the original imghdr module, this function would attempt to determine the type
    of image contained in the file.

    Args:
        file: A filename (string) or file object
        h: The first 32 bytes of the file, or None

    Returns:
        None always, as this is just a mock
    """
    return None


# These tests are needed by tweepy
tests = []
