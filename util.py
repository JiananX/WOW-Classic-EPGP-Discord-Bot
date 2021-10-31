from replit import db;

import constant;
import logging;

def is_valid_game_id(game_id):
  return (db.get('%s_ep'%(game_id)) != None) & (db.get('%s_gp'%(game_id)) != None);

def get_ep(game_id):
  return db['%s_ep'%(game_id)];

def get_gp(game_id):
  gp = db['%s_gp'%(game_id)];
  
  if (gp == 0):
    backfill_gp(game_id);

  return gp;

def set_ep(game_id, ep):
  db['%s_ep'%(game_id)] = ep;

def set_gp(game_id, gp):
  if (gp == 0):
    db['%s_gp'%(game_id)] = constant.initial_gp;
  else:
    db['%s_gp'%(game_id)] = gp;

def calculate_pr(game_id):
  return float(get_ep(game_id))/float(get_gp(game_id));

def backfill_gp(game_id):
  set_gp(game_id, constant.initial_gp);

# {game_id: number}
def generate_pr_list(pr_list, ep_list, gp_list):
  pr_message = 'ID  EP  GP  PR\n';
  # return List of key-value tuple/pair entry
  sorted_pr_list = sorted(pr_list.items(), key=lambda x: x[1], reverse=True);
  for entry in sorted_pr_list:
    game_id = entry[0];
    pr_message += '%s  %s  %s  %s\n'%(game_id, ep_list[game_id], gp_list[game_id], entry[1]);
  
  return pr_message;

def start_logger():
  formatter = logging.Formatter('%(asctime)s %(message)s');
  fh = logging.FileHandler('testing.log');
  fh.setLevel(level=logging.INFO);
  fh.setFormatter(formatter);

  logger = logging.getLogger('EPGP');
  logger.addHandler(fh);
  fh.setLevel(level=logging.INFO);

def log_msg(msg):
  logger = logging.getLogger('EPGP');
  logger.info(msg);