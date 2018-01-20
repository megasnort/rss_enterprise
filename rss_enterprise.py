import os
import json
import tkinter as tk
from tkinter import ttk, TclError, BOTH, Text, Frame
import feedparser

from future import Future


class RssEnterprise():
    def __init__(self):
        root = tk.Tk()
        root.geometry("800x500")

        top_frame = Frame(root)
        top_frame.pack(fill=BOTH, expand=True)

        bottom_frame = Frame(root)
        bottom_frame.pack(fill=BOTH, expand=True)

        self.tree = ttk.Treeview(top_frame, selectmode='browse', columns=('title', 'feed', 'published', ))
        self.refresh_list()

        scrollbar_tree = ttk.Scrollbar(top_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_tree.set)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.tree.heading('#0', text='title', anchor=tk.CENTER)
        self.tree.heading('#1', text='feed', anchor=tk.CENTER)
        self.tree.heading('#2', text='published', anchor=tk.CENTER)

        self.tree.column('#0', stretch=tk.YES, minwidth=50, width=430)
        self.tree.column('#1', stretch=tk.YES, minwidth=50, width=150)
        self.tree.column('#2', stretch=tk.YES, minwidth=50, width=200)

        scrollbar_tree.pack(side='right', fill='y')
        self.tree.pack(fill=BOTH, expand=True)

        text = Text(bottom_frame)

        scrollbar_text = ttk.Scrollbar(bottom_frame, orient="vertical", command=text.yview)
        text.configure(yscrollcommand=scrollbar_text.set)
        scrollbar_text.pack(side='right', fill='y')
        text.pack(fill=BOTH, expand=True)

        root.mainloop()

    def get_settings_path(self):
        return os.path.join('test', 'test_settings.json')

    def load_settings(self, settings_path):
        print('loading settings')
        with open(settings_path) as fp:
            settings = json.load(fp)
            return settings

    def load_news_items(self, feed_urls):
        print('loading news items')
        future_calls = [Future(feedparser.parse, rss_url) for rss_url in feed_urls]
        feeds = [future_obj() for future_obj in future_calls]

        entries = []

        for feed in feeds:
            for i in feed["items"]:
                i['channel_title'] = feed['channel']['title']
            entries.extend(feed["items"])

        sorted_entries = sorted(entries, key=lambda entry: entry['published'])

        return sorted_entries

    def refresh_list(self):
        settings_path = self.get_settings_path()
        settings = self.load_settings(settings_path)
        news_items = self.load_news_items(settings['feed_urls'])
        for i in news_items:
            # print(i)
            try:
                self.tree.insert('', 'end', i['id'], text=i['title'], values=(i['channel_title'], i['published'], ))
            except TclError:
                pass

    def on_tree_select(self, event):
        item = self.tree.selection()[0]
        item_text = self.tree.item(item, "text")
        item_id = self.tree.item(item, "value")
        print(item_id)


if __name__ == '__main__':
    rss_enterprise = RssEnterprise()
