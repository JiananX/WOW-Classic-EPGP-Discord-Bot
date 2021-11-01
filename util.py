import cfg
import constant
import logging


def get_ep(game_id):
    return cfg.raider_dict[game_id].EP


def get_gp(game_id):
    gp = cfg.raider_dict[game_id].GP

    if (gp == 0):
        backfill_gp(game_id)

    return gp


def set_ep(game_id, ep):
    cfg.raider_dict[game_id].EP = ep


def set_gp(game_id, gp):
    if (gp == 0):
        cfg.raider_dict[game_id].GP = constant.initial_gp
    else:
        cfg.raider_dict[game_id].GP = gp


def calculate_pr(game_id):
    return round(get_ep(game_id) / get_gp(game_id), 3)


def backfill_gp(game_id):
    set_gp(game_id, constant.initial_gp)


def generate_pr_list(pr_list, ep_list, gp_list):
    pr_message = 'ID  EP  GP  PR\n'
    # return List of key-value tuple/pair entry
    sorted_pr_list = sorted(pr_list.items(), key=lambda x: x[1], reverse=True)
    for entry in sorted_pr_list:
        game_id = entry[0]
        pr_message += '%s  %s  %s  %s\n' % (game_id, ep_list[game_id],
                                            gp_list[game_id], entry[1])

    return pr_message


def start_logger():
    formatter = logging.Formatter('%(asctime)s %(message)s')
    fh = logging.FileHandler('CF_Senior_EPGP.log')
    fh.setLevel(level=logging.INFO)
    fh.setFormatter(formatter)

    logger = logging.getLogger('EPGP')
    logger.addHandler(fh)
    logger.setLevel(level=logging.INFO)


def log_msg(msg):
    logger = logging.getLogger('EPGP')
    logger.info(msg)


def find_game_id(author):
    for raider in cfg.raider_dict.values():
        if (raider.author == author):
            return raider.ID

    return None
