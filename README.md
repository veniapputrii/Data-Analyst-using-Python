# SETUP ENVIRONMENT
conda create --name mynv python=3.8
conda activate mynv
pip install pandas matplotlib altair streamlit babel

# RUN STREAMLIT
streamlit run dashboard.py