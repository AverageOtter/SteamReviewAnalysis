""" Module that allows logging function"""
import logging

def configure_logger(logger_name, filename="SteamAI.log"):
    """
    The configure_logger function takes two arguments:
        logger_name - the name of the logger to be configured.
        filename - a string representing the filepath where log messages will be written.
    
    :param logger_name: Set the name of the logger
    :param filename: Specify the name of the log file
    :return: A logger object
    :doc-author: Trelent
    """
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
    file_handler = logging.FileHandler(filename)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
