import traceback


class LogDiscWriter:
    """
    Logs all writing attempts to the disk

    """

    def __init__(self):
        self.total_write_attempts = 0

    def __call__(self, *args, **kwargs):
        self.total_write_attempts += 1
        print(f"Write attempt: {self.total_write_attempts}")

        # show where write came from:
        stack = traceback.extract_stack()
        print(f"Write attempt from: {stack[-2]}")
