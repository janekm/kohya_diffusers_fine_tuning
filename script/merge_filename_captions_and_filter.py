import argparse
import glob
import os
import json
import re

from tqdm import tqdm

tag_replacements = {
    'wlop': 'painting by wlop',
    'enki': 'painting by enki bilal',
    'kagami': 'painting by kagami',
    'laure': 'painting by laure',
    'laureart': 'painting by laure',
    'guweiz': 'painting by guweiz',
    'sakimichan': 'painting by sakimichan',
    'markprinz': 'photo by markprinz',
    'supergirl': 'supergirl',
    'lalisa manobal': 'photo of lalisa manobal',
    'julia': 'photo of julia',
    'emma watson': 'emma watson',
    'suzu hirose': 'suzu hirose',
    'zhang jingna': 'fashion photo by zhang jingna',
    'roger davies': 'fashion photo by roger davies',
    'paul bellaart': 'fashion photo by paul bellaart',
    'nayo_photo': 'fashion photo by nayo',
    'michael_photo': 'fashion photo by michael',
    'matteu connie': 'fashion photo by matteu connie',
    'marc collins': 'fashion photo by marc collins',
    'lina tesch': 'fashion photo by lina tesch',
    'editorial': 'editorial',
    'beauty': 'beauty',
    'lara jade': 'fashion photo by lara jade',
    'joey wright': 'fashion photo by joey wright',
    'jay mawson': 'fashion photo by jay mawson',
    'james nader': 'editorial photo by james nader',
    'gary lupton': 'fashion photo by gary lupton',
    'david roemer': 'fashion photo by david roemer',
    'cole sproouse': 'editorial photo by cole sproouse',
    'ben watts': 'fashion photo by ben watts',
    'austin hargrave': 'editorial photo by austin hargrave',
    'anita sadowska': 'fashion photo by anita sadowska',
    'andrew yee': 'fashion photo by andrew yee',
    'alana tyler slutsky': 'fashion photo by alana tyler slutsky',
    'no humans': '',
    'young': '',
    'greyscale': 'greyscale, B&W',
    'asian': 'asian',
    'supergirl': 'supergirl',
    'alina': 'alina',
    'blackpink': 'blackpink',
    'blurry': 'shallow depth of field',
    'realistic': 'photo',
    'photorealistic': 'photo',
    'blurry': '',
    '1girl': '1girl, woman'
}

def main(args):
  caption_paths = glob.glob(os.path.join(args.train_data_dir, "*.txt"))
  print(f"found {len(caption_paths)} images.")

  print("cleaning captions and tags.")
  for caption_path in tqdm(caption_paths):
    print(caption_path)
    caption_fn = re.match(r"^./\d+-\d+-(photo of [^.]*)", caption_path).groups()[0] + ".txt"
    caption = re.match(r"^./\d+-\d+-photo of ([^(]*)", caption_path).groups()[0]
    filename_tags = caption.split(',')
    tags = list()
    for tag in filename_tags:
      tag = tag.strip()
      if tag in tag_replacements.keys():
        tag = tag_replacements[tag]
      if tag not in tags:
        tags.append(tag)
    with open(caption_path, "rt", encoding='utf-8') as f:
      caption_file_tags = f.readlines()[0].strip()
      caption_file_tags = caption_file_tags.split(',')
      print(caption_file_tags)
      for i, tag in enumerate(caption_file_tags):
        tag = tag.strip()
        if tag in tag_replacements:
          tag = tag_replacements[tag]
        if tag not in tags:
          tags.append(tag)
    print(f"tags: {tags}")
    tags_path = os.path.join(args.output_data_dir, caption_fn)
    with open(tags_path, "wt", encoding='utf-8') as f:
      f.write(','.join(tags))


if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("train_data_dir", type=str, help="directory for train images / 学習画像データのディレクトリ")
  parser.add_argument("output_data_dir", type=str, help="directory for output images / テスト画像データのディレクトリ")
  # parser.add_argument("--debug", action="store_true", help="debug mode")

  args = parser.parse_args()
  main(args)
