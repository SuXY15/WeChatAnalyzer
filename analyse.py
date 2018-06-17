#!coding=utf-8
import os, sys, time
import json, math, codecs, jieba.analyse
import PIL.Image as Image
from pyecharts import Bar,Grid,WordCloud,Pie,Map,Page
from collections import Counter

def get_pie(item_name,item_name_list,item_num_list):
    total = item_num_list[0]+item_num_list[1]+item_num_list[2]
    subtitle = "Count: %d"%total
    _pie = Pie(item_name, page_title=item_name, title_text_size=30, title_pos='center',\
        subtitle=subtitle, subtitle_text_size=25, width=650, height=650)
    _pie.add("", item_name_list, item_num_list, is_label_show=True, center=[50,45],\
        radius=[0,50], legend_pos='left', legend_orient='vertical', label_text_size=20)
    return _pie

def get_bar(item_name,item_name_list,item_num_list):
    subtitle = "Bar info"
    _bar = Bar(item_name, page_title=item_name, title_text_size=30, title_pos='center',\
        subtitle=subtitle, subtitle_text_size=25)
    
    _bar.add("", item_name_list, item_num_list, title_pos='center', xaxis_interval=0, xaxis_rotate=27,\
        xaxis_label_textsize=14, yaxis_label_textsize=14, yaxis_name_pos='end', yaxis_pos="50%")

    grid = Grid(width=650, height= 400)
    grid.add(_bar, grid_top="13%", grid_bottom="23%", grid_left="15%", grid_right="15%")
    return grid

def get_map(item_name,item_name_list,item_num_list):
    subtitle = "Map info"
    _map = Map(item_name, width=650, height=400, title_pos='center', title_text_size=30,\
        subtitle=subtitle, subtitle_text_size=25)
    _map.add("", item_name_list, item_num_list, maptype='china', is_visualmap=True, visual_text_color='#000')
    return _map

def word_cloud(item_name,item_name_list,item_num_list,word_size_range):
    _wordcloud = WordCloud(width=622, height=400)
    _wordcloud.add("", item_name_list, item_num_list, word_size_range=word_size_range, shape='pentagon')
    return _wordcloud
    
def dict2list(_dict):
    name_list = []
    num_list = []
    for key,value in _dict.items():
        name_list.append(key)
        num_list.append(value) 
    return name_list, num_list

def counter2list(_counter):
    name_list = []
    num_list = []
    for item in _counter:
        name_list.append(item[0])
        num_list.append(item[1]) 
    return name_list, num_list

def get_tag(text,cnt):
    tag_list = jieba.analyse.extract_tags(text)
    for tag in tag_list:
        cnt[tag] += 1

def mergeImage():
    print("Merging images")
    photo_width = 200
    photo_height = 200
    photo_path_list = []
    dirName = os.getcwd()+'/images'
    for root, dirs, files in os.walk(dirName):
            for file in files:
                if "jpg" in file:
                        photo_path_list.append(os.path.join(root, file))

    pic_num = len(photo_path_list)
    line_max = int(math.sqrt(pic_num))

    if line_max > 20:
        line_max = 20

    toImage = Image.new('RGBA',(photo_width*line_max,photo_height*line_max))

    for i in range(line_max): 
        for j in range(line_max):
            print("Merging%2d %2d %s"%(i,j,photo_path_list[line_max*i+j]))
            try:
                pic_fole_head = Image.open(photo_path_list[line_max*i+j])
            except:
                print("Wrong opening:%s"%photo_path_list[line_max*i+j])
            width, height =  pic_fole_head.size
            tmppic = pic_fole_head.resize((photo_width,photo_height))
            loc = (int(j%line_max*photo_width),int(i%line_max*photo_height))
            toImage.paste(tmppic,loc)

            if line_max*i+j >= len(photo_path_list):
                break

    toImage.save('./analyse/merged.png')

if __name__ == '__main__':
    Sex_dict = {1:'男',2:'女',0:'其他'}

    # Load data
    json_name = './data/friends.json'
    with codecs.open(json_name, encoding='utf-8') as f:
        friends = json.load(f)

    # Counters
    Sex_counter =  Counter()
    Province_counter = Counter()
    Signature_counter = Counter()
    NickName_counter = Counter()
    
    for friend in friends:
        Sex_counter[Sex_dict[friend['Sex']]] += 1
        if friend['Province'] != "":
            Province_counter[friend['Province']] += 1
        # tag extractor
        get_tag(friend['Signature'],Signature_counter)
        get_tag(friend['NickName'],NickName_counter)

    page = Page()

    # Sex
    name_list,num_list = dict2list(Sex_counter)
    page.add(get_pie('Gender',name_list,num_list))

    # Province & Map
    name_list,num_list = counter2list(Province_counter.most_common(15))
    page.add(get_bar('District',name_list,num_list))
    page.add(get_map('Map',name_list,num_list))

    # NickName
    name_list,num_list = counter2list(NickName_counter.most_common(200))
    page.add(word_cloud('NickName',name_list,num_list,[20,50]))

    # Signature
    name_list,num_list = counter2list(Signature_counter.most_common(200))
    page.add(word_cloud('Signature',name_list,num_list,[20,50]))
    
    page.render('./analyse/analyse.html')

    # Head Image
    mergeImage()
