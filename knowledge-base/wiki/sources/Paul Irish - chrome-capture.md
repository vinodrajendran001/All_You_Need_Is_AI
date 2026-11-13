---
type: source-summary
created: 2026-11-13
updated: 2026-11-13
source_id: src-2026-11-11-paulirish-chrome-capture
source_title: chrome-capture/README.md at main
source_author: Paul Irish
source_url: https://github.com/paulirish/chrome-capture/blob/main/README.md
tags:
  - source/summary
  - browser-automation
  - testing
  - developer-tools
source_ids:
  - src-2026-11-11-paulirish-chrome-capture
status: active
---

# chrome-capture

## Summary

The README for `chrome-capture`, a small library and CLI in the `paulirish/chrome-capture` GitHub
repository, records a Chrome tab at 60 to 120 frames per second, up to 2160p, straight to an AV1
`.mp4` with optional tab audio and no ffmpeg. It builds on `Page.startScreenRecording`, a Chrome
DevTools Protocol (CDP) method available from Chrome 153 that landed in September 2026. Unlike the
decade-old screencast path, which ships JPEG frames over the protocol for an external encoder, Chrome
now encodes in flight and writes the file as it goes. The README gives a CLI, an API that accepts
Playwright, Puppeteer, or raw CDP handles, a Playwright Test fixture that records every test, and a
benchmark against Playwright's `recordVideo`. It also verifies its own frame-rate claims by decoding
a frame counter from the output instead of trusting the file's metadata. The README is unsigned; the
author is inferred from the repository owner.

## Key claims

### A native recorder replaces the screencast pipeline

- For about a decade, `Page.startScreencast` (from about 2013, built so DevTools could preview a
  USB-tethered Android device) was the only way to get frames out of CDP. Chrome JPEG-encodes each
  frame, base64-encodes it into JSON, waits for an acknowledgement, and the client library pipes the
  JPEGs into ffmpeg. Playwright's `recordVideo` and Puppeteer's `page.screencast()` are built on it.
- With `Page.startScreenRecording`, frames go **from the compositor** to an out-of-process encoder over
  shared memory, and Chrome writes AV1 into the mp4 during recording. Stopping is nearly instant
  because no ffmpeg flush remains, and recording can start and stop at any point, for example after
  login and page warm-up.
- Puppeteer v25.10+ wraps it in an experimental `page.record()`, deprecating `page.screencast()`.
  Playwright is still on the screencast path; the author "suspect[s]" it will adopt the new API.
- The README invites readers to "point your agent at `src/index.ts` and steal the implementation.
  It's tiny." No license is stated in the capture.

### Interfaces

- **CLI:** records audio by default. It runs headless up to 60 fps and on macOS switches to a visible
  (headful) browser above 60 fps so Chrome can lock onto a 120 Hz ProMotion display.
- **API:** `startRecording()` takes a Playwright page, a Puppeteer page, or a CDP session. Defaults are
  **60** fps and **1280x720**, the capture area is the viewport or the browser window, optional audio
  is 48 kHz stereo Opus, and `await using` writes the file when the block exits.
- **Test fixture:** a `@playwright/test` fixture records every test and attaches the mp4 to the
  report. A raw CDP recorder is also exported, and Playwright's action overlay (cursor, element
  highlights, click badges) is drawn into the DOM, so it appears in recordings.

### Benchmark against the old pipeline

The README's comparison uses the same **6.4 s** UI replay at **1280x800** on an M4 Max, with
`chrome-capture` at its default 60 fps.

| Measure | `recordVideo` (screencast + ffmpeg) | `chrome-capture` |
| --- | --- | --- |
| Output fps | **25** (up to 60) | **60** (up to 120) |
| Total wall-clock | **21 s** | **11 s** |
| Stop + finalize | **3,800 ms** | **17 ms** |
| WebSocket traffic | **10.5 MB** | **450 KB** |
| Final file size | **480 KB** | **330 KB** |
| PSNR vs lossless screenshot | **32 dB** | **34 dB** |

