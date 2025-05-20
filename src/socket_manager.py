from WSmanager import ConnectionManager

# Create a singleton instance of ConnectionManager
manager = ConnectionManager()

# Export the singleton that can be imported by other modules
def get_manager() -> ConnectionManager:
    return manager
