# Hosting Review: Creative Compositor

## Current App Profile

| Characteristic | Detail |
|---|---|
| **Framework** | Streamlit (Python) |
| **Dependencies** | Pillow, watchdog, **ffmpeg** (system-level) |
| **CPU load** | Low for static composites, **high for video** (H.264 encoding, CRF 18, preset medium) |
| **Memory** | Moderate — loads full images into RAM, sequential processing |
| **Storage** | Grows with every render batch (outputs not auto-cleaned) |
| **Auth** | None — no user system |
| **File I/O** | Filesystem-based — no upload/download UI, files must be placed on server |
| **Multi-user** | Not supported — single shared `config.json`, no session isolation |

## Critical Gaps for Online Hosting

Before choosing a platform, these need addressing:

1. **No file upload mechanism** — users can't get assets onto the server
2. **No file download mechanism** — no way to retrieve rendered outputs
3. **Shared config.json** — all users overwrite each other's position settings
4. **No authentication** — anyone with the URL has full access
5. **ffmpeg dependency** — not available on most serverless/PaaS platforms without custom builds
6. **Sequential rendering** — blocks the UI; one user rendering blocks everyone

## Hosting Options Compared

### 1. Streamlit Community Cloud (Free)

| | |
|---|---|
| **Cost** | Free |
| **CPU/RAM** | ~1 vCPU, 1GB RAM |
| **Storage** | Ephemeral (wiped on reboot) |
| **ffmpeg** | Available via `packages.txt` (`apt` layer) |
| **Custom domain** | No |
| **Auth** | Basic (GitHub/Google SSO via Streamlit) |

**Verdict: Not viable for production.** Ephemeral storage means inputs/outputs disappear on every restart. 1GB RAM is tight for video processing. Good for demos only.

**Monthly cost: $0** but unusable for production.

---

### 2. Railway / Render (PaaS)

| | |
|---|---|
| **Cost** | ~$5-20/month (Railway Hobby), ~$7-25/month (Render) |
| **CPU/RAM** | 1-2 vCPU, 512MB-2GB RAM |
| **Storage** | Ephemeral by default; persistent volumes extra ($0.25/GB/month) |
| **ffmpeg** | Yes, via Dockerfile |
| **Custom domain** | Yes |
| **Auth** | DIY |

**Verdict: Possible for light use.** Need a Dockerfile with ffmpeg. Persistent volume needed for inputs/outputs. CPU limits will make video rendering slow.

**Monthly cost: ~$10-30** (compute + 10-50GB storage)

---

### 3. AWS EC2 / Lightsail

| | |
|---|---|
| **Cost** | Lightsail: $5-20/month; EC2: $15-80/month |
| **CPU/RAM** | Lightsail $10: 2 vCPU, 2GB. EC2 t3.medium: 2 vCPU, 4GB |
| **Storage** | Persistent EBS ($0.08/GB/month) |
| **ffmpeg** | Full control — install anything |
| **Custom domain** | Yes (Route 53 or external DNS) |
| **Auth** | DIY (or Cloudflare Access ~free) |

**Verdict: Best balance of control and cost.** Full ffmpeg support, persistent storage, enough CPU for video encoding.

#### Cost Estimate (Light)

