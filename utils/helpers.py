def safe_action(func):
    """
    A decorator to handle exceptions and log actions for Selenium interactions.
    """
    from functools import wraps
    from selenium.common.exceptions import NoSuchElementException, TimeoutException
    import logging

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TimeoutException as e:
            # Log timeout exceptions and raise to indicate test failure
            logging.error(f"Timeout occurred while executing {func.__name__}: {e}")
            raise
        except NoSuchElementException as e:
            # Log no such element exceptions
            logging.warning(f"Element not found in {func.__name__}: {e}")
            return None
        except Exception as e:
            # Log all other Selenium exceptions
            logging.error(f"An unexpected error occurred in {func.__name__}: {e}")
            raise

    return wrapper