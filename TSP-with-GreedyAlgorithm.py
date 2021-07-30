import random,time,math,sys
from tkinter import *

canvas_width = 1080
canvas_height = 720
n_cities = 20 # n of cities

"""
Initialize GUI and generate random coordinat
"""
def main():
    root = Tk()
    w = Canvas(root,
               width = canvas_width,
               height = canvas_height)
    w.pack()
    city_list = make_random_cities(0,canvas_width-1,
                                   0,canvas_height-1,
                                   n_cities)
    #Greedy Algorithm
    my_path = city_list[:1] #start with first city
    for i in range(len(city_list)):
        remaining_cities = [city for city in city_list if city not in my_path]
        if not remaining_cities:
            break
        last_city = my_path[-1]
        next_city_ind = find_closest_city(last_city, remaining_cities)
        my_path.append(remaining_cities[next_city_ind])
        w.delete("all")
        #Draw city list
        draw_city_path(w,city_list,color='black',connect=False)
        draw_city_path(w,my_path, color='green',connect=True)
        write_info_at_bottom(w, canvas_width, canvas_height, my_path)
        w.update()
        time.sleep(1.0/5.0) #5 fps
    mainloop()

def find_closest_city(city, remaining_cities):
    closest_index = 0
    closest_distance = sys.float_info.max
    for i in range(len(remaining_cities)):
        r = distance(city, remaining_cities[i])
        if r < closest_distance:
            closest_distance = r
            closest_index = i
    return closest_index


def draw_city_path(w, city_list, color='white', connect=False):
    for city in city_list:
        draw_city(w, city[0], city[1],color=color)
    draw_city(w,city_list[0][0], city_list[0][1], color='blue', name='Home')
    for i in range(len(city_list)-1):
        draw_city(w, city_list[i][0],city_list[i][1], color='yellow',
                  name=city_list[i])
    #Draw a lines
    if connect:
        for i in range(len(city_list)-1):
            w.create_line(city_list[i][0], city_list[i][1],
                          city_list[i+1][0], city_list[i+1][1])

def make_random_cities(xmin, xmax, ymin, ymax, n_cities):
    city_list = []
    for i in range(n_cities):
        x = random.randint(xmin,xmax)
        y = random.randint(ymin,ymax)
        city_list.append((x,y))
    return city_list

def draw_city(w,x,y, color='yellow', name=None):
    w.create_oval(x-5, y-5, x+5, y+5, fill=color)
    if name:
        w.create_text(x, y+10, text=name)

def write_info_at_bottom(w, width, height, city_list):
    n_cities = len(city_list)
    total_distance = path_length(city_list)
    w.create_text(width/2,height-60,
                  text='Greedy Algorithm',fill='red')
    w.create_text(width/2,height-40,
                  text='cities: %d'%n_cities, fill='red')
    w.create_text(width/2,height-20,
                  text='total_distance: %g'% total_distance,
                  fill='red')

def distance(x,y):
    x1 = x[0]
    y1 = x[1]
    x2 = y[0]
    y2 = y[1]
    r = math.sqrt((x2-x1)**2 + (y2-y1)**2)
    return r

def path_length(city_list):
    total_length = 0
    for i in range(len(city_list)-1):
        c1 = city_list[i]
        c2 = city_list[i+1]
        length = distance(c1,c2)
        total_length += length
    total_length += distance(city_list[-1], city_list[0])
    return length

if __name__ == '__main__':
    main()
    
