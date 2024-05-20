import logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S",
                    filename="server.log")

logger = logging.getLogger('request logger')

def log(*args):
    list ="".join(map(str,[arg for arg in args]))
    logger.info(f"LOG: {list}")

 





 