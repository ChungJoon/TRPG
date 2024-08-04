import random
from dataclass import PowerDamage
import re
import copy
from main import db

# コマンドの変数を保存するリスト
variables = {}
challengebool = {}
Actor = ""
Targets = []

def execute_code(code,actor,targets):
    global Actor,Targets,variables
    results = [f'<<< {actor}:{code} >>>']
    commands = code.split(';')
    variables = {}
    Actor = actor
    Targets = targets
    variables["self"] = Actor  # 変数に値を格納

    for command in commands:
        command = command.strip()
        # command = replace_variables(command)
        log_message, output_value = process_command(command)
        results.append(log_message)
        if output_value is not None:
            variables['last_result'] = output_value  # 変数 'last_result' に結果を保存

    return "\n".join(results)

def process_command(command_input):
    # 変数代入とコマンドの分割処理
    assignment_pattern = r'^(\w+)\s*=\s*(.*)$'
    match = re.match(assignment_pattern, command_input)
    
    if match:
        variable_name = match.group(1)
        command = match.group(2).strip()
        command = replace_variables(command)
        log_message, output_value = execute_single_command(command)
        variables[variable_name] = output_value  # 変数に値を格納
        return f"{log_message} > {variable_name} に値を代入しました。", output_value
    else:
        if "loop" in command_input:
            command = command_input
        else:
            command = replace_variables(command_input)
        return execute_single_command(command)

def replace_variables(command):
    variable_pattern = r'\$(\w+)'  # $variable の形式で変数を検出
    matches = re.findall(variable_pattern, command)
    
    for match in matches:
        if match == "target":
            command = command.replace(f"${match}", match)
        elif match in variables:
            command = command.replace(f"${match}", str(variables[match]))

    return command

