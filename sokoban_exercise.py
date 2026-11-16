"""第13回 倉庫番・演習版：完成デモを読み、別の構造へ処理を移植する。

演習の進め方
  ① TODO 1：WASDでプレイヤーを移動（範囲外に出さない）
  ② TODO 2：壁にぶつかると移動できないようにする
  ③ TODO 3：箱を押す処理を追加（壁や別の箱の手前では止まる）

完成デモと関数名やデータ構造が違います。必要な判定を読み取り、
このファイルの引数・変数に合わせて作り直しましょう。
演習途中でも実行できます（最初は移動キーを押しても動きません）。
"""

# 画面の左上が (0, 0)。右へ行くと x が増え、下へ行くと y が増える。
# WASD の差分：w=(0,-1), s=(0,1), a=(-1,0), d=(1,0)
KEY_TO_VECTOR = {"w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}

# # は壁、. はゴール、$ は箱、@ はプレイヤー。
# * はゴール上の箱、+ はゴール上のプレイヤー。
# 複数行文字列を splitlines() で行ごとのリストに変換する。
MAP_TEXT = [
    """#########
#       #
#  .    #
#  $    #
#  @    #
#       #
#########""",
    """##########
#        #
#  ..    #
#  $$    #
#   @    #
#        #
##########""",
    """###########
#         #
#         #
#    #    #
#    #    #
#  . # $  #
#      @  #
###########""",
]


def new_board(level_text):
    """ステージの文字列を読み、管理データを作る。引数：文字列。戻り値：辞書。"""
    rows = level_text.splitlines()
    if not rows or any(len(row) != len(rows[0]) for row in rows):
        raise ValueError("マップの横幅を揃えてください")
    board = {
        "size": (len(rows[0]), len(rows)),
        "solid": set(),  # 壁の座標集合
        "targets": set(),  # ゴールの座標集合
        "crates": set(),  # 箱の座標集合
        "hero": None,     # プレイヤーの座標
        "steps": 0,
        "past": [],       # 一手戻すための履歴
    }
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            p = (x, y)
            if ch == "#":
                board["solid"].add(p)
            if ch in ".+*":
                board["targets"].add(p)
            if ch in "$*":
                board["crates"].add(p)
            if ch in "@+":
                if board["hero"] is not None:
                    raise ValueError("プレイヤーは1人にしてください")
                board["hero"] = p
    if board["hero"] is None or not board["crates"] or len(board["crates"]) != len(board["targets"]):
        raise ValueError("プレイヤー1人、箱とゴールは同数にしてください")
    return board


def print_board(board):
    """現在の盤面を画面に表示する。引数：board。戻り値：なし。"""
    width, height = board["size"]
    print("\n" * 2 + "=== SOKOBAN : EXERCISE ===")
    print("# 壁  . ゴール  $ 箱  @ プレイヤー  * ゴール上の箱")
    for y in range(height):
        output = ""
        for x in range(width):
            p = (x, y)
            if p == board["hero"]:
                output += "+" if p in board["targets"] else "@"
            elif p in board["crates"]:
                output += "*" if p in board["targets"] else "$"
            elif p in board["solid"]:
                output += "#"
            elif p in board["targets"]:
                output += "."
            else:
                output += " "
        print(output)
    print(f"移動回数: {board['steps']} | WASD 移動 / U 戻す / R 再開 / Q 終了")


def in_field(board, point):
    """座標が盤面内か調べる。引数：board, (x,y)。戻り値：bool。"""
    x, y = point
    w, h = board["size"]
    return 0 <= x < w and 0 <= y < h


def next_position(origin, vector):
    """座標の足し算。引数：(x,y), (dx,dy)。戻り値：(x2,y2)。"""
    return (origin[0] + vector[0], origin[1] + vector[1])


def can_enter(board, destination):
    """TODO 2：壁判定。引数：board, 移動先座標。戻り値：移動可ならTrue。

    まず TODO 1 では呼ばなくてもよい。
    TODO 2 では、盤面内か、壁に含まれるかを確認しよう。
    デモ版では walls という名前だが、演習版では solid に入っている。
    """
    # TODO 2: 条件を実装する（現状では壁も通過できる）
    return in_field(board, destination)


def push_crate(board, crate_position, vector):
    """TODO 3：箱を押す。引数：board, 箱座標, 移動方向。戻り値：押せたらTrue。

    箱の一つ先に別の箱や壁がある場合は押せない。
    押せる場合は箱の集合を変更する。押せないときは変更しない。
    デモ版の辞書キー boxes と、演習版の crates は異なる。
    """
    # TODO 3: 箱の行き先を調べ、移動可能なら crates を更新する
    return False


def apply_move(board, direction_key):
    """TODO 1〜3：プレイヤーの移動。引数：board, WASDの1文字。戻り値：成功ならTrue。

    手順のヒント：
       1. KEY_TO_VECTOR から差分を取り出す
       2. next_position() で次の座標を計算する
       3. TODO 1：盤面外なら動かさず、盤面内なら hero を更新する
       4. TODO 2：壁チェックを追加する
       5. TODO 3：次が箱なら push_crate() を使う

    正しく動けるときだけ履歴に位置と箱集合のコピーを保存し、stepsを増やす。
    """
    if direction_key not in KEY_TO_VECTOR:
        return False
    vector = KEY_TO_VECTOR[direction_key]
    # TODO 1：現在の座標を取得し、次の座標を計算する。
    #           盤面内なら hero を更新する（最初は壁や箱を無視してよい）。
    # TODO 2：TODO 1の判定に can_enter() を組み込む。
    # TODO 3：次の位置が crates に含まれたら push_crate() を呼ぶ。
    #           箱が動かなければプレイヤーも移動してはいけない。
    # ヒント：移動が成功するときだけ次を実行する。
    # board["past"].append((board["hero"], board["crates"].copy()))
    # board["hero"] = 移動先の座標
    # board["steps"] += 1
    return False


def step_back(board):
    """Undoを実行。引数：board。戻り値：なし。"""
    if board["past"]:
        board["hero"], board["crates"] = board["past"].pop()
        board["steps"] -= 1


def completed(board):
    """すべての箱がゴール上にあるか調べる。引数：board。戻り値：bool。"""
    return board["crates"] == board["targets"]


def start():
    """キー入力・ステージ進行を管理する。戻り値：なし。"""
    index = 0
    board = new_board(MAP_TEXT[index])
    while True:
        print_board(board)
        if completed(board):
            print("ステージクリア！")
            index += 1
            if index == len(MAP_TEXT):
                print("全ステージクリア！")
                break
            input("Enterで次のステージへ...")
            board = new_board(MAP_TEXT[index])
            continue
        key = input("操作 > ").strip().lower()[:1]
        if key == "q":
            break
        if key == "r":
            board = new_board(MAP_TEXT[index])
        elif key == "u":
            step_back(board)
        else:
            apply_move(board, key)


if __name__ == "__main__":
    start()
