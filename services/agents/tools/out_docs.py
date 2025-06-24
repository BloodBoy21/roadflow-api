from loguru import logger

from repository import repository


def save_out_doc(context: dict):
    def save_out_doc_tool(text: str, publish: bool = False, tags: str = ""):
        """
        Save relevant text response as document in MongoDB.
        
        Args:
            text (str): The text to save as a document.
            publish (bool): Whether to publish the document or not. Defaults to False.
            tags (str): Comma-separated list of tags to associate with the document. Defaults to "".
            
        Returns:
            dict: A dictionary containing the success status and the created document data.
                - success (bool): Indicates whether the operation was successful.
                - data (dict): The created document data (if successful).
                - error (str): Error message (if unsuccessful).
        """
        if not text:
            logger.warning("No text provided to save as document.")
            return

        out_doc = {
            "organizationId": context.get("org_id"),
            "text": text,
            "workflow": context.get("workflow", ""),
            "publish": publish,
            "tags": [tag.strip() for tag in tags.split(",") if tag.strip()],
            "agent": context.get("agent_name"),
        }

        try:
            doc = repository.mongo.out_document.create(out_doc)
            logger.info(f"Document created with ID: {doc.id}")
            logger.info(f"Document saved successfully: {out_doc}")
            return {"success": True, "data": doc.model_dump()}
        except Exception as e:
            logger.error(f"Failed to save document: {e}")
            return {"success": False, "error": str(e)}

    return save_out_doc_tool