def execute_single_command(command):
    # 正規表現パターンの定義
    command_patterns = {
        'dice': r'^dice\((\d+),\s*(\d+)\)$',
        'getstatus': r'^getstatus\(([^,]+),\s*([^,]+)\)$',
        'setstatus': r'^setstatus\(([^,]+),\s*([^,]+),\s*([^,]+)\)$',
        'getweapon': r'^getweapon\((-?\d+),\s*(\S+)\)$',
        'getprotector': r'^getprotector\((-?\d+),\s*(\S+)\)$',
        'power': r'^power\((\d+),\s*(\d+)\)$',
        'getjoblevel': r'^getjoblevel\((\S+),\s*(\S+)\)$',
        'useitem': r'^useitem\((-?\d+),\s*(-?\d+)\)$',
        'heal': r'^heal\((\S+),\s*(-?\d+)\)$',
        'getbulletbox': r'^getbulletbox\((-?\d+),\s*(\S+),\s*(\S+)\)$',
        'get_magiclevel': r'^get_magiclevel\((\S+),\s*(\S+)\)$',
        'getsum': r'^getsum\(([^,]+(?:,\s*[^,]+)*)\)$',
        'getmax': r'^getmax\(([^,]+(?:,\s*[^,]+)*)\)$',
        'getmin': r'^getmin\(([^,]+(?:,\s*[^,]+)*)\)$',
        'plus': r'^plus\((-?\d+),\s*(-?\d+)\)$',
        'minus': r'^minus\((-?\d+),\s*(-?\d+)\)$',
        'multiply': r'^multiply\((-?\d+),\s*(-?\d+)\)$',
        'divide': r'^divide\((-?\d+),\s*(-?\d+)\)$',
        'ifmore': r'^ifmore\((-?\d+),\s*(-?\d+)\)$',
        'ifless': r'^ifless\((-?\d+),\s*(-?\d+)\)$',
        'ifequal': r'^ifequal\((-?\d+),\s*(-?\d+)\)$',
        'ifeqmore': r'^ifeqmore\((-?\d+),\s*(-?\d+)\)$',
        'ifeqless': r'^ifeqless\((-?\d+),\s*(-?\d+)\)$',
        'actionif': r'^actionif\((True|False|[a-zA-Z_]+\(([^,]+,\s*)*[^,]+\)),\s*([a-zA-Z_]+\(([^,]+,\s*)*[^,]+\))\)$',
        'loop': r'loop\s*\(\s*(True|False|[\w]+\([^()]*\))\s*,\s*((?:[\w]+=)?[\w]+\([^()]*\)(?:\s*\+\s*(?:[\w]+=)?[\w]+\([^()]*\))*)\s*,\s*([\w]+\([^()]*\))\s*\)',
        'criticalloop': r'^criticalloop\((-?\d+),\s*(-?\d+),\s*(-?\d+)\)$',
        'monstercriticalloop': r'^monstercriticalloop\((-?\d+),\s*(-?\d+)\)$',
        'basic_attack': r'^basic_attack\((-?\d+),\s*(-?\d+),\s*(-?\d+)\)$',
        'basic_attack_magic': r'^basic_attack_magic\((-?\d+),\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)\)$',
        'physical_attack': r'^physical_attack\((-?\d+)\)$',
        'basic_magic_attack': r'^basic_magic_attack\((-?\d+),\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)\)$',
        'magical_attack': r'^magical_attack\((-?\d+),\s*(-?\d+),\s*(\S+)\)$',
        'magical_attack_cpu': r'^magical_attack_cpu\((-?\d+),\s*(-?\d+),\s*(-?\d+)\)$',
        'shoot_attack': r'^shoot_attack\((-?\d+),\s*(-?\d+)\)$',
        'magishoot_attack': r'^magishoot_attack\((-?\d+),\s*(-?\d+),\s*(-?\d+)\)$',
        'attack': r'^attack\((-?\d+),\s*(-?\d+)\)$',
        'fixattack': r'^fixattack\((\S+),\s*(-?\d+)\)$',
        'challenge': r'^challenge\((-?\d+),\s*(-?\d+),\s*(-?\d+),\s*(-?\d+)\)$',
        'challenge_self': r'^challenge_self\((-?\d+)\)$',
        'challenge_dice': r'^challenge_dice\((-?\d+),\s*(-?\d+)\)$',
        'challenge_status': r'^challenge_status\((\S+),\s*(\S+)\)$',
        'challenge_attack': r'^challenge_attack\((\S+),\s*(-?\d+),\s*(-?\d+)\)$',
        'get_reaction': r'^get_reaction\((\S+),\s*(-?\d+),\s*(-?\d+)\)$',
        'cal_damage': r'^cal_damage\((-?\d+),\s*(-?\d+),\s*(-?\d+)\)$',
        'cal_physicaldamage': r'^cal_physicaldamage\((\S+),\s*(-?\d+),\s*(-?\d+)\)$',
        'give_damage': r'^give_damage\((\S+),\s*(-?\d+)\)$',
        'give_phygicaldamage': r'^give_phygicaldamage\((\S+),\s*(-?\d+)\)$',
        'give_magicaldamage': r'^give_magicaldamage\((\S+),\s*(-?\d+)\)$',
    }

    for command_name, pattern in command_patterns.items():
        match = re.match(pattern, command)
        if match:
            if command_name == 'dice':
                return dice(*match.groups())
            elif command_name == 'getstatus':
                return getstatus(*match.groups())
            elif command_name == 'setstatus':
                return setstatus(*match.groups())
            elif command_name == 'getweapon':
                return getweapon(*match.groups())
            elif command_name == 'getprotector':
                return getprotector(*match.groups())
            elif command_name == 'power':
                return power(*match.groups())
            elif command_name == 'getjoblevel':
                return getjoblevel(*match.groups())
            elif command_name == 'useitem':
                return useitem(*match.groups())
            elif command_name == 'heal':
                return heal(*match.groups())
            elif command_name == 'getbulletbox':
                return getbulletbox(*match.groups())
            elif command_name == 'get_magiclevel':
                return get_magiclevel(*match.groups())
            elif command_name == 'getsum':
                return getsum(*match.groups())
            elif command_name == 'getmax':
                return getmax(*match.groups())
            elif command_name == 'getmin':
                return getmin(*match.groups())
            elif command_name == 'plus':
                return plus(*match.groups())
            elif command_name == 'minus':
                return minus(*match.groups())
            elif command_name == 'multiply':
                return multiply(*match.groups())
            elif command_name == 'divide':
                return divide(*match.groups())
            elif command_name == 'ifmore':
                return ifmore(*match.groups())
            elif command_name == 'ifless':
                return ifless(*match.groups())
            elif command_name == 'ifequal':
                return ifequal(*match.groups())
            elif command_name == 'ifeqmore':
                return ifeqmore(*match.groups())
            elif command_name == 'ifeqless':
                return ifeqless(*match.groups())
            elif command_name == 'actionif':
                return actionif(match.group(1), match.group(3))
            elif command_name == 'loop':
                return loop(*match.groups())
            elif command_name == 'criticalloop':
                return criticalloop(*match.groups())
            elif command_name == 'monstercriticalloop':
                return monstercriticalloop(*match.groups())
            elif command_name == 'basic_attack':
                return basic_attack(*match.groups())
            elif command_name == 'basic_attack_magic':
                return basic_attack_magic(*match.groups())
            elif command_name == 'physical_attack':
                return physical_attack(*match.groups())
            elif command_name == 'basic_magic_attack':
                return basic_magic_attack(*match.groups())
            elif command_name == 'magical_attack':
                return magical_attack(*match.groups())
            elif command_name == 'magical_attack_cpu':
                return magical_attack_cpu(*match.groups())
            elif command_name == 'shoot_attack':
                return shoot_attack(*match.groups())
            elif command_name == 'magishoot_attack':
                return magishoot_attack(*match.groups())
            elif command_name == 'attack':
                return monsterattack(*match.groups())
            elif command_name == 'fixattack':
                return fixattack(*match.groups())
            elif command_name == 'challenge':
                log_message, bool, _, _ = challenge(*match.groups())
                return log_message, bool
            elif command_name == 'challenge_self':
                log_message, bool, _ = challenge_self(*match.groups())
                return log_message, bool
            elif command_name == 'challenge_dice':
                log_message, bool, _, _ = challenge_dice(*match.groups())
                return log_message, bool
            elif command_name == 'challenge_status':
                log_message, bool, _ = challenge_status(*match.groups())
                return log_message, bool
            elif command_name == 'challenge_attack':
                log_message, bool, _ = challenge_attack(*match.groups())
                return log_message, bool
            elif command_name == 'get_reaction':
                return get_reaction(*match.groups())
            elif command_name == 'cal_damage':
                return cal_damage(*match.groups())
            elif command_name == 'cal_physicaldamage':
                log_message, damage_value, _ = cal_physicaldamage(*match.groups())
                return log_message, damage_value
            elif command_name == 'give_damage':
                return give_damage(*match.groups())
            elif command_name == 'give_phygicaldamage':
                return give_phygicaldamage(*match.groups())
            elif command_name == 'give_magicaldamage':
                return give_magicaldamage(*match.groups())
    
    log_message = f'サポートされていないコマンドです: {command}'
    return log_message, None

