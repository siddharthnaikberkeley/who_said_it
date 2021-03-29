import os
import json
import uuid
from datetime import datetime
import random


data_folders = ['/Users/sid/Downloads/messages/inbox','/Users/sid/Downloads/messages/archived_threads']
c_team_files = ['whitepeople_ragynbj68a', 'ericweedlefanclub_xzjrdn06ma', 'impeachtrump_9c9y_l7fxg', 'allcarsonsfault_3ai3ztryng', 'y20dphpillsputsyouprettyclosetotheedge_ereuw4gjxq',
                '1thefirstquestioniswhatistheobjectofoursciencethesimplestandmostintelligibleanswertothisquestionisthattruthist_piwcmdzkgw',
                'shoeloversdiscussion_2vd8iwwnka', 'wraymanningjamessealskaelanshallowand6others_p08ic18u9a', 'allstartraeyoung_b3osmyvqxg',
                'zteam_msm-moicdg', 'shrinkaroyfacebookuserfacebookuserand3others_nffp6lucng', 'robotchinesecartoonexclusivediscussion_evtvvs0jgq', 'xmasteam_ta_enf02aa', 'shoeloversdiscussion_w_pojnjfzg',
                'twitterLLJripgus_gH0MCIbyZg', 'theflakehousewithcarsonbehre_faawmuxslw', 'cteam_nwz0vxxrbw', 'shittalksunnychat_iwiqazb_bq',
                'shrinkaroyfacebookuserandmattkralik_xlo5wo2wxg', 'crawdauntwithagunlikearealgunseriouslywatchwhereyourepointingthatcrawdaunt_aounqy-enw']

is_cteam = [ "Sunny Sharma", "Sean Fitzpatrick", "Kevin Peterson", "Neil Hegebarth", "Ben Block", "James Cho", "Carson Behre", "Sid Naik", "Wray Manning", "Kevin Dole Peterson"]

message_lengths = {}
message_concat_length = {}
images = {}
sounds = {}
message_freqs = {}
og_message_hash = {}
user_to_messages = {}
date_to_uuid = {}

curr_set = {}


def check_for_sender(hash):
  global og_message_hash
  if not og_message_hash:
    if os.path.exists('og_msg_hash.json'):
      with open('og_msg_hash.json', 'r') as f:
        og_message_hash = json.load(f)
    else:
      populate_structs()

  if og_message_hash.get(hash, None):
    sender = og_message_hash.get(hash)['sender']
    return sender
  else:
    return None


def get_choices():
  global user_to_messages
  if not user_to_messages:
    if os.path.exists('og_msg_hash.json'):
      with open('usr_2_messages.json', 'r') as f:
        user_to_messages = json.load(f)
    else:
      populate_structs()

  return list(user_to_messages.keys())

def get_messages_for_game(min_msg_length=20, min_message_concat=1, max_message_concat = 5, max_message_length=200, include_images=False, concat_automatically=True, min_time=None, max_time=None, exclude_users=None, include_audio=False, include_video=False):
  global og_message_hash
  global message_lengths
  if not og_message_hash:
    if os.path.exists('og_msg_hash.json'):
      with open('og_msg_hash.json', 'r') as f:
        og_message_hash = json.load(f)
      with open('msg_lens.json', 'r') as f:
        message_lengths = json.load(f)
    else:
      populate_structs()
  lens = list(message_lengths.keys())
  while True:
    len_lens = len(lens)
    sample = random.randrange(0, len_lens)
    bazinga = lens[sample]
    if min_msg_length < bazinga < max_message_length:
      break
  possibilities = message_lengths[bazinga]
  poss_len = len(possibilities)
  poss_sample = random.randrange(0, poss_len)
  random_uuid = possibilities[poss_sample]
  msg = og_message_hash[random_uuid]
  return msg,random_uuid



