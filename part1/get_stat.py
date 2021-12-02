#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from matplotlib.colors import BoundaryNorm, LogNorm
import numpy as np
import matplotlib.pyplot as plt
import os
import argparse
import cProfile

# povolene jsou pouze zakladni knihovny (os, sys) a knihovny numpy,
# matplotlib a argparse

from download import DataDownloader


def plot_stat(data_source,
              fig_location=None,
              show_figure=False):
    """Načíta a vizualizuje počty nehod získané v DataDownloader.
    Vytvára 2 grafy:
        -Absolútny
        -Relatívny voči príčine
    Vizualizuje dva pohľady na počet nehod v jednotlivých krajoch
    podľa Miestnej úpravy v prednosti v jazde. Pri zadaní argumentov
    mierne upravuje chovanie. 
    Vytvorí sa matica (regiony x dôvod priestupku) v ktorej sa postupne
    inkrementujú hodnoty v závislosti na kraji. Táto matica reprezentuje
    výsledný výskyt nehôd v daných regiónoch

    Args:
        data_source (dictionary): Vyparsované data z DataDownloader
        fig_location (str, optional): Výstupný adresár. Defaults to None.
        show_figure (bool, optional): Zobraziť graf. Defaults to False.
    """
    # dovod pokuty
    violations = {
        0: "Žádná úprava",
        1: "Preřušovana žlutá",
        2: "Semafor mimo provoz",
        3: "Dopravní značky",
        4: "Přenosné dopravní značky",
        5: "Nevyznačená"
    }
    # ziskaj spracovavane regiony
    regions = set(data_source["region"])
    regions = list(regions)

    # 2d numpy pole, reprezentujuce vyslednu maticu
    result_data = np.full((len(violations), len(regions)), 0, dtype='int64')

    # extrahuj p24 data
    p24_data = data_source["p24"]
    # prechod cez regiony
    for i_region, region in enumerate(regions):
        selected_region_data = np.where(data_source["region"] == region)
        # podla indexu regionu vybrat p24 hodnotu
        for i in selected_region_data[0]:
            # find match of violation index, and found p24 number
            for violation in violations.keys():
                # increment correct tile in matrix
                if violation == p24_data[i]:
                    count = result_data[violation, i_region]
                    count = count + 1
                    result_data[violation, i_region] = count
    plt.figure(figsize=(11.69, 8.27))
    #konštukcia grafov
    construct_log_graph(result_data, violations, regions)
    construct_linear_graph(result_data, violations, regions)

    # ulozit logaritmicky graf
    if fig_location is not None:
        dir = os.path.dirname(fig_location)  # get location
        file = os.path.basename(fig_location)  # get specified name of file

        if os.path.isdir(dir):  # check if directory exists
            plt.savefig(os.path.join(dir, file), dpi=600)
        else:
            os.mkdir(dir)
            plt.savefig(os.path.join(dir, file), dpi=600)

    # zobrazit logaritmický graf
    if show_figure:
        plt.show()

    return


def construct_linear_graph(result_data, violations, regions):
    """Vytvorí graf počtu nehod v lineárnom merítku(v percentách).
    Súčet riadkov musí dať hodnotu 100.

    Args:
        result_data (ndarray): (regiony x dôvod pokuty) matica
        violations (dictionary): slovník priestupkov
        regions (list str): list spracovaných regiónov
    """
    # 0 - 1 interval z countu
    normalized = result_data / np.sum(result_data, axis=1)[:, None]
    # nastavit nulove hodnoty na Not a nuber, aby sa zobrazili biele
    normalized[normalized == 0] = np.NaN

    # plot
    plt.subplot(2, 1, 2)

    # nastavenie heatmapy
    plt.imshow(normalized * 100, cmap=plt.cm.plasma)

    # nastavenie oboch osi
    plt.gca().set_yticks(np.arange(len(violations)))
    plt.gca().set_xticks(np.arange(len(regions)))
    plt.gca().tick_params(labelbottom=True, labeltop=False)
    # nastavenie labelov
    plt.gca().set_yticklabels(violations.values())
    plt.gca().set_xticklabels(regions)
    plt.colorbar()
    plt.title('Relativně vůči příčině')


def construct_log_graph(result_data, violations, regions):
    """Vytvorí graf reprezentujúci maticu absolútneho počtu
    nehôd v logaritmickom merítku.

    Args:
        result_data (ndarray): (regiony x dôvod pokuty) matica
        violations (dictionary): slovník priestupkov
        regions (list str): list spracovaných regiónov
    """
    plt.subplot(2, 1, 1)
    plt.imshow(
        result_data,
        cmap=plt.cm.viridis,
        norm=LogNorm(
            vmin=10**0,
            vmax=10**5))
    # set ticks
    plt.gca().set_yticks(np.arange(len(violations)))
    plt.gca().set_xticks(np.arange(len(regions)))
    plt.gca().tick_params(labelbottom=True, labeltop=False)
    # set tick labels
    plt.gca().set_yticklabels(violations.values())
    plt.gca().set_xticklabels(regions)
    # title
    plt.title('Absolutně')
    plt.colorbar()


if __name__ == "__main__":
    # ak nieje importovaný ako modul
    show_figure = False
    fig_location = None
    # parsovanie
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--fig_location',
        required=False,
        nargs=1,
        help="Absolútna cesta k výslednému grafu.")
    parser.add_argument(
        '--show_figure',
        required=False,
        action='store_true',
        help="Zobraziť výsledný graf. Pri zadaní --show_figure ")

    args = parser.parse_args()

    # priradenie argumentov
    if args.fig_location is not None:
        fig_location = args.fig_location[0]
    else:
        fig_location = None

    if args.show_figure:
        show_figure = True

    downloader = DataDownloader()

    # ziskanie dát
    dict = downloader.get_dict()

    # plotovanie
    plot_stat(dict, fig_location, show_figure)
