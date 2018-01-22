# RSS Enterprise

![RSS Enterprise](icon/icon.svg "RSS Enterprise")

In my opinion, existing RSS Readers make everything to complicated. I just want to

- subscribe to feeds
- view one list with the unread news items of all the feeds
- view the body of these news item by walking this list
- open the news item in the default browser, in the background
- have a RSS Reader with a hilarious name

## Usage

Once you have installed the necessary [requirements](requirements.txt) in a Python 3.6 environment, boot the program with

```bash
python rss_enterprise.py
```

Walk through the news items with the arrow keys or mouse. Press ENTER to open the link in your default browser. Once you view a specific item, it will not reappear in the list ever again.

## Setup

Once you started the application the first time, in `~/.rss_enterprise/feeds.txt` you will find some default feeds. Replace them, or add feeds of your liking. For now you need to ~~restart~~ re-engage RSS Enterprise to reload your feeds.


## Roadmap

- Make it available as a nice standalone app on
    - Linux (apt)
    - OSX (brew-cask)
    - Windows
- Open the link in a browser in the background
- Add easier way to edit the feeds (and refresh news items when adding/removing feeds)
- Create a véry nice icon
- Put it on PyPi
- Clean up code
- Tests
- ...
