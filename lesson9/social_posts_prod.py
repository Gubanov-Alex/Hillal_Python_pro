from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo


@dataclass
class User(ABC):
    name: str
    position: str
    rank: int = 0

    @abstractmethod
    def authorize_channel(self, channel) -> bool:
        pass

@dataclass
class Office(User):
    def authorize_channel(self, channel) -> bool:
        return True

@dataclass
class Cook(User):
    def authorize_channel(self, channel) -> bool:
        return isinstance(channel, CookShmuk)


@dataclass
class Post :
    message: str
    channels: list
    publishers: list[User]
    rank: int
    timestamp: datetime


class ChannelPost(ABC):
    """
    Representation of a channel post functionality.

    Provides an abstract base class for channel posting operations. The primary
    purpose is to enforce the implementation of required methods for various
    channel posting functionalities such as user authorization, health checks,
    and posting messages. This class serves as a template for deriving classes
    handling specific channel integrations.
    """
    def __init__(self, user):
        self.user = user

    @classmethod
    @abstractmethod
    def healthcheck(cls):
        """..."""

    @abstractmethod
    def authorize(self, user, **kwargs):
        """..."""

    @abstractmethod
    def post_a_message(self, user, message: str):
        """..."""


class YouTube(ChannelPost):
    """
    Represents the YouTube class for interfacing with YouTube services.

    This class provides methods to authorize, check the service health,
    and post messages on YouTube. It acts as a simplified client interface
    for interacting with YouTube's functionalities.
    """

    @classmethod
    def healthcheck(cls):
        # if Youtube.healthcheck() is False:
        #     raise Exception("Youtube is not available")
        return True

    def authorize(self, user: User, **kwargs):
        if user.authorize_channel(self):
            print("Some authorization action")
            print(f"Authorized {user} in Twitter")
            return True
        else:
            print(f"Error authorization for {user} in Twitter")
            return False


    def post_a_message(self, user, message: str):
        print(f"{message} from {user.name} {user.position} posted successfully in Youtube\n" + 40 * "=")

class Facebook(ChannelPost):
    """
    A class to represent interactions with Facebook.

    This class encapsulates methods for authorizing, checking health status, and
    posting messages to Facebook. It is designed to simplify and abstract the
    process of interacting with Facebook for developers.
    """


    @classmethod
    def healthcheck(cls):
        # if Facebook.healthcheck() is False:
        #     raise Exception("Facebook is not available")
        return True

    def authorize(self, user: User, **kwargs):
        return user.authorize_channel(self)

    def post_a_message(self, user,message: str) -> None:
        print(f"{message} from {user.name} {user.position} posted successfully in Facebook\n" + 40 * "=")

class Twitter(ChannelPost):
    """
    Represents integration with the Twitter platform.

    This class provides methods to authorize and interact with the Twitter
    platform. It offers functionality such as authorization and posting
    messages, as well as a basic health check to ensure the platform's
    availability.
    """

    @classmethod
    def healthcheck(cls):
        # if Twitter.healthcheck() is False:
        #     raise Exception("Twitter is not available")
        return True

    def authorize(self, user: User, **kwargs):
        if user.authorize_channel(self):
            print("Some authorization action")
            print(f"Authorized {user} in Twitter")
            return True
        else:
            print(f"Error authorization for {user} in Twitter")
            return False


    def post_a_message(self, user, message: str) -> None:
        print(f"{message} from {user.name} {user.position} posted successfully in Twitter\n" + 40 * "=")

class CookShmuk(ChannelPost):
    """
    Example
    """

    @classmethod
    def healthcheck(cls):
        # if CookShmuk.healthcheck() is False:
        #     raise Exception("Youtube is not available")
        return True

    def authorize(self, user: User, **kwargs):
        if user.authorize_channel(self):
            print("Some authorization action")
            print(f"Authorized {user} in CookShmuk")
            return True
        else:
            print(f"Error authorization for {user} in CookShmuk")
            return False


    def post_a_message(self, user, message: str):
        print(f"{message} from {user.name}  {user.position}  posted successfully in CookShmuk\n" + 40 * "=")


class ContentValidator:
    """
    Provides methods to validate content based on specific criteria including
    time and ranking. The class serves as a utility to ensure that certain
    conditions are met before performing further actions. It is assumed that
    the validation logic aligns with predefined business rules.

    """

    def time_validation(self, time: datetime) -> bool:
        current_time = datetime.now(ZoneInfo("UTC"))
        time = time.astimezone(ZoneInfo("UTC"))
        return time < current_time

    def rank_validation(self, post_rank: int, user_rank: int) -> bool:
        return user_rank >= post_rank


class ProcessSchedule(ContentValidator):
    """
    The ProcessSchedule class is responsible for validating and processing schedules of posts
    to be published across various channels by different publishers. It iteratively validates
    the post timestamps and rank compatibility of the message with the publisher before
    attempting to publish the message using the specified channel instances. This class acts
    as a base for managing and processing post schedules effectively.

    """

    def process_schedule(self, posts: list) -> None:
        for post in posts:
            if not self.time_validation(post.timestamp):
                continue
            for channel in post.channels:
                for publisher in post.publishers:
                    if not self.rank_validation(post.rank, publisher.rank):
                        print(
                            f"{publisher.name} with rank {publisher.rank} not allowed to work with message rank {post.rank}.")
                        continue
                    try:
                        channel_instance = channel(publisher)
                        if channel_instance.healthcheck() and channel_instance.authorize(publisher):
                            channel_instance.post_a_message(publisher, post.message)
                    except Exception as e:
                        print(f"Error processing channel {post.channels} for publisher {publisher.name}: {e}")
            print(20 * "^" + "New Message" + 20 * "^")



def main():

    director = Office(
        name= "Sasha",
        position= "General Manager",
        rank = 10
    )

    designer = Office(
        name= "Dasha",
        position= "Creator of content",
        rank = 5
    )

    cook = Cook(name="Den",
                position="Mangal",
                rank = 5
                )

    post_january = Post(message="January is the first message of the year!",
                        channels=[YouTube,Facebook],
                        publishers= [director],
                        rank= 2,
                        timestamp= datetime(2024, 1, 1, 3, 0, 0,tzinfo=ZoneInfo("UTC")))

    post_mart = Post(message="Mart is the start of spring!",
                        channels=[Twitter, Facebook],
                        publishers=[director,designer],
                        rank=7,
                        timestamp=datetime(2024, 3, 1, 3, 0, 0,tzinfo=ZoneInfo("UTC")))



    post_may = Post(message="May is the end of school!",
                     channels=[Twitter, Facebook,YouTube],
                     publishers=[designer, director,cook],
                     rank=3,
                     timestamp=datetime(2024, 3, 1, 3, 0, 0,tzinfo=ZoneInfo("UTC")))

    post_april = Post(message="Let`s fry potato!",
                     channels=[YouTube,Twitter, CookShmuk],
                     publishers=[cook,director],
                     rank= 2,
                     timestamp=datetime(2024, 3, 1, 3, 0, 0,tzinfo=ZoneInfo("UTC")))


    messages_for_post =[post_january, post_mart,post_may,post_april]
    scheduler = ProcessSchedule()
    scheduler.process_schedule(messages_for_post)

main()













