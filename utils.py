import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def rename_columns(df):
    columns = {
        "<b>Medication</b>": "Medication",
        "<b>Total %<sup>1</sup> (n) n=402</b>": "Total % (n) (n=402)",
        "<b>With Polypharmacy %<sup>2</sup> (n) n=344</b>": "With Polypharmacy % (n) (n=344)",
        "<b>Without Polypharmacy %<sup>2</sup> (n) n=58</b>": "Without Polypharmacy % (n) (n=58)",
        "<b>Pharmaceutical needs<sup>1</sup></b>": "Pharmaceutical needs",
        "<b>Types of DRP</b>": "Types of DRP",
        "<b>Total % (n) n=316</b>": "Total % (n) (n=316)",
        "<b>With Polypharmacy % (n) n=280</b>": "With Polypharmacy % (n) (n=280)",
        "<b>Without Polypharmacy % (n) n=36</b>": "Without Polypharmacy % (n) (n=36)",
        "<b>Intervention performed</b>": "Intervention performed",
        "<b>Total % (n) n=307</b>": "Total % (n) (n=307)",
        "<b>Therapeutic goal achieved % (n) n=202</b>": "Therapeutic goal achieved % (n) (n=202)",
        "<b>Therapeutic goal not achieved % (n) n=40</b>": "Therapeutic goal not achieved % (n) (n=40)",
    }
    
    df = df.rename(columns=columns)
    
    return df

def clean_data(df, col):
    base_name = col.split("%")[0].strip()
    df[col] = df[col].str.replace("-", "0 (0)")
    df[base_name] = df[col].str.split("(").str[1].str.replace(")", "")
    df[base_name] = pd.to_numeric(df[base_name])
    df = df.drop(col, axis=1)
    
    return df

def plot_medicines(df, output_path):
    df = df.sort_values("Total", ascending=False)
    plt.figure(figsize=(10, 8))
    plt.barh(df["Medication"], df["With Polypharmacy"], label="With Polypharmacy")
    plt.barh(df["Medication"], df["Without Polypharmacy"], left=df["With Polypharmacy"], label="Without Polypharmacy")
    plt.title("Medication Counts with and without Polypharmacy", fontsize=16)
    plt.xlabel("Count", fontsize=16)
    plt.ylabel("Medication", fontsize=16)
    plt.legend(fontsize=16)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    
def plot_drp(df, output_path):
    df = df.sort_values("Total", ascending=False)
    plt.figure(figsize=(10, 6))
    plt.barh(df["Types of DRP"], df["With Polypharmacy"], label="With Polypharmacy")
    plt.barh(df["Types of DRP"], df["Without Polypharmacy"], left=df["With Polypharmacy"], label="Without Polypharmacy")
    plt.title("Types of DRP with and without Polypharmacy", fontsize=16)
    plt.xlabel("Count", fontsize=16)
    plt.ylabel("Types of DRP", fontsize=16)
    plt.legend(fontsize=16)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    
def plot_interventions(df, output_path):
    achieved = df["Therapeutic goal achieved"]
    not_achieved = df["Therapeutic goal not achieved"]
    not_mentioned = df["Total"] - achieved - not_achieved
    plt.figure(figsize=(12, 7))
    plt.barh(df["Intervention performed"], achieved, label="Achieved")
    plt.barh(df["Intervention performed"], not_achieved, left=achieved, label="Not Achieved")
    plt.barh(df["Intervention performed"], not_mentioned, left=achieved + not_achieved, label="Not Mentioned")
    plt.title("Therapeutic Goals by Intervention", fontsize=16)
    plt.xlabel("Count", fontsize=16)
    plt.ylabel("Intervention Performed", fontsize=16)
    plt.legend(fontsize=16)
    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    
def plot_polypharmacy_heatmap(df, output_path):
    poly_cols = [col for col in df.columns if "Poly" in col]
    heatmap_data = df.set_index("Medical Condition")[poly_cols]
    heatmap_data = heatmap_data.replace("None", np.nan)
    heatmap_data = heatmap_data.apply(pd.to_numeric, errors="coerce").fillna(0)
    with_poly = heatmap_data[[c for c in heatmap_data.columns if "With " in c]]
    with_poly.columns = with_poly.columns.str.replace("With Poly ", "", regex=False)
    without_poly = heatmap_data[[c for c in heatmap_data.columns if "Without" in c]]
    without_poly.columns = without_poly.columns.str.replace("Without Poly ", "", regex=False)
    fig, axes = plt.subplots(1, 2, figsize=(16, 8), sharey=True)
    sns.heatmap(with_poly.astype(float), annot=True, fmt=".0f", cmap="coolwarm", ax=axes[0])
    axes[0].set_title("With Polypharmacy", fontsize=16)
    axes[0].set_ylabel("Medical Condition", fontsize=16)
    axes[0].set_xlabel("Outcome Category", fontsize=16)
    sns.heatmap(without_poly.astype(float), annot=True, fmt=".0f", cmap="coolwarm", ax=axes[1])
    axes[1].set_title("Without Polypharmacy", fontsize=16)
    axes[1].set_ylabel("", fontsize=16)
    axes[1].set_xlabel("Outcome Category", fontsize=16)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    
def plot_drp_causes_pie(df):
    plt.figure(figsize=(8, 8))
    wedges, texts, autotexts = plt.pie(df["Count (n)"], labels=df["Cause of DRP"], autopct="%1.1f%%", startangle=140, textprops={'fontsize': 16})
    plt.legend(wedges, df["Cause of DRP"], title="Causes", loc="center left", bbox_to_anchor=(1, 0, 0.5, 1), fontsize=16, title_fontsize=16)
    plt.title("Distribution of Drug-Related Problem Causes", fontsize=16)
    plt.tight_layout()
    plt.show()
    
def plot_conditions_pie(output_path):
    labels = ["Hypertension", "Diabetes", "Dyslipidemia", "Other"]
    sizes = [29.5, 22, 19.4, 100 - (29.5 + 22 + 19.4)]
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=140, textprops={'fontsize': 16})
    plt.title("Distribution of Patient Conditions", fontsize=16)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