| Component | Cost |
|---|---|
| Lightsail 2 vCPU / 2GB | $10/month |
| 50GB storage (included) | $0 |
| Snapshots/backups | ~$2/month |
| Domain + SSL (Let's Encrypt) | ~$1/month |
| **Total** | **~$13/month** |

#### Cost Estimate (Heavy Video Workloads)

| Component | Cost |
|---|---|
| EC2 c5.xlarge 4 vCPU / 8GB (on-demand) | ~$124/month |
| EC2 c5.xlarge (reserved 1yr) | ~$76/month |
| 100GB EBS gp3 | ~$8/month |
| **Total** | **~$84-132/month** |

---

### 4. DigitalOcean Droplet

| | |
|---|---|
| **Cost** | $6-24/month |
| **CPU/RAM** | $12: 1 vCPU, 2GB; $24: 2 vCPU, 4GB |
| **Storage** | 50-80GB SSD included |
| **ffmpeg** | Full control |
| **Custom domain** | Yes |
| **Auth** | DIY |

**Verdict: Strong option, simpler than AWS.** Good UI, predictable pricing, managed firewalls.

**Monthly cost: ~$12-24**

---

### 5. Google Cloud Run (Serverless Container)

| | |
|---|---|
| **Cost** | Pay-per-use: ~$0.00002400/vCPU-second |
| **CPU/RAM** | Up to 8 vCPU, 32GB (configurable) |
| **Storage** | Ephemeral; need Cloud Storage ($0.02/GB/month) for persistence |
| **ffmpeg** | Yes, via Dockerfile |
| **Custom domain** | Yes |
| **Auth** | IAP (Identity-Aware Proxy) free |

**Verdict: Cost-efficient for sporadic usage.** Scales to zero when idle. Streamlit's WebSocket connection doesn't map cleanly to serverless — sessions may drop. Video renders could hit timeout limits.

#### Cost Estimate (Light, ~2 hrs/day)

| Component | Cost |
|---|---|
| Cloud Run (2 vCPU, 4GB, ~60 hrs) | ~$5-10/month |
| Cloud Storage 50GB | ~$1/month |
| Networking/egress | ~$1-3/month |
| **Total** | **~$7-14/month** |

#### Cost Estimate (Heavy, 8+ hrs/day): ~$30-60/month

---

### 6. Hugging Face Spaces (Streamlit)

| | |
|---|---|
| **Cost** | Free (2 vCPU, 16GB); upgraded: $9/month (persistent storage) |
| **CPU/RAM** | Free: 2 vCPU, 16GB |
| **Storage** | Free: ephemeral; $9: persistent |
| **ffmpeg** | Available via `packages.txt` |
| **Custom domain** | No (free); Yes ($9+) |
| **Auth** | HF login (optional) |

**Verdict: Surprisingly viable for internal/demo use.** Generous free tier, native Streamlit support, ffmpeg available. Goes to sleep after inactivity.

**Monthly cost: $0-9**

---

## Recommended Production Architecture

```
                    ┌──────────────┐
                    │  Cloudflare  │  (CDN + SSL + Auth)
                    │  or Nginx    │  ~$0-5/month
                    └──────┬───────┘
                           │
                    ┌──────┴───────┐
                    │  Streamlit   │  (UI only)
                    │  App Server  │  2 vCPU, 4GB
                    └──────┬───────┘
                           │
              ┌────────────┼────────────┐
              │            │            │
     ┌────────┴──┐  ┌──────┴─────┐  ┌──┴──────────┐
     │ S3/GCS    │  │  Worker    │  │  Auth       │
     │ File      │  │  Queue     │  │  Layer      │
     │ Storage   │  │  (video    │  │  (SSO/      │
     │           │  │  renders)  │  │  password)  │
     └───────────┘  └────────────┘  └─────────────┘
```

### Backend Changes Required

1. **File upload/download** — Add `st.file_uploader()` and `st.download_button()` or integrate S3/GCS
2. **Per-user config** — Move from shared `config.json` to `st.session_state` or a database
3. **Background rendering** — Move video encoding to a task queue (Celery/RQ) so it doesn't block the UI
4. **Authentication** — Add `streamlit-authenticator` or put behind Cloudflare Access
5. **Storage cleanup** — Auto-purge old outputs or use lifecycle policies on cloud storage

---

## Recommendation Summary

| Scenario | Platform | Monthly Cost |
|---|---|---|
| **Quick demo / internal team eval** | HF Spaces or Streamlit Cloud | $0-9 |
| **Small team, occasional use** | DigitalOcean Droplet (2GB) | ~$12 |
| **Production, moderate use** | AWS Lightsail or DO Droplet (4GB) | ~$13-24 |
| **Production, heavy video** | AWS EC2 c5.xlarge (reserved) | ~$84 |
| **Variable/sporadic use** | Google Cloud Run + GCS | ~$7-60 |

### Starting Recommendation

A **$12-24/month DigitalOcean Droplet** or **AWS Lightsail** instance gives the best starting point:
- Full ffmpeg support
- Persistent storage included
- Enough CPU for video encoding
- Room to add auth/upload features incrementally
- Simple to set up and manage

Scale to Cloud Run or larger EC2 if usage grows.
