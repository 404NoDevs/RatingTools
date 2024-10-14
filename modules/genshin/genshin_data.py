'''个人数据数据处理'''

from modules.base.base_data import BaseData

# 数据常量



class Data(BaseData):
    def __init__(self):
        super().__init__({
            "module_name": "genshin",
            "maxLevel": 20,
            "maxScore": 70.2
        })

        self.entryArray = ["暴击率", "暴击伤害", "攻击力", "生命值", "防御力", "元素精通", "元素充能效率"]
        self.posName = ["生之花", "死之羽", "时之沙", "空之杯", "理之冠"]
        self.mainTagType = {
            "时之沙": ["生命值", "攻击力", "防御力", "元素精通", "元素充能效率"],
            "空之杯": ["生命值", "攻击力", "防御力", "元素精通", "物理伤害加成", "火元素伤害加成", "雷元素伤害加成",
                       "水元素伤害加成", "草元素伤害加成", "风元素伤害加成", "岩元素伤害加成", "冰元素伤害加成"],
            "理之冠": ["生命值", "攻击力", "防御力", "元素精通", "暴击率", "暴击伤害", "治疗加成"],
        }
        self.combinationType = {
            "1+1+1+1+1": [
                ["C", "C", "C", "C", "C"]
            ],
            "4+1": [
                ["A", "A", "A", "A", "A"],
                ["C", "A", "A", "A", "A"],
                ["A", "C", "A", "A", "A"],
                ["A", "A", "C", "A", "A"],
                ["A", "A", "A", "C", "A"],
                ["A", "A", "A", "A", "C"]
            ],
            "2+2+1": [
                # 三个A两个B情况
                ["A", "A", "A", "B", "B"],
                ["A", "A", "B", "A", "B"],
                ["A", "A", "B", "B", "A"],
                ["A", "B", "A", "A", "B"],
                ["A", "B", "A", "B", "A"],
                ["A", "B", "B", "A", "A"],
                ["B", "A", "A", "A", "B"],
                ["B", "A", "A", "B", "A"],
                ["B", "A", "B", "A", "A"],
                ["B", "B", "A", "A", "A"],
                # 三个B两个A情况
                ["B", "B", "B", "A", "A"],
                ["B", "B", "A", "B", "A"],
                ["B", "B", "A", "A", "B"],
                ["B", "A", "B", "B", "A"],
                ["B", "A", "B", "A", "B"],
                ["B", "A", "A", "B", "B"],
                ["A", "B", "B", "B", "A"],
                ["A", "B", "B", "A", "B"],
                ["A", "B", "A", "B", "B"],
                ["A", "A", "B", "B", "B"],
                # 两个A两个B一个C情况
                ["C", "A", "A", "B", "B"],
                ["C", "A", "B", "A", "B"],
                ["C", "A", "B", "B", "A"],
                ["C", "B", "B", "A", "A"],
                ["C", "B", "A", "B", "A"],
                ["C", "B", "A", "A", "B"],
                ["A", "C", "A", "B", "B"],
                ["A", "C", "B", "A", "B"],
                ["A", "C", "B", "B", "A"],
                ["B", "C", "B", "A", "A"],
                ["B", "C", "A", "B", "A"],
                ["B", "C", "A", "A", "B"],
                ["A", "A", "C", "B", "B"],
                ["A", "B", "C", "A", "B"],
                ["A", "B", "C", "B", "A"],
                ["B", "B", "C", "A", "A"],
                ["B", "A", "C", "B", "A"],
                ["B", "A", "C", "A", "B"],
                ["A", "A", "B", "C", "B"],
                ["A", "B", "A", "C", "B"],
                ["A", "B", "B", "C", "A"],
                ["B", "B", "A", "C", "A"],
                ["B", "A", "B", "C", "A"],
                ["B", "A", "A", "C", "B"],
                ["B", "B", "A", "A", "C"],
                ["B", "A", "B", "A", "C"],
                ["B", "A", "A", "B", "C"],
                ["A", "A", "B", "B", "C"],
                ["A", "B", "A", "B", "C"],
                ["A", "B", "B", "A", "C"]
            ]
        }
        self.coefficient = {
            '暴击率': 2,
            '暴击伤害': 1,
            '攻击力百分比': 1.331429,
            '生命值百分比': 1.331429,
            '防御力百分比': 1.066362,
            '攻击力': 0.199146,
            '生命值': 0.012995,
            '防御力': 0.162676,
            '元素精通': 0.332857,
            '元素充能效率': 1.197943
        }
        self.average = {
            '暴击率': 3.3,
            '暴击伤害': 6.6,
            '攻击力百分比': 4.975,
            '生命值百分比': 4.975,
            '防御力百分比': 6.2,
            '攻击力': 16.75,
            '生命值': 254,
            '防御力': 19.75,
            '元素精通': 19.75,
            '元素充能效率': 5.5
        }


    def getEntryArray(self):
        return self.entryArray

    def getPosName(self):
        return self.posName

    def getMainTagType(self):
        return self.mainTagType

    def getCoefficient(self):
        return self.coefficient

    def getAverage(self):
        return self.average

    # 获取下标
    def getIndexByCharacter(self, character):
        result = {"suitA": 0, "suitB": 0, "时之沙": [], "空之杯": [], "理之冠": []}
        if character in self.artifactScheme:
            artifactSchemeItem = self.artifactScheme[character]
            for key in artifactSchemeItem:
                if key == "suitA" or key == "suitB":
                    suitKeyArray = list(self.suitConfig.keys())
                    if artifactSchemeItem[key] in suitKeyArray:
                        result[key] = suitKeyArray.index(artifactSchemeItem[key]) + 1
                elif key in self.posName:
                    result[key] = artifactSchemeItem[key]
        return result

    # 推荐圣遗物
    def recommend(self, params):
        # 获取组合类型
        if params["suitA"] == "选择套装" and params["suitB"] == "选择套装":
            combinationKey = "1+1+1+1+1"
        elif params["suitA"] == "选择套装" and params["suitB"] != "选择套装":
            params["suitA"] = params["suitB"]
            combinationKey = "4+1"
        elif params["suitA"] != "选择套装" and params["suitB"] == "选择套装":
            combinationKey = "4+1"
        elif params["suitA"] != "选择套装" and params["suitB"] != "选择套装":
            if params["suitA"] == params["suitB"]:
                combinationKey = "4+1"
            else:
                combinationKey = "2+2+1"
        else:
            combinationKey = "1+1+1+1+1"

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
                if posItem in self.mainTagType:
                    if artifactValue["mainTag"] not in params["needMainTag"][posItem]:
                        # print("主词条不符合")
                        continue

                # 开始筛选
                tempItem = {}
                tempItem["artifactID"] = artifactKey
                tempItem["name"] = artifactValue["name"]
                tempItem["score"] = self.newScore(artifactValue, params["character"])[1]

                if combinationKey == "1+1+1+1+1":
                    array['C'].append(tempItem)
                elif combinationKey == "4+1":
                    if artifactValue["name"] == self.suitConfig[params["suitA"]][posItem]:
                        array["A"].append(tempItem)
                    else:
                        array['C'].append(tempItem)
                elif combinationKey == "2+2+1":
                    if artifactValue["name"] == self.suitConfig[params["suitA"]][posItem]:
                        array["A"].append(tempItem)
                    elif artifactValue["name"] == self.suitConfig[params["suitB"]][posItem]:
                        array["B"].append(tempItem)
                    else:
                        array['C'].append(tempItem)

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
            scheme = self.artifactScheme[owner]

            params = {}
            params["suitA"] = scheme["suitA"]
            params["suitB"] = scheme["suitB"]
            params["needMainTag"] = {
                "时之沙": scheme["时之沙"],
                "空之杯": scheme["空之杯"],
                "理之冠": scheme["理之冠"],
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
