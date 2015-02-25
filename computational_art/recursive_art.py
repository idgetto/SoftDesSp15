""" TODO: Put your header comment here """ #Where's header comment?

import random
from PIL import Image
import math
import threading
import time

MIN_VALUE = 1e-10

def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    random_func = []

    func = get_some_func(min_depth, max_depth);
    num_params = func_params_table[func]

    random_func.append(func)

    # add the appropriate number of parameteres  <--Commenting is good, 
    for i in range(num_params):
        param = build_random_function(min_depth - 1, max_depth - 1)
        random_func.append(param)

    return random_func

def get_some_func(min_depth, max_depth):
    # func should have no params
    if max_depth == 1:
        func = random.choice(no_param_func_names)
    elif min_depth <= 1:
        func = random.choice(all_func_names)
    else:
        func = random.choice(param_func_names)

    return func

def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
        >>> evaluate_random_function(["prod", ["x"], ["y"]], 2, 5)
        10
        >>> evaluate_random_function(["avg", ["prod", ["x"], ["cos_pi", ["y"]]], ["avg", ["sin_pi", ["y"]], ["x"]]], 2, 3.14)
        -0.5112718753572876
    """
    func_name = f[0]

    try:
        function = func_table[func_name]
        params = f[1:]
        return function(params, x, y);
    except KeyError: #Nice error catching!
        raise Exception("no such function:", func_name)

def remap_interval(val, input_interval_start, input_interval_end, output_interval_start, output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    input_range = input_interval_end - input_interval_start
    rel_input = val - input_interval_start
    percent = rel_input / float(input_range)

    output_range = output_interval_end - output_interval_start
    rel_output = percent * output_range;
    output = rel_output + output_interval_start;

    return output;

def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(6, 7)
    green_function = build_random_function(3, 5)
    blue_function = build_random_function(5, 6)

    func_file = "func-" + filename + ".txt"
    f = open(func_file, "w")
    f.write(str(red_function))
    f.write("\n")
    f.write(str(green_function))
    f.write("\n")
    f.write(str(blue_function))
    f.close()

    print red_function 
    print blue_function
    print green_function
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()

    threads = []
    num_threads = 4
    block_size = x_size / num_threads

    for i in range(num_threads):
        x_range = range(i * block_size, (i + 1) * block_size)
        y_range = range(y_size)
        thread = threading.Thread(target=draw_block, args=(pixels, x_range, x_size, y_range, y_size, red_function, blue_function, green_function))
        threads.append(thread)
        thread.start()

    for thread in threads: #ooh, multithreading is cool
        thread.join()

    im.save(filename)

def draw_block(pixels, x_range, x_size, y_range, y_size, red_func, blue_func, green_func):
    for i in x_range:
        rel_i = i - x_range[0]
        dist = len(x_range)
        print 100 * rel_i / float(dist) #Please, please don't print things in long looping scripts. It takes forever to run
        for j in y_range:
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_func, x, y)),
                    color_map(evaluate_random_function(green_func, x, y)),
                    color_map(evaluate_random_function(blue_func, x, y))
                    )

#This is a interesting expanded format, but your function is becoming a tad long and unwieldy
def prod(L, x, y):
    a = evaluate_random_function(L[0], x, y)
    b = evaluate_random_function(L[1], x, y)
    return a * b

def avg(L, x, y):
    a = evaluate_random_function(L[0], x, y)
    b = evaluate_random_function(L[1], x, y)
    return 0.5 * (a + b)

def mod(L, x, y):
    a = evaluate_random_function(L[0], x, y)
    b = evaluate_random_function(L[1], x, y)
    b = max(b, MIN_VALUE)
    try:
        return math.fmod(a, b)
    except ValueError: #Nice error catching!
        print a, b
        raise

def cos_pi(L, x, y):
    a = evaluate_random_function(L[0], x, y)
    return math.cos(math.pi * a)

def sin_pi(L, x, y):
    a = evaluate_random_function(L[0], x, y)
    return math.sin(math.pi * a)

def frexp(L, x, y):
    a = evaluate_random_function(L[0], x, y)
    return math.frexp(a)[0]

def inter(L, x, y):
    return random.choice([-1, 0, 1])

def x_over_y(L, x, y):
    #return float(x) / (float(y) + 0.0001)
    return x./(y+0.0001) #works as well

def x(L, x, y):
    return x

def y(L, x, y):
    return y

    

no_param_func_names = [
    "inter",
    "x_over_y",
    "x",
    "y"
]

param_func_names = [
    "cos_pi",
    "sin_pi",
    "frexp",
    "prod",
    "avg",
    "mod"
]

all_func_names = no_param_func_names + param_func_names

func_params = [
    0,
    0,
    0,
    0,
    1,
    1,
    1,
    2,
    2,
    2
]

funcs = [
    inter,
    x_over_y,
    x,
    y,
    cos_pi,
    sin_pi,
    frexp,
    prod,
    avg,
    mod
]

func_table = dict(zip(all_func_names, funcs))
func_params_table = dict(zip(all_func_names, func_params))

if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you  <--Delete code not useful to your final turn in
    #       implement remap_interval and evaluate_random_function
    file_name = "cgi-" + time.strftime("%Y-%m-%d-%H-%M-%S") + ".png"
    generate_art(file_name, 2560, 1440) #Ok, neat, but in final turn in I'm running everyone's code and my computer
                                        #runs forever on this. Please make sure final code is easy to run

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    #test_image("noise.png")
