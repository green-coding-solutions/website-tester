## What?

This repository tries to explore the question if:
- We can monitor a website over time and can see if the energy cost for rendering changes
- If different websites have different energies for rendering which is uncorrelated to the pure time it takes for rendering (aka different power draw)

## How?

We use the [Green Metrics Tool](https://github.com/green-coding-berlin/green-metrics-tool/) to setup a simple Playwright Headless Browser based benchmark.

There are different types of pages:

- bbc.co.uk - Media. Lots of images and tracking
- theguardian.co.uk - Media. Lots if images and tracking
- michaelkors.de - Playing video
- green-coding.io - low fi
- svgator.com - SVG Animation