import sys
import logging as log


class LRUCache:
    DEFAULT_FORMAT = log.Formatter("%(asctime)s\t%(name)s\t%(levelname)s\t%(message)s")
    DEFAULT_LOG_LEVEL = log.DEBUG
    DEFAULT_HAND_LEVEL = log.DEBUG
    DEFAULT_LOG_PATH = "cache.log"

    def __init__(self, limit=4, *,
                 user_logging=(DEFAULT_LOG_LEVEL, DEFAULT_HAND_LEVEL, DEFAULT_FORMAT, DEFAULT_LOG_PATH),
                 stream_logging=(DEFAULT_HAND_LEVEL, DEFAULT_FORMAT)):
        self.cache = {}
        self.capacity = limit
        self.logger = log.getLogger("log")
        self.handler = log.FileHandler(user_logging[3])
        self.stream_handler = None
        self.init_logging(user_logging[:-1], stream_logging)
        self.logger.info(f'''Inst info: capacity={self.capacity}, 
                                               logging_info: log_level={self.logger.level}, 
                                                             handler_level={self.handler.level}''')
        if self.stream_handler is not None:
            self.logger.info(f'''stdout_logging_info: log_level={self.logger.level}, 
                                                         hand_level={self.stream_handler.level}''')
        self.logger.debug("LRUCache instance has been initialized")

    def init_logging(self, user_logging: tuple, stream_logging: tuple):
        self.handler.setLevel(user_logging[1])
        self.logger.setLevel(user_logging[0])
        self.handler.setFormatter(user_logging[2])
        self.logger.addHandler(self.handler)
        try:
            if sys.argv[1] == "-s":
                self.stream_handler = log.StreamHandler(sys.stdout)
                self.stream_handler.setLevel(stream_logging[0])
                self.stream_handler.setFormatter(stream_logging[1])
                self.logger.addHandler(self.stream_handler)
        except IndexError:
            pass

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
    form = log.Formatter("%(asctime)s - %(name)s - %(levelname)-7s - %(message)s")
    lru = LRUCache(1, stream_logging=(log.WARNING, form))
    lru[2] = 2
    lru[2] = 2
    lru[2]
    lru['ww']
    lru[3] = 3
