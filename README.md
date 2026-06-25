# ML Hub

A production-ready Flask app that hosts multiple machine-learning projects behind one modern dashboard. The architecture is **plugin-based**: adding a project means dropping a folder into `Project/projects/` — no edits to the core app.

Six models ship pre-trained and ready to run:

| Project | Category | Type | Algorithm |
|---|---|---|---|
| Fracture & Bone Health Analysis | Healthcare | Tabular | Decision Tree |
| Stroke Risk Prediction | Healthcare | Tabular | Logistic Regression |
| Potato Leaf Disease Detection | Agriculture | Image | CNN (TensorFlow/Keras) |
| Sentiment Analysis | NLP | Tabular (text) | TF-IDF + Naive Bayes |
| Motor Predictive Maintenance | Industrial | Tabular | K-Means + Random Forest |
| Weather Forecast | Environment | Tabular | Random Forest |

## Run locally

```bash
pip install -r requirements.txt
cd Project
python app.py
# open http://localhost:5000
```

The app works out of the box — all models are included.

## Structure

```
<repo root>/
├── requirements.txt            # dependencies (installed from the root)
├── runtime.txt                 # Python version for Render
├── Render Deploy Guide.txt     # deployment steps
└── Project/                    # the Flask app
    ├── app.py                  # factory + home / model-summary / health routes
    ├── core/                   # the framework every project plugs into
    │   ├── spec.py             #   ProjectSpec / Field / PredictionResult
    │   ├── registry.py         #   auto-discovers project plugins
    │   ├── views.py            #   shared GET/POST prediction page
    │   └── utils.py            #   logging, uploads, input validation
    ├── projects/               # one self-contained folder per ML project
    │   └── <project>/
    │       ├── __init__.py     #   PROJECT (ProjectSpec) + bp (Blueprint)
    │       ├── predictor.py    #   load() + predict() functions
    │       ├── notebook.ipynb  #   original training notebook (reference)
    │       ├── model/          #   saved model(s) + metrics.json
    │       └── data/           #   dataset
    ├── templates/              # base, home, shared project_predict, model_summary, errors
    ├── static/                 # css, js (dark mode + search + filtering), sample images
    └── How to add a new ml model.txt
```

## How it works

On startup the registry scans `Project/projects/` and registers every folder that exposes a `PROJECT` (a `ProjectSpec`) and a `bp` (a Blueprint). The homepage cards, routing, forms, validation and result rendering are all driven from that single `ProjectSpec`. Both tabular and image projects use the same shared prediction page; the only difference is whether a field has `type="file"`.

## Adding a new project

Create one folder under `Project/projects/` and restart — it is discovered automatically. See **`Project/How to add a new ml model.txt`** for the full walkthrough with copy-paste skeletons.

## Deploying

See **`Render Deploy Guide.txt`** — build/start commands and the one environment variable (`SECRET_KEY`) you need.

## Disclaimer

The healthcare models (fracture, stroke) are screening / educational aids built on public datasets and are **not** medical devices or a substitute for professional diagnosis.
