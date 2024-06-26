
def get_grid_from_res(res):
    index_of_first_image = res.index_of_first_image

    grid = None
    if index_of_first_image > 0:
        images = res.images
        grid = images[index_of_first_image - 1]

    return grid, index_of_first_image
