#!/usr/bin/env python
# coding: utf-8



from PIL import Image, ImageDraw, ImageFont
import random
from itertools import combinations
import time
import os

def input_to_bool(string):
    return string.lower() in ['true','t','1','yes','y']

def parse_input(lines,keyword):
    for line in lines:
        if line.split(':')[0].lower()==keyword.lower():
            return(':'.join(line.split(':')[1:]).strip('\n').strip(' '))
    return ''

def get_max_width(string):
    global font
    lines = string.split('\n')
    max_width = max(font.getlength(line) for line in lines) - .001*min(len(line) for line in lines)
    return max_width

def distribute_words(string, num_lines):
    global timeout
    words = string.split()
    num_words = len(words)
    
    # Generate all possible combinations of line breaks
    all_combinations = combinations(range(1, num_words), num_lines - 1)
    
    # Initialize variables for the best distribution
    min_max_width = float('inf')
    best_distribution = []
    
    # Iterate through all combinations
    start_time = time.perf_counter()
    for comb in all_combinations:
        current_distribution = []
        start_index = 0
        for end_index in comb:
            current_distribution.append(words[start_index:end_index])
            start_index = end_index
        current_distribution.append(words[start_index:])
        
        # Calculate the maximum width for the current distribution
        current_max_width = get_max_width('\n'.join([' '.join(line) for line in current_distribution]))
        #print(current_max_width)
        
        
        # Update the best distribution if the current one has a smaller maximum width
        if current_max_width < min_max_width:
            min_max_width = current_max_width
            best_distribution = current_distribution
            
        if time.perf_counter() - start_time > timeout:
            break
    
    # Join the words in the best distribution to form the wrapped string
    wrapped_string = '\n'.join([' '.join(line) for line in best_distribution])
    
    return wrapped_string

def best_square(string):
    global font
    smallest_square = float('inf')
    best_wrapped_string = string
    for num_lines in range(1,len(string.split())+1):
        wrapped_string = distribute_words(string, num_lines)
        if max(get_max_width(wrapped_string),(num_lines*font.getsize(' ')[1]))<smallest_square:
            best_wrapped_string = wrapped_string
            smallest_square = max(get_max_width(wrapped_string),num_lines*font.getsize(' ')[1])
    return best_wrapped_string

def efficient_wrap_to_square(string):
    global font_name
    font_size = 12
    font = ImageFont.truetype(font_name, font_size)
    
    # Split the string into words
    words = string.split()
    num_words = len(words)
    
    # Determine the width and height of characters based on the font and font size
    char_width = font.getsize('x')[0]  # Width of the character 'x'
    char_height = font.getsize('x')[1]  # Height of the character 'x'
    
    # Calculate the ideal width and height of the resulting square based on character dimensions
    ideal_width = max(1,int((num_words * char_width) ** 0.5))
    ideal_height = max(1,int(ideal_width / 2.5))
    
    # Calculate the side length of the square
    side_length = min(ideal_width, ideal_height)  # Choose the smaller dimension to ensure a square
    
    # Create lines with appropriate words
    lines = [' '.join(words[i:i+side_length]) for i in range(0, num_words, side_length)]
    
    # Add line breaks
    wrapped_text = '\n'.join(lines)
    return wrapped_text

def string_to_square(string):
    global max_best_length
    if len(string.split())<=max_best_length:
        return best_square(string)
    else:
        return efficient_wrap_to_square(string)
#     if len(string.split())<max_best_length:
#         out_string = best_square(string)
#     else:
#         out_string = efficient_wrap_to_square(string)
#     out_list = out_string.split('\n')
#     for i in range(len(out_list)):
#         out_list[i] = out_list[i].strip(' ').strip('-').strip(' ')
#     return '\n'.join(out_list)

def get_squares_dict(unformatted_squares,box_size):
    global free_text
    squares = {-1:[free_text, max_font_size(free_text,box_size)]}
    for i in range(len(unformatted_squares)):
        #formatted_square = best_square(unformatted_squares[i])
        formatted_square = string_to_square(unformatted_squares[i])
        squares[i] = [formatted_square, max_font_size(formatted_square,box_size)]
    return squares
def max_font_size(text,box_size):
    global font_name
    for font_size in range(2,80):
        font = ImageFont.truetype(font_name, font_size)
        text_width, text_height = draw.textsize(text, font=font)
        if max(text_height,text_width)>box_size*.8:
            return font_size
    return font_size

