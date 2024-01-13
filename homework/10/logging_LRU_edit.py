import sys
import logging as log

DEFAULT_FORMAT = log.Formatter("%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s")
DEFAULT_STREAM_FORMAT = log.Formatter("%(asctime)s - %(name)s - %(levelname)-7s - %(message)s")
DEFAULT_LOG_LEVEL = log.DEBUG
DEFAULT_HAND_LEVEL = log.DEBUG
DEFAULT_LOG_PATH = "cache.log"


def init_logging(user_logging=(DEFAULT_LOG_LEVEL, DEFAULT_HAND_LEVEL, DEFAULT_FORMAT, DEFAULT_LOG_PATH),
                 stream_logging=(DEFAULT_HAND_LEVEL, DEFAULT_STREAM_FORMAT)):
    logger = log.getLogger("log")
    handler = log.FileHandler(user_logging[3])
    handler.setLevel(user_logging[1])
    logger.setLevel(user_logging[0])
    handler.setFormatter(user_logging[2])
    logger.addHandler(handler)
    try:
        if sys.argv[1] == "-s":
            stream_handler = log.StreamHandler(sys.stdout)
            stream_handler.setLevel(stream_logging[0])
            stream_handler.setFormatter(stream_logging[1])
            logger.addHandler(stream_handler)
    except IndexError:
        pass
    return logger


class LRUCache:

    def __init__(self, limit=4, *, logger):
        self.cache = {}
        self.capacity = limit
        self.logger = logger
        self.logger.info(f'''Inst info: capacity={self.capacity}, 
                                               logging_info: log_level={self.logger.level}, 
                                                             handler_level={self.logger.handlers[0].level}''')
        if len(self.logger.handlers) > 1:
            self.logger.info(f'''stdout_logging_info: log_level={self.logger.level}, 
                                                         hand_level={self.logger.handlers[1].level}''')
        self.logger.debug("LRUCache instance has been initialized")

    def __getitem__(self, item):
        try:
            self.logger.info(f"Trying to get value on key {repr(item)}")
            self.cache[item] = self.cache.pop(item)
        except KeyError:
            self.logger.error(f"Tried to get value on non-existing key {repr(item)}")
            print(f"Key {repr(item)} doesn't exist")
        else:
            self.logger.debug(f"got existing value {repr(self.cache[item])}")
            return self.cache[item]

    def __setitem__(self, key, value):
        self.logger.info(f"Trying to set value {repr(value)} on key {repr(key)}")
        if key in self.cache:
            self.logger.warning(f"Value {repr(value)} on key {repr(key)} already exists, moving to the end")
            self.cache.pop(key)
            self.cache[key] = value
            return
        if len(self.cache) >= self.capacity and key not in self.cache:
            self.logger.warning("Got max capacity, deleting 1st item")
            self.cache.pop(list(self.cache.keys())[0])
        self.logger.debug(f"Setting val {repr(value)} on key {repr(key)}")
        self.cache[key] = value

    def __str__(self):
        return str(self.cache)


if __name__ == "__main__":
    lru = LRUCache(1, logger=init_logging())
    lru[2] = 2
    lru[2] = 2
    lru[2]
    lru['ww']
    lru[3] = 3
