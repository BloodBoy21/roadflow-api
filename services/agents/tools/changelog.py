from loguru import logger

from repository import repository


def save_changelog(context: dict):
    def save_changelog_tool(title: str, description: str, position: int, show: bool = True, estimated_date: str = ""):
        """
        Save a changelog entry in the database.
        
        Args:
            title (str): The title of the changelog entry.
            description (str): The description of the changelog entry.
            position (int): The position of the changelog entry.
            show (bool): Whether to show the changelog entry. Defaults to True.
            estimated_date (str): The estimated date for the changelog entry. Defaults to "".
            
        Returns:
            dict: A dictionary containing the success status and the created changelog data.
                - success (bool): Indicates whether the operation was successful.
                - data (dict): The created changelog entry data (if successful).
                - error (str): Error message (if unsuccessful).
        """
        if not title or not description:
            logger.warning("Title and description are required to save a changelog entry.")
            return

        changelog_entry = {
            "organizationId": context.get("org_id"),
            "title": title,
            "description": description,
            "position": position,
            "show": show,
            "estimated_date": estimated_date,
        }

        try:
            doc = repository.mongo.changelog.create(changelog_entry)
            logger.info(f"Changelog created with ID: {doc.id}")
            logger.info(f"Changelog saved successfully: {changelog_entry}")
            return {"success": True, "data": doc.model_dump()}
        except Exception as e:
            logger.error(f"Failed to save changelog: {e}")
            return {"success": False, "error": str(e)}

    return save_changelog_tool

def get_changelog(context: dict):
    def get_changelog_tool() -> dict:
        """
        Retrieve all changelog entries for the organization.

        Returns:
            dict: A dictionary containing the success status and a list of changelog entries.
                - success (bool): Indicates whether the retrieval was successful.
                - data (list[dict]): A list of changelog entries, each represented as a dictionary.
                - error (str): Error message (if unsuccessful).
        """
        try:
            changelogs = repository.mongo.changelog.find({"organizationId": context.get("org_id")})
            logger.info(f"Retrieved {len(changelogs)} changelog entries.")
            return {
                "success": True,
                "data": [changelog.model_dump() for changelog in changelogs],
            }
        except Exception as e:
            logger.error(f"Failed to retrieve changelogs: {e}")
            return {"success": False, "error": str(e)}

    return get_changelog_tool


def delete_changelog(context: dict):
    def delete_changelog_tool(changelog_id: str):
        """
        Delete a changelog entry by its ID.
        
        Args:
            changelog_id (str): The ID of the changelog entry to delete.
        
        Returns:
            dict: A dictionary containing the success status and operation result.
                - success (bool): Indicates whether the deletion was successful.
                - data (dict): Success message (if successful).
                - error (str): Error message (if unsuccessful).
        """
        if not changelog_id:
            logger.warning("Changelog ID is required to delete a changelog entry.")
            return

        try:
            repository.mongo.changelog.delete_by_id(changelog_id)
            logger.info(f"Changelog with ID {changelog_id} deleted successfully.")
            return {
                "success": True,
                "data": {
                    "message": f"Changelog with ID {changelog_id} deleted successfully."
                },
            }
        except Exception as e:
            logger.error(f"Failed to delete changelog: {e}")
            return {"success": False, "error": str(e)}

    return delete_changelog_tool

def sort_changelog(context: dict):
    def sort_changelog_tool(changelog_ids: list[str], positions: list[int]):
        """
        Sort changelog entries by updating their positions.
        
        Args:
            changelog_ids (list[str]): List of changelog entry IDs to update.
            positions (list[int]): Corresponding positions for the changelog entries.
        
        Returns:
            dict: A dictionary containing the success status and operation result.
                - success (bool): Indicates whether the sorting was successful.
                - data (dict): Success message (if successful).
                - error (str): Error message (if unsuccessful).
        """
        if not changelog_ids or not positions or len(changelog_ids) != len(positions):
            logger.warning("Invalid input for sorting changelogs.")
            return

        try:
            for changelog_id, position in zip(changelog_ids, positions, strict=False):
                repository.mongo.changelog.update_by_id(
                    changelog_id,
                    {"position": position}
                )
            logger.info("Changelogs sorted successfully.")
            return {
                "success": True,
                "data": {"message": "Changelogs sorted successfully."},
            }
        except Exception as e:
            logger.error(f"Failed to sort changelogs: {e}")
            return {"success": False, "error": str(e)}

    return sort_changelog_tool

def update_changelog(context: dict):
    def update_changelog_tool(changelog_id: str, title: str, description: str, position: int, show: bool = True, estimated_date: str = ""):
        """
        Update an existing changelog entry.
        
        Args:
            changelog_id (str): The ID of the changelog entry to update.
            title (str): The new title for the changelog entry.
            description (str): The new description for the changelog entry.
            position (int): The new position for the changelog entry.
            show (bool): Whether to show the changelog entry. Defaults to True.
            estimated_date (str): The new estimated date for the changelog entry. Defaults to "".
        
        Returns:
            dict: A dictionary containing the success status and operation result.
                - success (bool): Indicates whether the update was successful.
                - data (dict): Success message (if successful).
                - error (str): Error message (if unsuccessful).
        """
        if not changelog_id or not title or not description:
            logger.warning("Changelog ID, title, and description are required to update a changelog entry.")
            return

        try:
            repository.mongo.changelog.update_by_id(
                changelog_id,
                {
                    "title": title,
                    "description": description,
                    "position": position,
                    "show": show,
                    "estimated_date": estimated_date
                }
            )
            logger.info(f"Changelog with ID {changelog_id} updated successfully.")
            return {
                "success": True,
                "data": {
                    "message": f"Changelog with ID {changelog_id} updated successfully."
                },
            }
        except Exception as e:
            logger.error(f"Failed to update changelog: {e}")
            return {"success": False, "error": str(e)}

    return update_changelog_tool
