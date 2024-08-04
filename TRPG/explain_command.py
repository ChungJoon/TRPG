basic_commands = [
    {
        'name': 'dice(x,y)',
        'description': 'x:ダイスの数,y:面の数',
        'return': '合計値',
        'details': '任意の数・面のダイスを振り合計値を取得する。',
        'example': 'dice(2,6)'
    },
    {
        'name': 'getstatus(unit_name,status_name)',
        'description': 'unit_name:ユニットの名前, status_name:ステータスの名前',
        'return': 'ステータス値',
        'details': '指定されたユニットの特定のステータスを取得する。',
        'example': 'getstatus(アデル,命中)'
    },
    {
        'name': 'setstatus(unit_name,status_name,status_value)',
        'description': 'unit_name:ユニットの名前, status_name:ステータスの名前, status_value:ステータスの変化量',
        'return': 'ステータス値',
        'details': '指定されたユニットの特定のステータスを変更する。',
        'example': 'setstatus(アデル,命中,1)'
    },
    {
        'name': 'getweapon(weapon_id,status_name)',
        'description': 'weapon_id:武器のid, status_name:ステータスの名前',
        'return': 'ステータス値',
        'details': '指定されたユニットの特定のステータスを取得する。',
        'example': 'getweapon(1,威力)'
    },
    {
        'name': 'getprotector(protector_id,status_name)',
        'description': 'protector_id:防具の名id, status_name:ステータスの名前',
        'return': 'ステータス値',
        'details': '指定されたユニットの特定のステータスを取得する。',
        'example': 'getprotector(2,回避)'
    },
    {
        'name': 'power(power,dice)',
        'description': 'power:威力, dice:ダイス値',
        'return': 'ステータス値',
        'details': '威力表の該当する値を取得する。',
        'example': 'power(30,7)'
    },
    {
        'name': 'getjoblevel(unit_name,jobname)',
        'description': 'unit_name:ユニット名,jobname:技能名',
        'return': '技能レベル',
        'details': '技能レベルを取得する',
        'example': 'getjoblevel(アデル,フェンサー)'
    },
    {
        'name': 'useitem(item_id,num)',
        'description': 'useitem:アイテムID,num:使用する個数',
        'return': 'アイテムのコマンドのreturn値',
        'details': 'アイテムを使用する。このときアイテムのコマンドが実行される。使用したアイテムが消耗品の場合その個数分消費する。',
        'example': 'useitem(2,1)'
    },
    {
        'name': 'heal(unit_name,value)',
        'description': 'unit_name:ユニットの名前,value:回復量',
        'return': '回復後のHP',
        'details': '特定のユニットに対して回復を行う。',
        'example': 'heal(アデル,20)'
    }, 
    {
        'name': 'getbulletbox(weapon_id,col,status_name)',
        'description': 'weapon_id:武器ID,col:弾倉の1番目なら「col1」3番目なら「col3」,status_name:弾のステータス名',
        'return': 'ステータス値',
        'details': '弾倉に入っている弾のステータスを取得する。',
        'example': 'getbulletbox(2,col1,補正命中)'
    },
    {
        'name': 'get_magiclevel(unit_name,magictype)',
        'description': 'unit_name:ユニット名,magictype:魔法種類',
        'return': '魔法レベル',
        'details': '真語魔法などの魔法種類を指定してユニットの魔法レベルを取得する。',
        'example': 'get_magiclevel(アデル,真語魔法)'
    },
]
caliculation_commands = [
    {
        'name': 'getsum(a,b,c...)',
        'description': '任意の数字の列',
        'return': '合計値',
        'details': '合計値を取得する。',
        'example': 'getsum(1,5,2,-2)'
    },
    {
        'name': 'getmax(a,b,c...)',
        'description': '任意の数字の列',
        'return': '最大値',
        'details': '最大値を取得する。',
        'example': 'getmax(1,5,2,-2)'
    },
    {
        'name': 'getmin(a,b,c...)',
        'description': '任意の数字の列',
        'return': '最小値',
        'details': '最小値を取得する。',
        'example': 'getmin(1,5,2,-2)'
    },
    {
        'name': 'plus(x,y)',
        'description': 'x:任意の数,y:任意の数',
        'return': '数字の和',
        'details': 'x+yをする。',
        'example': 'plus(1,5)'
    },
    {
        'name': 'minus(x,y)',
        'description': 'x:任意の数,y:任意の数',
        'return': '数字の差',
        'details': 'x-yをする。',
        'example': 'minus(1,5)'
    },
    {
        'name': 'multiply(x,y)',
        'description': 'x:任意の数,y:任意の数',
        'return': '数字の積',
        'details': 'x*yをする。',
        'example': 'multiply(1,5)'
    },
    {
        'name': 'divide(x,y)',
        'description': 'x:任意の数,y:任意の数',
        'return': '数字の商',
        'details': 'x/yをする。余りは切り捨て。',
        'example': 'divide(1,5)'
    },

]

