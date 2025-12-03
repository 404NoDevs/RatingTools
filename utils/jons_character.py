# 角色json 调整工具

import json


# 使用常量或枚举来定义类型
MODIFY_ALL = 0
MODIFY_GENSHIN = 1
MODIFY_STARRAIL = 2
MODIFY_ZZZ = 3

modify_module_name = MODIFY_ZZZ

if modify_module_name == MODIFY_GENSHIN:

    json_path = "../src/genshin/character.json"
    # 读取数据
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(data)
    # 更新每个角色的 weight 结构
    for character_name, character_data in data.items():
        if 'weight' in character_data:
            old_weight = character_data['weight']

            # 创建新的 weight 结构
            new_weight = {
                "暴击率": old_weight.get("暴击率", 0.0),
                "暴击伤害": old_weight.get("暴击伤害", 0.0),
                "生命值百分比": old_weight.get("生命值", 0.0),
                "攻击力百分比": old_weight.get("攻击力", 0.0),
                "防御力百分比": old_weight.get("防御力", 0.0),
                "生命值": 0.0,
                "攻击力": 0.0,
                "防御力": 0.0,
                "元素精通": old_weight.get("攻击力", 0.0),
                "元素充能效率": old_weight.get("攻击力", 0.0)
            }

            character_data['weight'] = new_weight

        if "core" in character_data:
            del character_data["core"]

    # 保存更新后的数据
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

elif modify_module_name == MODIFY_STARRAIL:

    json_path = "../src/starRail/character.json"
    # 读取数据
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(data)
    # 更新每个角色的 weight 结构
    for character_name, character_data in data.items():
        if 'weight' in character_data:
            old_weight = character_data['weight']

            # 创建新的 weight 结构
            new_weight = {
                "暴击率": old_weight.get("暴击率", 0.0),
                "暴击伤害": old_weight.get("暴击伤害", 0.0),
                "生命值百分比": old_weight.get("生命值", 0.0),
                "攻击力百分比": old_weight.get("攻击力", 0.0),
                "防御力百分比": old_weight.get("防御力", 0.0),
                "生命值": 0.0,
                "攻击力": 0.0,
                "防御力": 0.0,
                "速度": old_weight.get("速度", 0.0),
                "击破特攻": old_weight.get("击破特攻", 0.0),
                "效果命中": old_weight.get("效果命中", 0.0),
                "效果抵抗": old_weight.get("效果抵抗", 0.0)
            }

            character_data['weight'] = new_weight

        if "core" in character_data:
            del character_data["core"]

    # 保存更新后的数据
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

elif modify_module_name == MODIFY_ZZZ:

    json_path = "../src/zzz/character.json"
    # 读取数据
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(data)
    # 更新每个角色的 weight 结构
    for character_name, character_data in data.items():
        if 'weight' in character_data:
            old_weight = character_data['weight']

            # 创建新的 weight 结构
            new_weight = {
                "暴击率": old_weight.get("暴击率", 0.0),
                "暴击伤害": old_weight.get("暴击伤害", 0.0),
                "生命值百分比": old_weight.get("生命值", 0.0),
                "攻击力百分比": old_weight.get("攻击力", 0.0),
                "防御力百分比": old_weight.get("防御力", 0.0),
                "生命值": 0.0,
                "攻击力": 0.0,
                "防御力": 0.0,
                "异常精通": old_weight.get("异常精通", 0.0),
                "穿透值": old_weight.get("穿透值", 0.0)
            }

            character_data['weight'] = new_weight

        if "core" in character_data:
            del character_data["core"]

    # 保存更新后的数据
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

else:
    pass