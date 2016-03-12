import pickle
from collections import defaultdict

with open('futurama_scripts.pkl','rb') as f:
  scripts = pickle.load(f)

with open('futurama_stats.pkl','rb') as f:
    dialogs, words = pickle.load(f)

# sort the characters by the number of lines they have, reverse order
sorted_x = sorted(dialogs.items(), key=lambda x:x[1],reverse=True)

main_scripts = defaultdict(list)
main_dialogs = defaultdict(int)
main_words = defaultdict(int)

for key, _ in sorted_x[:50]:
  main_scripts[key] = scripts[key]
  main_dialogs[key] = dialogs[key]
  main_words[key] = words[key]

with open('futurama_main.pkl','wb') as f:
  pickle.dump([main_scripts, main_dialogs, main_words], f)