def loop(init, code, trigger):
    count = 0
    log_messages = ''
    result = '1'

    if init == "True" or init == True:
        bool = True
    elif init == "False" or init == False:
        bool = False
        log_messages = "ループ繰り返し: False"
    else:
        bool = sub_code(init)[1]

    while bool == True and count < 20:
        count +=  1
        command = copy.copy(trigger)
        log_message,result = sub_code(code)
        nextbool = sub_code(command)[1]
        bool = nextbool
        log_messages = log_messages+","+str(log_message)+","+f"ループ繰り返し: {bool}"

    return log_messages, result

def actionif(bool, command):
    if bool == "True" or bool == True:
        log_message,result = sub_code(command)
        return log_message,result 
    else:
        bool = sub_code(bool)[1]
        if bool == True:
            log_message,result = sub_code(command)
            return log_message,result 
        else:
            log_message = "実行なし"
            return log_message,None
    
def sub_code(code):
    log_message = ""
    commands = code.split('+')
    for command in commands:
        command = command.strip()
        command = replace_variables(command)
        message, output_value = process_command(command)
        log_message = log_message + message
    if output_value is not None:
        variables['result'] = output_value
    return log_message,output_value


def dice(x, y):
    num_dice = int(x)
    num_sides = int(y)
    rolls = [random.randint(1, num_sides) for _ in range(num_dice)]
    sum_value = sum(rolls)
    log_message = f"ダイス結果: {', '.join(map(str, rolls))} (合計: {sum_value})"
    return log_message, sum_value

def getstatus(unit_name,status_name):
    if unit_name == "target":
        log_message = ""
        for target in Targets:
            message,status_value=getstatus(target,status_name)
            log_message = log_message + message

        return log_message,status_value

    from dataclass import Unit
    unit = Unit.query.filter_by(name=unit_name).first()

    if unit is None:
        log_message = "ユニットが存在しません"
        return log_message,None
    else:
        try:
            status_value = getattr(unit,status_name)
            log_message = f"{unit_name}の{status_name}: {status_value}"
        except:
            status_value = 0
            log_message = f"{unit_name}に'{status_name}'というステータスは存在しません"
        if unit.type == "魔物":
            log_message = f"魔物のステータスは閲覧できません。"
        
    return log_message,status_value

def setstatus(unit_name,status_name,value):
    from dataclass import Unit

    if unit_name == "target":
        log_message = ""
        for target in Targets:
            message,status_value=setstatus(target,status_name,value)
            log_message = log_message + message

        return log_message,status_value

    unit = Unit.query.filter_by(name=unit_name).first()
    value = int(value)

    if unit is None:
        log_message = "ユニットが存在しません"
        return log_message,None
    
    else:
        try:
            # MP軽減ありの時計算
            if status_name == "MP":
                if value < 0:
                    mpcover = unit.MP軽減
                    value = int(value) + int(mpcover)
                    unit.MP軽減 = unit.MP消費カット
                    if value > 0:
                        value = 0

            status_value = getattr(unit,status_name)
            new_value = status_value + int(value)
            setattr(unit,status_name,new_value)
            db.session.add(unit)
            db.session.commit()
            if unit.type == "魔物":
                log_message = f" {unit_name}の{status_name}を {value} 変化させました。"
            else:
                log_message = f" {unit_name}の{status_name}を {value} 変化させました。 現在{status_name}: {new_value}"
        except:
            log_message = f" {unit_name}に'{status_name}'というステータスは存在しません。"
            new_value = 0
        
    return log_message,new_value

def getweapon(weapon_id,status_name):
    from dataclass import Weapon
    weapon = Weapon.query.filter_by(id=weapon_id).first()

    if weapon is None:
        log_message = f" ID{weapon_id}の武器が存在しません。"
        return log_message,0
    else:
        try:
            status_value = getattr(weapon,status_name)
            log_message = f" {weapon.name}の{status_name}: {status_value}"
        except:
            log_message = f" {weapon.name}に'{status_name}'というステータスは存在しません。"
            status_value =0
        
    return log_message,status_value

def getprotector(protetor_id,status_name):
    from dataclass import Protector
    weapon = Protector.query.filter_by(id=protetor_id).first()

    if weapon is None:
        log_message = f" ID{protetor_id}の防具が存在しません。"
        return log_message,None
    else:
        try:
            status_value = getattr(weapon,status_name)
            log_message = f" {weapon.name}の{status_name}: {status_value}"
        except:
            log_message = f" {weapon.name}に'{status_name}'というステータスは存在しません。"
        
    return log_message,status_value

