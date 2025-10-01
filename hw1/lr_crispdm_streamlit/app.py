import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from model import generate_data, fit_linear_regression
from io import BytesIO
import pickle

st.set_page_config(page_title="CRISP-DM Linear Regression Demo", layout="wide")

# Sidebar: CRISP-DM nav + controls
st.sidebar.title("Controls & Presets")
st.sidebar.markdown("Use presets to quickly load example data or set custom parameters below.")

preset = st.sidebar.selectbox("Preset examples", options=["Custom", "Easy (a=2,b=1)", "Steep (a=5,b=0)", "Noisy (noise=3)"])

# default params
default_params = dict(a=2.0, b=1.0, noise=1.0, n_points=100, seed=42)
if preset == "Easy (a=2,b=1)":
    default_params.update(a=2.0, b=1.0, noise=0.8, n_points=120)
elif preset == "Steep (a=5,b=0)":
    default_params.update(a=5.0, b=0.0, noise=0.5, n_points=80)
elif preset == "Noisy (noise=3)":
    default_params.update(a=1.0, b=0.0, noise=3.0, n_points=200)

st.sidebar.subheader("Data generation")
a = st.sidebar.number_input("True slope (a)", value=float(default_params['a']), step=0.1, format="%.3f")
b = st.sidebar.number_input("True intercept (b)", value=float(default_params['b']), step=0.1, format="%.3f")
noise = st.sidebar.slider("Noise standard deviation", 0.0, 10.0, float(default_params['noise']), 0.1)
n_points = st.sidebar.slider("Number of points", 5, 5000, int(default_params['n_points']), 1)
seed = st.sidebar.number_input("Random seed", value=int(default_params['seed']), step=1)

st.sidebar.subheader("Modeling")
test_ratio = st.sidebar.slider("Test set ratio", 0.0, 0.9, 0.2, 0.05)
fit_intercept = st.sidebar.checkbox("Fit intercept", value=True)
run_button = st.sidebar.button("Run CRISP-DM flow")

st.title("CRISP-DM: Simple Linear Regression (ax + b)")

with st.expander("What is CRISP-DM?", expanded=False):
    st.markdown(
        "CRISP-DM is a standard process model for data mining projects.\n\n"
        "Phases: Business Understanding → Data Understanding → Data Preparation → Modeling → Evaluation → Deployment.\n\n"
        "This demo generates synthetic 1D data (y = a*x + b + noise), fits a linear model, and walks through each CRISP-DM step."
    )

st.markdown("---")

st.subheader("Project goal (editable prompt)")
default_prompt = "建立一個線性回歸模型，目標是從帶有雜訊的 1D 數據中估計係數 a 和 b，並展示 CRISP-DM 的每個步驟。"
user_prompt = st.text_area("Modeling prompt", value=default_prompt, height=80)

col_main, col_sidebar = st.columns([3, 1])

with col_main:
    if run_button:
        # Business Understanding
        st.markdown("### 1) Business Understanding")
        st.write(user_prompt)

        # Data Understanding & Preparation
        st.markdown("### 2) Data Understanding")
        X, y = generate_data(a=a, b=b, n=n_points, noise=noise, seed=int(seed))
        df = pd.DataFrame({"x": X.ravel(), "y": y.ravel()})
        st.dataframe(df.head(20))
        st.write(f"Generated {len(df)} samples (noise={noise})")

        split_idx = int(len(df) * (1 - test_ratio))
        X_train, X_test = X[:split_idx], X[split_idx:]
        y_train, y_test = y[:split_idx], y[split_idx:]

        # Modeling
        st.markdown("### 3-4) Data Preparation & Modeling")
        result = fit_linear_regression(X_train, y_train, X_test=X_test, y_test=y_test, fit_intercept=fit_intercept)
        st.write("Estimated parameters:")
        st.code(f"slope = {result['coef']:.6f}\nintercept = {result['intercept']:.6f}")
        st.write("Metrics:")
        cols = st.columns(3)
        cols[0].metric("Train MSE", f"{result['train_mse']:.6f}")
        cols[1].metric("Test MSE", f"{result['test_mse']:.6f}")
        cols[2].metric("Test R^2", f"{result['test_r2']:.6f}")

        # Evaluation
        st.markdown("### 5) Evaluation")
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.scatter(X.ravel(), y.ravel(), alpha=0.6, label='data')
        xs = np.linspace(X.min(), X.max(), 200)
        ax.plot(xs, a * xs + b, color='green', label='true line')
        ax.plot(xs, result['coef'] * xs + result['intercept'], color='red', linestyle='--', label='fitted line')
        ax.legend()
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        st.pyplot(fig)

        # Deployment
        st.markdown("### 6) Deployment")
        st.write("Download the dataset and the fitted model for deployment or later inspection.")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download dataset (CSV)", data=csv, file_name='lr_data.csv', mime='text/csv')

        model_obj = {'coef': float(result['coef']), 'intercept': float(result['intercept'])}
        buf = BytesIO()
        pickle.dump(model_obj, buf)
        buf.seek(0)
        st.download_button("Download fitted model (pickle)", data=buf, file_name='lr_model.pkl')

        # Process log
        with st.expander("Process log (過程)", expanded=True):
            st.write("1) Business goal clarified from prompt")
            st.write(f"2) Data generated: a={a}, b={b}, noise={noise}, n={n_points}")
            st.write(f"3) Train/test split: train={len(X_train)}, test={len(X_test)} (test_ratio={test_ratio})")
            st.write("4) Fitted linear regression (scikit-learn)")
            st.write(f"   - estimated slope={result['coef']:.6f}, intercept={result['intercept']:.6f}")
            st.write("5) Evaluated metrics (MSE, R^2)")
            st.write("6) Artifacts prepared for download (CSV, pickle)")

        st.success("CRISP-DM flow completed")
    else:
        st.info("Use the sidebar controls and click 'Run CRISP-DM flow' to start")

with col_sidebar:
    st.markdown("### Quick tips")
    st.write("- Use presets to explore different regimes")
    st.write("- Increase noise to see how estimates degrade")
    st.write("- Reduce number of points to see variance in estimates")