At 2160p, stopping takes **91 ms** versus **20.5 s**. In the benchmarked replay, the whole test
finishes about **10 s** sooner.

### Bitrate and limits, measured from the output

- There is no bitrate or quality setting yet. Chrome uses libaom AV1 in realtime one-pass VBR, with
  target bitrate scaling linearly with pixel rate: **2 Mbps** at 720p30, **9 Mbps** at 1080p60, **18
  Mbps** at 1080p120, and **72 Mbps** at 2160p120. The sweet spot is 1080p60 and up. For lossless
  1-pixel text at about 10 to 15 fps, an offline PNG screencast into ffmpeg "still has a place".
- **"Video files can lie about fps."** The stress test draws a binary frame counter on every animation
  frame and decodes it from the mp4 to count unique frames.
  - Headless Mac: **2160p at 60 fps**, because headless drives animation from a synthetic 60 Hz timer.
  - Headful Mac on a 120 Hz display: **1080p and 2160p at 120 fps** (**119.9 fps**, **59.8 Mbps** on
    WebGL scenes).
  - Headless Linux without a GPU, as in CI: **1080p at 60 fps** (**60.4** unique fps), **1440p at 60
    fps** (about **58**), or **75 to 83 fps** at 1080p with vsync uncapped.
  - Windows and Linux with a discrete GPU: unknown.
- On GPU-accelerated Macs, uncapping vsync makes animation frames spin at **1,600 to 9,800 fps**,
  starving capture and dropping 2160p at 60 fps to **0.3 fps**.

## Why it matters

Browser-test video is the evidence humans and agents use to check what a UI agent or an end-to-end
test actually did. The vault's [[Agentic Testing]] page concerns verification artifacts that can be
trusted. This source adds a cheaper, higher-fidelity artifact: per-test recording becomes a fixture
default rather than a 3.8-second tax. It also adds a method: the author does not trust the container
metadata's frame rate and instead measures the artifact by decoding a frame counter embedded in the
content. That is the same move as checking a grader against ground truth, applied to a test
recording.

## Tensions / open questions

- **Unsigned README, inferred author.** The capture has no author, publication date, or description.
  `source_author: Paul Irish` is inferred from the repository owner (`paulirish`), and the date in
  this source's ID is the capture date, not a publication date.
- **Single-machine benchmark.** All comparative numbers are from one M4 Max and one replay. The
  linked benchmark methodology is not captured, and Windows and discrete-GPU results are unknown.
- **Reported figures to read carefully.** **60.4** unique fps exceeds the 60 Hz vsync it is said to
  run at, which may be timing jitter; the README does not explain it. The **59.8 Mbps** reported for
  the 120 fps runs is not tied to a resolution; it is below the **72 Mbps** 2160p120 target but
  above the **18 Mbps** 1080p120 target, and the README does not explain it.
- **Ecosystem claims are time-bound.** Playwright's adoption is speculation, and Puppeteer's
  `page.record()` is experimental.
- **"Steal the implementation"** with no license in the capture: reuse terms need checking at the
  repository. The demo video is credited to a "Gemini Argon generation", which the capture does not
  explain further.

## Affected pages

- [[Agentic Testing]]

## Raw capture

- [[knowledge-base/raw/sources/chrome-capture]]

## Citations

- URL: https://github.com/paulirish/chrome-capture/blob/main/README.md (capture title
  "chrome-capture/README.md at main").
- Author: not stated in the capture. Paul Irish is inferred from the repository path
  `github.com/paulirish/...` and is not a byline.
- Published: not stated. Captured 2026-11-11; the ID date reflects the capture.
- Credits in the README: Alex Rudenko for landing `Page.startScreenRecording`; Sam1983Aing/senna-800kg
  for the demo video.

## Related pages

- [[Agentic Testing]]
- [[Computer Use Agents]]
- [[Agent Observability]]
- [[ByteByteGo - How GitHub Used AI to Port Copilot From TypeScript to Rust in Record Time]]
- [[@0xCodila - Reverse Engineering with REA and Opus 5.5 (Full Course)]]
