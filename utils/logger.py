import logging


def configure_logging() -> None:
    # Use one format for API and UI logs for easier reading.
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        force=True,
    )
