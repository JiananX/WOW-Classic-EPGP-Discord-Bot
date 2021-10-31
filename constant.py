import cfg

# user.py
login_reg = "Login ([^ ]+)";

# admin.py
start_new_raid_reg = "(Admin|a) start";
add_new_member_reg = "(Admin|a) add .+";
all_pr_list_reg = "(Admin|a) PR";
decay_reg = "(Admind|a) decay";
adjust_reg = "(Admind|a) adjust .+";
sync_epgp_from_gsheet_to_json = "(Admin|a) g2js pr";
sync_loot_from_gsheet_to_json = "(Admin|a) g2js loot";
load_epgp_from_json_to_memory = "(Admin|a) js2m pr";
load_loot_from_json_to_memory = "(Admin|a) js2m loot";
dump_epgp_from_memory_to_json = "(Admin|a) m2js pr";
dump_loot_from_memory_to_json = "(Admin|a) m2js loot";

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


user_raid_pr_list_id = "user_raid_pr_list";
user_my_pr_id = "user_my_pr";
user_main_spec_id = "user_main_spec"

loot_gbid_confirm_id = "loot_gbid";
loot_main_spec_confirm_id = "loot_main_spec";
loot_cancel_id = "loot_cancel";

# common constant
initial_gp = 1000;
decay_factor = 0.85;
update_message_button_response_type = 7;