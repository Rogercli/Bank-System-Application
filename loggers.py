import logging

'''setting and getting logger'''
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


'''defining file handler and setting formatter'''
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')

file_handler = logging.FileHandler('logfiles.log')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)

'''adding file handler to logger'''
logger.addHandler(file_handler)


