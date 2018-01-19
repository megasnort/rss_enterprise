import os
import json
import tkinter as tk
from tkinter import ttk, TclError
import feedparser

from future import Future


def get_settings_path():
    return os.path.join('test', 'test_settings.json')


def load_settings(settings_path):
    print('loading settings')
    with open(settings_path) as fp:
        settings = json.load(fp)
        return settings


def load_news_items(feed_urls):
    print('loading news items')
    future_calls = [Future(feedparser.parse, rss_url) for rss_url in feed_urls]
    feeds = [future_obj() for future_obj in future_calls]

    entries = []

    for feed in feeds:
        entries.extend(feed["items"])

    sorted_entries = sorted(entries, key=lambda entry: entry['published'])

    return sorted_entries


def refresh_list(tree):
    settings_path = get_settings_path()
    settings = load_settings(settings_path)
    news_items = load_news_items(settings['feed_urls'])
    for i in news_items:
        print(i)
        try:
            tree.insert('', 'end', i['id'], text=i['title'])
        except TclError:
            pass

def main():
    root = tk.Tk()

    tree = ttk.Treeview(root)
    refresh_list(tree)

    tree.pack()

    root.mainloop()


if __name__ == '__main__':
    main()
