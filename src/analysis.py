"""
Fluktuace a stabilita zaměstnanců 55+ -- analýza
=================================================

Autor: Jana Dolečková
Zdroje dat:
  - U.S. Bureau of Labor Statistics (BLS), Employee Tenure Summary, leden 2024
    https://www.bls.gov/news.release/tenure.t01.htm
    https://www.bls.gov/news.release/tenure.t04.htm
    https://www.bls.gov/opub/ted/2024/median-tenure-with-current-employer-was-3-9-years-in-january-2024.htm
  - AIER, "New Careers for Older Workers" (2015)
    https://aier.org/wp-content/uploads/2015/09/newcareersolderworkers-aier.pdf

Pozn.: BLS data jsou za USA (nejpodrobnější veřejně dostupná data spojující
délku setrvání u zaměstnavatele s věkem A vzděláním zároveň). Český
kontext (ČSÚ VŠPS, MPSV) je uveden samostatně jako doplňkový rámec, protože
ČSÚ veřejně nezveřejňuje srovnatelný křížový rozpad věk x vzdělání x fluktuace
ve stažitelné podobě.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

DATA_DIR = "../data/bls"
OUT_DIR = "../visuals"

COLOR_PRIMARY = "#2C6E49"     # zelená - stabilita/55+
COLOR_SECONDARY = "#C9A227"   # zlatá - akcent
COLOR_MUTED = "#B0B0B0"       # šedá - mladší kohorty / kontext

plt.rcParams.update({
    "font.size": 11,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})


def load_data():
    tenure_age_sex = pd.read_csv(f"{DATA_DIR}/tenure_by_age_sex_2014_2024.csv")
    tenure_edu_age = pd.read_csv(f"{DATA_DIR}/tenure_by_education_age_2024.csv")
    tenure_dist = pd.read_csv(f"{DATA_DIR}/tenure_distribution_by_age_2024.csv")
    return tenure_age_sex, tenure_edu_age, tenure_dist


def chart_tenure_by_age_2024(tenure_age_sex):
    """Medián let u zaměstnavatele podle věku, 2024 (jádrový graf)."""
    df = tenure_age_sex[
        (tenure_age_sex["sex"] == "Total")
        & (tenure_age_sex["age_group"].isin(
            ["25 to 34", "35 to 44", "45 to 54", "55 to 64", "65 and over"]))
    ].copy()
    labels_cz = {
        "25 to 34": "25–34",
        "35 to 44": "35–44",
        "45 to 54": "45–54",
        "55 to 64": "55–64",
        "65 and over": "65+",
    }
    df["label"] = df["age_group"].map(labels_cz)

    colors = [COLOR_MUTED, COLOR_MUTED, COLOR_SECONDARY, COLOR_PRIMARY, COLOR_PRIMARY]

    fig, ax = plt.subplots(figsize=(8, 5))
    bars = ax.bar(df["label"], df["year_2024"], color=colors, width=0.6)
    for bar, val in zip(bars, df["year_2024"]):
        ax.annotate(f"{val:.1f}", (bar.get_x() + bar.get_width() / 2, val),
                    textcoords="offset points", xytext=(0, 5), ha="center",
                    fontsize=11, fontweight="bold")

    ax.set_title("Medián let u současného zaměstnavatele podle věku (USA, leden 2024)",
                  fontsize=13, fontweight="bold", pad=15)
    ax.set_ylabel("Medián let u zaměstnavatele")
    ax.set_xlabel("Věková skupina")
    ax.set_ylim(0, 11)
    ax.text(0.5, -0.22,
            "Pracovníci 55+ setrvávají u zaměstnavatele více než 3x déle než pracovníci 25–34 let.\n"
            "Zdroj: U.S. Bureau of Labor Statistics, Employee Tenure Summary, leden 2024",
            transform=ax.transAxes, ha="center", fontsize=8.5, color="dimgray")
    fig.tight_layout()
    fig.savefig(f"{OUT_DIR}/01_median_tenure_by_age.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


def chart_tenure_trend(tenure_age_sex):
    """Vývoj mediánu let u zaměstnavatele 2014-2024 pro vybrané věkové skupiny."""
    df = tenure_age_sex[
        (tenure_age_sex["sex"] == "Total")
        & (tenure_age_sex["age_group"].isin(["25 to 34", "45 to 54", "55 to 64"]))
    ].copy()
    labels_cz = {"25 to 34": "25–34 let", "45 to 54": "45–54 let", "55 to 64": "55–64 let"}
    years = [2014, 2016, 2018, 2020, 2022, 2024]
    year_cols = [f"year_{y}" for y in years]

    fig, ax = plt.subplots(figsize=(8, 5))
    colors = {"25 to 34": COLOR_MUTED, "45 to 54": COLOR_SECONDARY, "55 to 64": COLOR_PRIMARY}
    for _, row in df.iterrows():
        ax.plot(years, row[year_cols].values, marker="o", linewidth=2.5,
                label=labels_cz[row["age_group"]], color=colors[row["age_group"]])

    ax.set_title("Fluktuace v čase: mladší pracovníci mění zaměstnavatele stále rychleji,\nstarší zůstávají stabilní (2014–2024)",
                  fontsize=12.5, fontweight="bold", pad=15)
    ax.set_ylabel("Medián let u zaměstnavatele")
    ax.set_xlabel("Rok")
    ax.legend(frameon=False, loc="center left", bbox_to_anchor=(1.0, 0.5))
    ax.text(0.5, -0.22,
            "Zdroj: U.S. Bureau of Labor Statistics, Employee Tenure Summary, 2014–2024",
            transform=ax.transAxes, ha="center", fontsize=8.5, color="dimgray")
    fig.tight_layout()
    fig.savefig(f"{OUT_DIR}/02_tenure_trend_2014_2024.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


def chart_tenure_by_education(tenure_edu_age):
    """Medián let u zaměstnavatele: vysokoškoláci (Bc./Mgr.) podle věku."""
    df = tenure_edu_age[
        (tenure_edu_age["sex"] == "All")
        & (tenure_edu_age["education"].isin(
            ["High school graduate no college", "Bachelor's degree only", "Master's degree"]))
    ].copy()
    age_cols = ["age_25_34", "age_35_44", "age_45_54", "age_55_64"]
    age_labels = ["25–34", "35–44", "45–54", "55–64"]
    edu_labels = {
        "High school graduate no college": "Střední škola (bez VŠ)",
        "Bachelor's degree only": "Bakalářský titul",
        "Master's degree": "Magisterský titul",
    }
    edu_colors = {
        "High school graduate no college": COLOR_MUTED,
        "Bachelor's degree only": COLOR_SECONDARY,
        "Master's degree": COLOR_PRIMARY,
    }

    x = range(len(age_labels))
    width = 0.25
    fig, ax = plt.subplots(figsize=(9, 5.5))
    for i, (_, row) in enumerate(df.iterrows()):
        offsets = [xi + (i - 1) * width for xi in x]
        ax.bar(offsets, row[age_cols].values, width=width,
               label=edu_labels[row["education"]], color=edu_colors[row["education"]])

    ax.set_xticks(list(x))
    ax.set_xticklabels(age_labels)
    ax.set_title("Vysokoškolsky vzdělaní pracovníci 45+ setrvávají u zaměstnavatele\nvýrazně déle než mladší kolegové (USA, 2024)",
                  fontsize=12.5, fontweight="bold", pad=15)
    ax.set_ylabel("Medián let u zaměstnavatele")
    ax.set_xlabel("Věková skupina")
    ax.legend(frameon=False)
    ax.text(0.5, -0.24,
            "Zdroj: U.S. Bureau of Labor Statistics, Employee Tenure Summary, Table 4, leden 2024",
            transform=ax.transAxes, ha="center", fontsize=8.5, color="dimgray")
    fig.tight_layout()
    fig.savefig(f"{OUT_DIR}/03_tenure_by_education_age.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


def chart_short_tenure_share(tenure_dist):
    """Podíl pracovníků s krátkou dobou (<=1 rok) u zaměstnavatele podle věku."""
    df = tenure_dist[tenure_dist["age_group"] != "Total"].copy()
    labels_cz = {
        "16 to 19": "16–19", "20 to 24": "20–24", "25 to 34": "25–34",
        "35 to 44": "35–44", "45 to 54": "45–54", "55 to 64": "55–64",
        "65 and over": "65+",
    }
    df["label"] = df["age_group"].map(labels_cz)
    colors = [COLOR_MUTED] * 4 + [COLOR_SECONDARY, COLOR_PRIMARY, COLOR_PRIMARY]

    fig, ax = plt.subplots(figsize=(8.5, 5))
    bars = ax.bar(df["label"], df["pct_12m_or_less"], color=colors, width=0.6)
    for bar, val in zip(bars, df["pct_12m_or_less"]):
        ax.annotate(f"{val:.0f}%", (bar.get_x() + bar.get_width() / 2, val),
                    textcoords="offset points", xytext=(0, 5), ha="center",
                    fontsize=10, fontweight="bold")

    ax.set_title("Podíl pracovníků s max. 1 rokem u současného zaměstnavatele\n(nejčerstvější příchozí / největší fluktuace)",
                  fontsize=12.5, fontweight="bold", pad=15)
    ax.set_ylabel("% pracovníků dané věkové skupiny")
    ax.set_xlabel("Věková skupina")
    ax.yaxis.set_major_formatter(mticker.PercentFormatter())
    ax.text(0.5, -0.24,
            "Zdroj: BLS, Economics Daily, leden 2024 (podíl s tenure <= 12 měsíců)",
            transform=ax.transAxes, ha="center", fontsize=8.5, color="dimgray")
    fig.tight_layout()
    fig.savefig(f"{OUT_DIR}/04_short_tenure_share_by_age.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


def chart_long_tenure_share(tenure_dist):
    """Podíl pracovníků s dlouhou dobou (10+ let) u zaměstnavatele podle věku."""
    df = tenure_dist[tenure_dist["age_group"] != "Total"].copy()
    df["pct_10y_plus"] = df["pct_10_14y"] + df["pct_15_19y"] + df["pct_20y_plus"]
    labels_cz = {
        "16 to 19": "16–19", "20 to 24": "20–24", "25 to 34": "25–34",
        "35 to 44": "35–44", "45 to 54": "45–54", "55 to 64": "55–64",
        "65 and over": "65+",
    }
    df["label"] = df["age_group"].map(labels_cz)
    colors = [COLOR_MUTED] * 4 + [COLOR_SECONDARY, COLOR_PRIMARY, COLOR_PRIMARY]

    fig, ax = plt.subplots(figsize=(8.5, 5))
    bars = ax.bar(df["label"], df["pct_10y_plus"], color=colors, width=0.6)
    for bar, val in zip(bars, df["pct_10y_plus"]):
        ax.annotate(f"{val:.0f}%", (bar.get_x() + bar.get_width() / 2, val),
                    textcoords="offset points", xytext=(0, 5), ha="center",
                    fontsize=10, fontweight="bold")

    ax.set_title("Podíl pracovníků s 10+ lety u současného zaměstnavatele\n(dlouhodobá stabilita)",
                  fontsize=12.5, fontweight="bold", pad=15)
    ax.set_ylabel("% pracovníků dané věkové skupiny")
    ax.set_xlabel("Věková skupina")
    ax.yaxis.set_major_formatter(mticker.PercentFormatter())
    ax.text(0.5, -0.24,
            "Zdroj: BLS, Economics Daily, leden 2024 (součet podílů 10-14, 15-19 a 20+ let)",
            transform=ax.transAxes, ha="center", fontsize=8.5, color="dimgray")
    fig.tight_layout()
    fig.savefig(f"{OUT_DIR}/05_long_tenure_share_by_age.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


def chart_career_change_success():
    """Ilustrace AIER zjištění o úspěšnosti změny kariéry po 45."""
    labels = ["Úspěšná změna\nkariéry po 45", "Neúspěšná / bez\nzjevného úspěchu"]
    values = [82, 18]
    colors = [COLOR_PRIMARY, COLOR_MUTED]

    fig, ax = plt.subplots(figsize=(5.5, 5.5))
    wedges, _, autotexts = ax.pie(
        values, labels=None, colors=colors, autopct="%1.0f%%",
        startangle=90, wedgeprops={"edgecolor": "white", "linewidth": 2},
        textprops={"fontsize": 14, "fontweight": "bold", "color": "white"},
    )
    ax.legend(wedges, labels, loc="center left", bbox_to_anchor=(1.0, 0.5), frameon=False)
    ax.set_title("Změna kariéry po 45. roce věku je\nve většině případů úspěšná",
                  fontsize=13, fontweight="bold", pad=15)
    fig.text(0.5, 0.01,
              "Zdroj: AIER, \"New Careers for Older Workers\" (2015), n = průzkum mezi respondenty 45+,\n"
              "kteří se rozhodli pro změnu kariéry",
              ha="center", fontsize=8.5, color="dimgray")
    fig.tight_layout(rect=[0, 0.06, 1, 1])
    fig.savefig(f"{OUT_DIR}/06_career_change_success_aier.png", dpi=160, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    tenure_age_sex, tenure_edu_age, tenure_dist = load_data()
    chart_tenure_by_age_2024(tenure_age_sex)
    chart_tenure_trend(tenure_age_sex)
    chart_tenure_by_education(tenure_edu_age)
    chart_short_tenure_share(tenure_dist)
    chart_long_tenure_share(tenure_dist)
    chart_career_change_success()
    print("Hotovo -- grafy uloženy do", OUT_DIR)
