def count_layer_values(pixels, value = 0):
    return sum([1 for i in pixels if int(i) == value])

def check_for_corruption(image, width = 25, height = 6):
    pixel_count = width * height
    zero_counts = []
    for s,e in zip(range(0, len(image), pixel_count), range(pixel_count, len(image) + 1, pixel_count)):
        zero_counts.append(count_layer_values(image[s:e]))
    lowest_zero_layer = zero_counts.index(min(zero_counts))
    layer_pixels = image[lowest_zero_layer*pixel_count:lowest_zero_layer*pixel_count + pixel_count]
    return count_layer_values(layer_pixels, 1) * count_layer_values(layer_pixels, 2)

def first_solid_or_last(pixels):
    return next(filter(lambda x: int(x) < 2, pixels), pixels[-1])

def build_image(image, width = 25, height = 6):
    pixel_count = width * height
    image_colors = [None] * pixel_count
    for i in range(pixel_count):
        image_colors[i] = first_solid_or_last(image[i::pixel_count])
    image_colors = ['█' if i is '0' else i for i in image_colors]
    for i in range(height - 1):
        image_colors.insert(i * width + width + i, '\n')
    return ''.join(image_colors)

if __name__ == '__main__':
    with open('part1_input.txt') as problem_input:
        print(str(check_for_corruption(problem_input.read())))
    with open('part2_input.txt') as problem_input:
        print(str(build_image(problem_input.read())))
