
LEVELS = [
    [
        "#########",
        "#       #",
        "#  .    #",
        "#  $    #",
        "#  @    #",
        "#       #",
        "#########",
    ],
    [
        "##########",
        "#        #",
        "#  ..    #",
        "#  $$    #",
        "#   @    #",
        "#        #",
        "##########",
    ],
    [
        "###########",
        "#         #",
        "#         #",
        "#    #    #",
        "#    #    #",
        "#  . # $  #",
        "#      @  #",
        "###########",
    ],
]

DIRECTIONS = {"w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}


def load_level(rows):
    walls, goals, boxes = set(), set(), set()
    player = None
    width = len(rows[0])
    if not rows or any(len(row) != width for row in rows):
        raise ValueError("マップの行の長さをそろえてください")
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            pos = (x, y)
            if ch == "#":
                walls.add(pos)
            elif ch in ".+*":
                goals.add(pos)
            if ch in "$*":
                boxes.add(pos)
            if ch in "@+":
                if player is not None:
                    raise ValueError("プレイヤーは1人にしてください")
                player = pos
    if player is None or not boxes or len(boxes) != len(goals):
        raise ValueError("プレイヤー1人、箱とゴールは同じ数が必要です")
    return {"walls": walls, "goals": goals, "boxes": boxes, "player": player,
            "width": width, "height": len(rows), "moves": 0, "history": []}


def draw_game(game):
    print("\n" * 2 + "=== SOKOBAN ===")
    print("# 壁   . ゴール   $ 箱   @ プレイヤー   * ゴール上の箱")
    for y in range(game["height"]):
        line = ""
        for x in range(game["width"]):
            pos = (x, y)
            if pos == game["player"]:
                line += "+" if pos in game["goals"] else "@"
            elif pos in game["boxes"]:
                line += "*" if pos in game["goals"] else "$"
            elif pos in game["walls"]:
                line += "#"
            elif pos in game["goals"]:
                line += "."
            else:
                line += " "
        print(line)
    print(f"移動回数: {game['moves']} | WASD: 移動 / U: 一手戻す / R: リスタート / Q: 終了")


def inside(game, pos):
    return 0 <= pos[0] < game["width"] and 0 <= pos[1] < game["height"]


def move_player(game, key):
    if key not in DIRECTIONS:
        return False
    dx, dy = DIRECTIONS[key]
    x, y = game["player"]
    target = (x + dx, y + dy)
    if not inside(game, target) or target in game["walls"]:
        return False
    pushed_to = None
    if target in game["boxes"]:
        pushed_to = (target[0] + dx, target[1] + dy)
        if (not inside(game, pushed_to) or pushed_to in game["walls"]
                or pushed_to in game["boxes"]):
            return False
    game["history"].append((game["player"], game["boxes"].copy()))
    if pushed_to is not None:
        game["boxes"].remove(target)
        game["boxes"].add(pushed_to)
    game["player"] = target
    game["moves"] += 1
    return True


def undo(game):
    if game["history"]:
        game["player"], game["boxes"] = game["history"].pop()
        game["moves"] -= 1


def is_cleared(game):
    return game["boxes"] == game["goals"]


def main():
    level_index = 0
    game = load_level(LEVELS[level_index])
    while True:
        draw_game(game)
        if is_cleared(game):
            print("クリア！ 次のステージへ進みます。")
            level_index += 1
            if level_index == len(LEVELS):
                print("全ステージクリア！")
                break
            input("Enterを押して次へ...")
            game = load_level(LEVELS[level_index])
            continue
        key = input("操作 > ").strip().lower()[:1]
        if key == "q":
            break
        if key == "r":
            game = load_level(LEVELS[level_index])
        elif key == "u":
            undo(game)
        else:
            move_player(game, key)


if __name__ == "__main__":
    main()
