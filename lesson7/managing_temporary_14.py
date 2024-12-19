import logging
from copy import deepcopy

# Configure logging for debugging and tracking operations
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Global configuration representing application settings
GLOBAL_CONFIG = {
    "feature_a": True,
    "feature_b": False,
    "max_retries": 3
}


class Configuration:
    def __init__(self, updates, validator=None):

        """Context manager for temporarily modifying the global configuration."""

        # Store the updates and the optional validator
        self.updates = updates
        self.validator = validator

        # To store the original state of the global configuration
        self.original_config = None

    def __enter__(self):
        """
        Enter the context manager. Apply the configuration updates and validate if required.
        """
        # TODO: Save a copy of the current GLOBAL_CONFIG so it can be restored later.
        self.original_config = deepcopy(GLOBAL_CONFIG)

        # TODO: Apply the updates to the GLOBAL_CONFIG.
        GLOBAL_CONFIG.update(self.updates)

        # TODO: Log the changes for debugging purposes.
        logging.info("Applied temporary updates enter: %s", self.updates)

        # If the validation fails, log the error and restore the original configuration.
        if self.validator:
            try:
                if not self.validator(GLOBAL_CONFIG):
                    raise ValueError("Validation Failed enter")
            except Exception as e:
                # TODO: If an exception occurs within the context block, ensure the original configuration is restored.
                GLOBAL_CONFIG.update(self.original_config)
                logging.error("Validation failed. Restored original enter: %s", self.original_config)
                raise e
        return self



    def __exit__(self, exc_type, exc_value, traceback):
        """
        Exit the context manager. Restore the original configuration.
        """

        # TODO: If a validator is provided, check the modified configuration.
        if self.validator is None or self.validator(GLOBAL_CONFIG):
            logging.info("Validator is provided successfully exit: %s", GLOBAL_CONFIG)

        # TODO: If an exception occurs within the context block, ensure the original configuration is restored.
        GLOBAL_CONFIG.update(self.original_config)
        logging.info("Restored original configuration exit: %s", self.original_config)

        if exc_type:
            logging.error("Exception occurred exit: %s", exc_value)
        return False

# Example validator function (Optional)
def validate_config(config: dict) -> bool:
    """
    Example validator function to check the validity of the configuration.
    Returns True if the configuration is valid, False otherwise.
    """

    errors = []
    # TODO: Implement validation logic, e.g., ensure 'max_retries' is non-negative.
    if config.get("feature_a") == "invalid_value":
        errors.append("Invalid value for feature_a.")

    if config.get("feature_b") == "invalid_value":
        errors.append("Invalid value for feature_b.")

    if config.get("max_retries", 0) < 0:
        errors.append("max_retries should be >= 0.")

    if errors:
        for error in errors:
            logging.error(error)
        return False
    return True

# Example usage (for students to test once implemented)
if __name__ == "__main__":
    logging.info("Initial GLOBAL_CONFIG: %s", GLOBAL_CONFIG)

    # Example 1: Successful configuration update
    try:
        # TODO: Use the Configuration context manager to update 'feature_a' and 'max_retries'
        with Configuration({"feature_a": False, "max_retries": 5}):
            logging.info("Inside context: %s", GLOBAL_CONFIG)
    except Exception as e:
        logging.error("Error: %s", e)

    logging.info("After context: %s", GLOBAL_CONFIG)

    # Example 2: Configuration update with validation failure
    try:
        # TODO: Use the Configuration context manager with invalid updates and a validator
        # to see how the context handles validation errors.
        with Configuration({"feature_a": "invalid_value", "max_retries": -1}, validator=validate_config):
            logging.info("This should not be printed if validation fails.")
    except Exception as e:
        logging.error("Caught exception: %s", e)

    logging.info("After failed context: %s", GLOBAL_CONFIG)