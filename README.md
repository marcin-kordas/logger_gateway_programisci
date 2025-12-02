# HR Analytics Dashboard - Logger Gateway Programiści

Streamlit-based HR Analytics Dashboard for candidate intelligence and recruitment analysis.

## Features

- **Leaderboard**: Rank candidates using customizable scoring scenarios (Startup vs Enterprise mode)
- **Comparative Analysis**: Visualize candidate skills with radar charts, skill matrices, and scatter plots
- **Candidate Deep Dive**: Detailed candidate profiles with gap analysis, interview strategies, and skill mapping

## Project Structure

```
logger_gateway_programisci/
├── app/
│   ├── app.py          # Main Streamlit application
│   └── images/         # Candidate profile images
├── data/
│   ├── candidates.json                      # Main candidate data
│   ├── candidate_intelligence_dossiers.json # Detailed dossiers
│   └── ...             # Other data files
├── docs/
│   ├── cvs/            # Candidate CVs
│   └── recruitment/    # Job postings and materials
└── archive/
    └── scripts/        # One-off processing scripts

```

## Setup

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the application:

```bash
cd app
python -m streamlit run app.py
```

3. Open your browser to `http://localhost:8501`

## Data

The application loads candidate data from `data/candidates.json`. Ensure this file exists and contains valid JSON data.

## Deployment

This application can be deployed to Streamlit Community Cloud. Make sure to:

- Push code to a GitHub repository
- Configure Streamlit Cloud to use the `app/app.py` as the entry point
- Ensure `data/` directory is included

## Requirements

- Python 3.8+
- Streamlit
- Pandas
- Matplotlib
- Seaborn
- NumPy
