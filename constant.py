# user.py
login_reg = "Login ([^ ]+)"

# admin.py
start_new_raid_reg = "(Admin|a) start"
add_new_member_reg = "(Admin|a) add .+"
decay_reg = "(Admind|a) decay"
adjust_reg = "(Admind|a) adjust .+"
standby_reg = "(Admind|a) standby .+"
recover_reg = "(Admind|a) recover"
sync_epgp_from_gsheet_to_json = "(Admin|a) g2js pr"
sync_loot_from_gsheet_to_json = "(Admin|a) g2js loot"
load_epgp_from_json_to_memory = "(Admin|a) js2m pr"
load_loot_from_json_to_memory = "(Admin|a) js2m loot"
dump_epgp_from_memory_to_json = "(Admin|a) (write|w)"
dump_loot_from_memory_to_json = "(Admin|a) m2js loot"

# distribute.py
announcement_reg = "(Distribute|d) [a-z]+"

# common
admin_reg = "(Admin|a) .+"
dis_reg = "(Distribute|d) .+"

user_raid_pr_list_id = "user_raid_pr_list"
user_my_pr_id = "user_my_pr"
user_main_spec_id = "user_main_spec"

loot_gbid_confirm_id = "loot_gbid"
loot_main_spec_confirm_id = "loot_main_spec"
loot_cancel_id = "loot_cancel"

reward_20_ep = 'reward 20'
reward_150_ep = 'reward 150'
reward_200_ep = 'reward 200'

# common constant
initial_gp = 1000
decay_factor = 0.85
update_message_button_response_type = 7
''' TODO: Hide these token '''
admin_token = 'Angulardart/Ditt#8629, Airbkb/Bigblackbang#0025'
