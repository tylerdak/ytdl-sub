from typing import List
from typing import Optional
from typing import Tuple

from ytdl_sub.subscriptions.subscription import Subscription
from ytdl_sub.utils.exceptions import ValidationException
from ytdl_sub.utils.file_handler import FileHandlerTransactionLog
from ytdl_sub.utils.logger import Logger

logger = Logger.get()


def _maybe_validate_transaction_log_file(transaction_log_file_path: Optional[str]) -> None:
    if transaction_log_file_path:
        try:
            with open(transaction_log_file_path, "w", encoding="utf-8"):
                pass
        except Exception as exc:
            raise ValidationException(
                f"Transaction log file '{transaction_log_file_path}' cannot be written to. "
                f"Reason: {str(exc)}"
            ) from exc


def output_transaction_log(
    transaction_logs: List[Tuple[Subscription, FileHandlerTransactionLog]],
    transaction_log_file_path: Optional[str],
) -> None:
    """
    Maybe print and/or write transaction logs to a file

    Parameters
    ----------
    transaction_logs
        The transaction logs from downloaded subscriptions
    transaction_log_file_path
        Optional file path to write to
    """
    transaction_log_file_contents = ""
    for subscription, transaction_log in transaction_logs:
        if transaction_log.is_empty:
            transaction_log_contents = f"\nNo files changed for {subscription.name}"
        else:
            transaction_log_contents = (
                f"Transaction log for {subscription.name}:\n"
                f"{transaction_log.to_output_message(subscription.output_directory)}"
            )

        if transaction_log_file_path:
            transaction_log_file_contents += transaction_log_contents
        else:
            logger.info(transaction_log_contents)

    if transaction_log_file_contents:
        with open(transaction_log_file_path, "w", encoding="utf-8") as transaction_log_file:
            transaction_log_file.write(transaction_log_file_contents)
