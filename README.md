# `subscene-downloader`
An incredibly bad and unintuitive interactive shell for downloading subtitles from Subscene.

### Featuring
- 0% Scrapy (it's `request` and `bs4` all the way down.)
- 0% clean code
- 100% bias towards English SDH (subtitles for the deaf and hard of hearing) / HI (hearing impaired) subtitles, because why not

### Getting started / User manual
Hint: go figure.
```
$ python subscene.py

> ?
HINTS:
    MISC
        [?]help, e[x]it, [cl]s
    SETTINGS
        [st] setTitle(title)
        [sl] setLang(lang)
        [sh] setHI(hi)
        [c] current()
    ACTIONS
        [s] search(query)
        [l] getlist(title, lang, hi_only)
        [d] download(id, lang)
    LANGUAGE
        Full name or 'all'

> s("death to 2021")
Fetching site (search)...
death-to-2021 | Death to 2021 (2021)

> st("death-to-2021")

> c()
Current settings:
Language = english; HI only = True; Keyword Filter = True
Title = death-to-2021

> l()
Fetching site (listing)...
0/107 subtitles remains

> sh(False)

> l()
Fetching site (listing)...
2/107 subtitles remains
2655108 | English | Death.To.2021.2021.1080p.WEBRip.x264-RARBG  | myvideolinksnet
2655105 | English | Death.To.2021.2021.1080p.WEBRip.x264.AAC5.1-[YTS.MX]  | myvideolinksnet

> d(2655105)
Fetching (download)...
36325 bytes written.

> x

$ ls -l
-rw-r--r-- 1 arch root 36325 Jan  1 12:00 death-to-2021_2655105_english.zip
```

### Room for Improvements
A metric/imperial ton. Here's a few that's on top of my mind:
- Rewrite as CLI tool instead of interactive shell
  - Or as GUI tool? (any lightweight, sensible and cross-platform UI framework on Python?)
- Enable customization of keyword filters
- Auto unpack zip files after download (so you can get right into the ass (or srt))
