# Standard Lib
import threading

# Third Party
from sentry_sdk import capture_exception

# Local
from calllogger.utils import ExitCodeManager
from calllogger import running


class ThreadExceptionManager(threading.Thread):
    exit_code = ExitCodeManager()

    def run(self) -> bool:
        try:
            self.entrypoint()
        except Exception as err:
            capture_exception(err)
            self.exit_code.set(1)
            return False
        except SystemExit as err:
            self.exit_code.set(err.code)
            return True
        else:
            return True
        finally:
            running.clear()

    def entrypoint(self):  # pragma: no cover
        raise NotImplementedError
