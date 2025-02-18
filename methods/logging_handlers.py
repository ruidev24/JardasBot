import logging
import logging.handlers


##############################################################################
#set logging
def setup_logging(logger: logging.Logger):
    logger.setLevel(logging.INFO)
    logging.getLogger('discord.gateway').setLevel(logging.DEBUG)
    
    handler = logging.handlers.RotatingFileHandler(
        filename='JardasBot.log',
        encoding='utf-8',
        maxBytes=32 * 1024 * 1024,  # 32 MiB
        backupCount=5,  # Rotate through 5 files
    )
    
    dt_fmt = '%Y-%m-%d %H:%M:%S'
    formatter = logging.Formatter('[{asctime}] [{levelname:<8}] {name}: {message}', dt_fmt, style='{')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return