def power(x, y):
    power_value = int(x)
    column_number = int(y)
    
    # データベースから値を取得
    power_damage = PowerDamage.query.filter_by(Power=power_value).first()
    
    if not power_damage:
        return f" Power {power_value} のレコードが見つかりません。", None
    
    # カラム名を動的に構築
    column_name = f"col{column_number}"
    
    if not hasattr(power_damage, column_name):
        return f" カラム {column_number} が存在しません。", None
    
    column_value = getattr(power_damage, column_name)
    log_message = f" 威力 {power_value} のダメージは {column_value} です。"
    return log_message, int(column_value)

def monsterattack(critical, additionaldamage):
    # 命中判定
    Accuracy = int(getstatus(Actor,"命中")[1])

    # 自分のダイスと結果取得
    log_message, mydice, myvalue = challenge_self(Accuracy)

    # クリティカル計算
    log_message += " クリティカル計算:"
    message, cvalue = monstercriticalloop(critical,mydice)
    log_message += message

    # ダメージ計算
    maindamage = int(mydice) + int(cvalue) + int(additionaldamage)
    message, bool = basic_attack(Accuracy,maindamage,mydice)
    log_message += message

    return log_message, bool

def fixattack(type,value):
    # 命中判定
    if type == "物理":
        Accuracy = int(getstatus(Actor,"命中")[1])
        # 自分のダイスと結果取得
        log_message, mydice, myvalue = challenge_self(Accuracy)
        message, bool = basic_attack(Accuracy,value,mydice)
    elif type == "魔法":
        magicchallenge = int(getstatus(Actor,"魔力")[1])
        # 自分のダイスと結果取得
        log_message, mydice, myvalue = challenge_self(magicchallenge)
        message, bool = basic_attack_magic(magicchallenge,value,0,mydice)
    elif type == " 射撃":
        Accuracy = int(getstatus(Actor,"命中")[1])
        # 自分のダイスと結果取得
        log_message, mydice, myvalue = challenge_self(Accuracy)
        message, bool, mydice = challenge_attack(type,mydice,Accuracy)
        log_message += message
        message, damage_value = get_reaction(type,value,0)
    else:
        log_message = "タイプは物理か魔法です。"
        bool = False
        return log_message, bool
    
    log_message += message


    return log_message, bool

def ifmore(x, y):
    x = int(x)
    y = int(y)
    result = x > y
    log_message = f"大きい: {result}"
    return log_message, result

def ifeqmore(x, y):
    x = int(x)
    y = int(y)
    result = x >= y
    log_message = f" 以上: {result}"
    return log_message, result

def ifless(x, y):
    x = int(x)
    y = int(y)
    result = x < y
    log_message = f" 小さい: {result}"
    return log_message, result

def ifeqless(x, y):
    x = int(x)
    y = int(y)
    result = x <= y
    log_message = f" 以下: {result}"
    return log_message, result

def ifequal(x, y):
    x = int(x)
    y = int(y)
    result = x == y
    log_message = f" 等しい: {result}"
    return log_message, result

def plus(x, y):
    x = int(x)
    y = int(y)
    result = x + y
    log_message = f" 和: {result}"
    return log_message, result

def minus(x, y):
    x = int(x)
    y = int(y)
    result = x - y
    log_message = f" 差: {result}"
    return log_message, result

def multiply(x, y):
    x = int(x)
    y = int(y)
    result = x * y
    log_message = f" 積: {result}"
    return log_message, result

def divide(x, y):
    x = int(x)
    y = int(y)
    if y == 0:
        result = 0
        log_message = f" 0で割っています。"
    else:
        x = int(x)
        y = int(y)
        result = x // y
        log_message = f" 商: {result}"
    return log_message, result

def getmax(numlist):
    # カンマで分割し、リストに変換
    numbers = [int(num.strip()) for num in numlist.split(',')]
    # 最大値を計算
    max_value = max(numbers)
    log_message = f' {numbers}の最大値は{max_value}です。'
    return log_message, max_value

def getmin(numlist):
    # カンマで分割し、リストに変換
    numbers = [int(num.strip()) for num in numlist.split(',')]
    # 最大値を計算
    min_value = min(numbers)
    log_message = f' {numbers}の最小値は{min_value}です。'
    return log_message, min_value

def getsum(numlist):
    # カンマで分割し、リストに変換
    numbers = [int(num.strip()) for num in numlist.split(',')]
    # 最大値を計算
    sum_value = sum(numbers)
    log_message = f' {numbers}の合計値は{sum_value}です。'
    return log_message, sum_value

def dicebool(mydice,tdice,myvalue,tvalue):
    # 成功失敗判定
    if int(mydice) == 2:
        bool = False
    elif int(tdice) == 12:
        bool = False
    elif int(mydice) == 12 and int(tdice) != 12 :
        bool = True
    elif int(mydice) != 2 and int(tdice) == 2:
        bool = True
    else:
        bool = myvalue > tvalue

    return bool

def challenge_status(mystatus,targetstatus):
    mybonus = getstatus(Actor,mystatus)[1]
    log_message,mydice,myvalue = challenge_self(mybonus)

    for target in Targets:
        targetbonus = getstatus(target,targetstatus)[1]
        message,tdice = dice(2,6)
        tvalue = int(targetbonus) + int(tdice)
        tresult = message
        
        bool = dicebool(mydice,tdice,myvalue,tvalue)
        challengebool[target] = bool

        if getstatus(target,"type")[1] == "魔物":
            log_message = log_message + f" << {target}の{tresult},判定:{bool} >> "
        else:
            log_message = log_message + f" << {target}の{tresult} 補正値:{targetbonus} 判定値:{tvalue} 判定:{bool} >> "
            print(log_message)
    return log_message, bool, mydice


