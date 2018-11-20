import os
import tkinter as tk
from tkinter import ttk, TclError, BOTH, Frame
import feedparser
from dateutil.parser import parse
import webbrowser
import subprocess
from pathlib import Path
from shutil import copyfile
from tkinterhtml import HtmlFrame
from time import sleep


class RssEnterprise():
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry("1000x700")
        self.root.title('RSS Enterprise')
        # self.root.iconbitmap("/home/stef/Python/rss_enterprise/icon.ico")

        self.settings_folder_path = os.path.join(Path.home(), '.rss_enterprise')

        self.assert_settings()

        with open(self.get_cache_path(), mode='a') as self.fp_cache:
            top_frame = Frame(self.root)
            top_frame.pack(fill=BOTH, expand=True)

            bottom_frame = Frame(self.root)
            bottom_frame.pack(fill=BOTH, expand=True)

            self.tree = ttk.Treeview(top_frame, selectmode='browse', columns=('title', 'feed', 'published',))
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

            self.text = HtmlFrame(self.root, fontscale=1.2, horizontal_scrollbar="auto")
            self.text.pack(fill=BOTH, expand=True)

            self.root.mainloop()

    def assert_settings(self):
        if not os.path.isdir(self.settings_folder_path):
            os.mkdir(self.settings_folder_path)

        if not os.path.isfile(self.get_feeds_path()):
            copyfile(os.path.join('test', 'feeds.txt'), self.get_feeds_path())

        if not os.path.isfile(self.get_cache_path()):
            with open(self.get_cache_path(), mode="w") as fp:
                fp.write('')

    def open_current_weblink(self, event):
        id = self.tree.selection()[0]
        self.open_link(id)

    def get_feeds_path(self):
        return os.path.join(self.settings_folder_path, 'feeds.txt')

    def get_cache_path(self):
        return os.path.join(self.settings_folder_path, 'cache')

    def load_feeds(self, feeds_path):
        print('loading feeds')
        with open(feeds_path, 'r') as fp:
            feeds = [l.strip() for l in fp.read().splitlines() if l.strip() != '']
            return feeds

    def add_line_to_cache(self, line):
        self.fp_cache.write(line + '\n')

    def load_news_items(self, feed_urls):
        print('loading news items')

        feeds = []

        for rss_url in feed_urls:
            result = feedparser.parse(rss_url)
            
            if result['status'] == 404:
                print(rss_url, 'was not found') 
            else:
                feeds.append(result)

        entries = []

        for feed in feeds:
            for i in feed["items"]:
                i['channel_title'] = feed['channel']['title']
                try:
                    i['formatted_date'] = parse(i['published'])
                except KeyError:
                    i['formatted_date'] = parse(i['updated'])

            entries.extend(feed["items"])

        sorted_entries = sorted(entries, key=lambda entry: entry['formatted_date'])
        sorted_entries.reverse()

        return sorted_entries

    def refresh_list(self):
        with open(self.get_cache_path(), 'r') as fp:
            cache = fp.read().splitlines()

        feeds = self.load_feeds(self.get_feeds_path())
        all_news_items = self.load_news_items(feeds)
        for i in all_news_items:
            try:
                if i['link'] not in cache:
                    self.tree.insert(
                        '', 'end', i['link'], text=i['title'],
                        values=(i['channel_title'], i['formatted_date'], i['summary'],)
                    )
            except (TclError, KeyError):
                # in case of double entries, or entries without a link, we just forget about them
                pass

    def on_tree_select(self, event):
        id = self.tree.selection()[0]
        summary = self.tree.item(id, "values")[2]
        self.set_input(summary)
        self.add_line_to_cache(id)

    def open_link(self, link):
        # works only on linux
        subprocess.Popen(['xdg-open', link])
        sleep(0.5)
        subprocess.Popen(['wmctrl', '-a', 'RSS Enterprise', ])

    def set_input(self, value):
        self.text.set_content(value)


if __name__ == '__main__':
    rss_enterprise = RssEnterprise()
