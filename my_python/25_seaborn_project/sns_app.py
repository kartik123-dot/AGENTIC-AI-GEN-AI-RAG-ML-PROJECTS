import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid")

tips = sns.load_dataset("tips")

st.title("MR.Kartik Soni Seaborn Project")
st.write("This is a Streamlit app that demonstrates various Seaborn plots using the tips dataset.")

# function created to display the plots
def display_plot(title, plot_func):
    st.subheader(title)
    fig, ax = plt.subplots(figsize=(8, 6))
    plot_func(ax=ax)
    st.pyplot(fig)
    plt.close(fig)


# Plot
def scatter_plot(ax):
    sns.scatterplot(x="total_bill", y="tip", data=tips, hue="sex", style="time", size="size", sizes=(20, 200), palette="deep", alpha=0.7, edgecolor="black", legend="full")
    ax.set_title("Scatter Plot of Total Bill vs Tip")

def line_plot(ax):
    sns.lineplot(x="total_bill", y="tip", data=tips, hue="sex", style="time", markers=True, dashes=False, palette="deep", alpha=0.7, legend="full", ci=None, err_style="bars")
    ax.set_title("Line Plot of Total Bill vs Size")

def bar_plot(ax):
    sns.barplot(x="day", y="total_bill", data=tips, hue="sex", palette="muted", alpha=0.7, ci=None, errcolor="black", errwidth=1.5, capsize=0.1, dodge=True)
    ax.set_title("Bar Plot of Total Bill by Day and Sex")

def box_plot(ax):
    sns.boxplot(x="day", y="tip", data=tips, hue="sex", palette="pastel",  fliersize=5, linewidth=1.5, notch=False, dodge=True)
    ax.set_title("Boxplot of tip by Day and Smoker Status")

def violin_plot(ax):
    sns.violinplot(x="day", y="total_bill", data=tips, hue="time", palette="muted", split=True, inner="quartile", scale="count", width=0.8, bw=0.2, cut=0, scale_hue=True, dodge=True)
    ax.set_title("Violin Plot of Total Bill by Day and Time")

def count_plot(ax):
    sns.countplot(x="day", data=tips, hue="smoker", palette="pastel", alpha=0.7, edgecolor="black", linewidth=1.5, dodge=True, order=["Thur", "Fri", "Sat", "Sun"])
    ax.set_title("Count Plot of Days by Smoker Status")

def reg_plot(ax):
    sns.regplot(x="total_bill", y="tip", data=tips, color="blue", marker="o", scatter_kws={"s": 50, "alpha": 0.7}, line_kws={"color": "red", "linewidth": 2}, ci=None, truncate=True, x_jitter=0.1, y_jitter=0.1,  logistic=False)
    ax.set_title("Regression Plot of Total Bill vs Tip")

def hist_plot(ax):
    sns.histplot(data=tips, x="total_bill", bins=20, kde=True, color="blue", alpha=0.7, edgecolor="black", linewidth=1.5, stat="density", multiple="layer", element="bars", fill=True, discrete=False, common_norm=True, cumulative=False, log_scale=False, legend=True)
    ax.set_title("Histogram of Total Bill with KDE")

def pair_plot(ax):
    sns.pairplot(tips, hue="sex", vars=["total_bill", "tip", "size"], kind="scatter", palette="husl", diag_kind="kde", markers=["o", "s"], height=2.5, aspect=1, dropna=True, plot_kws={"alpha": 0.7, "s": 50, "edgecolor": "black"}, diag_kws={"shade": True, "linewidth": 1.5}, corner=False)
    ax.set_title("Pair Plot: Numeric Variables by Gender")

def cat_plot(ax):
    sns.catplot(data=tips, x='day', y='tip', hue='sex', kind='point', palette='bright', height=6, aspect=1.5, ci=None, dodge=True, markers=["o", "s"], linestyles=["-", "--"], legend=True)
    ax.set_title("catplot(point):Tips by day and gender")

def strip_plot(ax):
    sns.stripplot(data=tips, x='day', y='tip', hue='sex', jitter=True, palette='Set1', size=8, alpha=0.7, edgecolor='black', linewidth=1.5, dodge=True, marker='o')
    ax.set_title("strip plot: Tips by day and gender")

def kde_plot(ax):
    sns.kdeplot(data=tips, x='total_bill',hue='sex', fill=True, palette='tab10', alpha=0.7, linewidth=1.5, bw_adjust=0.5, cut=0, common_norm=True, multiple='layer', legend=True, cumulative=False, log_scale=False, clip=None, warn_singular=True)
    ax.set_title("kde plot:Total bill density by gender")


display_plot("Scatter Plot", scatter_plot)
display_plot("Line Plot", line_plot)
display_plot("Bar Plot", bar_plot)
display_plot("Box Plot", box_plot)
display_plot("Violin Plot", violin_plot)
display_plot("Count Plot", count_plot)
display_plot("Regression Plot", reg_plot)
display_plot("Histogram Plot", hist_plot)
display_plot("Strip Plot", strip_plot)
display_plot("KDE Plot", kde_plot)

