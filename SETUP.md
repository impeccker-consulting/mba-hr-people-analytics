# Setup (one time, instructor only)

No folders need to be uploaded. Everything in this package is a plain file, and the week folders are created for you automatically.

1. Create a new **public** repository (name: `mba-hr-people-analytics`).
2. **Settings > Pages > Build and deployment > Source**: choose **GitHub Actions**.
3. **Add file > Upload files**: select all files from this package (not a folder) and drag them in. Commit.
4. **Add file > Create new file**. In the name box type exactly `.github/workflows/pages.yml` (typing the slashes creates the folders). Open `workflow-to-paste.yml` from this package, copy everything, paste it into the editor, and commit.
5. Open the **Actions** tab. When "Build and deploy site" shows a green tick, the week folders have appeared in the repo and your site is live at the address shown in Settings > Pages.

# Every week

1. Click into that week's folder on GitHub, then **Add file > Upload files**, drop in the new `.html` file, and commit. (Upload from inside the folder and the file lands in it.)
2. About a minute later the site updates itself.

Tips
- Give each simulation a clear `<title>` and a one-line `<meta name="description" content="...">`. They become the card's name and subtitle.
- Prefix file names with the session number (for example `s05-logistic-regression.html`) so they list in order.
- Anything outside the syllabus goes in the `extras` folder.
- Week titles and topic chips can be edited in `build_index.py` (the WEEKS list at the top).