condition_commands = [
    {
        'name': 'ifmore(x,y)',
        'description': 'x:任意の数,y:任意の数',
        'return': 'True/False',
        'details': 'x>yを判定する。',
        'example': 'ifmore(1,5)'
    },
    {
        'name': 'ifless(x,y)',
        'description': 'x:任意の数,y:任意の数',
        'return': 'True/False',
        'details': 'x<yを判定する。',
        'example': 'ifless(1,5)'
    },
    {
        'name': 'ifequal(x,y)',
        'description': 'x:任意の数,y:任意の数',
        'return': 'True/False',
        'details': 'x=yを判定する。',
        'example': 'ifequal(1,5)'
    },
    {
        'name': 'ifeqmore(x,y)',
        'description': 'x:任意の数,y:任意の数',
        'return': 'True/False',
        'details': 'x>=yを判定する。',
        'example': 'ifeqmore(1,5)'
    },
    {
        'name': 'ifeqless(x,y)',
        'description': 'x:任意の数,y:任意の数',
        'return': 'True/False',
        'details': 'x<=yを判定する。',
        'example': 'ifeqless(1,5)'
    },
    {
        'name': 'actionif(bool,action)',
        'description': 'bool:TrueまたはFalseまたはreturnがTrue/Falseのコマンド,action:任意のコマンド',
        'return': 'コマンドのreturn値',
        'details': '判定がTureの時のみ実行する。',
        'example': 'actionif(ifeqmore(8,7),dice(2,6))'
    },
    {
        'name': 'loop(trigger,action,bool)',
        'description': 'trigger:ループに突入するか判断するreturnがTrue/Falseのコマンド,action:任意のコマンド,bool:ループ継続するか判断するreturnがTrue/Falseのコマンド',
        'return': 'コマンドのreturn値',
        'details': '判定がTureの限り繰り返し実行する。無限ループ防止のため上下２０回',
        'example': 'loop(ifeqmore(8,7),a=dice(2,6),loop(ifeqmore($a,7))'
    },
    {
        'name': 'criticalloop(critical,power,mydice)',
        'description': 'trigger:ループに突入するか判断するreturnがTrue/Falseのコマンド,action:任意のコマンド,bool:ループ継続するか判断するreturnがTrue/Falseのコマンド',
        'return': 'クリティカルダメージ',
        'details': '威力とクリティカル値を指定してクリティカルダメージを計算する。',
        'example': 'criticalloop(10,30,11)'
    },
    {
        'name': 'monstercriticalloop(critical,mydice)',
        'description': 'trigger:ループに突入するか判断するreturnがTrue/Falseのコマンド,action:任意のコマンド,bool:ループ継続するか判断するreturnがTrue/Falseのコマンド',
        'return': 'クリティカルダメージ',
        'details': 'クリティカル値を指定してダイス値をそのまま足したクリティカルダメージを計算する。',
        'example': 'monstercriticalloop(10,11)'
    },
]

