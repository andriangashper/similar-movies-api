import logging

def configure_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    
    # Create file handler to write logs to .log file
    file_handler = logging.FileHandler('data.log')
    file_handler.setLevel(logging.INFO)

    # Create stream handler to write logs to the console
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    
    # Create formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(name)s - %(message)s')
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)
    
    # Add the handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    
    return logger
