from typing import Optional
from wildlife_tracker.habitat_management.habitat import Habitat
from wildlife_tracker.migration_tracking.migration_path import MigrationPath 

class Migration:

    def __init__(self, 
                 migration_id: int,
                 migration_path: MigrationPath,  
                 current_location: str,
                 status: str = "Scheduled",
                 health_status: Optional[str] = None) -> None:
        self.migration_id = migration_id
        self.migration_path = migration_path
        self.current_location = current_location
        self.status = status
        self.health_status = health_status