attack_commands = [
    {
        'name': 'basic_attack(Accuracy,damage,mydice)',
        'description': 'Accuracy:命中,damage:ダメージ量,mydice:自分のダイス値',
        'return': 'True/False',
        'details': '命中とダメージ量を指定してターゲットに対する物理攻撃を行う。',
        'example': 'basic_attack(15,20,8)'
    },
    {
        'name': 'basic_attack_magic(magicchallenge,damage,cvalue,mydice)',
        'description': 'magicchallenge:魔法行使判定,damage:ダメージ量,mydice:自分のダイス値',
        'return': 'True/False',
        'details': '魔力とダメージ量を指定してターゲットに対する魔法攻撃を行う。',
        'example': 'basic_attack_magic(15,20,12,10)'
    },
    {
        'name': 'physical_attack(weapon_id)',
        'description': 'weapon_id:使用する武器のID',
        'return': 'True/False',
        'details': 'ターゲットに対する物理攻撃を行う。',
        'example': 'physical_attack(1)'
    },
    {
        'name': 'basic_magic_attack(critical,mpower,magicpower,mp)',
        'description': 'critical:クリティカル値,mpower:魔法の威力,magicpower:魔力,mp:消費MP',
        'return': 'True/False',
        'details': 'クリティカル値や威力、魔力を指定してターゲットに対する魔法攻撃を行う。',
        'example': 'basic_magic_attack(10,20,16,5)'
    },
    {
        'name': 'magical_attack(power,mp,magictype)',
        'description': 'power:魔法の威力, mp:消費MP, magictype:魔法の分類(真語魔法、操霊魔法など)',
        'return': 'True/False',
        'details': '威力と魔法種を指定してターゲットに対する魔法攻撃を行う。',
        'example': 'magical_attack(20,6,真語魔法)'
    },
    {
        'name': 'magical_attack_cpu(critical,mpower,mp)',
        'description': 'critical:クリティカル値, mpower:魔法の威力, mp:消費MP',
        'return': 'True/False',
        'details': 'デフォルトの魔力値を使い、クリティカル値も指定してターゲットに対する魔法攻撃を行う。',
        'example': 'magical_attack_cpu(10,20,8)'
    },
    {
        'name': 'shoot_attack(weapon_id)',
        'description': 'weapon_id:使用する武器のID',
        'return': 'True/False',
        'details': 'ターゲットに対する射撃攻撃を行う。',
        'example': 'shoot_attack(5)'
    },
    {
        'name': 'magishoot_attack(power,mp,weapon_id)',
        'description': 'power:武器の威力, mp:消費MP, weapon_id:使用する武器のID',
        'return': 'True/False',
        'details': 'ターゲットに対して魔法を乗せた射撃攻撃を行う。',
        'example': 'magishoot_attack(20,3,8)'
    },
    {
        'name': 'attack(critical,damage)',
        'description': 'critical:クリティカル値, damage:打撃点',
        'return': 'True/False',
        'details': 'モンスター用。ターゲットに対してダイス+打撃点の攻撃を行う。',
        'example': 'attack(10,20)'
    },
    {
        'name': 'fixattack(type,value)',
        'description': 'type:攻撃タイプ（魔法か物理）,value:固定ダメージ値',
        'return': 'True/False',
        'details': '魔法か物理の固定ダメージを与える。True/Falseは基本ダメージの値',
        'example': 'fixattack(物理,20)'
    },
]

