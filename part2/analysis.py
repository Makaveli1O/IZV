#!/usr/bin/env python3.9
# coding=utf-8
"""
Autor: Samuel Líška (xliska20)
Python: 3.9.7 64-bit
Dátum: 2.12.2021
"""
from matplotlib import pyplot as plt
import pandas as pd
from pandas.core.algorithms import value_counts
import seaborn as sns
import numpy as np
import datetime
import matplotlib.dates as mdates

from seaborn import palettes
from seaborn.utils import ci


def get_dataframe(filename: str, verbose: bool = False) -> pd.DataFrame:
    """Načíta lokálne uložený súbor so štatistikou nehôd, vytvorí v dataframe
    stĺpec date. Adekvátne upraví datové týpy jednotlivých stĺpcov. Pri zadaní
    verbose true vypíše rozdiely vo veľkosti pred a po spracovaní.

    Args:
        filename (str): meno súboru
        verbose (bool, optional): Výpis veľkostí. Defaults to False.

    Returns:
        [type]: dataframe
    """
    df = pd.read_pickle(filename)
    o_size = round(df.memory_usage(index=True, deep=True).sum()/1048576, 1)
    for i in df:
        # date
        if i == "p2a":
            # coerce = invalid parsing will be set to NaN
            df['date'] = pd.to_datetime(df[i], errors="coerce")
        elif i == 'p1' or i == 'region':
            continue
        # strings p10,p18 category coz in 2nd(3rd) graph it is required
        elif df[i].dtypes == 'object' or i == "p10" or i == "p18":
            df[i] = df[i].astype('category')
        # numbers
        else:
            df[i] = pd.to_numeric(df[i], downcast='signed', errors='coerce')
    new_size = round(df.memory_usage(index=True, deep=True).sum()/1048576, 1)
    if verbose:
        print("orig_size={} MB".format(o_size))
        print("new_size={} MB".format(new_size))

    return df

# Ukol 2: počty nehod v jednotlivých regionech podle druhu silnic


def plot_roadtype(df: pd.DataFrame, fig_location: str = None,
                  show_figure: bool = False):
    """Vytvorí graf počtu nehod v závislosti na jednotlivých regiónoch
    podľa druhu komunikácie. Vizualizuje 4 vybrané kraje. Na začiatku sa
    vytvorípomocný stĺpec count podľa ktorého sa použi group by a
    sčítali sa nehody. P21 s hodnotou 4 sa replacnu za 3jku pretože
    nerozlišujeme rozdielné druhy štvorpruhovej komunikácie.
    Následne sa vyberú pre jednotlivé grafy potrebné data pomocou query,
    a grafy sa upravia podľa zadania.

    Args:
        df (pd.DataFrame): [Spracovávaný dataframe]
        fig_location (str, optional): [Miesto uloženia grafu]. Defaults to None
        show_figure (bool, optional): [Zobraziť graf]. Defaults to False.
    """
    roads = {
        0: "Jiná komunikace",
        1: "Dvoupruhová komunikace",
        2: "Třípriuhová komunikace",
        3: "Čtyřpruhová komunukace",
        4: "Vícepruhová komunikace",
        5: "Rychlostní komunikace"
    }
    regions = ("JHM", "OLK", "ULK", "ZLK")
    # nerozlisovat ctyrpruhove komunikace
    df.p21 = df.p21.apply(lambda x: 3 if (x == 4) else x)

    # pomocny sloupec
    df["count"] = df["p21"].astype("str")
    # cast dataframu ktora je potrebna
    df = pd.concat([df[df["region"] == region] for region in regions],
                   sort=False)[['region', 'p21', "count"]]
    # výber na
    df = df.groupby(["region", "p21"], as_index=False).agg("count")
    # fig
    fig, axs = plt.subplots(2, 3, figsize=(11.69, 8.27),
                            constrained_layout=True, sharex=True)
    fig.suptitle("Druhy silnic")
    # iterovanie cez osi
    axs = axs.flatten()

    for i, road in enumerate(roads):
        # skip 4
        if road > 3:
            road = road + 1
        dfx = df.query("p21 == "+str(road))
        # plotnutie grafu
        sns.barplot(palette="Set1", data=dfx, ax=axs[i], x="region", y="count")
        # titulok
        axs[i].set_title(roads[i])
        # y popisky
        if i == 0 or i == 3:
            axs[i].set_ylabel("Počet nehod")
        else:
            axs[i].set_ylabel("")
        # x popisky
        if i == 0 or i == 1 or i == 2:
            axs[i].set_xlabel("")
        else:
            axs[i].set_xlabel("Kraj")
    if fig_location:
        plt.savefig(fig_location, bbox_inches='tight')
    if show_figure is True:
        plt.show()
    plt.close
    return


