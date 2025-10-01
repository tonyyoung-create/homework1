Interactive features (new)
--------------------------
 - Auto-update preview: a live preview plot in the sidebar updates automatically when you change parameters (a, b, noise, n_points, seed). This preview uses a smaller sample for speed and shows the true line and a fitted line.
- Auto-run full flow: an optional toggle in the sidebar that (when enabled) will automatically execute the full CRISP-DM flow whenever parameters change. The Run button still exists for manual control.

Streamlit main file path for deployment
--------------------------------------
When creating the app on Streamlit Cloud, set the main file path to:

- `hw1/lr_crispdm_streamlit/app.py`
If you prefer the repository root to contain the app directly (so the main file path can be `app.py`), see the README in the repo root for instructions to re-init and push from `lr_crispdm_streamlit` as the repository root.

# CRISP-DM Linear Regression Demo

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io)

A small Streamlit app that walks through the CRISP-DM process for a simple linear regression problem (y = a*x + b + noise).

Features:
- Interactive controls for true slope (a), intercept (b), noise level, number of points, and train/test split.
- Shows CRISP-DM steps, process log, model metrics, and visual comparison between true line and fitted line.
- Offers dataset and fitted model download.

How to run (Windows pwsh):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```

Reference projects:
- https://github.com/huanchen1107/20250920_AutoDeployLR
- https://aiotda.streamlit.app/

Deployment to Streamlit Cloud (recommended)
1. Create a GitHub repository and push this folder (`lr_crispdm_streamlit`) as the repository root (or the branch you want to deploy).
2. In Streamlit Cloud (https://share.streamlit.io), click 'New app', connect your GitHub, pick the repository and branch, and set the main file to `app.py`.
3. Add `requirements.txt` (already present) — Streamlit Cloud will install dependencies automatically.
4. Deploy. The UI should be accessible at `https://share.streamlit.io/<your-username>/<repo-name>/main` and can look similar to the reference `https://aiotda.streamlit.app/` with the same layout and theme.

Checklist before upload
- [x] `app.py` Streamlit app implemented and interactive
- [x] `requirements.txt` lists dependencies
- [x] small unit test in `tests/` to validate helper functions
- [x] `.streamlit/config.toml` for theme and server config
- [x] README updated with deployment steps

If you'd like, I can prepare a ready-to-push GitHub layout (top-level `README.md`, `.gitignore`) and add a one-click Streamlit Cloud badge. Tell me if you want that and which GitHub repo name to use.

Push to GitHub (example PowerShell commands)
1. Create a GitHub repository (e.g. `AutoDeployLR-modified`) and copy the repo URL (HTTPS).
2. From this folder (`lr_crispdm_streamlit`) run:

```powershell
git init
git add .
git commit -m "Initial CRISP-DM linear regression Streamlit app"
git branch -M main
git remote add origin https://github.com/<your-username>/AutoDeployLR-modified.git
git push -u origin main
```

3. In Streamlit Cloud (share.streamlit.io) create a new app, connect the GitHub repository, choose branch `main`, and set the main file path to `app.py` (or `lr_crispdm_streamlit/app.py` if you pushed the folder as a subfolder). Streamlit Cloud will install `requirements.txt` and deploy the app.

Prompt and helper script
- `PROMPT.txt`: contains the project prompt and requirements and will be included in the repo.
- `push_to_github.ps1`: a PowerShell script to automate git init/add/commit/push (it will prompt you for the remote URL).

To run the helper script (PowerShell):

```powershell
cd 'C:\Users\user\Desktop\物聯網\hw1\lr_crispdm_streamlit'
.\push_to_github.ps1
```