challenge_commands = [
    {
        'name': 'challenge(mydice,tdice,mybonus,tbonus)',
        'description': 'mydice:自分のダイス値,tdice:相手のダイス値,mybonus:自分側の補正値,tbonus:相手側の補正値',
        'return': 'True/False',
        'details': '自分のダイス＋ボーナスと相手のダイス＋ボーナスを比較',
        'example': 'challenge(8,7,10,12)'
    },
    {
        'name': 'challenge_self(mybonus)',
        'description': 'mybonus:自分側の補正値',
        'return': 'ダイス値',
        'details': '自分のダイスを振りボーナスを足す',
        'example': 'challenge_self(12)'
    },
    {
        'name': 'challenge_dice(mybonus,tbonus)',
        'description': 'mybonus:自分側の補正値,tbonus:相手側の補正値',
        'return': 'True/False',
        'details': '自分と相手のダイスを振り、ボーナスを足して比較',
        'example': 'challenge_dice(8,7)'
    },
    {
        'name': 'challenge_status(mystatus,targetstatus)',
        'description': 'mystatus:自分が参照するステータス,targetstatus:相手が参照するステータス',
        'return': 'True/False',
        'details': 'お互いのステータスを参照して挑戦（命中や魔法など）',
        'example': 'challenge_status(命中,回避)'
    },
    {
        'name': 'challenge_attack(type,mydice,mybonus)',
        'description': 'type:物理か魔法か射撃,mydice:自分のダイス値,mybonus:補正値',
        'return': 'True/False',
        'details': '物理と射撃の時は対回避、魔法の時は対精神抵抗で判定',
        'example': 'challenge_attack(物理,10,12)'
    },
    {
        'name': 'get_reaction(type,maindamage,cvalue)',
        'description': 'type:物理か魔法か射撃,maindamage:メインダメージ,cvalue:クリティカルダメージ',
        'return': 'damage_value',
        'details': 'challengeコマンドによって得られたTrue,Falseに基づきターゲットにダメージ計算を行う。',
        'example': 'get_reaction(物理,21,0)'
    },
]

commands = [
    {
        'name': 'cal_damage(attackpower,basicdamage,mydice)',
        'description': 'attackpower:威力,basicdamage:基本ダメージ,mydice:自分のダイス値',
        'return': 'True/False',
        'details': '指定した威力とダイス値におけるダメージ計算',
        'example': 'cal_damage(30,15,8)'
    },
    {
        'name': 'cal_physicaldamage(unit_name,weapon_id,mydice)',
        'description': 'unit_name:ユニット名,weapon_id:武器id,mydice:自分のダイス値',
        'return': 'True/False',
        'details': 'ユニットの基本ダメージと武器から物理ダメージ計算',
        'example': 'cal_physicaldamage(アデル,1,8)'
    },
    {
        'name': 'give_damage(unit_name,damage_value)',
        'description': 'unit_name:ユニット名,damage_value:ダメージ量',
        'return': 'ダメージ値',
        'details': 'ユニットに任意のダメージを加える。',
        'example': 'give_damage(アデル,30)'
    },
    {
        'name': 'give_phygicaldamage(unit_name,damage_value)',
        'description': 'unit_name:ユニット名,damage_value:ダメージ量',
        'return': 'ダメージ値',
        'details': 'ユニットに任意の物理ダメージを加える。実際に引かれるHP量はユニットの防護点が引かれた値になる。',
        'example': 'give_phygicaldamage(アデル,30)'
    },
    {
        'name': 'give_magicaldamage(unit_name,damage_value)',
        'description': 'unit_name:ユニット名,damage_value:ダメージ量',
        'return': 'ダメージ値',
        'details': 'ユニットに任意の魔法ダメージを加える。実際に引かれるHP量はユニットの魔法耐性が引かれた値になる。',
        'example': 'give_magicaldamage(アデル,30)'
    },
    {
        'name': 'get_criticalline(unit_name,weapon_id)',
        'description': 'unit_name:ユニット名,weapon_id:武器id',
        'return': 'クリティカル値',
        'details': '武器のクリティカル値とユニットのクリティカルボーナスから正味のクリティカル値を計算する。',
        'example': 'cal_damage(アデル,3)'
    },
    {
        'name': 'cal_magicpower(unit_name,jobname)',
        'description': 'unit_name:ユニット名,jobname:魔法技能',
        'return': '魔力',
        'details': 'ソーサラーなどの魔法技能を指定してその魔法レベルを取得して魔力を計算する。',
        'example': 'cal_damage(アデル,ソーサラー)'
    },
    {
        'name': 'cal_accuracy(unit_name,weapon_id)',
        'description': 'unit_name:ユニット名,weapon_id:武器id',
        'return': 'damage_value',
        'details': '武器の命中補正とユニットの命中から正味の命中を計算する。',
        'example': 'cal_damage(アデル,3)'
    },
    # 他のコマンドを追加
]