def challenge(mydice,tdice,mybonus,tbonus):
    # 自分と相手のダイス値と補正値から成否判定
    myvalue = int(mybonus) + int(mydice)
    tvalue = int(tbonus) + int(tdice)

    bool = dicebool(mydice,tdice,myvalue,tvalue)
    log_message = f'判定結果:{bool}'

    return log_message, bool, myvalue, tvalue


def challenge_self(mybonus):
    # 自分のダイスを振って補正値を足す
    message,mydice = dice(2,6)
    myvalue = int(mybonus) + int(mydice)
    myresult = message
    
    if getstatus(Actor,"type")[1] == "魔物":
        log_message = f" << {Actor}の{myresult} >> "
    else:
        log_message = f" << {Actor}の{myresult} 補正値:{mybonus} 判定値:{myvalue} >> "
    
    return log_message, mydice, myvalue


def challenge_dice(mybonus,tbonus):
    # 自分と相手のダイスを振って補正値を足して成否判定
    message,mydice = dice(2,6)
    myvalue = int(mybonus) + int(mydice)
    myresult = message
    
    if getstatus(Actor,"type")[1] == "魔物":
        log_message = f" << {Actor}の{myresult} >> "
    else:
        log_message = f" << {Actor}の{myresult} 補正値:{mybonus} 判定値:{myvalue} >> "
    
    for target in Targets:
        message,tdice = dice(2,6)
        tresult = message
        message, bool, myvalue, tvalue = challenge(mydice,tdice,mybonus,tbonus)
        challengebool[target] = bool

        if getstatus(target,"type")[1] == "魔物":
            log_message = log_message + f" << {target}の{tresult} {message} >> "
        else:
            log_message = log_message + f" << {target}の{tresult} 補正値:{tbonus} 判定値:{tvalue} {message} >>"

    return log_message, bool, mydice, tdice


def challenge_attack(type,mydice,mybonus):
    # 攻撃時の成否判定を実行

    # 攻撃種類の判定
    if type == "物理":
        log_message = "物理攻撃の成否判定"
        targetstatus = "回避"
    elif type == "魔法": 
        log_message = "魔法攻撃の成否判定"
        targetstatus = "精神抵抗"
    elif type == "射撃":
        log_message = "物理攻撃の成否判定"
        targetstatus = "回避"
    else:
        log_message = "typeに物理か魔法を指定してください。"
        bool = False
        mydice = 2
        return log_message, bool, mydice 
    
    for target in Targets:
        # ターゲットの補正値取得
        tbonus = getstatus(target,targetstatus)[1]
        # カウンターの有無判定
        t_counter = getstatus(target,"カウンター")[1]
        # カウンター発生時
        if type == "物理" and int(t_counter) > 0:
            message, bool, tdice = CalCounter(target,t_counter,mydice,myvalue)
            log_message += message
            # カウンターの解除
            setcounter(target,0)
            if bool == True:
                # ダメージ結果
                weapon_id = t_counter
                message, damage_value, cvalue = cal_physicaldamage(target,weapon_id,tdice)
                log_message += message
                
                message = f" {Actor}に{damage_value}のダメージを与えます。"
                log_message += message

                message, newHP = give_phygicaldamage(Actor,damage_value)

                mydice = -100
                challengebool[target] = False
                return log_message, bool, mydice 
            
            elif bool == False:
                mydice = 12
                log_message += " カウンターに失敗しました。"
                challengebool[target] = True
                return log_message, bool, mydice

        else:
            message,tdice = dice(2,6)
            tresult = message
            message, bool, myvalue, tvalue = challenge(mydice,tdice,mybonus,tbonus)
            challengebool[target] = bool

        if getstatus(target,"type")[1] == "魔物":
            log_message = log_message + f" << {target}の{tresult},判定:{bool} >> "
        else:
            log_message = log_message + f" << {target}の{tresult} 補正値:{tbonus} 判定値:{tvalue} 判定:{bool} >>"
    return log_message, bool, mydice

def CalCounter(target,weapon_id,mydice,myvalue):
    from dataclass import Weapon,coalesce
    from sqlalchemy import func

    log_message = f' {target}がカウンターの判定を行います。'
    Accuracy = getstatus(target,"命中")[1]
    WeaponAccuracy = db.session.query(func.sum(Weapon.命中)).filter_by(id=weapon_id).scalar()
    targetbonus = coalesce(WeaponAccuracy) + int(Accuracy)

    message,tdice = dice(2,6)
    tvalue = int(targetbonus) + int(tdice)
    tresult = message

    bool = dicebool(tdice,mydice,tvalue,myvalue)
    challengebool[target] = bool

    if getstatus(target,"type")[1] == "魔物":
        log_message += f" << {target}の{tresult},判定:{bool} >> "
    else:
        log_message += f" << {target}の{tresult} 補正値:{targetbonus} 判定値:{tvalue} 判定:{bool} >>"
    
    return log_message, bool, mydice

