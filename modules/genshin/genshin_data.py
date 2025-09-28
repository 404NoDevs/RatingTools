'''个人数据数据处理'''

from modules.base.base_data import BaseData
from modules.genshin.genshin_constants import *
from utils import markPrint


class Data(BaseData):
    def __init__(self):

        self.entryArray = ["暴击率", "暴击伤害", "攻击力", "生命值", "防御力", "元素精通", "元素充能效率"]
        self.posName = ["生之花", "死之羽", "时之沙", "空之杯", "理之冠"]
        self.mainAttrType = {
            "时之沙": ["生命值", "攻击力", "防御力", "元素精通", "元素充能效率"],
            "空之杯": ["生命值", "攻击力", "防御力", "元素精通", "物理伤害加成", "火元素伤害加成", "雷元素伤害加成", "水元素伤害加成", "草元素伤害加成", "风元素伤害加成", "岩元素伤害加成", "冰元素伤害加成"],
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
            '攻击力': 0.398291 * 0.15,
            '生命值': 0.025990 * 0.15,
            '防御力': 0.335252 * 0.15,
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
        self.evaluate = [
            (50, (230, 179, 34), "传世珍品"),
            (40, (255, 217, 0), "十分宝贵"),
            (30, (163, 224, 67), "基本合格"),
            (20, (238, 121, 118), "有点屁用"),
            (0, (255, 0, 0), "屁用没有")
        ]

        super().__init__({
            "module_name": "genshin",
            "maxLevel": 20,
            "maxScore": 59.4,  # 标准最大值
            "maxScore2": 70.2,  # 理论最大值
            "oneMaxScore": 39.6,  # 单词条标准最大值
            "oneMaxScore2": 46.6   # 单词条理论最大值
        })

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

    def get_evaluate_config(self):
        return self.evaluate

    def get_evaluate(self, score):
        for item in self.evaluate:
            if score >= item[0]:
                return item

    def checkArtifactName(self, name, parts):
        result = False
        for item in self.suitConfig:
            if isinstance(self.suitConfig[item], dict):
                if self.suitConfig[item][parts] == name:
                    result = True
                    break
        return result

    # 获取下标
    def getIndexByCharacter(self, character):
        result = {"suitA": 0, "suitB": 0, "时之沙": [], "空之杯": [], "理之冠": []}
        if character in self.characters:
            characterItem = self.characters[character]
            for key in characterItem:
                if key == "suitA" or key == "suitB":
                    suitKeyArray = list(self.suitConfig.keys())
                    if characterItem[key] in suitKeyArray:
                        result[key] = suitKeyArray.index(characterItem[key]) + 1
                elif key in self.posName:
                    result[key] = characterItem[key]
        return result

    # 推荐圣遗物
    def recommend(self, params):
        if params["suitA"] == "":
            params["suitA"] = NO_SELECT_KEY
        if params["suitB"] == "":
            params["suitB"] = NO_SELECT_KEY

        # 获取组合类型
        combinationKey = ""
        if params["suitA"] == NO_SELECT_KEY and params["suitB"] == NO_SELECT_KEY:
            combinationKey = "1+1+1+1+1"
        elif params["suitA"] == NO_SELECT_KEY and params["suitB"] != NO_SELECT_KEY:
            params["suitA"] = params["suitB"]
            combinationKey = "4+1"
        elif params["suitA"] != NO_SELECT_KEY and params["suitB"] == NO_SELECT_KEY:
            combinationKey = "4+1"
        elif params["suitA"] != NO_SELECT_KEY and params["suitB"] != NO_SELECT_KEY:
            if TWO_PIECE_SET_KEY not in params["suitA"] and \
               TWO_PIECE_SET_KEY not in params["suitB"] and \
               params["suitA"] == params["suitB"]:
                combinationKey = "4+1"
            else:
                combinationKey = "2+2+1"
        else:
            combinationKey = "1+1+1+1+1"

        def tempFunction(suitA, suitB):

            # 获取组合描述文本
            if combinationKey == "4+1":
                combinationText = f"4{suitA[:2]}+1散件"
            elif combinationKey == "2+2+1":
                combinationText = f"2{suitA[:2]}+2{suitB[:2]}+1散件"
            else:
                combinationText = "5散件"

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

                    if combinationKey == "1+1+1+1+1":
                        array['C'].append(tempItem)
                    elif combinationKey == "4+1":
                        if artifactValue["name"] == self.suitConfig[suitA][posItem]:
                            array["A"].append(tempItem)
                        else:
                            array['C'].append(tempItem)
                    elif combinationKey == "2+2+1":
                        if artifactValue["name"] == self.suitConfig[suitA][posItem]:
                            array["A"].append(tempItem)
                        elif artifactValue["name"] == self.suitConfig[suitB][posItem]:
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
            tempScoreArray = []
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
                        # tempFlag = 1
                        # break
                        pass

                # if tempFlag:
                #     # print("圣遗物不存在 计分中止2")
                #     continue
                scoreItem = {}
                scoreItem["combinationType"] = f"[{combinationText}]{''.join(combinationItem)}"
                scoreItem["combinationName"] = combinationName
                scoreItem["scoreSum"] = round(scoreSum, 1)
                tempScoreArray.append(scoreItem)
            return tempScoreArray

        # 添加散件套逻辑
        scoreArray = []
        if combinationKey == "2+2+1":
            if TWO_PIECE_SET_KEY in params["suitA"]:
                suitA_arryay = self.suitConfig[params["suitA"]]
            else:
                suitA_arryay = [params["suitA"]]

            if TWO_PIECE_SET_KEY in params["suitB"]:
                suitB_arryay = self.suitConfig[params["suitB"]]
            else:
                suitB_arryay = [params["suitB"]]

            combinations = [list(item) for item in {
                frozenset({x, y})  # 自动去重顺序
                for x in suitA_arryay
                for y in suitB_arryay
                if x != y  # 禁止同元素组合
            }]
            # print(combinations)

            for combinationItem in combinations:
                scoreArray.extend(tempFunction(combinationItem[0], combinationItem[1]))  # 用 extend 合并子列表
        else:
            scoreArray = tempFunction(params["suitA"], params["suitB"])


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
            "suitName": "",
            "suitPart": ""
        }
        for suitName in self.suitConfig:
            for part in self.suitConfig[suitName]:
                if self.suitConfig[suitName][part] == ocr_result["name"]:
                    suitData["suitName"] = suitName
                    suitData["suitPart"] = part

        if any((
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
            # print("any" in self.characters[character].get("suit", []))
            # print(suitData["suitName"] in self.characters[character].get("suit", []))
            # print(self.characters[character].get("suitA", "") == suitData["suitName"])
            # print(self.characters[character].get("suitB", "") == suitData["suitName"])
            if any((
                    "any" in self.characters[character].get("suit", []),
                    suitData["suitName"] in self.characters[character].get("suit", []),
                    self.characters[character].get("suitA", "no") == suitData["suitName"],
                    self.characters[character].get("suitB", "no") == suitData["suitName"]
            )):
                # 检查主词条是否合规
                if any((
                        ocr_result["parts"] not in self.characters[character],
                        ocr_result["mainAttr"] in self.characters[character].get(ocr_result["parts"], [])
                )):

                    super = []
                    core = []
                    aux = []
                    for key, value in self.characters[character]["weight"].items():
                        if key in ["攻击力", "生命值", "防御力"]:
                            key += "百分比"
                        if value > 1.5:  # 超级词条
                            super.append(key)
                        if value > 0.75:  # 核心词条
                            core.append(key)
                        elif value > 0.375:  # 辅助词条
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

                    super_len = len(set(super) & set(ocr_result["subAttr"].keys()))
                    core_len = len(set(core) & set(ocr_result["subAttr"].keys()))
                    aux_len = len(set(aux) & set(ocr_result["subAttr"].keys()))

                    if any((
                            super_len >= 1,
                            mainInSub and core_len >= 1,
                            mainInSub and aux_len >= 1,
                            core_len >= 2,
                            core_len >= 1 and aux_len >= 1
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
        # for item in tempList:

        result["list"] = tempList
        markPrint(result)
        return result


data = Data()
