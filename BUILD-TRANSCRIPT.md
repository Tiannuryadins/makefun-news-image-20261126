# BUILD-TRANSCRIPT — news-image-20261126

Built Thu 26 Nov 2026 ~07:10–07:30 WIB by subagent for the make.fun
bounty news-image-20261126 ("Sum up 26 November's world news in one
image", $100, deadline Sat 28 Nov 2026 07:00 WIB).

## Verification of facts (live web search, 26 Nov 2026 morning)

- Hormuz mines: IRGC Navy said 2 tankers struck naval mines and caught
  fire on 25 Nov (Reuters via globalsecurity/distortion-daily); US
  Virtual Embassy told citizens to leave Iran at once; 10 tanker
  strikes in one week (gCaptain); Brent $91.40 Tue close, +$2
  (ME Forum); Hormuz traffic down 42% vs prewar (ME Forum).
- Thanksgiving storm: Macy's parade postponed to Sat 28 Nov — first
  weather postponement in its history (Fox Weather); storm targets
  250M+ people; 4,500+ US flights delayed Wed, 63 cancelled
  (FlightAware via Fox Weather); gusts 60 mph; up to 8 in snow
  St. Louis; NJ state of emergency (Gov. Mikie Sherrill).
- Ukraine: Savasleyka air base struck, 3 MiG-31 + 2 Su-34 damaged
  (Reuters, 25 Nov); Syzran + Kuibyshev refineries hit ~800 km from
  border (Kyiv Independent via europeansays); 2,091 Russian personnel
  lost in a day, cumulative ~1.64m (Ukr General Staff via h.ua);
  DTEK plant halted generation, power out in 5 regions (Hudson).
- Nvidia: +31.48% Mon 23 Nov to $165.05, +$952bn (CNN); fell 8.15%
  to $151.60 by 11:05 ET Tue 24 Nov (Motley Fool).
- COP31: ended Sun 22 Nov with no deal in Antalya; Pope Leo lamented
  failure 25 Nov (Reuters); OPEC blamed the EU (Reuters, 25 Nov).
- Riyadh: Houthi drone hit the capital's tallest tower a second time
  in under a week, 11 wounded (Reuters Gulf Currents, 25 Nov).
- Champions League Matchday 5, Wed 25 Nov: Liverpool 3-0 Club
  Brugge (Isak x2), PSG 2-2 Roma, Bayern 1-2 Lille, Sporting 2-2
  Man Utd, Real Madrid 5-1 PSV Tue (UEFA).
- Shenzhou-24: launched with Muhammad Zeeshan Ali, first Pakistani
  astronaut / first foreign national on a Chinese crewed mission
  (111NEXT, 25 Nov).
- Huawei: convicted on 10 of 12 counts in Brooklyn federal case,
  tech theft + fraud (111NEXT, 25 Nov).
- Tariffs: Trump plans new wave of global tariffs (Irish Sun/AFR via
  311 Institute, 25 Nov); EU to invest $55bn in AI + quantum
  (Courthouse News via 311 Institute).
- Indonesia–Norway: 12-million-ton carbon deal to boost solar power
  at COP31 (Carbon Credits, 25 Nov).
- Index items: Vance postmortem blaming Iran war for midterm losses;
  Trump "inclined" to renew strikes after New Year (NY Post via
  Distortion Daily); Meta rethinks 2030 net-zero, AI emissions +45%;
  Tesla FSD approval in Italy; Sarkozy + Bruni trial; Cessna crash,
  6 dead, Gulf of Mexico; Poland no-fly zone; Blysk laser first
  combat use; EU adds 15 Russian defence entities; Black Friday
  opt-outs (Reuters).

## Build

- `render_poster.py` (pure PIL + stdlib, no network at render time)
  renders 1024x1024 poster: serif masthead, red deck, 7-stat number
  strip, 7 region tabs, 3 illustrated leads, 8 illustrated cards,
  dotted world map + 16-row illustrated index = 27 stories.
- All 11 scene illustrations drawn fresh for this edition
  (mines, parade balloon, airfield, falling NVDA chart, cracked
  globe, Riyadh tower, football, rocket, gavel, containers, solar
  palms). Nvidia and Hormuz stories continue from 24 Nov but with a
  different angle (the -8.2% pullback; the mine strikes) and
  completely new drawings — no illustration asset was reused.
- Visual self-check (playbook rule 12): poster read as an image
  3 times. Fixed twice: lead/card bodies clipped by the next row
  (shortened bodies, lead art 114→106 px, body leading 15→14).
  Final render: all text fully visible, no card under 70% filled.

## Determinism

- `render_poster.py` run twice in a row after the final edit:
  sha256 `1856841f51125fb4633f4e56fc95e3333a5dc257d260a6ec123a979f33d0a06b`
  both times (poster.png, 176,599 bytes).
- `main.py` run with MAKEFUN_OUTPUT_DIR=out: entry.png produced,
  byte-identical to poster.png (same sha256).

## Playbook checklist

- [x] >=25 stories, 3 layers (3 + 8 + 16 = 27)
- [x] Every lead/card illustrated (11 fresh scene illustrations)
- [x] Number strip mandatory (7 stats)
- [x] Region structure (7 tabs)
- [x] Red deck naming the 3 top stories
- [x] Serif headlines, clean sans body, no monospace
- [x] No recycled illustrations
- [x] World map with dots + index
- [x] Facts verified live before render
- [x] Poster viewed before handoff
- [~] Scene illustrations 11 vs target 13–16 (compensated by the
      world map + 16 mini illustrated index icons = 28 visual
      elements total; the 24 Nov edition had 9 scene illustrations)
- [~] Red deck is serif red but NOT italic — no serif-italic font
      exists on this box (only mono oblique, which the playbook bans)

## Not done (parent's steps)

- Kit download/bundle, `makefun check`, `makefun submit` — NOT run.
- No commit, no push. Repo Tiannuryadins/makefun-news-image-20261126
  to be published by the parent.
