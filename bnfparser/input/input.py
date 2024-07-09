"""input module"""

class Input:
    """Managed a string source that needs to be matched
    """

    def __init__(self, source: str):
        self.__source = source
        self.current = 0

    def reset(self):
        """Reset that allow to match again
        """

        self.current = 0

    def match(self, destination: str) -> bool:
        """Try to match a destination based on the current cursor

        Args:
            destination (str): Word that must match

        Returns:
            bool: Is matched
        """

        size = len(destination)
        ret = self.__source[self.current:self.current + size] == destination

        if ret:
            self.current += size

        return ret

    def is_full_match(self) -> bool:
        """Return if the source has been entirely matched

        Returns:
            bool: Is matched
        """
        return self.current >= len(self.__source)