# Ukol3: zavinění zvěří
def plot_animals(df: pd.DataFrame, fig_location: str = None,
                 show_figure: bool = False):
    """Vytvorí graf poču nehod v jednotlivých reiónoch v závislosti na
    dôsledku vyhýbania sa zveri. 4 vybrané kraje sú znázornené na grafe.
    Rok 2021 nieje kompletný, takže sa skipuje. Najskôr sa p10 konvertujú
    z 1 a 2 -> "ridičem", 4-> "zveri" a ostatok ako "jiné". Následne sa
    cez dt accessor pristupuje k mesiacom. Graf je vykreslený pomocou
    seaborn metody catplot.

    Args:
        df (pd.DataFrame): [Spracovávaný dataframe]
        fig_location (str, optional): [Cesta uloženia]. Defaults to None.
        show_figure (bool, optional): [Zobraziť graf]. Defaults to False.
    """
    regions = ("JHM", "OLK", "ULK", "ZLK")
    # cast dataframu ktora je potrebna
    df = pd.concat([df[df["region"] == region] for region in regions],
                   sort=False)[['region', 'p58', "p10", "date"]]
    df = df.query('p58 == 5')
    df = df[['region', 'p10', 'date']]

    # nahradenie čísel p10 s ridicem,jine,zveri
    dfc = df.copy(deep=True)
    dfc['p10'] = pd.cut(dfc.p10, right=False, include_lowest=True,
                        ordered=False,  bins=[0, 1, 3, 4, 5, 7],
                        labels=['jiné', 'řidičem', 'jiné', 'zvěří', 'jiné'])

    # vyfiltrovať cez dt accessor rok 2021
    dfc = dfc[dfc.date.dt.year < 2021]
    # extrahovať mesiac
    dfc['date'] = dfc['date'].dt.month
    # pomocny sloupec
    dfc['count'] = dfc["p10"].astype("str")
    dfc = dfc.groupby(["region", "p10", "date"], as_index=False).agg('count')
    # tvorba grafu
    sns.set_theme()
    graph = sns.catplot(aspect=1.2, data=dfc, x="date", y="count", hue="p10",
                        kind="bar", col_wrap=2, col="region", ci=None,
                        sharex=False, sharey=False)

    # úprava grafu
    axes = graph.axes.flatten()
    for i, region in enumerate(regions):
        axes[i].set_title("Kraj: "+region)
        axes[i].set_ylabel("Počet nehod")
        axes[i].set_xlabel("Měsíc")
    graph.fig.set_size_inches(11.69, 8.27)
    # legenda
    graph.legend.set_title("Zavinění")
    # align
    graph.tight_layout()
    if fig_location:
        plt.savefig(fig_location, bbox_inches='tight')
    if show_figure is True:
        plt.show()
    plt.close()
    return


