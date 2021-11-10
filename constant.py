# reg for message
login_reg = "Login ([^ ]+)"
admin_reg = "(Admin|a) .+"
announcement_reg = "(Distribute|d) [a-z]+"

start_new_raid_reg = "(Admin|a) start"
add_new_member_reg = "(Admin|a) add .+"
decay_reg = "(Admind|a) decay"
adjust_reg = "(Admind|a) adjust .+"
gbid_reg = "(Admind|a) gbid .+"
standby_reg = "(Admind|a) standby .+"
sync_epgp_from_gsheet_to_json = "(Admin|a) g2js pr"
sync_loot_from_gsheet_to_json = "(Admin|a) g2js loot"
load_epgp_from_json_to_memory = "(Admin|a) js2m pr"
load_loot_from_json_to_memory = "(Admin|a) js2m loot"
dump_epgp_from_memory_to_json = "(Admin|a) (write|w)"
dump_loot_from_memory_to_json = "(Admin|a) m2js loot"

# reg for button custom id
user_raid_pr_list_id = "user_raid_pr_list"
user_my_pr_id = "user_my_pr"

loot_main_spec_confirm_id = "loot_main_spec_confirm"
loot_off_spec_confirm_id = "loot_off_spec_confirm"
user_main_spec_id = "loot_main_spec"
user_off_spec_id = "loot_off_spec"
loot_cancel_id = "loot_cancel"

reward_20_ep = 'reward 20'
reward_150_ep = 'reward 150'
reward_200_ep = 'reward 200'

# common constant
initial_gp = 1000
decay_factor = 0.85
update_message_button_response_type = 7

raid_channel = 849111061840003079
loot_channel = 907482797579595806

gp_off_spec_factor = 0.5
gp_main_spec_factor = 1

class_dict = {
    '战士': 1,
    '圣骑士': 2,
    '法师': 3,
    '术士': 4,
    '猎人': 5,
    '盗贼': 6,
    '萨满': 7,
    '牧师': 8,
    '德鲁伊': 9
}

spec_dic = {
    '防护': 1,
    '狂暴': 2,
    '武器': 3,
    '神圣': 2,
    '惩戒': 3,
    '奥术': 1,
    '冰霜': 2,
    '火焰': 3,
    '毁灭': 1,
    '痛苦': 2,
    '恶魔': 3,
    '射击': 1,
    '生存': 2,
    '野兽控制': 3,
    '战斗': 1,
    '刺杀': 2,
    '敏锐': 3,
    '增强': 1,
    '恢复': 2,
    '元素': 3,
    '暗影': 1,
    '戒律': 3,
    '野性': 1,
    '平衡': 3,
}
