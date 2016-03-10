import pickle
from collections import defaultdict

with open('futurama_scripts.pkl','rb') as f:
  all_scripts = pickle.load(f)

# build stats
num_of_dialogs_dict = defaultdict(int)
num_of_words_dict = defaultdict(list)

for character, dialogs in all_scripts.items():
  num_of_dialogs_dict[character] += len(dialogs)
  for dialog in dialogs:
    num_of_words_dict[character].append(len(dialog.split()))

# pickle my results
with open('futurama_stats.pkl','wb') as f:
  pickle.dump([num_of_dialogs_dict, num_of_words_dict], f)