def max_title_size(text,max_length,max_height):
    global font_name
    for font_size in range(2,80):
        font = ImageFont.truetype(font_name, font_size)
        text_width, text_height = draw.textsize(text, font=font)
        if max(text_height,text_width)>max_length:
            return font_size
    return font_size


def make_dir(path):
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)
        
with open("input.txt") as my_file:
    input_file = my_file.read()

input_vars = input_file.split('Songs:')[0].split('\n')
song_list = 'Songs:'.join(input_file.split('Songs:')[1:]).strip(' ').strip('\n').strip(' ').strip('\n').split('\n')

with open("config.txt") as my_file:
    config = my_file.read()

config_vars = config.split('\n')

timeout = int(parse_input(config_vars,'timeout'))
max_best_length = int(parse_input(config_vars,'max_best_length'))

title = parse_input(input_vars,'Round Title')
rowlen=int(parse_input(input_vars,'Number of Rows'))
free=input_to_bool(parse_input(input_vars,'Include Free'))
cards_to_generate = int(parse_input(input_vars,'Number of Cards to Make'))


cards_per_page = int(parse_input(config_vars,'Cards Per Page'))
free_text = parse_input(config_vars,'Free Space Text')
write_BINGO=input_to_bool(parse_input(config_vars,'Include BINGO'))
insta_text = parse_input(config_vars,'Insta Text')
font_name = parse_input(config_vars,'Font Name')
italic_font_name = parse_input(config_vars,'Italic Font Name')
insta_y_offset = int(parse_input(config_vars,'insta_y_offset'))
insta_x_offset = int(parse_input(config_vars,'insta_x_offset'))


font = ImageFont.truetype(font_name, 12)


make_dir(title)

if cards_per_page==2:
    # Define the dimensions of the grid and the size of each text box
    grid_width = int(parse_input(config_vars,'grid_width'))
    grid_height = int(parse_input(config_vars,'grid_height'))
    
    standard_box_size=int(parse_input(config_vars,'standard_box_size'))
    
    title_w = int(parse_input(config_vars,'title_w'))
    title_h = int(parse_input(config_vars,'title_h'))
    title_x0 = int(parse_input(config_vars,'title_x0'))
    if rowlen==5 and write_BINGO==True:
        title_y0 = int(parse_input(config_vars,'title_y0'))
        bingo_y0 = int(parse_input(config_vars,'bingo_y0'))
    else:
        title_y0 = int(parse_input(config_vars,'title_y0'))
    
    grid_x_offset = int(parse_input(config_vars,'grid_x_offset'))
    grid_y_offset = int(parse_input(config_vars,'grid_y_offset'))
    grid2_x_offset = int(parse_input(config_vars,'grid2_x_offset'))
    title2_x_offset = int(parse_input(config_vars,'title2_x_offset'))
    
else:
    # Define the dimensions of the grid and the size of each text box
    grid_width = int(parse_input(config_vars,'grid_width1'))
    grid_height = int(parse_input(config_vars,'grid_height1'))
    standard_box_size=int(parse_input(config_vars,'standard_box_size1'))
    
    title_w = int(parse_input(config_vars,'title_w1'))
    title_h = int(parse_input(config_vars,'title_h1'))
    title_x0 = int(parse_input(config_vars,'title_x01'))
    
    if rowlen==5 and write_BINGO==True:
        title_y0 = int(parse_input(config_vars,'title_y01'))
        bingo_y0 = int(parse_input(config_vars,'bingo_y01'))
    else:
        title_y0 = int(parse_input(config_vars,'title_y01'))
    
    grid_x_offset = int(parse_input(config_vars,'grid_x_offset1'))
    grid_y_offset = int(parse_input(config_vars,'grid_y_offset1'))

# if cards_per_page==2:
#     # Define the dimensions of the grid and the size of each text box
#     grid_width = 1100
#     grid_height = 850
    
#     standard_box_size=100
    
#     title_w = 500
#     title_h = 90
#     title_x0 = 40
#     if rowlen==5 and write_BINGO==True:
#         title_y0 = 0
#         bingo_y0 = 100
#     else:
#         title_y0 = 100
    
#     grid_x_offset = 20
#     grid_y_offset = 200
#     grid2_x_offset = 550
#     title2_x_offset = 530
    
# else:
#     # Define the dimensions of the grid and the size of each text box
#     grid_width = 850
#     grid_height = 1100
#     standard_box_size=140
    
#     title_w = 600
#     title_h = 90
#     title_x0 = 200
    
#     if rowlen==5 and write_BINGO==True:
#         title_y0 = 30
#         bingo_y0 = 100
#     else:
#         title_y0 = 100
    
