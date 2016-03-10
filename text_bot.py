import pickle

with open('futurama_scripts.pkl','r') as f:
  all_scripts, url_slug, urls = pickle.load(f)
