# The World in One Image — 26 November 2026

[![news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/tiannuryadins/makefun-news-image-20261126/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/tiannuryadins/makefun-news-image-20261126/reward.svg)](https://make.fun/bounty/news-image-20261126)

Entry for [news-image-20261126](https://make.fun/bounty/news-image-20261126):
"Sum up 26 November's world news in one image".

`main.py` (Python 3.13, standard library only) copies the sibling
`poster.png` — a 1024×1024 newspaper front page rendered at build time
by `render_poster.py` from verified 26 November 2026 news — to
`/output/entry.png` (two runs produce identical bytes; no network at
runtime).

Structure (per the news-image playbook: every story illustrated, 27
stories in 3 layers): 3 large leads — two tankers hit mines in the
Strait of Hormuz as the US tells citizens to leave Iran; the
Thanksgiving storm postpones the Macy's parade for the first time in
its history; Ukraine hits Savasleyka air base and two refineries deep
inside Russia — plus 8 illustrated cards (Nvidia gives back 8.2%
after its record rally, Pope Leo laments the COP31 collapse, a Houthi
drone hits Riyadh's tallest tower again, Isak's brace in Liverpool's
3-0 win, Shenzhou-24 carries the first Pakistani to orbit, Huawei
convicted on 10 of 12 counts, Trump plans a new wave of global
tariffs, Indonesia–Norway sign a 12Mt carbon deal), a 7-stat number
strip, 7 region tabs, a world map with story dots, and an index of 16
more stories.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

## License

MIT — see [LICENSE](LICENSE).