def setcounter(unit_name,weapon_id):
    from dataclass import Unit
    unit = Unit.query.filter_by(name=unit_name).first()
    unit.カウンター = weapon_id
    db.session.add(unit)
    db.session.commit()

    log_message = f" {unit_name}がカウンターの構えを取りました。"

    return log_message, weapon_id

def basic_attack(Accuracy,damage,mydice):
    # 命中判定
    Accuracy = int(Accuracy)

    message, bool, mydice = challenge_attack("物理",mydice,Accuracy)
    log_message = message

    # カウンター発動時
    if mydice == -100:
        log_message = message
        bool = False
        return log_message, bool
    
    # 自動失敗
    if mydice == 2:
        message = f"  攻撃は自動失敗しました。"
        log_message += message
        return log_message, bool

    # ダメージ計算
    damage_value = int(damage)

    # ターゲットに対するダメージ計算
    message, damage_value = get_reaction("物理",damage_value,0)
    log_message += message

    return log_message, bool

def basic_attack_magic(magicchallenge,damage,cvalue,mydice):

    # 魔法行使判定値
    magicchallenge = int(magicchallenge)

    message, bool, mydice = challenge_attack("魔法",mydice,magicchallenge)
    log_message = message
    
    # 自動失敗
    if mydice == 2:
        message = f"  攻撃は自動失敗しました。"
        log_message += message
        return log_message, bool

    # ターゲットに対するダメージ計算
    message, damage_value = get_reaction("魔法",damage,cvalue)
    log_message += message

    return log_message, bool

def physical_attack(weapon_id):
    from dataclass import Weapon,Unit

    # 命中判定
    Accuracy = int(getstatus(Actor,"命中")[1]) + int(getweapon(weapon_id,"命中")[1])
    # 自分のダイスと結果取得
    log_message, mydice, myvalue = challenge_self(Accuracy)

    # ダメージ計算
    message, damage_value, cvalue = cal_physicaldamage(Actor,weapon_id,mydice)
    log_message += message

    message, bool = basic_attack(Accuracy,damage_value,mydice)
    log_message += message

    return log_message, bool

def basic_magic_attack(critical,mpower,magicpower,mp):
    log_message = f" MPを{mp}消費します。"
    # MP消費
    mp = int(mp)
    mp = -mp

    message, newMP = setstatus(Actor,"MP",mp)
    log_message += message

    # 魔力
    magicpower = int(magicpower)
    log_message += f" 魔法威力:{mpower} 魔力:{magicpower}"

    # 抵抗判定
    magicchallenge = magicpower + int(getstatus(Actor,"魔法行使判定")[1])
    message, mydice, myvalue = challenge_self(magicchallenge)
    log_message += message

    # ダメージ計算
    message, maindamage = cal_damage(mpower,magicpower,mydice)
    log_message += message
    # クリティカル計算
    log_message += " クリティカル計算:"
    message, cvalue = criticalloop(critical,mpower,mydice)
    log_message += message

    # ターゲットに対するダメージ計算
    message, bool = basic_attack_magic(magicchallenge,maindamage,cvalue,mydice)
    log_message += message

    return log_message, bool

def magical_attack_cpu(critical,mpower,mp):
    # 魔力
    magicpower = getstatus(Actor,"魔力")[1]
    magicpower = int(magicpower)

    log_message, bool = basic_magic_attack(critical,mpower,magicpower,mp)

    return log_message, bool

def magical_attack(mpower,mp,magictype):
    # 使用する魔法の基本ダメージ計算
    magiclevel = get_magiclevel(Actor,magictype)[1]
    magicbonus = getstatus(Actor,"魔力ボーナス")[1]
    magicpower = int(magiclevel) + int(magicbonus)

    # クリティカル計算
    criticalbonus = getstatus(Actor,"魔法クリティカル")[1]
    critical_line = 10 - int(criticalbonus)

    log_message, bool = basic_magic_attack(critical_line,mpower,magicpower,mp)

    return log_message, bool

def shoot_attack(weapon_id):
    # 武器威力
    mpower = getweapon(weapon_id)
    # 狙撃
    log_message,bool = magishoot_attack(mpower,0,weapon_id)

    return log_message, bool


def magishoot_attack(mpower,mp,weapon_id):

    # 弾情報
    bulletacr = getbulletbox(weapon_id,"col1","補正命中")[1]
    bulletdmg = getbulletbox(weapon_id,"col1","補正ダメージ")[1]
    bulletmp = getbulletbox(weapon_id,"col1","消費MP")[1]

    message, bulletbool = usebulletbox(weapon_id,1)
    if bulletbool == False:
        log_message = message
        bool = False
        return log_message, bool

    # MP消費
    mp = int(mp) + int(bulletmp)
    log_message = f" MPを{mp}消費します。"
    mp = -mp

    message, newMP = setstatus(Actor,"MP",mp)
    log_message += message

    # 魔力計算
    magicpower = cal_magicpower(Actor,"マギテック")[1]
    log_message += f" 威力:{mpower} 魔力:{magicpower}"

    # 命中判定
    Accuracy = cal_accuracy(Actor,weapon_id)[1] + int(bulletacr)
    # 自分のダイスと結果取得
    message, mydice, myvalue = challenge_self(Accuracy)
    log_message += message
    message, bool, mydice = challenge_attack("射撃",mydice,Accuracy)
    log_message += message

    # ダメージ計算
    message, maindamage = cal_damage(mpower,magicpower,mydice)
    log_message += message
    # クリティカル計算
    log_message += " クリティカル計算:"
    criticalline = get_criticalline(Actor,weapon_id)[1]
    message, cvalue = criticalloop(criticalline,mpower,mydice)
    log_message += message
    damage_value = int(maindamage) + int(cvalue) + int(bulletdmg)

    # ターゲットに対するダメージ計算
    message, damage_value = get_reaction("射撃",damage_value,0)
    log_message += message

    return log_message, bool

