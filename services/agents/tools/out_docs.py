from loguru import logger

from repository import repository


def save_out_doc(context:dict):
    def save_out_doc_tool(text: str, publish: bool = False, tags: str = ""):
        """
        save relevant text response as document in mongo db
        Args:
            text (str): The text to save as a document.
            publish (bool): Whether to publish the document or not. Defaults to False.
            tags (str): List of tags to associate with the document. Defaults to "".
        Returns:
            None
        """
        if not text:
            logger.warning("No text provided to save as document.")
            return

        out_doc = {
            "organizationId": context.get("org_id"),
            "text": text,
            "workflow": context.get("workflow"),
            "publish": publish,
            "tags": [tag.strip() for tag in tags.split(",") if tag.strip()],
            "agent": context.get("agent_name"),
        }

        try:
            doc = repository.mongo.out_document.create(out_doc)
            logger.info(f"Document created with ID: {doc.id}")
            logger.info(f"Document saved successfully: {out_doc}")
            return None
        except Exception as e:
            logger.error(f"Failed to save document: {e}")
            return None

    return save_out_doc_tool
