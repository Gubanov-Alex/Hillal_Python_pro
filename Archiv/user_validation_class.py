import time


def command(user_input_name, *args, **kwargs):
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


def main():
    """
    Entry point of the program, managing the user interaction loop.
    Workflow:
        Initializes the AuthorizationUser manager.
        Prompts the user to log in with a valid username/password.
        Allows authorized users to perform operations or revalidate after session expiration.
    Users can exit the program by typing quiet.
    """

    manager = AuthorizationUser(session_timeout=10)

    print("--- Authorization System Initialized")
    print("Type 'quiet' to exit the program.")

    while True:
        user_input_name = input("Enter your name: ").strip().lower()
        if not manager.verify_user(user_input_name):
            retry_option = input(
                "Authorization failed. Type 'retry' to try again or 'quiet' to exit: ").strip().lower()
            if retry_option == 'quiet':
                print("Exiting program. Goodbye!")
                return False
            elif retry_option == 'retry':
                continue

        if user_input_name == 'quiet':
            print("Exiting program. Goodbye!")
            return False

        else:
            command(user_input_name, example_arg="example_value")
            while True:
                user_input_operation = input('Do you want to make operation: Y/N : ').strip().lower()
                if user_input_operation == 'y':
                    if not manager.verify_user(user_input_name):
                        retry_option = input(
                            "Authorization failed. Type 'retry' to try again or 'quiet' to exit: ").strip().lower()
                        if retry_option == 'quiet':
                            print("Exiting program. Goodbye!")
                            return False
                        elif retry_option == 'retry':
                            continue
                    command(user_input_name, example_arg="example_value")
                    continue
                else :
                    print("Thank you and bye.")
                return False

if __name__ == "__main__":
    main()

# while True:
#     user_input_operation = input('Do you want to make operation: Y/N : ').strip().lower()
#     if user_input_operation == 'y':
#         if not manager.verify_user(user_input_name):
#             retry_option = input(
#                 "Authorization failed. Type 'retry' to try again or 'quiet' to exit: ").strip().lower()
#             if retry_option == 'quiet':
#                 print("Exiting program. Goodbye!")
#                 return False
#             elif retry_option == 'retry':
#                 break
#         else:
#             command(user_input_name, example_arg="example_value")
#             continue
#     else:
#         print("Thank you and bye.")
#     return False