def usebullet(mybox):
    for i in range(mybox.maxbullet-1):
        cola = f'col{i+2}'
        colb = f'col{i+1}'
        bid = getattr(mybox,cola)
        setattr(mybox,colb,bid)

        db.session.add(mybox)
        db.session.commit()

        log_message = "弾を使用しました。"
    
    return log_message, mybox

def criticalloop(critical,powerscore,mydice):
    damage = 0
    log_message = " "
    critical = int(critical)
    mydice = int(mydice)
    if mydice >= critical:
        message, dvalue = dice(2,6)
        log_message += message
        message, damage = power(powerscore,dvalue)
        log_message += message
        if dvalue >= critical:
            message, cvalue = criticalloop(critical,powerscore,dvalue)
            log_message += message
            damage = int(damage) + int(cvalue)

    return log_message, damage
    
def monstercriticalloop(critical,mydice):
    cvalue = 0
    log_message = ""
    critical = int(critical)
    mydice = int(mydice)
    if mydice >= critical:
        log_message, dvalue = dice(2,6)
        cvalue = int(dvalue)
        if dvalue >= critical:
            message, cvalue = monstercriticalloop(critical,mydice)
            log_message += message

    return log_message, cvalue

def useitem(item_id,num):
    from dataclass import Item
    item = Item.query.filter_by(id=item_id).first()
    if not item is None:
        log_message = f'{item.name}を{num}個使用しました。'
        result=0
        item_num = int(item.num) 
        for i in range(int(num)):
            command = item.command
            message,result = sub_code(command)
            log_message += message
            if item.type == "消耗品":
                item_num -= 1
            
        item.num = item_num
        db.session.add(item)
        db.session.commit()
    else:
        log_message = "アイテムが見つかりません。"
        result = 0
    
    return log_message,result


def heal(unit_name,value):
    if unit_name == "target":
        log_message = ""
        for target in Targets:
            message,status_value=heal(target,value)
            log_message = log_message + message

        return log_message,status_value

    from dataclass import Unit
    unit = Unit.query.filter_by(name=unit_name).first()
    status_value = 0

    if unit is None:
        log_message = "ユニットが存在しません"
        return log_message,None
    else:
        try:
            status_value = getattr(unit,"HP")
            healbonus = unit.回復ボーナス
            healvalue = int(value) + int(healbonus)
            status_value = status_value + healvalue
            setattr(unit,"HP",status_value)
            db.session.add(unit)
            db.session.commit()
            log_message = f"{healvalue}の回復を行います。{unit_name}のHP: {status_value}"
        except:
            status_value = 0
            log_message = f"{unit_name}にHPというステータスは存在しません"
        if unit.type == "魔物":
            log_message = f"魔物のステータスは閲覧できません。"
        
    return log_message,status_value

def getjoblevel(unit_name,jobname):
    log_message = ""
    if unit_name == "target":
        for target in Targets:
            message,joblevel=getjoblevel(target,jobname)
            log_message += message

        return log_message,joblevel

    from dataclass import Unit,Job
    unit = Unit.query.filter_by(name=unit_name).first()

    if unit is None:
        log_message = "ユニットが存在しません"
        return log_message,0
    else:
        job = Job.query.filter_by(related_id=unit.related_id,name=jobname).first()
        if job is None:
            log_message = f'{jobname}は習得していません。'
            return log_message, 0
        
        joblevel = job.level
        log_message = f'{unit_name}の{jobname}レベルは{joblevel}です。'
        
    return log_message,joblevel

def cal_damage(attackpower,basicdamage,mydice):
    powerdamage = power(int(attackpower),int(mydice))[1]
    maindamage = int(basicdamage) + int(powerdamage)
    log_message = f"  基礎ダメージ:{maindamage}"
    return log_message, maindamage

def cal_physicaldamage(unit_name,weapon_id,mydice):
    weaponpower = getweapon(weapon_id,"威力")[1]
    weaponcritical = getweapon(weapon_id,"クリティカル")[1]
    weapondamage = getweapon(weapon_id,"追加ダメージ")[1]

    criticalbonus = getstatus(unit_name,"クリティカルボーナス")[1]
    basicdamage = getstatus(unit_name,"基本ダメージ")[1]

    maindamage = cal_damage(weaponpower,basicdamage,mydice)[1] + int(weapondamage)

    log_message = f"  基礎ダメージ:{maindamage}"

    # クリティカル計算
    log_message += " クリティカル計算:"
    critical_line = int(weaponcritical) - int(criticalbonus)
    message, cvalue = criticalloop(critical_line,weaponpower,mydice)
    log_message += message
    damage_value = maindamage + cvalue
        
    return log_message, damage_value, cvalue

