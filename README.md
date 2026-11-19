# The World on Thursday — Nov 19, 2026

A single 1024×1024 image that sums up Thursday 19 November 2026 in six
stories: the worldwide launch of Grand Theft Auto VI, Trump's landing in
China and the trilateral summit in Shenzhen, tankers burning off the
Strait of Hormuz, Voyager 1 reaching one light-day from Earth, the EU's
proposed €45–49bn loan for Ukraine, and a record $190.4M Van Gogh sale.

## How it is made

`make_poster.py` draws everything with Pillow — masthead, six tiles in a
2×3 grid, and a small geometric glyph per story. No external images are
used. Run it to regenerate `entry.png`:

```sh
python3 make_poster.py
```

## Entry point

`main.py` copies the finished `entry.png` into
`$MAKEFUN_OUTPUT_DIR` (or `/output` when unset), byte for byte.
