import logging


def start_logger():
    formatter = logging.Formatter('%(asctime)s %(message)s')
    fh = logging.FileHandler('CF_Senior_EPGP.log')
    fh.setLevel(level=logging.INFO)
    fh.setFormatter(formatter)

    logger = logging.getLogger('EPGP')
    logger.addHandler(fh)
    logger.setLevel(level=logging.INFO)


def log_adjustment(raider_names, ep=0, gp=0, loot=None):
    adjustment_msg = '%s ' % (raider_names)
    if (loot != None):
        adjustment_msg += '获得物品%s ' % (loot.name)

    if (ep != 0):
        adjustment_msg += '获得%sEP ' % (ep)

    if (gp != 0):
        adjustment_msg += '获得%sGP ' % (gp)

    _log_msg(adjustment_msg)


def _log_msg(msg):
    logger = logging.getLogger('EPGP')
    logger.info(msg)
