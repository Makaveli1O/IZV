import numpy as np
import pandas as pd
import scipy.stats as st
import matplotlib.pyplot as plt
import seaborn as sns
from seaborn import palettes


def plot_specific_situations():
    """Vykreslí graf, ktorý zobrazuje počeť nehôd sposobených
    v okolí nejakého špecifického miesta alebo objektu
    """
    causes = ["Prechod",
              "Do 20m od prechodu",
              "Nezabezpečený ŽP",
              "Zabezpečený ŽP",
              "Most/Nadjezd/Podjezd/Tunel",
              "Zastávka",  # p27 6 a 7 berieme ako jeden
              "Výjezd",  # p36 == 7,8
              "Čerpadlo pohonných hmot",
              "Parkovište"]
    df = pd.read_pickle("accidents.pkl.gz")
    # výber vhodnej časti dataframu
    dfs = df.copy()
    dfs = dfs.query("p27 != 0")
    # nahradiť čísla labelmi
    dfs['p27'] = pd.cut(dfs.p27, right=False, include_lowest=True,
                        ordered=True,  bins=[1, 2, 3, 4, 5, 6,
                                             8, 9, 10, float("inf")],
                        labels=[causes[0], causes[1], causes[2], causes[3],
                                causes[4], causes[5], causes[6], causes[7],
                                causes[8]])
    # plot
    fig, axis = plt.subplots()
    sns.countplot(palette="Blues", data=dfs, x="p27", hue="p27",
                          dodge=False)
    # osi
    axis.set_title("Špecifické miesta a objekty v mieste nehody")
    axis.set_ylabel("Počet")
    axis.set_xlabel("Počet nehod")
    axis.xaxis.set_visible(False)
    axis.yaxis.grid(True)
    # legenda
    plt.legend(title="Miesto / Objekt")
    plt.tight_layout()
    plt.savefig("doc1.png", bbox_inches='tight')
    plt.show()


def specific_causes_statistic():
    """Vykreslí koláčový graf, ktorý zobrazuje pomer
    nehôd sposobených pri špecifických voči všetkým zaznamenaným
    nehodám za posledné roky.
    """
    df = pd.read_pickle("accidents.pkl.gz")
    overall_causes = len(df["p27"].tolist())
    special_causes = len(df['p27'].where(df['p27'] != 0).dropna().tolist())
    print("Celkový počet nehôd: " + str(overall_causes))
    print("Počet nehôd v okolí špecifického miesta alebo situácie: "
          + str(special_causes))
    value = special_causes / overall_causes
    # Percento nehôd spôsobené v okolí špecifických miest a objektov
    percentage = "{:.0%}".format(value)
    print(percentage+" nehôd bolo sposobené pri špecifickej situácií")  
    y = np.array([overall_causes - special_causes, special_causes])
    labels = ["Iné situácie", "Pri špecifických miestach"]
    colors = ['#ccd5e6', '#668dc2']
    # odtrhnúť druhú časť
    explode = (0, 0.1)
    # plot
    plt.pie(y, labels=labels, colors=colors, autopct='%.2f%%',
            shadow=True, labeldistance=None, explode=explode)
    plt.xlabel("")
    plt.legend()
    plt.tight_layout()
    plt.savefig("doc2.png", bbox_inches='tight')
    plt.show()


def pedestrians():
    """Počíta pomer nehôd idúcich vozidiel v obci a mimo obce
    """
    df = pd.read_pickle("accidents.pkl.gz")
    # počet nehôd v obci
    dft = df.copy().query("p5a == 1")
    dft_count = len(dft["p5a"].tolist())
    # počet nehôd mimo obec
    dfo = df.copy().query("p5a == 2")
    dfo_count = len(dfo["p5a"].tolist())

    causes = ["čelná", "bočná", "z boku", "zozadu"]
    places = ["v obci", "mimo obec"]
    # potrebná časť dataframu
    df = df[["p7", "p5a"]]
    # iba druh zrážky jedoucích vozidel
    df = df.query("p7 != 0")
    # pomocný sloupec 
    df['počet'] = df["p7"].astype("str")
    df = df.groupby(["p7", "p5a"], as_index=False).agg('count')
    # nahradiť čísla za labely
    df['p7'] = pd.cut(df.p7, right=False, include_lowest=True,
                       ordered=True,  bins=[1, 2, 3, 4, float("inf")],
                       labels=[causes[0], causes[1], causes[2], causes[3]])
    df['p5a'] = pd.cut(df.p5a, right=False, include_lowest=True,
                       ordered=True,  bins=[1, 2, float("inf")],
                       labels=[places[0], places[1]])
    # výpis
    print("Celkový počet nehôd v obci : " + str(dfo_count))
    print("Celkový počet nehôd mimo obec : " + str(dft_count))
    print(df)
    # výpočet
    town_counts = df["počet"][::2].tolist()
    outside_percentages = [percentage(item, dfo_count) for item in df["počet"] if item not in town_counts]
    town_percentages = [percentage(item, dft_count) for item in town_counts]
    print("Percentuálny pomer nehôd mimo obce: " + str(outside_percentages))
    print("Percentuálny pomer v obci: " + str(town_percentages))


def percentage(num, ovrl):
    return round(num / ovrl * 100, 2)


if __name__ == "__main__":
    # plot_specific_situations()
    # specific_causes_statistic()
    # pedestrians()
