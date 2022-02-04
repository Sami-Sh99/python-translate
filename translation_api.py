#pip install googletrans==4.0.0rc1

'''Translating CNN dataset from english to arabic'''

from googletrans import Translator 
from asyncio.log import logger
import os
import logging

translate_from=r'C:\Users\sbs10\OneDrive - American University of Beirut\Desktop\cnn_stories\cnn\stories'
translate_to=r'C:\Users\sbs10\OneDrive - American University of Beirut\Desktop\cnn_stories\cnn\stories_ar'
lang_code = 'ar'
max_character_limit=5000

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
translator = Translator(service_urls=[
      'translate.google.com',
    #   'translate.google.co.kr',
    ])

#Apply actual translation
with open('mapping_for_translation.txt') as f:
    counter=len(already_translated)
    for sample_file in f:
        with open(sample_file[:-1],encoding="utf-8") as sample_data:
            sample_data_text=sample_data.read()
            if len(sample_data_text)>max_character_limit:
                num_orig-=1
                continue
            while True:
                try:
                    sample_output = translator.translate(str(sample_data_text),src='en',dest=lang_code).text
                    break
                except KeyboardInterrupt:
                    exit()
                except Exception as e:
                    logger.error("Unknown error has occured, trying to retrieve data again...\n "+str(e.args))
            counter+=1
            with open(os.path.join(translated_stories_dir,sample_file.split('\\')[-1][:-1]),'w',encoding='utf-8') as new_file:
                new_file.write(sample_output)
            if counter%10==0:
                logging.info('Translated '+str( round(counter/num_orig*100,2))+"% \t"+str(counter)+' out of '+str(num_orig)+'% till done' )

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