def populate_structs():
  for q in data_folders:
    for x in os.listdir(q):
      full_data_path = os.path.join(q,x)
      if x not in c_team_files:
        continue
      print(full_data_path)
      if not os.path.isdir(full_data_path):
        continue
      for y in os.listdir(full_data_path):
        message_files = os.path.join(full_data_path,y)
        print(message_files)
        if 'message' in y:
          with open(message_files, 'r') as f:
            temp = json.load(f)
            if not temp.get('messages', None) and not temp.get('type', '') == 'generic':
              continue
            else:
              msgs = temp['messages']
              curr_sender = None
              consec_msgs = 0
              consec_uuids = []
              last_timestamp = None
              for z in msgs:
                sender = z['sender_name']
                if sender not in is_cteam:
                  continue
                time = z['timestamp_ms']
                time_sec = time / 1000
                dt_object = datetime.fromtimestamp(time_sec)
                str_time = dt_object.strftime('%m/%d/%Y, %H:%M:%S')
                str_time_key = dt_object.strftime('%m,%Y')

                is_audio = False
                is_photo = False
                msg_uuid = str(uuid.uuid4())
                if z.get('audio_files', None):
                  is_audio = True
                if z.get('photos', None):
                  is_photo = True
                if is_audio:
                  audios = z['audio_files']
                  for v in audios:
                    audio_uri = v['uri']
                    audio_hash = audio_uri.split('/')[-1].split('.')[0]
                    sounds[audio_hash] = { 'sender' : sender,
                                           'human_time' : str_time }
                  if date_to_uuid.get(str_time_key, None):
                    date_to_uuid[str_time_key].append(audio_hash)
                  else:
                    date_to_uuid[str_time_key] = [audio_hash]
                  continue
                if is_photo:
                  photos = z['photos']
                  for w in photos:
                    photo_uri = w['uri']
                    # messages/inbox/Zteam_MSm-mOIcdg/photos/12436083_10207956969665143_1259837278_n_10207956969665143.jpg
                    photo_hash = photo_uri.split('/')[-1].split('.')[0]
                    images[photo_hash] = { 'sender' : sender,
                                           'human_time' : str_time}
                  if date_to_uuid.get(str_time_key, None):
                    date_to_uuid[str_time_key].append(photo_hash)
                  else:
                    date_to_uuid[str_time_key] = [photo_hash]
                  continue
                if z.get('content', None):
                  content = z['content']
                  if curr_sender and last_timestamp and (sender != curr_sender or abs(time - last_timestamp) > 300000):
                    if message_concat_length.get(consec_msgs, None):
                      message_concat_length[consec_msgs].append(consec_uuids)
                    else:
                      message_concat_length[consec_msgs] = [consec_uuids]
                    curr_sender = sender
                    consec_msgs = 1
                    consec_uuids = [msg_uuid]
                    last_timestamp = time
                  elif curr_sender and sender == curr_sender:
                    consec_msgs += 1
                    consec_uuids.append(msg_uuid)
                    last_timestamp = time
                  else:
                    curr_sender = sender
                    consec_msgs = 1
                    consec_uuids = [msg_uuid]
                    last_timestamp = time

                  msg_len = len(content)
                  og_message_hash[msg_uuid] = {
                    'body' : content,
                    'sender' : sender,
                    'human_time' : str_time
                  }

                  if date_to_uuid.get(str_time_key, None):
                    date_to_uuid[str_time_key].append(msg_uuid)
                  else:
                    date_to_uuid[str_time_key] = [msg_uuid]


                  if message_lengths.get(msg_len, None):
                    message_lengths[msg_len].append(msg_uuid)
                  else:
                    message_lengths[msg_len] = [msg_uuid]

                  content_hash = hash(content)
                  if message_freqs.get(content_hash, None):
                    message_freqs[content_hash] += 1
                  else:
                    message_freqs[content_hash] = 1

                  if user_to_messages.get(sender, None):
                    user_to_messages[sender].append(msg_uuid)
                  else:
                    user_to_messages[sender] = [msg_uuid]

  with open('usr_2_messages.json', 'w') as f:
    print(user_to_messages.keys())
    json.dump(user_to_messages, f)
  with open('msg_freq.json', 'w') as f:
    json.dump(message_freqs, f)
  with open('date_to_uuid.json', 'w') as f:
    json.dump(date_to_uuid, f)
  with open('og_msg_hash.json', 'w') as f:
    print(len(og_message_hash))
    json.dump(og_message_hash, f)
  with open('msg_concat.json', 'w') as f:
    json.dump(message_concat_length, f)
  with open('msg_lens.json', 'w') as f:
    json.dump(message_lengths, f)
  with open('imgs.json', 'w') as f:
    json.dump(images, f)
  with open('audio.json', 'w') as f:
    json.dump(sounds, f)
