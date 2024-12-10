import time

SESSION_TIMEOUT = 5

applied_users = {'sasha': '1234', 'masha': '2345', 'dasha': '3456', 'bora': '4567'}

authorized_users = {}


def auth_user_input(func):
    """
        A decorator function to handle user authentication for any decorated function.

        If the user is already authorized and the session is still valid, the decorated function will execute.
        Otherwise, the user is prompted to input their password for re-authentication.

        If the user is not in the registered users' list or provides an incorrect password, they are denied access.

        Parameters:
            f (function): The function to be executed after successful authentication.

        Returns:
            function: The wrapped version of the given function with authentication checks.
        """
    def wrapped(user_input_name:str, *args, **kwargs):
        current_time = time.time()
        # Check if the user is already authorized
        if user_input_name in authorized_users:
            session_start_time = authorized_users[user_input_name]
            if current_time - session_start_time < SESSION_TIMEOUT:
                return func(*args, **kwargs)
            else:
                print("--- Session expired. Please input password.")
                authorized_users.pop(user_input_name)
                return None

        print(f"--- User '{user_input_name}' is not authorized.")
        user_input_password = input("Enter the Password: ")

        if applied_users[user_input_name] != user_input_password:
            print("--- Authorization failed\nPlease input a correct password.")
            return None

        authorized_users[user_input_name] = time.time()
        return func(user_input_name,*args, **kwargs)
    return wrapped

@auth_user_input
def command(*args, **kwargs):
    """
        A sample function to simulate a command execution for an authorized user.

        This function is wrapped with `auth_user_input` to ensure that the user is authenticated
        before executing the command.

        Parameters:
            *args: Positional arguments for the command.
            **kwargs: Keyword arguments for the command.

        Returns:
            str: A success message ("ok") after executing the command.
        """
    print("-----some message----" , args)
    print("-----some result----" , kwargs)
    return "ok"



def main():
    """
        The main function to start the authorization system and interact with users.

        This function implements:
        - Continuous checks for user input
        - Authorization attempts using usernames and passwords
        - Command executions after successful authorization
        - Safe program exit when the user inputs "quiet"
        """
    print("--- Authorization begin\nPlease input a resolved name.")
    while True:
        user_input_name = input("Enter the Name: ").strip().lower()
        if user_input_name == 'quiet':
            print('Thank you and bye.')
            break
        elif user_input_name not in applied_users:
            print("--- Authorization failed\nPlease input a resolved name.")
            continue

        if not command(user_input_name):
            continue
        while True:
            user_input_operation = input('Do you want to make operation: Y/N ').strip().lower()
            if user_input_operation == 'y':
                if not command(user_input_name):
                    break
            else:
                print('Thank you and bye.')
                return False

if __name__ == "__main__":
    main()

# assert command('sasha','1234',234,455,'ewer')
# assert command('masha','2345',7777,'aew','ewer')
# print('Ok!')