def give_phygicaldamage(unit_name,damage_value):
    defence = getstatus(unit_name,"防護点")[1]
    defence = int(defence)
    damage_value = int(damage_value)
    actualdamage = (damage_value - defence) * (-1)
    if actualdamage > 0:
        actualdamage = 0
    log_message, newHP = setstatus(unit_name,"HP",actualdamage)
        
    return log_message, actualdamage

def give_magicaldamage(unit_name,damage_value):
    defence = getstatus(unit_name,"魔法耐性")[1]
    defence = int(defence)
    damage_value = int(damage_value)
    actualdamage = (damage_value - defence) * (-1)
    if actualdamage > 0:
        actualdamage = 0
    log_message, newHP = setstatus(unit_name,"HP",actualdamage)
        
    return log_message, actualdamage

def give_damage(unit_name,damage_value):
    actualdamage = int(damage_value) * (-1)
    log_message, newHP = setstatus(unit_name,"HP",actualdamage)
        
    return log_message, actualdamage

def get_reaction(type,maindamage,cvalue):
    log_message = ""
    maindamage = int(maindamage)
    cvalue = int(cvalue)
    damage_value = maindamage
    for target in Targets:
        if challengebool[target] == True:
            damage_value = maindamage + cvalue
            message = f" {target}に{damage_value}のダメージを与えます。"
            if type == "物理":
                give_phygicaldamage(target,damage_value)
            elif type == "魔法":
                give_magicaldamage(target,damage_value)
            elif type == "射撃":
                give_damage(target,damage_value)
            
        else:
            if type == "物理" or type == "射撃":
                message = f" {target}は回避しました。"
            elif type == "魔法":
                damage_value = maindamage // 2
                message = f" {target}は抵抗しました。{target}に{damage_value}のダメージを与えます。"
                give_magicaldamage(target,damage_value)
        
        log_message += message
    
    return log_message, damage_value

def getbulletbox(weapon_id,col,status_name):
    from dataclass import BulletBox,Bullet
    mybox = BulletBox.query.filter_by(related_id=weapon_id).first()

    if mybox is None:
        log_message = f" ID{weapon_id}の武器の弾倉が存在しません。"
        return log_message,0
    else:
        try:
            bullet_id = getattr(mybox,col)
            mybullet = Bullet.query.filter_by(id=bullet_id).first()
            status_value = getattr(mybullet,status_name)
            log_message = f" {mybox.name}の{mybullet.name}の{status_name}: {status_value}"
        except:
            log_message = f" 指定の列に弾が存在しないか、'{status_name}'というステータスが存在しません。"
            status_value =0
        
    return log_message,status_value

def usebulletbox(weapon_id,num):
    from dataclass import BulletBox,Bullet

    mybox = BulletBox.query.filter_by(related_id=weapon_id).first()
    if mybox is None:
        log_message = f" ID{weapon_id}の武器の弾倉が存在しません。"
        bool = False
        return log_message,bool

    if mybox.col1 is None or mybox.col1 == "":
        log_message = "不発！弾がありません。"
        bool = False
        return log_message, bool

    log_message = f'{num}発の弾を使用します。'
    for i in range(int(num)):
        mybullet = Bullet.query.filter_by(id=mybox.col1).first()
        if mybullet is None:
            log_message = "不発！弾がありません。"
            bool = False
            return log_message, bool

        message,mybox = usebullet(mybox)
        log_message += message
        mybullet.個数 = int(mybullet.個数) - 1
        db.session.add(mybullet)
        db.session.commit()

    bool = True
        
    return log_message,bool

def getmessage(unit_name,status_name,status_value):
    unit_type = getstatus(unit_name,"type")[1]
    if unit_type == "魔物":
        log_message = "魔物のステータスは閲覧できません。"
    else:
        log_message = f" {unit_name}の{status_name}: {status_value} "
    return log_message

def get_criticalline(unit_name,weapon_id):
    # クリティカル値計算
    weaponcritical = getweapon(weapon_id,"クリティカル")[1]
    criticalbonus = getstatus(unit_name,"クリティカルボーナス")[1]
    critical_line = int(weaponcritical) - int(criticalbonus)

    log_message = getmessage(unit_name,"クリティカル値",critical_line)
    return log_message, critical_line

def cal_magicpower(unit_name,jobname):
    # 魔力計算
    magiclevel = getjoblevel(unit_name,jobname)[1]
    magicbonus = getstatus(unit_name,"魔力ボーナス")[1]
    magicpower = int(magiclevel) + int(magicbonus)

    log_message = getmessage(unit_name,"魔力",magicpower)
    return log_message, magicpower

def cal_accuracy(unit_name,weapon_id):
    # 命中計算
    unitaccuracy = getstatus(unit_name,"命中")[1]
    weaponaccuracy = getweapon(weapon_id,"命中")[1]
    Accuracy = int(unitaccuracy) + int(weaponaccuracy)

    log_message = getmessage(unit_name,"命中",Accuracy)
    return log_message, Accuracy

def get_magiclevel(user_name,magictype):
    from dataclass import UserMagic,Unit
    # 使用する魔法の魔法技能取得
    unit = Unit.query.filter_by(name=user_name).first()
    magic = UserMagic.query.filter_by(related_id=unit.id,name=magictype).first()
    magiclevel = magic.level

    log_message = f'{user_name}の{magictype}のレベルは{magiclevel}です。'
    return log_message, magiclevel