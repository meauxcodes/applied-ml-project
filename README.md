# Project Site — Setup Notes

This is a plain HTML/CSS site (no build step required) with all tabs required by the
Module 1 Project Part 1 assignment already in place:

- `index.html` — Introduction
- `dataprep.html` — Data Prep / EDA
- `clustering.html` — Clustering
- `pca.html` — PCA
- `naivebayes.html` — Naive Bayes
- `dectrees.html` — Decision Trees
- `svms.html` — SVM
- `regression.html` — Regression
- `nn.html` — Neural Networks
- `conclusions.html` — Conclusions
- `about.html` — About Me (the one page allowed to be written in first person)

Every page shares `style.css` and the same navigation rail across the top, so the
site reads as one connected project rather than separate pages.

Content — the actual paragraphs, images, links, and figures — should be edited
directly in each `.html` file as the corresponding Module is completed. Each method
page (Clustering, PCA, Naive Bayes, etc.) already has the four required subsections
built in: Overview, Data, Code, Results.

## Deploying with GitHub Pages (free, recommended)

1. Create a new **public** GitHub repository (e.g. `applied-ml-project`).
2. Upload all files in this folder (`index.html`, the other `.html` files, and
   `style.css`) to the root of that repository.
3. In the repo, go to **Settings → Pages**.
4. Under "Build and deployment," set **Source** to `Deploy from a branch`, branch
   `main`, folder `/ (root)`. Save.
5. GitHub will give you a live URL, typically:
   `https://<your-username>.github.io/<repo-name>/`
6. That URL — pointing at `index.html` (the Introduction tab) — is what you submit
   in the .docx for each Project Part deliverable.

Any time you push new commits to the repo, the live site updates automatically
within a minute or two — so each Module, you just edit the relevant page(s), commit,
and push.

## What's still placeholder (dashed boxes)

Every dashed box on the site marks something that still needs real content —
these are intentional "TK" (to come) markers, not bugs. As each Module is
completed, replace the relevant dashed box with the real writeup, figure,
or links, and delete the box.

## Images

Images referenced by figures are not yet linked — each `<figure class="figure">`
currently shows a placeholder box. Once you have real images (plots, raw/clean data
screenshots, etc.), save them into an `/images` folder in the repo and replace the
placeholder `<div class="ph">...</div>` with `<img src="images/yourfile.png" alt="...">`.
