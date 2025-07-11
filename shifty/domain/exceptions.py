class InvalidDateRangeException(Exception):
    """Exception raised when a date range is invalid."""
    pass

class NotExistsException(Exception):
    """Exception raised when an entity does not exists"""
    pass

class InvalidAvailabilityException(Exception):
    """Exception raised when an availability is invalid."""
    pass

class InvalidOverrideException(Exception):
    """Exception raised when an override is invalid."""
    pass

class InvalidShiftException(Exception):
    """Exception raised when a shift is invalid."""
    pass

class OverlappingShiftException(Exception):
    """Exception raised when a shift overlaps with another."""
    pass