#     grid_x_offset = 60
#     grid_y_offset = 240

    
#non 5x5 bingo adjustment
box_size = standard_box_size*(5/rowlen)

if len(song_list)<rowlen*rowlen:
    raise Exception("Not enough words to fill grid")

    
image = Image.new("RGB", (grid_width, grid_height), "white")
draw = ImageDraw.Draw(image)
squares = get_squares_dict(song_list,box_size)


if cards_per_page == 2:
    for page_no in range(1,-1*(-1*cards_to_generate//2)+1):
        
        # Create a blank image with white background
        image = Image.new("RGB", (grid_width, grid_height), "white")
        draw = ImageDraw.Draw(image)


        title_font = ImageFont.truetype(font_name, max_title_size(title,title_w,title_h))
        title_width, title_height = draw.textsize(title, font=title_font)
    
        if rowlen==5 and write_BINGO==True:
            bingo_font_scale = .7
            font_size = max_font_size('B',box_size*bingo_font_scale)
            for j in range(5):
                # Calculate the position of the top-left corner of the text box
                x0 = j * box_size + grid_x_offset
                y0 = -1 * box_size*bingo_font_scale + grid_y_offset
                x1 = x0 + box_size
                y1 = y0 + box_size*bingo_font_scale

                # Draw the rectangle for the text box
                draw.rectangle([(x0, y0), (x1, y1)])

                font = ImageFont.truetype(font_name, font_size)
                text_width, text_height = draw.textsize("BINGO"[j], font=font)
                text_x = x0 + (box_size - text_width) // 2
                text_y = y0 + (box_size*bingo_font_scale - text_height) // 2

                # Draw the text in the center of the text box
                draw.text((text_x, text_y), "BINGO"[j], fill="black", font=font, align="center")

            for j in range(5):
                # Calculate the position of the top-left corner of the text box
                x0 = j * box_size + grid2_x_offset
                y0 = -1 * box_size*bingo_font_scale + grid_y_offset
                x1 = x0 + box_size
                y1 = y0 + box_size*bingo_font_scale

                # Draw the rectangle for the text box
                draw.rectangle([(x0, y0), (x1, y1)])

                font = ImageFont.truetype(font_name, font_size)
                text_width, text_height = draw.textsize("BINGO"[j], font=font)
                text_x = x0 + (box_size - text_width) // 2
                text_y = y0 + (box_size*bingo_font_scale - text_height) // 2

                # Draw the text in the center of the text box
                draw.text((text_x, text_y), "BINGO"[j], fill="black", font=font, align="center")



        title_x = title_x0 + (title_w - title_x0 - title_width) // 2
        title_y = title_y0 + title_h - title_height

        # Draw the text in the center of the text box
        draw.text((title_x, title_y), title, fill="black", font=title_font, align="center")

        draw.text((title_x+title2_x_offset, title_y), title, fill="black", font=title_font, align="center")
        
        
        
        insta_font_scale = .8
        insta_font = ImageFont.truetype(italic_font_name, int(insta_font_scale*max_title_size(insta_text,title_w,title_h)))
        insta_width, insta_height = draw.textsize(insta_text, font=insta_font)
        
        insta_x = title_x0 + (title_w - title_x0 - insta_width) // 2
        insta_y = title_y0 + insta_y_offset
        # Insta tag
        draw.text((insta_x, insta_y), insta_text, fill="black", font=insta_font, align="center")

        draw.text((insta_x+title2_x_offset, insta_y), insta_text, fill="black", font=insta_font, align="center")
        

        card_order = list(range(len(squares)-1))
        random.shuffle(card_order)
        if rowlen%2==1 and free:
            card_order = card_order[:int((rowlen*rowlen)/2)] + [-1] + card_order[int((rowlen*rowlen)/2):rowlen*rowlen+1]


        counter = 0
        for i in range(rowlen):
            for j in range(rowlen):
                # Calculate the position of the top-left corner of the text box
                x0 = j * box_size + grid_x_offset
                y0 = i * box_size + grid_y_offset
                x1 = x0 + box_size
                y1 = y0 + box_size

                # Draw the rectangle for the text box
                draw.rectangle([(x0, y0), (x1, y1)], outline="black", width=2)

                font = ImageFont.truetype(font_name, squares[card_order[counter]][1])
                text_width, text_height = draw.textsize(squares[card_order[counter]][0], font=font)
                text_x = x0 + (box_size - text_width) // 2
                text_y = y0 + (box_size - text_height) // 2

                # Draw the text in the center of the text box
                draw.text((text_x, text_y), squares[card_order[counter]][0], fill="black", font=font, align="center")
                counter+=1

        card_order = list(range(len(squares)-1))
        random.shuffle(card_order)
        if rowlen%2==1 and free:
            card_order = card_order[:int((rowlen*rowlen)/2)] + [-1] + card_order[int((rowlen*rowlen)/2):rowlen*rowlen+1]


        counter = 0
        for i in range(rowlen):
            for j in range(rowlen):
                # Calculate the position of the top-left corner of the text box
                x0 = j * box_size + grid2_x_offset
                y0 = i * box_size + grid_y_offset
                x1 = x0 + box_size
                y1 = y0 + box_size

                # Draw the rectangle for the text box
                draw.rectangle([(x0, y0), (x1, y1)], outline="black", width=2)

                font = ImageFont.truetype(font_name, squares[card_order[counter]][1])
                text_width, text_height = draw.textsize(squares[card_order[counter]][0], font=font)
                text_x = x0 + (box_size - text_width) // 2
                text_y = y0 + (box_size - text_height) // 2

                # Draw the text in the center of the text box
                draw.text((text_x, text_y), squares[card_order[counter]][0], fill="black", font=font, align="center")
                counter+=1


        # Save or display the image
        image.save(f"{title}/page_{page_no}.png")
        
        
else:
    
    
    
    for page_no in range(1,cards_to_generate+1):
        
        # Create a blank image with white background
        image = Image.new("RGB", (grid_width, grid_height), "white")
        draw = ImageDraw.Draw(image)


        title_font = ImageFont.truetype(font_name, max_title_size(title,title_w,title_h))
        title_width, title_height = draw.textsize(title, font=title_font)
    
        if rowlen==5 and write_BINGO==True:
            bingo_font_scale = .7
            font_size = max_font_size('B',box_size*bingo_font_scale)
            for j in range(5):
                # Calculate the position of the top-left corner of the text box
                x0 = j * box_size + grid_x_offset
                y0 = -1 * box_size*bingo_font_scale + grid_y_offset
                x1 = x0 + box_size
                y1 = y0 + box_size*bingo_font_scale

                # Draw the rectangle for the text box
                draw.rectangle([(x0, y0), (x1, y1)])

                font = ImageFont.truetype(font_name, font_size)
                text_width, text_height = draw.textsize("BINGO"[j], font=font)
                text_x = x0 + (box_size - text_width) // 2
                text_y = y0 + (box_size*bingo_font_scale - text_height) // 2

                # Draw the text in the center of the text box
                draw.text((text_x, text_y), "BINGO"[j], fill="black", font=font, align="center")



        title_x = title_x0 + (title_w - title_x0 - title_width) // 2
        title_y = title_y0 + title_h - title_height


        # Draw the text in the center of the text box
        draw.text((title_x, title_y), title, fill="black", font=title_font, align="center")
        
        

        insta_font_scale = .8
        insta_font = ImageFont.truetype(italic_font_name, int(insta_font_scale*max_title_size(insta_text,title_w,title_h)))
        insta_width, insta_height = draw.textsize(insta_text, font=insta_font)
        
        insta_x = title_x0 + (title_w - title_x0 - insta_width) // 2
        insta_y = title_y0 + insta_y_offset
        # Insta tag
        draw.text((insta_x, insta_y), insta_text, fill="black", font=insta_font, align="center")


        card_order = list(range(len(squares)-1))
        random.shuffle(card_order)
        if rowlen%2==1 and free:
            card_order = card_order[:int((rowlen*rowlen)/2)] + [-1] + card_order[int((rowlen*rowlen)/2):rowlen*rowlen+1]


        counter = 0
        for i in range(rowlen):
            for j in range(rowlen):
                # Calculate the position of the top-left corner of the text box
                x0 = j * box_size + grid_x_offset
                y0 = i * box_size + grid_y_offset
                x1 = x0 + box_size
                y1 = y0 + box_size

                # Draw the rectangle for the text box
                draw.rectangle([(x0, y0), (x1, y1)], outline="black", width=2)

                font = ImageFont.truetype(font_name, squares[card_order[counter]][1])
                text_width, text_height = draw.textsize(squares[card_order[counter]][0], font=font)
                text_x = x0 + (box_size - text_width) // 2
                text_y = y0 + (box_size - text_height) // 2

                # Draw the text in the center of the text box
                draw.text((text_x, text_y), squares[card_order[counter]][0], fill="black", font=font, align="center")
                counter+=1

        # Save or display the image
        image.save(f"{title}/page_{page_no}.png")

#image.show()




