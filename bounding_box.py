import sys

def find_groups(grid):
    rows = len(grid)
    if rows == 0:
        return []
    cols = len(grid[0])

    visited = [[False] * cols for _ in range(rows)]
    groups = []

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == '*' and not visited[row][col]:
                group = []
                stack = [(row, col)]
                visited[row][col] = True
                while stack:
                    curr_row, curr_col = stack.pop()
                    group.append((curr_row, curr_col))

                    # Check neighbors
                    for row_direction, col_direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        next_row = curr_row + row_direction
                        next_col = curr_col + col_direction
                        if 0 <= next_row < rows and 0 <= next_col < cols and \
                           grid[next_row][next_col] == '*' and not visited[next_row][next_col]:
                            visited[next_row][next_col] = True
                            stack.append((next_row, next_col))
                groups.append(group)
    return groups

def find_bounding_box(group):
    if not group:
        return None
    min_r = min(r for r, c in group)
    max_r = max(r for r, c in group)
    min_c = min(c for r, c in group)
    max_c = max(c for r, c in group)


    return ((min_r, min_c), (max_r, max_c))

def do_boxes_overlap(box1, box2):
    (r1_a, c1_a), (r2_a, c2_a) = box1
    (r1_b, c1_b), (r2_b, c2_b) = box2
    return (r1_a <= r2_b and r2_a >= r1_b and c1_a <= c2_b and c2_a >= c1_b)

def main():
    split_lines = [line.strip("`\n") for line in sys.stdin.readlines()]
    grid = [list(line) for line in split_lines if line] 
    # if the grid is empty or has no columns, return
    if not grid or not grid[0]:
        return

    groups = find_groups(grid)

    boxes = [find_bounding_box(g) for g in groups]

    
    valid_boxes = []
    for i, box1 in enumerate(boxes):
        is_valid = True
        for j, box2 in enumerate(boxes):
            if i != j and do_boxes_overlap(box1, box2):
                is_valid = False
                break
        if is_valid:
            valid_boxes.append(box1)

    if not valid_boxes:
        return


    # calculate area
    valid_boxes_with_area = []
    for (r1, c1), (r2, c2) in valid_boxes:
        area = (r2 - r1 + 1) * (c2 - c1 + 1)
        valid_boxes_with_area.append((area, ((r1, c1), (r2, c2))))
    
    # find the largest box by area
    largest_box = max(valid_boxes_with_area, key=lambda x: x[0])

    coords = largest_box[1]
    (r1, c1), (r2, c2) = coords

    result = f"({r1+1},{c1+1})({r2+1},{c2+1})"

    print(result)
    # return the coordinates to 1-based format
    return result

if __name__ == "__main__":
    main()