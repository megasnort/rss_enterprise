import os
import json
import tkinter as tk
from tkinter import ttk, TclError, BOTH, Text, Frame, END
import feedparser
from dateutil.parser import parse
from future import Future
import webbrowser
from pathlib import Path
from shutil import copyfile


class RssEnterprise():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1000x700")

        self.settings_folder_path = os.path.join(Path.home(), '.rss_enterprise')

        self.assert_settings()

        top_frame = Frame(self.root)
        top_frame.pack(fill=BOTH, expand=True)

        bottom_frame = Frame(self.root)
        bottom_frame.pack(fill=BOTH, expand=True)

        self.tree = ttk.Treeview(top_frame, selectmode='browse', columns=('title', 'feed', 'published', ))
        self.refresh_list()

        scrollbar_tree = ttk.Scrollbar(top_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_tree.set)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind('<Return>', self.open_current_weblink)
        self.tree.heading('#0', text='title', anchor=tk.CENTER)
        self.tree.heading('#1', text='feed', anchor=tk.CENTER)
        self.tree.heading('#2', text='published', anchor=tk.CENTER)

        self.tree.column('#0', stretch=tk.YES, minwidth=50, width=630)
        self.tree.column('#1', stretch=tk.YES, minwidth=50, width=150)
        self.tree.column('#2', stretch=tk.YES, minwidth=50, width=200)

        scrollbar_tree.pack(side='right', fill='y')
        self.tree.pack(fill=BOTH, expand=True)

        self.text = Text(bottom_frame)

        scrollbar_text = ttk.Scrollbar(bottom_frame, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=scrollbar_text.set)
        scrollbar_text.pack(side='right', fill='y')
        self.text.pack(fill=BOTH, expand=True)

        self.root.mainloop()

    def assert_settings(self):
        if not os.path.isdir(self.settings_folder_path):
            os.mkdir(self.settings_folder_path)

        if not os.path.isfile(self.get_settings_path()):
            copyfile(os.path.join('test', 'settings.json'), self.get_settings_path())

        if not os.path.isfile(self.get_cache_path()):
            with open(self.get_cache_path(), mode="w") as fp:
                fp.write('')

    def open_current_weblink(self, event):
        id = self.tree.selection()[0]
        self.open_link(id)

    def get_settings_path(self):
        return os.path.join(self.settings_folder_path, 'settings.json')

    def get_cache_path(self):
        return os.path.join(self.settings_folder_path, 'cache')

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
                i['formatted_date'] = parse(i['published'])
            entries.extend(feed["items"])

        sorted_entries = sorted(entries, key=lambda entry: entry['formatted_date'])
        sorted_entries.reverse()

        return sorted_entries

    def refresh_list(self):
        settings_path = self.get_settings_path()
        settings = self.load_settings(settings_path)
        news_items = self.load_news_items(settings['feed_urls'])
        for i in news_items:
            try:
                self.tree.insert(
                    '', 'end', i['link'], text=i['title'], values=(i['channel_title'], i['formatted_date'], i['summary'], )
                )
            except (TclError, KeyError):
                # in case of double entries, or entries without a link, we just forget about them
                pass

    def on_tree_select(self, event):
        id = self.tree.selection()[0]
        summary = self.tree.item(id, "values")[2]
        self.set_input(summary)

    def open_link(self, link):
        webbrowser.open(link, 9, autoraise=False)
        self.bring_to_front()

    def set_input(self, value):
        self.text.delete(1.0, END)
        self.text.insert(1.0, value)

    def bring_to_front(self):
        # self.root.attributes('-topmost', True)
        # self.root.update()
        # self.root.attributes('-topmost', False)

        # self.root.after(1, lambda: self.root.focus_force())

        # self.root.lift()
        # self.root.attributes('-topmost', False)
        # self.root.call('wm', 'attributes', '.', '-topmost', True)
        # self.root.after_idle(self.root.call, 'wm', 'attributes', '.', '-topmost', False)
        pass

if __name__ == '__main__':
    rss_enterprise = RssEnterprise()
