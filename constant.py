# user.py
login_reg = "Login ([^ ]+)";
raid_pr_list_reg = "Raid PR";
main_spec_reg = "(Main Spec|1)";

# admin.py
start_new_raid_reg = "(Admin|a) start";
add_new_member_reg = "(Admin|a) add .+";
all_pr_list_reg = "(Admin|a) PR";
decay_reg = "(Admind|a) decay";
adjust_reg = "(Admind|a) adjust .+";
sync_epgp_from_gsheet = "(Admin|a) pull pr";
sync_loot_from_gsheet = "(Admin|a) pull loot";

# raid.py
reward_ep = "(Raid|r) Reward [0-9]+($| -r .+)";
retrive_roster = "(Raid|r) Roster";

# distribute.py
announcement_reg = "(Distribute|d) [^ ]+ [0-9]+";
dis_cancel_reg = "(Distribute|d) cancel";
dis_confirm_reg = "(Distribute|d) confirm($|.+$)";

# common
raid_op_reg = "(Raid|r) .+";
admin_reg = "(Admin|a) .+";
dis_reg = "(Distribute|d) .+";

# common constant
initial_gp = 1000;
decay_factor = 0.85;