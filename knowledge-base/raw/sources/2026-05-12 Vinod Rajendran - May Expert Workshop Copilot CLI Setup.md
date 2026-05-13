---
type: raw-source
source_id: expert-workshop-copilot-cli-setup-2026-05
title: "May Expert Workshop - Copilot CLI Setup Guide"
author: Vinod Rajendran
url: ""
captured: 2026-05-13
tags: [copilot, cli, setup, wsl, workshop]
status: active
---

# May Expert Workshop - Copilot CLI Setup Guide

## Prerequisites

1. GitHub Copilot access
   ![[Pasted image 20260512094954.png]]

2. Local Windows admin access
   ![[Pasted image 20260512095353.png]]

## Setup Steps

### Install WSL

Open PowerShell in **administrator** mode by right-clicking and selecting "Run as administrator", enter the `wsl --install` command, then restart your machine.

```
wsl --install
```

### Launch VS Code

In terminal, click `+` → Ubuntu (WSL)

### Install Copilot CLI

Execute the below commands:

```bash
sudo apt update

sudo apt install nodejs npm

sudo npm install -g @github/copilot
```

### Launch Copilot

```bash
/mnt/c/Users/uixxxxx$ copilot
```

### Login

Inside the Copilot CLI:

```
/login
```

Select *github.com* → this will generate the 8-digit alphanumeric code.

In the browser, go to https://github.com/login/device

Click `continue` or `next` a couple of times then you'll end up with a one-time code page.

Key in the 8-digit code then `submit` and `authorize` it.

In the Copilot CLI:
- You need to accept the risk by selecting `yes`

The login will be successful.

### Selecting the Model

```
/model
```

![[Pasted image 20260512094241.png]]

![[Pasted image 20260512094408.png]]
