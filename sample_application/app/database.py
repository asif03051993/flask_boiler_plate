
from flask_sqlalchemy import SQLAlchemy
import functools

# set autocommit as false (default) to use transaction for all queries
# by making autocommit as true we can track which queries are getting committed or rolling back .
db = SQLAlchemy(session_options={'autocommit': True, 'autoflush': False})

def drop_all():
    db.drop_all()


def create_all():
    db.create_all()


def remove_session():
    db.session.remove()

class TRANSACTIONAL_OPTIONS:
    NESTED = 1
    SUBTRANSACTIONS = 2

import contextlib

@contextlib.contextmanager
def transactional_session(transaction_option = TRANSACTIONAL_OPTIONS.SUBTRANSACTIONS):
    """Context manager which provides transaction management for the nested
       block. A transaction is started when the block is entered, and then either
       committed if the block exits without incident, or rolled back if an error
       is raised.

       Nested (SAVEPOINT) transactions is passed, meaning that this context manager can be nested within another and the
       transactions treated as independent units-of-work from the perspective of the nested
       blocks. If the error is handled further up the chain, the outer transactions will
       still be committed, while the inner ones will be rolled-back independently."""

    if transaction_option == TRANSACTIONAL_OPTIONS.SUBTRANSACTIONS:
        db.session.begin(subtransactions=True)
    elif transaction_option == TRANSACTIONAL_OPTIONS.NESTED:
        db.session.begin(nested=True)
    try:
        yield db.session
    except:
        # Roll back if the nested block raised an error
        db.session.rollback()
        raise
    else:
        # Commit if it didn't (so flow ran off the end of the try block)
        db.session.commit()


def transactional(*args, **kwargs):
    """Decorator which wraps the decorated function in a transactional session. If the
       function completes successfully, the transaction is committed. If not, the transaction
       is rolled back.

        retries:  function will retry 'retries + 1' times on exception.
        using virtual transactions (sub transactions) session.
    """
    def outer_wrapper(func):
        @functools.wraps(func)
        def wrapper(*orig_args, **orig_kwargs):
            result = None
            retries = kwargs.get('retries', 0)
            while retries + 1:
                retries -= 1
                db.session.begin(subtransactions=True)
                try:
                    result = func(*orig_args, **orig_kwargs)
                except:
                    # Roll back if the nested block raised an error
                    db.session.rollback()
                    if not (retries + 1):
                        raise
                else:
                    # Commit if it didn't (so flow ran off the end of the try block)
                    db.session.commit()
                    return result
        return wrapper
    return outer_wrapper
