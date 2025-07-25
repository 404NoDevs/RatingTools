''' 个人数据数据处理 '''
import json
import os
import shutil
import globalsData


class BaseData:

    def __init__(self, params):

        # 获取子类参数
        self.module_name = params.get("module_name", "genshin")
        self.maxLevel = params.get("maxLevel", 0)
        self.maxScore = params.get("maxScore", 0)
        self.oneMaxScore = params.get("oneMaxScore", 0)

        # 初始化常量
        self.suitConfig_path = f"src/{self.module_name}/suitConfig.json"
        self.defaulCharacter_path = f"src/{self.module_name}/character.json"
        self.folder_root = os.path.expanduser('~/Documents') + f'/RatingTools/{self.module_name}'
        self.character_path = self.folder_root + '/character.json'
        if globalsData.debug:
            self.character_path = self.defaulCharacter_path
        self.artifact_path = self.folder_root + '/artifacts.json'
        self.artifactOwner_path = self.folder_root + '/artifactOwner.json'

        # 初始化变量
        self.artifactList = {}
        self.artifactOwnerList = {}
        self.suitConfig = {}
        self.characters = {}

        # 加载数据
        self.loadData()

    def loadData(self):
        if os.path.exists(self.folder_root):
            # 读取圣遗物保存数据
            if os.path.exists(self.artifact_path):
                with open(self.artifact_path, 'r', encoding='utf-8') as fp:
                    self.artifactList = json.load(fp)
            # 读取圣遗物装备者保存数据
            if os.path.exists(self.artifactOwner_path):
                with open(self.artifactOwner_path, 'r', encoding='utf-8') as fp:
                    self.artifactOwnerList = json.load(fp)
            # 读取角色参数配置
            if os.path.exists(self.character_path):
                with open(self.defaulCharacter_path, 'r', encoding='utf-8') as fp:
                    default = json.load(fp)
                with open(self.character_path, 'r', encoding='utf-8') as fp:
                    self.characters = json.load(fp)
                diff = default.keys() - self.characters.keys()
                if diff != set():
                    for item in diff:
                        self.characters[item] = default[item]
                    with open(self.character_path, 'w', encoding='utf-8') as fp:
                        json.dump(self.characters, fp, ensure_ascii=False, indent=4)
            else:
                shutil.copy(self.defaulCharacter_path, self.character_path)
                with open(self.character_path, 'r', encoding='utf-8') as fp:
                    self.characters = json.load(fp)
        else:
            os.makedirs(self.folder_root)
            shutil.copy(self.defaulCharacter_path, self.character_path)
            with open(self.character_path, 'r', encoding='utf-8') as fp:
                self.characters = json.load(fp)

        with open(self.suitConfig_path, 'r', encoding='utf-8') as fp:
            self.suitConfig = json.load(fp)

    # 获取圣遗物套装配置
    def getSuitConfig(self):
        return self.suitConfig

    # 获取两件套列表
    def getSuitListByKey(self, key):
        if key in self.suitConfig and isinstance(self.suitConfig[key], list):
            return self.suitConfig[key]
        return []

    # 获取英雄配置
    def getCharacters(self):
        return self.characters

    # 更新英雄配置
    def setCharacters(self, character, config):
        if character not in self.characters:
            self.characters[character] = {}

        self.characters[character].update(config)

        with open(self.character_path, 'w', encoding='utf-8') as fp:
            json.dump(self.characters, fp, ensure_ascii=False, indent=4)

    def getArtifactOwner(self, character):
        if character in self.artifactOwnerList:
            return self.artifactOwnerList[character]
        else:
            return {}

    # 通过角色名及装备列表替换装备
    def setArtifactOwner(self, character, newArtifactOwnerItem):
        for pos in newArtifactOwnerItem:
            ownerCharacter = self.getOwnerCharacterByArtifactId(pos, newArtifactOwnerItem[pos])
            if ownerCharacter:
                del self.artifactOwnerList[ownerCharacter][pos]

            if character not in self.artifactOwnerList:
                self.artifactOwnerList[character] = {}
            self.artifactOwnerList[character][pos] = newArtifactOwnerItem[pos]

        # 保存数据
        with open(self.artifactOwner_path, 'w', encoding='utf-8') as fp:
            json.dump(self.artifactOwnerList, fp, ensure_ascii=False, indent=4)

    # 通过ID及位置查询装备角色名称
    def getOwnerCharacterByArtifactId(self, pos, artifactID):
        for character in self.artifactOwnerList:
            if pos in self.artifactOwnerList[character] and self.artifactOwnerList[character][pos] == artifactID:
                return character
        return None

    # 通过ID及位置查询装备
    def getArtifactItem(self, pos, artifactID):
        if pos in self.artifactList:
            if artifactID in self.artifactList[pos]:
                return self.artifactList[pos][artifactID]
            else:
                return {}
        else:
            return {}

    # 保存圣遗物
    def saveArtifactList(self, data):

        if not self.checkArtifactName(data["name"], data["parts"]):
            print("装备不合法 " + data["name"])
            return False

        # 判定数据是否被矫正过
        if "isCorrected" in data:
            if data["isCorrected"]:
                print("数据发生过矫正，无法保存")
                return False
            del data["isCorrected"]

        # 判断是否强化满级
        if data["lvl"] != str(self.maxLevel):
            print("未强化满级")
            return False

        # 得分校验
        score = self.newScore(data, "全属性")[1]
        if score > self.maxScore * 2:  # 权重最大值为2 所以最大得分*2
            print("得分异常", score)
            return False

        # 获取圣遗物ID
        nameArray = []
        nameArray.append(data["name"])
        for itemName, itemNum in data["subAttr"].items():
            nameArray.append(str(itemNum))
        nameStr = '-'.join(nameArray)
        parts = data["parts"]

        if nameStr in self.artifactList[parts]:
            print("当前圣遗物已存在")
            return False

        # 存储数据
        self.artifactList[parts][nameStr] = data
        with open(self.artifact_path, 'w', encoding='utf-8') as fp:
            json.dump(self.artifactList, fp, ensure_ascii=False, indent=4)
            print("保存成功")

    def getCharacterIndex(self, character):
        resultIndex = 0
        if character in self.characters:
            characterKeyArray = list(self.characters.keys())
            resultIndex = characterKeyArray.index(character)
        return resultIndex

    # 获取配置文件夹路径
    def getUserDataPath(self):
        return self.folder_root

    def newScore(self, ocr_result, character):
        config = self.characters[character]["weight"]

        scores = []
        sums = 0
        powerupArray = []
        entriesSum = 0

        # 补分逻辑
        add_score_switch = True
        addScore = 0
        if add_score_switch:
            # 检查主词条是否合规
            if ocr_result['parts'] in self.getMainAttrType():
                attrList = [key for key, value in config.items() if value > 0]
                if ocr_result['mainAttr'] in attrList:
                    addScore = (self.oneMaxScore / 4) * config[ocr_result['mainAttr']]
        # debugPrint("主词条补分", addScore)

        for key, value in ocr_result['subAttr'].items():
            # 兼容角色配置未区分百分比的情况
            if key == '生命值百分比' or key == '攻击力百分比' or key == '防御力百分比':
                key_s = key[:3]
            else:
                key_s = key

            # key值存在误识别情况，则判定为0
            coefficient = self.getCoefficient()
            score = round(value * config[key_s] * coefficient[key], 1)
            scores.append(score)
            sums += score

            # 计算强化次数 及 有效词条数量
            average = self.getAverage()
            powerup = round(value / average[key]) - 1
            powerupArray.append(powerup)
            if key_s in config and config[key_s] > 0:
                entries = value / average[key]
                # print(key, entries)
                entriesSum += entries

        if add_score_switch:
            sums += addScore

        if 'isCorrected' in ocr_result and ocr_result['isCorrected']:
            # 如果数据发生过矫正则总分为-1
            sums = -1

        # print(scores, round(sums, 1), powerupArray, round(entriesSum, 1))
        return scores, round(sums, 1), powerupArray, round(entriesSum, 1)

    def get_evaluate_tips(self, score):
        config = self.get_evaluate()
        for item in config:
            if score >= item[0]:
                return item[1]
        return "未找到评价标准"

    def get_table_data(self):
        resule = {}
        for character, equipment in self.artifactOwnerList.items():
            resule[character] = {}
            resule[character].update(self.characters[character])
            resule[character].update({"equipment": equipment})

        return resule

    ''' 子类方法 '''

    # 获取属性词条枚举
    def getEntryArray(self):
        print("方法 getEntryArray 未在子类实现")

    # 获取圣遗物类型配置
    def getMainAttrType(self):
        print("方法 getMainAttrType 未在子类实现")

    # 获取圣遗物位置名称
    def getPosName(self):
        print("方法 getPosName 未在子类实现")

    # 获取系数
    def getCoefficient(self):
        print("方法 getCoefficient 未在子类实现")

    # 获取平均分
    def getAverage(self):
        print("方法 getAverage 未在子类实现")

    # 获取分析数据
    def getAnalyzeData(self, ocr_result):
        print("方法 getAnalyzeData 未在子类实现")

    # 获取评价配置
    def get_evaluate_config(self):
        print("方法 get_evaluate_config 未在子类实现")

    def get_evaluate(self):
        print("方法 get_evaluate 未在子类实现")

    # 检查圣遗物是否存在
    def checkArtifactName(self, name, parts):
        print("方法 checkArtifactName 未在子类实现")