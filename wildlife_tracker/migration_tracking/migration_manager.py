from typing import Any, List, Optional
from wildlife_tracker.migration_tracking.migration import Migration, MigrationPath
from wildlife_tracker.habitat_management.habitat import Habitat


class MigrationManager:

    migrations: dict[int, Migration] = {}
    paths: dict[int, MigrationPath] = {}

    def get_migration_by_id(self, migration_id: int) -> Migration:
        pass

    def get_migration_details(self, migration_id: int) -> dict[str, Any]:
        pass

    def get_migration_path_by_id(self, path_id: int) -> MigrationPath:
        pass

    def get_migration_paths(self) -> List[MigrationPath]:
        pass

    def get_migration_paths_by_destination(self, destination: Habitat) -> List[MigrationPath]:
        pass

    def get_migration_paths_by_species(self, species: str) -> List[MigrationPath]:
        pass

    def get_migration_paths_by_start_location(self, start_location: Habitat) -> List[MigrationPath]:
        pass

    def get_migrations(self) -> List[Migration]:
        pass

    def get_migrations_by_current_location(self, current_location: str) -> List[Migration]:
        pass

    def get_migrations_by_migration_path(self, migration_path_id: int) -> List[Migration]:
        pass

    def get_migrations_by_start_date(self, start_date: str) -> List[Migration]:
        pass

    def get_migrations_by_status(self, status: str) -> List[Migration]:
        pass

    def get_migration_path_details(self, path_id: int) -> dict:
        pass

    def cancel_migration(self, migration_id: int) -> None:
        pass

    def remove_migration_path(self, path_id: int) -> None:
        pass

    def schedule_migration(self, migration_path: MigrationPath) -> None:
        pass

    def update_migration_details(self, migration_id: int, **kwargs: Any) -> None:
        pass

    def update_migration_path_details(self, path_id: int, **kwargs: Any) -> None:
        pass