# Ukol 4: Povětrnostní podmínky
def plot_conditions(df: pd.DataFrame, fig_location: str = None,
                    show_figure: bool = False):
    """Počty nehod v jednotlivých regiónoch poda poveternostných podmienok.
    Pre 4 vybrané kraje sa vytvoria 4 grafy zobrazujúce obdobie od 1.1.2016 do
    1.1.2020. Rok 2021 je vyfiltrovaný kôli nedostatku dát. Najskôr sa
    vyfiltrujú záznamy ktoré neobsahujú p18==0. Následne sa pomocou
    funkcie pd.cut zmenia číselné reprezentácie na korešpondujúce textové.
    Následne sa tabuľka pootáča pomocou pivotu a dajú sa do stacked formátu.
    V tomto formáte sa pre každý región podvzorkujú denná záznamy na mesačné.
    Následne sa data uspariadajú naspäť a z upravených dát sa vytvorí graf,
    ktorý sa následne upravý do zmysluplnej podoby.

    Args:
        df (pd.DataFrame): [Spracovávaný dataframe]
        fig_location (str, optional): [Miesto uloženia]. Defaults to None.
        show_figure (bool, optional): [Zobraziť graf]. Defaults to False.
    """
    regions = ("JHM", "OLK", "ULK", "ZLK")
    # potrebna cast dataframu
    df = pd.concat([df[df["region"] == region] for region in regions],
                   sort=False)[['region', 'p18', "date"]]
    df = df.query('p18 != 0')
    # prevod p18 na textorú reprezentáciu
    dfc = df.copy(deep=True)
    dfc['p18'] = pd.cut(dfc.p18, right=True, include_lowest=False,
                        ordered=False,  bins=[0, 1, 2, 3, 4, 5, 6, 7],
                        labels=['neztížené',
                                'mlha',
                                'na počátku deště',
                                'déšť',
                                'sněžení',
                                'náledí',
                                'vítr'])
    # pomocny sloupec
    dfc['count'] = dfc["p18"].astype("str")
    # pivot
    dfc = pd.pivot_table(dfc, columns="p18", index=["region", "date"],
                         values="count", aggfunc="count")
    # podvzorkovanie na mesiace
    regions_monthly = {}
    for region in regions:
        # pristup k regionalnym dennym datam
        daily = dfc.loc[region]
        # konvertovat na mesacne statistiky a stacknut
        monthly = daily.resample("1M").sum().stack(level=['p18'])
        regions_monthly[region] = monthly
    dfc = pd.concat(regions_monthly)
    # vyfiltrovať rok 2021
    regions_filtered = {}
    for region in regions:
        filtered = dfc[region].loc[:'2020-12']
        regions_filtered[region] = filtered
    dfc = pd.concat(regions_filtered)
    # konvertovať na stlpce
    dfc = dfc.reset_index(name="count")
    dfc = dfc.rename(columns={"level_0": "region"})
    # vykreslenie grafu
    sns.set_theme()
    graph = sns.relplot(data=dfc, x="date", y="count", hue="p18", kind="line",
                        col="region", col_wrap=2)
    # úprava grafu
    axes = graph.axes.flatten()
    # nastavit locator na spravnu frekvenciu
    months = mdates.MonthLocator(interval=12)
    for i, region in enumerate(regions):
        axes[i].set_title("Kraj: "+region)
        axes[i].set_ylabel("Počet nehod")
        axes[i].set_xlabel("")
        axes[i].set_xlim([datetime.date(2016, 1, 1),
                          datetime.date(2020, 1, 1)])
        axes[i].xaxis.set_major_locator(months)
        axes[i].tick_params(labelbottom=True)
    graph.fig.set_size_inches(11.69, 8.27)
    # legenda
    graph.legend.set_title("Podmínky")
    # align
    graph.tight_layout()
    if fig_location:
        plt.savefig(fig_location, bbox_inches='tight')
    if show_figure is True:
        plt.show()
    plt.close()
    return


if __name__ == "__main__":
    # zde je ukazka pouziti, tuto cast muzete modifikovat podle libosti
    # skript nebude pri testovani pousten primo, ale budou volany konkreni ¨
    # funkce.
    df = get_dataframe("accidents.pkl.gz", True)
    plot_roadtype(df, fig_location="01_roadtype.png", show_figure=True)
    plot_animals(df, "02_animals.png", True)
    plot_conditions(df, "03_conditions.png", True)
