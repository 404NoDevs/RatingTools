''' 个人数据数据处理 '''
from modules.base.base_data import BaseData


class Data(BaseData):
    def __init__(self):
        super().__init__({
            "module_name": "starRail",
            "maxLevel": 15,
            "maxScore": 58.5
        })

        self.entryArray = ["速度", "生命值", "攻击力", "防御力", "暴击率", "暴击伤害", "击破特攻", "效果命中", "效果抵抗"]
        self.posNameOut = ["头部", "手部", "躯干", "脚部"]
        self.posNameIn = ["位面球", "连结绳"]
        self.mainAttrType = {
            "躯干": ["生命值", "攻击力", "防御力", "暴击率", "暴击伤害", "治疗量加成", "效果命中"],
            "脚部": ["生命值", "攻击力", "防御力", "速度"],
            "位面球": ["生命值", "攻击力", "防御力", "物理属性伤害提高", "火属性伤害提高", "冰属性伤害提高",
                       "雷属性伤害提高", "风属性伤害提高", "量子属性伤害提高", "虚数属性伤害提高", ],
            "连结绳": ["生命值", "攻击力", "防御力", "击破特攻", "能量恢复效率"]
        }
        self.combinationTypeOut = {
            "1+1+1+1": [
                ["B", "B", "B", "B"]
            ],
            "2+2": [
                # 两个A两个B
                ["A", "A", "B", "B"],
                ["A", "B", "A", "B"],
                ["A", "B", "B", "A"],
                ["B", "A", "A", "B"],
                ["B", "A", "B", "A"],
                ["B", "B", "A", "A"]
            ],
            "4": [
                ["A", "A", "A", "A"]
            ]
        }
        self.combinationTypeIn = {
            "1+1": [
                ["B", "B"]
            ],
            "2": [
                ["A", "A"]
            ]
        }
        self.coefficient = {
            '暴击率': 2,
            '暴击伤害': 1,
            '攻击力百分比': 1.5,
            '生命值百分比': 1.5,
            '防御力百分比': 1.2,
            '攻击力': 0.076535,
            '生命值': 0.153071,
            '防御力': 0.153071,
            "速度": 2.492308,
            '击破特攻': 1,
            '效果命中': 1.5,
            '效果抵抗': 1.5
        }
        self.average = {
            '暴击率': 2.915,
            '暴击伤害': 5.83,
            '攻击力百分比': 3.89,
            '生命值百分比': 3.89,
            '防御力百分比': 4.86,
            '攻击力': 18.966667,
            '生命值': 37.933333,
            '防御力': 18.966667,
            "速度": 2.3,
            '击破特攻': 5.83,
            '效果命中': 3.89,
            '效果抵抗': 3.89
        }

    def getSuitConfig(self, type):
        return self.suitConfig.get(type, {})

    def getEntryArray(self):
        return self.entryArray

    def getPosName(self):
        return self.posNameOut + self.posNameIn

    def getMainAttrType(self):
        return self.mainAttrType

    def getCoefficient(self):
        return self.coefficient

    def getAverage(self):
        return self.average

    # 获取下标
    def getIndexByCharacter(self, character):
        result = {"suitA": 0, "suitB": 0, "suitC": 0, "躯干": [], "脚部": [], "位面球": [], "连结绳": []}
        if character in self.characters:
            artifactSchemeItem = self.characters[character]
            for key in artifactSchemeItem:
                if key == "suitA" or key == "suitB":
                    suitKeyArray = list(self.suitConfig["外圈"].keys())
                    if artifactSchemeItem[key] in suitKeyArray:
                        result[key] = suitKeyArray.index(artifactSchemeItem[key]) + 1
                if key == "suitC":
                    suitKeyArray = list(self.suitConfig["内圈"].keys())
                    if artifactSchemeItem[key] in suitKeyArray:
                        result[key] = suitKeyArray.index(artifactSchemeItem[key]) + 1
                elif key in (self.posNameOut + self.posNameIn):
                    result[key] = artifactSchemeItem[key]
        return result

    # 推荐圣遗物
    def recommend(self, params):
        # 获取组合类型
        if params["suitA"] == "选择套装" and params["suitB"] == "选择套装":
            combinationKeyOut = "1+1+1+1"
        elif params["suitA"] == "选择套装" and params["suitB"] != "选择套装":
            params["suitA"] = params["suitB"]
            combinationKeyOut = "4"
        elif params["suitA"] != "选择套装" and params["suitB"] == "选择套装":
            combinationKeyOut = "4"
        elif params["suitA"] != "选择套装" and params["suitB"] != "选择套装":
            if params["suitA"] == params["suitB"]:
                combinationKeyOut = "4"
            else:
                combinationKeyOut = "2+2"
        else:
            combinationKeyOut = "1+1+1+1"

        if params["suitC"] == "选择套装":
            combinationKeyIn = "1+1"
        elif params["suitC"] != "选择套装":
            combinationKeyIn = "2"

        # 筛选评分最大值套装
        # 计算外圈
        suitOut = {
            "A": {},
            "B": {}
        }
        for posItem in self.posNameOut:
            arrayOut = {
                "A": [],
                "B": []
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
                    # print(params["needMainAttr"][posItem])
                    if artifactValue["mainAttr"] not in params["needMainAttr"][posItem]:
                        # print("主词条不符合")
                        continue

                # 开始筛选
                tempItem = {}
                tempItem["artifactID"] = artifactKey
                tempItem["name"] = artifactValue["name"]
                tempItem["score"] = self.newScore(artifactValue, params["character"])[1]

                if combinationKeyOut == "1+1+1+1":
                    arrayOut['B'].append(tempItem)
                elif combinationKeyOut == "2+1+1":
                    if artifactValue["name"] == self.suitConfig["外圈"][params["suitA"]][posItem]:
                        arrayOut["A"].append(tempItem)
                    else:
                        arrayOut['B'].append(tempItem)
                elif combinationKeyOut == "4":
                    if artifactValue["name"] == self.suitConfig["外圈"][params["suitA"]][posItem]:
                        arrayOut["A"].append(tempItem)
                elif combinationKeyOut == "2+2":
                    if artifactValue["name"] == self.suitConfig["外圈"][params["suitA"]][posItem]:
                        arrayOut["A"].append(tempItem)
                    elif artifactValue["name"] == self.suitConfig["外圈"][params["suitB"]][posItem]:
                        arrayOut["B"].append(tempItem)

            # 取出当前位置最大值
            for suitKey in suitOut.keys():
                suitOut[suitKey][posItem] = 0
                if len(arrayOut[suitKey]) > 0:
                    arrayOut[suitKey].sort(key=lambda x: x["score"], reverse=True)
                    suitOut[suitKey][posItem] = arrayOut[suitKey][0]

        # 计算内圈
        suitIn = {
            "A": {},
            "B": {}
        }
        for posItem in self.posNameIn:
            arrayIn = {
                "A": [],
                "B": []
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
                    # print(params["needMainAttr"][posItem])
                    if artifactValue["mainAttr"] not in params["needMainAttr"][posItem]:
                        # print("主词条不符合")
                        continue

                # 开始筛选
                tempItem = {}
                tempItem["artifactID"] = artifactKey
                tempItem["name"] = artifactValue["name"]
                tempItem["score"] = self.newScore(artifactValue, params["character"])[1]

                if combinationKeyIn == "1+1":
                    arrayIn['B'].append(tempItem)
                elif combinationKeyIn == "2":
                    if artifactValue["name"] == self.suitConfig["内圈"][params["suitC"]][posItem]:
                        arrayIn["A"].append(tempItem)

            # 取出当前位置最大值
            for suitKey in suitIn.keys():
                suitIn[suitKey][posItem] = 0
                if len(arrayIn[suitKey]) > 0:
                    arrayIn[suitKey].sort(key=lambda x: x["score"], reverse=True)
                    suitIn[suitKey][posItem] = arrayIn[suitKey][0]

        # print(suitOut)
        # print(suitIn)

        # 根据组合类型选出来总分最大组合

        # 筛选外圈
        scoreArrayOut = []
        combinationOut = self.combinationTypeOut[combinationKeyOut]
        for combinationItem in combinationOut:
            combinationName = {}
            tempFlag = False
            scoreSum = 0

            for posItem, combinationItemItem in zip(self.posNameOut, combinationItem):
                if suitOut[combinationItemItem][posItem]:
                    scoreNum = suitOut[combinationItemItem][posItem]["score"]
                    combinationName[posItem] = suitOut[combinationItemItem][posItem]["artifactID"]
                    scoreSum += scoreNum
                else:
                    print(posItem + " 不存在 计分中止1")
                    tempFlag = True
                    break

            if tempFlag:
                # print("不存在 计分中止2")
                continue
            scoreOutItem = {}
            scoreOutItem["combinationType"] = "".join(combinationItem)
            scoreOutItem["combinationName"] = combinationName
            scoreOutItem["scoreSum"] = round(scoreSum, 1)
            scoreArrayOut.append(scoreOutItem)

        # 筛选内圈
        scoreArrayIn = []
        combinationIn = self.combinationTypeIn[combinationKeyIn]
        for combinationItem in combinationIn:
            combinationName = {}
            tempFlag = False
            scoreSum = 0

            for posItem, combinationItemItem in zip(self.posNameIn, combinationItem):
                if suitIn[combinationItemItem][posItem]:
                    scoreNum = suitIn[combinationItemItem][posItem]["score"]
                    combinationName[posItem] = suitIn[combinationItemItem][posItem]["artifactID"]
                    scoreSum += scoreNum
                else:
                    print(posItem + " 不存在 计分中止21")
                    tempFlag = True
                    break

            if tempFlag:
                # print("不存在 计分中止22")
                continue
            scoreInItem = {}
            scoreInItem["combinationType"] = "".join(combinationItem)
            scoreInItem["combinationName"] = combinationName
            scoreInItem["scoreSum"] = round(scoreSum, 1)
            scoreArrayIn.append(scoreInItem)

        # print(scoreArrayOut)
        # print(scoreArrayIn)

        scoreArray = []
        for outItem in scoreArrayOut:
            for inItem in scoreArrayIn:
                tempItem = {}
                tempItem["combinationType"] = outItem["combinationType"] + inItem["combinationType"]
                outItem["combinationName"].update(inItem["combinationName"])
                tempItem["combinationName"] = outItem["combinationName"]
                tempItem["scoreSum"] = round(outItem["scoreSum"] + inItem["scoreSum"], 1)
                scoreArray.append(tempItem)
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
            params["suitC"] = scheme["suitC"]
            params["needMainAttr"] = {
                "躯干": scheme["躯干"],
                "脚部": scheme["脚部"],
                "位面球": scheme["位面球"],
                "连结绳": scheme["连结绳"]
            }
            params["character"] = owner
            params["heroConfig"] = self.characters[owner]
            params["selectType"] = 1
            recommendResult, _ = self.recommend(params)

            if recommendResult:
                new = recommendResult[0]["combinationName"]
                old = self.artifactOwnerList[owner]
                for pos in (self.posNameOut + self.posNameIn):
                    if new[pos] != old[pos]:
                        result.append(owner)
                        break
            else:
                # 没有推荐结果
                print("没有推荐结果")
                pass
        return result


data = Data()
