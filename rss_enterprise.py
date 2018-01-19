import os
import json
import tkinter as tk
from tkinter import ttk, TclError, BOTH, Text, Frame
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
        # print(i)
        try:
            tree.insert('', 'end', i['id'], text=i['title'])
        except TclError:
            pass


def main():
    root = tk.Tk()
    root.geometry("800x500")

    top_frame = Frame(root)
    top_frame.pack(fill=BOTH, expand=True)

    bottom_frame = Frame(root)
    bottom_frame.pack(fill=BOTH, expand=True)

    tree = ttk.Treeview(top_frame, selectmode='browse')
    refresh_list(tree)

    scrollbar_tree = ttk.Scrollbar(top_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar_tree.set)
    scrollbar_tree.pack(side='right', fill='y')
    tree.pack(fill=BOTH, expand=True)

    text = Text(bottom_frame)

    scrollbar_text = ttk.Scrollbar(bottom_frame, orient="vertical", command=text.yview)
    text.configure(yscrollcommand=scrollbar_text.set)
    scrollbar_text.pack(side='right', fill='y')
    text.pack(fill=BOTH, expand=True)

    root.mainloop()


if __name__ == '__main__':
    main()
