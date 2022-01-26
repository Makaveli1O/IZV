#!/usr/bin/python3.8
# coding=utf-8
from logging import log
from contextily.plotting import ZOOM
import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import contextily as ctx
import sklearn.cluster
import numpy as np
# muzete pridat vlastni knihovny


def make_geo(df: pd.DataFrame) -> geopandas.GeoDataFrame:
    """Vytvorí geoDataframe zo vstupného dataframu. Nastaví správne
    coords systém a ostráni riadky u ktorých je pozícia nehody nezáma

    Args:
        df (pd.DataFrame): Vstupný dataframe

    Returns:
        geopandas.GeoDataFrame: Konfertovaný geoDataframe
    """
    # odstranit riadky kde je NaN v stlpcoch 'd' a 'e'
    df = df.dropna(subset=["d", "e"])
    # krovakovo zobrazeni
    gdf = geopandas.GeoDataFrame(df,
                                 geometry=geopandas.points_from_xy(df["d"],
                                                                   df["e"]),
                                 crs="EPSG:5514")
    return gdf


def plot_geo(gdf: geopandas.GeoDataFrame, fig_location: str = None,
             show_figure: bool = False):
    """Vykreslí graf obsahujúci 6 podgrafov ktoré znázorňujú
    pozície nehôd v Jihomoravském kraji. Vykreslený graf je posunutý
    aby sedel na jihomoravský kraj. V prípade iného kraja je možné že
    sa krajné nehody odrežú, pretože je celá osa posunutá o -10 000 y.
    P36:0 -> dalnice, p36:1 -> silnice 1. tridy
    Args:
        gdf (geopandas.GeoDataFrame): [Vstupný geoPandaDataframe]
        fig_location (str, optional): [Výstupný súbor]. Defaults to None.
        show_figure (bool, optional): [Vykreslenie grafu]. Defaults to False.
    """
    gdf = gdf.query('region == "JHM"').to_crs("epsg:3857")
    gdf = gdf[['p2a', 'p36', 'geometry']]
    gdf["p2a"] = pd.to_datetime(gdf["p2a"])
    fig, axes = plt.subplots(3, 2, figsize=(11.69, 11.27))
    years = [2018, 2019, 2020]
    axes = axes.flatten()
    for i in range(0, 5, 2):
        # filtrovat rok
        gdf_yearly = gdf[gdf.p2a.dt.year == years[0]]
        gdf_yearly[gdf_yearly["p36"] == 0].plot(ax=axes[i],
                                                markersize=2,
                                                color="#82E15E")
        # posun mapy mserom dole (nezmestil isa vsetky data)
        x1, y1, x2, y2 = gdf_yearly.total_bounds
        axes[i].set_ylim(y1-10000, y2)
        axes[i].set_xlim(x1, x2)
        axes[i].set_title("JHM kraj: diaľnica "+str(years[0]))
        # podkladná mapa
        ctx.add_basemap(axes[i], crs=gdf.crs,
                        source=ctx.providers.Stamen.TonerLite)
        # odstranit osi
        axes[i].xaxis.set_visible(False)
        axes[i].yaxis.set_visible(False)
        # grafy na pravo
        gdf_yearly[gdf_yearly["p36"] == 1].plot(ax=axes[i+1],
                                                markersize=2,
                                                color="#EC7438")
        x1, y1, x2, y2 = gdf_yearly.total_bounds
        axes[i+1].set_ylim(y1-10000, y2)
        axes[i+1].set_xlim(x1, x2)
        axes[i+1].set_title("JHM kraj: cesta 1. triedy "+str(years[0]))
        # podkladná mapa
        ctx.add_basemap(axes[i+1], crs=gdf.crs,
                        source=ctx.providers.Stamen.TonerLite)
        axes[i+1].xaxis.set_visible(False)
        axes[i+1].yaxis.set_visible(False)
        years.pop(0)
    plt.tight_layout()
    # vykreslenie a ulozenie
    if fig_location:
        plt.savefig(fig_location, bbox_inches='tight')
    if show_figure is True:
        plt.show()
    plt.close
    return


def plot_cluster(gdf: geopandas.GeoDataFrame, fig_location: str = None,
                 show_figure: bool = False):
    """Vykreslí všetky nehody vo vybranom kraji tak, že znázorní úseky s
    nehodami na cestách 1. triedy. Nehody v danom úseku sú zafarbené podľa
    počtu nehôd. Funkcia rodelí nehody do 15tich zhlukov pomocou algoritmu
    KMeans, ktorý sa používa pri všeobecných zhlukoch, plochej geometrií
    a tam kde sa nevyužíva veľké množstvo zhlukov.
    Args:
        gdf (geopandas.GeoDataFrame): [Vstupný geoPandaDataframe]
        fig_location (str, optional): [Výstupný súbor]. Defaults to None.
        show_figure (bool, optional): [Vykreslenie grafu]. Defaults to False.
    """
    # vybrat potrebne stlpce
    gdf = gdf.query('region == "JHM"')
    # cesta 1. triedy
    gdf = gdf.query("p36 == 1")
    # region pouzijem neskor na agregovanie
    gdf = gdf[["geometry", "region"]]
    coords = pd.DataFrame()
    # model
    coords['X'] = gdf.centroid.x
    coords['Y'] = gdf.centroid.y
    model = sklearn.cluster.MiniBatchKMeans(n_clusters=15)
    db = model.fit(coords)
    # priradenie bodov ku clusterom do dataframu
    gdf["cluster"] = db.labels_
    # spocitanie bodov v jednotlivych clusteroch
    gdf = gdf.dissolve(by="cluster", aggfunc={"region": "count"})
    # plot
    fx, ax = plt.subplots(figsize=(11.69, 8.27))
    gdf.plot(ax=ax, markersize=1, legend=True, column="region")
    ctx.add_basemap(ax, crs=gdf.crs, source=ctx.providers.Stamen.TonerLite)
    plt.legend(loc='upper center', ncol=7)
    # osi
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_title("Nehody v JHM kraji na cestách 1. triedy")
    plt.tight_layout()
    # vykreslenie a ulozenie
    if fig_location:
        plt.savefig(fig_location, bbox_inches='tight')
    if show_figure is True:
        plt.show()
    plt.close
    return


if __name__ == "__main__":
    # zde muzete delat libovolne modifikace
    gdf = make_geo(pd.read_pickle("accidents.pkl.gz"))
    # plot_geo(gdf, "geo1.png", True)
    plot_cluster(gdf, "geo2.png", True)
