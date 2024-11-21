'''个人数据数据处理'''
from modules.base.base_data import BaseData


class Data(BaseData):
    def __init__(self):
        super().__init__({
            "module_name": "zzz",
            "maxLevel": 15,
            "maxScore": 43.2,  # 标准最大值
            "maxScore2": 43.2  # 理论最大值
        })

        self.entryArray = ["暴击率", "暴击伤害", "攻击力", "生命值", "防御力", "异常精通", "穿透值"]
        self.posName = ["分区1", "分区2", "分区3", "分区4", "分区5", "分区6"]
        self.mainAttrType = {
            "分区4": ["生命值", "攻击力", "防御力", "暴击率", "暴击伤害", "异常精通"],
            "分区5": ["生命值", "攻击力", "防御力", "穿透率", "物理伤害加成", "火属性伤害加成", "冰属性伤害加成", "电属性伤害加成", "以太伤害加成"],
            "分区6": ["生命值", "攻击力", "防御力", "异常掌控", "冲击力", "能量自动回复"],
        }
        self.combinationType = {
            "4+2": [
                ["A", "A", "A", "A", "B", "B"],
                ["A", "A", "A", "B", "A", "B"],
                ["A", "A", "A", "B", "B", "A"],
                ["A", "A", "B", "A", "A", "B"],
                ["A", "A", "B", "A", "B", "A"],
                ["A", "A", "B", "B", "A", "A"],
                ["A", "B", "A", "A", "A", "B"],
                ["A", "B", "A", "A", "B", "A"],
                ["A", "B", "A", "B", "A", "A"],
                ["A", "B", "B", "A", "A", "A"],
                ["B", "A", "A", "A", "A", "B"],
                ["B", "A", "A", "A", "B", "A"],
                ["B", "A", "A", "B", "A", "A"],
                ["B", "A", "B", "A", "A", "A"],
                ["B", "B", "A", "A", "A", "A"]
            ]
        }
        self.coefficient = {
            '暴击率': 2,
            '暴击伤害': 1,
            '攻击力百分比': 1.6,
            '生命值百分比': 1.6,
            '防御力百分比': 1,
            '攻击力': 0.252632 / 2,
            '生命值': 0.042857 / 2,
            '防御力': 0.32 / 2,
            "异常精通": 0.533333,
            "穿透值": 0.533333
        }
        self.average = {
            '暴击率': 2.4,
            '暴击伤害': 4.8,
            '攻击力百分比': 3,
            '生命值百分比': 3,
            '防御力百分比': 4.8,
            '攻击力': 19,
            '生命值': 112,
            '防御力': 15,
            "异常精通": 9,
            "穿透值": 9
        }
        self.evaluate = [
            (35, (230, 179, 34), "传世珍品"),
            (25, (255, 217, 0), "十分宝贵"),
            (15, (163, 224, 67), "基本合格"),
            (10, (238, 121, 118), "有点屁用"),
            (0, (255, 0, 0), "屁用没有")
        ]

    def getEntryArray(self):
        return self.entryArray

    def getPosName(self):
        return self.posName

    def getMainAttrType(self):
        return self.mainAttrType

    def getCoefficient(self):
        return self.coefficient

    def getAverage(self):
        return self.average

    def get_evaluate(self, score):
        for item in self.evaluate:
            if score >= item[0]:
                return item

    # 获取下标
    def getIndexByCharacter(self, character):
        result = {"suitA": 0, "suitB": 0, "分区4": [], "分区5": [], "分区6": []}
        if character in self.characters:
            artifactSchemeItem = self.characters[character]
            for key in artifactSchemeItem:
                if key == "suitA" or key == "suitB":
                    suitKeyArray = list(self.suitConfig.keys())
                    if artifactSchemeItem[key] in suitKeyArray:
                        result[key] = suitKeyArray.index(artifactSchemeItem[key]) + 1
                elif key in self.posName:
                    result[key] = artifactSchemeItem[key]
                else:
                    result[key] = []
        return result

    # 推荐圣遗物
    def recommend(self, params):
        # 获取组合类型
        if params["suitA"] != "选择套装" and params["suitB"] != "选择套装":
            if params["suitA"] != params["suitB"]:
                combinationKey = "4+2"
                flag = True
            else:
                flag = False
        else:
            flag = False

        if not flag:
            return False, "目前仅支持4+2套装类型推荐"

        # 筛选评分最大值套装
        suit = {
            "A": {},
            "B": {},
            "C": {},
        }
        for posItem in self.posName:
            array = {
                "A": [],
                "B": [],
                "C": [],
            }
            for artifactKey, artifactValue in self.artifactList[posItem].items():

                # 限制一 是否已装备
                if params["selectType"] == 1:
                    ownerCharacter = self.getOwnerCharacterByArtifactId(posItem, artifactKey)
                    if ownerCharacter and ownerCharacter != params["character"]:
                        # print("该装备已装备")
                        continue

                # 限制二 对比主词条
                if posItem in self.mainAttrType:
                    if artifactValue["mainAttr"] not in params["needMainAttr"][posItem]:
                        # print("主词条不符合")
                        continue

                # 开始筛选
                tempItem = {}
                tempItem["artifactID"] = artifactKey
                tempItem["name"] = artifactValue["name"]
                tempItem["score"] = self.newScore(artifactValue, params["character"])[1]

                if combinationKey == "4+2":
                    if artifactValue["name"] == params["suitA"]:
                        array["A"].append(tempItem)
                    elif artifactValue["name"] == params["suitB"]:
                        array["B"].append(tempItem)
                    else:
                        array['C'].append(tempItem)
                else:
                    pass

            # 取出当前位置最大值
            for suitKey in suit.keys():
                suit[suitKey][posItem] = 0
                if len(array[suitKey]) > 0:
                    array[suitKey].sort(key=lambda x: x["score"], reverse=True)
                    suit[suitKey][posItem] = array[suitKey][0]

        # print(suit)

        # 根据组合类型选出来总分最大组合
        scoreArray = []
        combination = self.combinationType[combinationKey]
        for combinationItem in combination:
            combinationName = {}
            tempFlag = 0
            scoreSum = 0
            for index in range(len(self.posName)):
                posItem = self.posName[index]
                combinationItemItem = combinationItem[index]
                if suit[combinationItemItem][posItem]:
                    scoreNum = suit[combinationItemItem][posItem]["score"]
                    combinationName[posItem] = suit[combinationItemItem][posItem]["artifactID"]
                    scoreSum += scoreNum
                else:
                    # print( posItem +" 不存在 计分中止1")
                    tempFlag = 1
                    break

            if tempFlag:
                # print("圣遗物不存在 计分中止2")
                continue
            scoreItem = {}
            scoreItem["combinationType"] = "".join(combinationItem)
            scoreItem["combinationName"] = combinationName
            scoreItem["scoreSum"] = round(scoreSum, 1)
            scoreArray.append(scoreItem)
        scoreArray.sort(key=lambda x: x["scoreSum"], reverse=True)
        # print(scoreArray)
        if len(scoreArray) > 0:
            return scoreArray, "推荐成功"
        else:
            return False, "没有推荐结果"

    # 检查圣遗物是否可以更新
    def checkUpdate(self):
        # 检查是否有装备可以更新
        result = []
        for owner in self.artifactOwnerList:
            scheme = self.characters[owner]

            params = {}
            params["suitA"] = scheme["suitA"]
            params["suitB"] = scheme["suitB"]
            params["needMainAttr"] = {
                "分区4": scheme["分区4"],
                "分区5": scheme["分区5"],
                "分区6": scheme["分区6"],
            }
            params["character"] = owner
            params["heroConfig"] = self.characters[owner]
            params["selectType"] = 1
            recommendResult, _ = self.recommend(params)

            if recommendResult:
                new = recommendResult[0]["combinationName"]
                old = self.artifactOwnerList[owner]
                for pos in self.posName:
                    if new[pos] != old[pos]:
                        result.append(owner)
                        break
            else:
                # 没有推荐结果
                print("没有推荐结果")
                pass
        return result


data = Data()
