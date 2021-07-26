import sys
import os
import time
import io
import pandas as pd
import numpy as np
from googlesearch import search
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from pprint import pprint

def hero_format(hero_string):
    return hero_string.strip().replace(' ','_').lower()

def get_hero_url_list(driver):
    driver.get('https://dota2.fandom.com/wiki/Dota_2_Wiki')

    heroentries = driver.find_elements_by_xpath('//div[@class="heroentry"]/div/a')

#    for element in heroentries:
#        print(element.get_attribute('title'),element)

    print(len(heroentries),'heros found')

    return [x.get_attribute('href') for x in heroentries]

def get_hero_data(driver, hero_url):
    driver.get(hero_url)
    time.sleep(2)

    hero_data = {}

    # get title/unformatted title
    raw_title = driver.find_element_by_css_selector('#firstHeading').text
    print('Hero name:',raw_title)
    hero_data.update({'title':hero_format(raw_title)})
    hero_data.update({'title_raw':raw_title})

    # primary stat
    primary_stat = driver.find_element_by_xpath('//div[@id="primaryAttribute"]/a').get_attribute('title')
    hero_data.update({'primary_stat':primary_stat})

    # get image_path
    image_element = driver.find_element_by_css_selector('.infobox > tbody:nth-child(1) > tr:nth-child(1) > th:nth-child(1) > div:nth-child(1) > a:nth-child(1) > img:nth-child(1)')

    image_path = os.getcwd() + "/data/portraits/"+hero_format(str(image_element.get_attribute('data-image-name')))
    image_url = image_element.get_attribute('src')
    with open(image_path, 'wb') as fp:
        fp.write(image_element.screenshot_as_png)

    hero_data.update({'image_path':image_path})

    print(image_path, image_url)

    #
    # SWITCH TO COUNTERS
    driver.get(hero_url+'/Counters')

    # bad against
    bad_against = driver.find_elements_by_xpath('//div[contains(@style,"box-shadow:0px 0px 2px 4px red;")]/a')
    bad_against = [hero_format(x.get_attribute('title')) for x in bad_against]
    hero_data.update({'bad_against':bad_against})

    # good against
    good_against = driver.find_elements_by_xpath('//div[contains(@style,"box-shadow:0px 0px 2px 4px chartreuse;")]/a')
    good_against = [hero_format(x.get_attribute('title')) for x in good_against]
    hero_data.update({'good_against':good_against})

    # works well with
    well_with = driver.find_elements_by_xpath('//div[contains(@style,"box-shadow:0px 0px 2px 4px skyblue;")]/a')
    well_with = [hero_format(x.get_attribute('title')) for x in well_with]
    hero_data.update({'well_with':well_with})


#    pprint(hero_data)
    return hero_data

driver = webdriver.Firefox()
hero_entries = get_hero_url_list(driver)

df = pd.read_csv('./data/hero_data.csv')
print(df)

for i, hero_url in enumerate(hero_entries):
    df = df.append(hero_data := get_hero_data(driver, hero_url), ignore_index=True)
    print(hero_data,'\n')
    df.to_csv('./data/hero_data.csv',index=False)


driver.quit()
