import random
import os





def set_ship(it):
    def rand_ship_1():
        list_filsname =[] 
        for x in os.listdir("images/"):
            if x.startswith("ship_1_"):
                list_filsname.append(f"{x.replace('.png', '')}")
        return "ship_1" if 1 != random.randint(0,10) else random.choice(list_filsname)
    ship_designer = ["ship_up"]
    
    ship_d = [rand_ship_1() ,"ship_2"]
    if it > 2:
        for x in range(it-2):
            ship_designer.append(ship_d[x])

    if it > 1:
        ship_designer.append("ship_down") 
    return ship_designer

def is_point_in_square(pos: tuple[int,int], square: list[tuple[int,int]]):
    x1, y1 = square[0]
    x2, y2 = square[1]
    x3, y3 = square[2]
    x4, y4 = square[3]

    return (min(x1, x2, x3, x4) <= pos[0] <= max(x1, x2, x3, x4) ) and (min(y1, y2, y3, y4) <= pos[1] <= max(y1, y2, y3, y4))





def check_next_elements(matrix: list, pos: tuple[int, int], angle: int, depth: int):

    vec_ang = [0,0]
    # angel
    if angle==0 or angle==360:
        vec_ang[1] = 1
    if angle==180:
        vec_ang[1] = -1

    if angle==90:
        vec_ang[0] = 1 
    if angle==270:
        vec_ang[0] = -1
    
    
    vec_ang_r = (vec_ang[1] + vec_ang[0], -vec_ang[0] + vec_ang[1])
    vec_ang_l = (-vec_ang[1] + vec_ang[0], vec_ang[0] + vec_ang[1])
    
    head_vec_r = (vec_ang[1], -vec_ang[0])
    head_vec_l = (-vec_ang[1], vec_ang[0])

    if check_pos(matrix, (pos[1] + -vec_ang[1], pos[0] + -vec_ang[0] ), 1):
        return False

    for head_x, head_y in [head_vec_r, head_vec_l]:
        if not pos_in_array(matrix, ( pos[1] + head_y, pos[0] + head_x )):
            continue
        
        if check_pos(matrix, (pos[1] + head_y, pos[0] + head_x ), 1):
            return False



    for value in range(depth):
        for _x, _y in [vec_ang_r, vec_ang, vec_ang_l]:
            x = pos[0] + _x + (vec_ang[0]*value)
            y = pos[1] + _y + (vec_ang[1]*value)
            if not pos_in_array(matrix, (y, x)):
                continue
            if check_pos(matrix, (y, x), 1):
                return False
    
    x = pos[0] + vec_ang[0]*(depth -1)
    y = pos[1] + vec_ang[1]*(depth -1)
    if not pos_in_array(matrix, (y , x)) :
        return False
    
    return not check_pos(matrix, (y, x), 1)

#matrix = y;x
#pos = x;y


def pos_in_array(matrix, pos):
    dy,dx = pos
    return (dy < len(matrix) and dy >= 0) and (dx < len(matrix[0]) and dx >= 0)

def check_pos(matrix, pos, _status=0) -> bool:
    dy,dx = pos
    return pos_in_array(matrix, pos) and matrix[dy][dx].status_cell == _status

def rotate_ship(matrix, pos: tuple[int, int], angle: int, ship_array):
    dx, dy = pos
    lx, ly = 0, 0
    if angle == 0 or angle == 360:
        ly += 1
    elif angle == 180:
        ly -= 1
    elif angle == 90:
        lx += 1
    elif angle == 270:
        lx -= 1

    last_cell = None
    for num, value in enumerate(ship_array):
        if num != 0:
            dx += lx
            dy += ly

        cell = matrix[dy][dx]
        cell.status_cell = 1
        

        cell.set_texture(f"images/{value}.png")
        cell.rotate_texture(angle)
        cell.render()
        cell.last_cell = last_cell

        last_cell = cell

    while True:
        if last_cell is None:
            break
        for pos in [ [1,1],[1,0],[1,-1], [0,1],[0,-1], [-1,1],[-1,0],[-1,-1] ]:
            if check_pos(matrix, (pos[1]+last_cell.pos_in_array[0], pos[0]+last_cell.pos_in_array[1])):
                _cell = matrix[pos[1]+last_cell.pos_in_array[0]][pos[0]+last_cell.pos_in_array[1]]
                _cell.status_cell = 3
                _cell.render()

                
        last_cell = last_cell.last_cell

def zone(pos: tuple[int, int], size: tuple[int, int]):
    return [
        pos,
        (pos[0]+size[0], pos[1]+size[1]),
        (pos[0], pos[1]+size[1]),
        (pos[0]+size[0], pos[1])
    ]