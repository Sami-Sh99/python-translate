'''Translating CNN dataset from english to arabic'''

from asyncio.log import logger
import time
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from random import randint
import urllib.parse
import logging

translate_from=r'C:\Users\sbs10\OneDrive - American University of Beirut\Desktop\cnn_stories\cnn\stories'
translate_to=r'C:\Users\sbs10\OneDrive - American University of Beirut\Desktop\cnn_stories\cnn\stories_ar'
xpath_google_trans='/html/body/c-wiz/div/div[2]/c-wiz/div[2]/c-wiz/div[1]/div[2]/div[3]/c-wiz[2]/div[6]/div/div[1]/span[1]'
lang_code = 'ar '

stories_dir = os.path.abspath(translate_from)
translated_stories_dir = os.path.abspath(translate_to)
num_orig = len(os.listdir(stories_dir))

logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',level=logging.INFO,datefmt='%Y-%m-%d %H:%M:%S')

logging.info("Preparing to translate from %s to %s..." % (stories_dir, translated_stories_dir))
stories = os.listdir(stories_dir)
already_translated = os.listdir(translated_stories_dir)
to_translate = [x for x in stories if x not in already_translated]
logging.info("Making list of files to translate...")

with open("mapping_for_translation.txt", "w") as f:
    for s in to_translate:
        if (not s.endswith('story')):
            continue
        f.write("%s\n" % (os.path.join(stories_dir, s)))

#Launch translator
# launch browser with selenium:=>
options = webdriver.ChromeOptions()
options.binary_location = "C:\Program Files\Google\Chrome\Application\chrome.exe"
chrome_driver_binary = "chromedriver.exe"
browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)


#Apply actual translation
with open('mapping_for_translation.txt') as f:
    counter=len(already_translated)
    for sample_file in f:
        with open(sample_file[:-1],encoding="utf-8") as sample_data:
            sample_data_text=sample_data.read()
            if len(sample_data_text)>5000:
                num_orig-=1
                continue
            sample_data_text= urllib.parse.quote_plus(sample_data_text)
            while True:
                try:
                    browser.get("https://translate.google.co.in/?sl=auto&tl="+lang_code+"&text="+sample_data_text+"&op=translate")
                    time.sleep(4)
                    sample_output = browser.find_element_by_xpath(xpath_google_trans).text
                    break
                except KeyboardInterrupt:
                    exit()
                except:
                    logger.error("Unknown error has occured, trying to retrieve data again...")
            counter+=1
            with open(os.path.join(translated_stories_dir,sample_file.split('\\')[-1][:-1]),'w',encoding='utf-8') as new_file:
                new_file.write(sample_output)
            if counter%10==0:
                logging.info('Translated '+str(counter)+' out of '+str(num_orig)+" == "+str( round(counter/num_orig*100,2))+'% till done' )

# Check that the translated stories directory contains the same number of files as the original directory
num_orig = len(os.listdir(stories_dir))
num_translated = len(os.listdir(translated_stories_dir))
if num_orig != num_translated:
    raise Exception(
        "The translated stories directory %s contains %i files, but it should contain the same number as %s (which has %i files). Was there an error during translation?" % (
        translated_stories_dir, num_translated, stories_dir, num_orig))
logging.info("Successfully finished tokenizing %s to %s.\n" % (stories_dir, translated_stories_dir))

logging.info("Translation has finished.")
os.remove("mapping_for_translation.txt")