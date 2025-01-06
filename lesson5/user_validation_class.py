import time


def command(user_input_name:str, *args, **kwargs):
    """
    Simulates a command execution using the authorized user's name.
    Parameters:
    user_input_name (str):
        The currently logged-in user’s name.
    *args:
        Optional positional arguments for the command.
    **kwargs:
        Optional keyword arguments for the command.
    Returns:
        A string acknowledging successful execution.
    """

    print(f"Command executed by {user_input_name}:")
    print("Args:", args)
    print("Kwargs:", kwargs)
    return "Command executed successfully."


class AuthorizationUser:
    """
    Responsible for managing user credentials and authorization sessions.

    Attributes:
        session_timeout (int):
            Duration (in seconds) for which a user remains authorized.
        applied_users (dict):
            Predefined username-password mappings.
        authorized_users (dict):
            Tracks active sessions with login timestamps.
    """

    def __init__(self, session_timeout=5):
        self.session_timeout = session_timeout
        self.applied_users = {'sasha': '1234', 'masha': '2345', 'dasha': '3456', 'bora': '4567'}
        self.authorized_users = {}

    def verify_user(self, user_input_name):
        """
        Authenticates the user by checking credentials or an active session.
        Validates the password if necessary.
        Resets session timeout if the user is re-verified.
        """

        current_time = time.time()

        if user_input_name in self.authorized_users:
            session_start_time = self.authorized_users[user_input_name]
            if current_time - session_start_time < self.session_timeout:
                return True
            else:
                print("--- Session expired. Please input password.")
                self.authorized_users.pop(user_input_name)


        if user_input_name not in self.applied_users:
            print(f"Please input a resolved name.")
            return False


        user_input_password = input(f"Enter the password for '{user_input_name}': ").strip()
        if self.applied_users[user_input_name] != user_input_password:
            print("--- Authorization failed. Incorrect password.")
            return False


        self.authorized_users[user_input_name] = time.time()
        return True


class AuthorizationSystem:
    """
    The AuthorizationSystem class is responsible for managing an interactive user authorization system.
    It validates user identities, authorizes actions for authenticated users, and manages user operations
    within an interactive loop.
    Attributes:
        _init__(self, session_timeout=5) Initializes the AuthorizationSystem with a default session timeout.
        Internally, it creates an instance of AuthorizationUser for managing user authorization.
    """
    def __init__(self, session_timeout=5):
        self.manager = AuthorizationUser(session_timeout=session_timeout)

    def run(self):
        """
        Entry point of the program, managing the user interaction loop.
        """
        print("--- Authorization System Initialized")
        print("Type 'quiet' to exit the program.")

        while True:
            user_input_name = self.prompt_user("Enter your name: ").lower()
            if user_input_name == 'quiet':
                self.exit_program()
                return False

            if not self.authorize_user(user_input_name):
                continue

            self.perform_operations(user_input_name)
            return False

    def prompt_user(self, message):
        """Helper method to safely handle user input."""
        return input(message).strip()

    def authorize_user(self, user_input_name):
        """
        Handles user authorization.
        """
        if not self.manager.verify_user(user_input_name):
            print("Authorization failed. Type 'Name' again : ")
            return False

        return True

    def perform_operations(self, user_input_name):
        """
        Allows the user to perform commands if authorized.
        """
        while True:
            command(user_input_name, example_arg="example_value")
            user_choice = self.prompt_user("Do you want to perform another operation? Y/N: ").lower()
            if user_choice == 'n':
                print("Thank you and goodbye.")
                self.exit_program()
                return False
            elif user_choice == 'y':
                if not self.manager.verify_user(user_input_name):
                    print("--- Reauthorization required.")
                    if not self.authorize_user(user_input_name):
                        break
            else:
                print("--- Invalid choice. Please enter 'Y' or 'N'.")
                break

    def exit_program(self):
        """Safely exits the program."""
        print("Exiting program. Goodbye.")



if __name__ == "__main__":
    AuthorizationSystem(session_timeout=5).run()

