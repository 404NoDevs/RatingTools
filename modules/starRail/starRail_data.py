''' 个人数据数据处理 '''
from modules.base.base_data import BaseData
from utils import markPrint


class Data(BaseData):
    def __init__(self):
        super().__init__({
            "module_name": "starRail",
            "maxLevel": 15,
            "maxScore": 52.4,  # 标准最大值
            "maxScore2": 58.5  # 理论最大值
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
            '攻击力': 0,
            '生命值': 0,
            '防御力': 0,
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
        self.evaluate = [
            (45, (230, 179, 34), "传世珍品"),
            (35, (255, 217, 0), "十分宝贵"),
            (25, (163, 224, 67), "基本合格"),
            (15, (238, 121, 118), "有点屁用"),
            (0, (255, 0, 0), "屁用没有")
        ]

    def getSuitConfig(self, type="all"):
        result = {}
        if type == "all":
            result.update(self.suitConfig.get("外圈", {}))
            result.update(self.suitConfig.get("内圈", {}))
        else:
            result.update(self.suitConfig.get(type, {}))
        return result

    def getEntryArray(self):
        return self.entryArray

    def getPosName(self, type="all"):
        result = []
        if type == "all":
            result = self.posNameOut + self.posNameIn
        elif type == "out":
            result += self.posNameOut
        elif type == "in":
            result += self.posNameIn
        else:
            result += []
        return result
    def getMainAttrType(self):
        return self.mainAttrType

    def getCoefficient(self):
        return self.coefficient

    def getAverage(self):
        return self.average

    def get_evaluate_config(self):
        return self.evaluate

    def get_evaluate(self, score):
        for item in self.evaluate:
            if score >= item[0]:
                return item

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
                    # print(posItem + " 不存在 计分中止1")
                    # tempFlag = True
                    # break
                    pass

            # if tempFlag:
            #     # print("不存在 计分中止2")
            #     continue
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
                    # print(posItem + " 不存在 计分中止21")
                    # tempFlag = True
                    # break
                    pass

            # if tempFlag:
                # print("不存在 计分中止22")
                # continue

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
                    if new.get(pos, "") != old.get(pos, ""):
                        result.append(owner)
                        break
            else:
                # 没有推荐结果
                print("没有推荐结果")
                pass
        return result

    def getAnalyzeData(self, ocr_result):
        result = {
            "list": [],
            "tips": ""
        }
        if "isCorrected" in ocr_result and ocr_result["isCorrected"]:
            # 数据发生过矫正，无需分析
            result["tips"] = "数据发生过矫正，无需分析"
            return result

        # 获取套装名称及位置
        suitData = {
            "suitType": "",
            "suitName": "",
            "suitPart": ""
        }
        for type in self.suitConfig:
            for suitName in self.suitConfig[type]:
                for part in self.suitConfig[type][suitName]:
                    if self.suitConfig[type][suitName][part] == ocr_result["name"]:
                        suitData["suitType"] = type
                        suitData["suitName"] = suitName
                        suitData["suitPart"] = part

        if any((
                suitData["suitType"] == "",
                suitData["suitName"] == "",
                suitData["suitPart"] == ""
        )):
            result["tips"] = "未识别到套装"
            return result

        # 分析可使用者
        tempList = []
        for character in self.characters:
            # 检查套装名称是否合规
            # print(character)
            # print(suitData)
            # print("any" in self.characters[character].get("suit", []))
            # print(suitData["suitName"] in self.characters[character].get("suit", []))
            # print(self.characters[character].get("suitA", "no") == suitData["suitName"])
            # print(self.characters[character].get("suitB", "no") == suitData["suitName"])
            # print(self.characters[character].get("suitC", "no") == suitData["suitName"])
            if any((
                    "any" in self.characters[character].get("suit", []),
                    suitData["suitName"] in self.characters[character].get("suit", []),
                    self.characters[character].get("suitA", "no") == suitData["suitName"],
                    self.characters[character].get("suitB", "no") == suitData["suitName"],
                    self.characters[character].get("suitC", "no") == suitData["suitName"]
            )):
                # 检查主词条是否合规
                if any((
                        ocr_result["parts"] not in self.characters[character],
                        ocr_result["mainAttr"] in self.characters[character].get(ocr_result["parts"], [])
                )):
                    super_core = []
                    core = []
                    aux = []
                    for key, value in self.characters[character]["weight"].items():
                        if key in ["攻击力", "生命值", "防御力"]:
                            key += "百分比"
                        if value >= 1.5:  # 超级核心词条
                            super_core.append(key)
                        if value >= 0.7:  # 核心词条
                            core.append(key)
                        elif value >= 0.3:  # 辅助词条
                            aux.append(key)
                        else:
                            # 无效词条
                            pass

                    mainInSub = False
                    if suitData["suitPart"] in self.mainAttrType:
                        mainAttr = ocr_result["mainAttr"]
                        if mainAttr in ["攻击力", "生命值", "防御力"]:
                            mainAttr += "百分比"
                        if mainAttr in core or mainAttr in aux:
                            mainInSub = True

                    super_core_len = len(set(super_core) & set(ocr_result["subAttr"].keys()))
                    coreLen = len(set(core) & set(ocr_result["subAttr"].keys()))
                    auxLen = len(set(aux) & set(ocr_result["subAttr"].keys()))
                    if any((
                            super_core_len >= 1,
                            mainInSub and coreLen >= 1,
                            mainInSub and auxLen >= 1,
                            coreLen >= 2,
                            coreLen >= 1 and auxLen >= 1
                    )):
                        tempResult = {
                            "name": character
                        }
                        current = self.newScore(ocr_result, character)
                        tempResult["current_score"] = current[1]
                        tempResult["current_entries"] = current[3]

                        already_artifact_data = {}
                        already_artifact = self.getArtifactOwner(character)
                        if suitData["suitPart"] in already_artifact:
                            already_artifactId = already_artifact[suitData["suitPart"]]
                            already_artifact_data = self.getArtifactItem(suitData["suitPart"], already_artifactId)
                        if already_artifact_data:
                            already = self.newScore(already_artifact_data, character)
                            tempResult["already_score"] = already[1]
                            tempResult["already_entries"] = already[3]
                        tempList.append(tempResult)

        if len(tempList) == 0:
            result["tips"] = "未找到适配的角色"
        else:
            if ocr_result["lvl"] == str(self.maxLevel):
                # 已满级 进行分析
                for item in tempList:
                    if item["current_score"] >= self.maxScore / 2:
                        result["tips"] = "还行，能用"
                        break
                    else:
                        result["tips"] = "建议分解"
            else:
                result["tips"] = "当前装备未满级"

        result["list"] = tempList

        markPrint(result)
        return result


data = Data()
