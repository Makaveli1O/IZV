#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import gzip
import pickle
import numpy
import zipfile
import os
import io
import csv
import cProfile
import pickle
from io import StringIO
from bs4 import BeautifulSoup
import requests as r
from zipfile import ZipFile as ZF


class DataDownloader:
    """ TODO: dokumentacni retezce

    Attributes:
        headers    Nazvy hlavicek jednotlivych CSV souboru, tyto nazvy nemente!
        regions     Dictionary s nazvy kraju : nazev csv souboru
        p1 -> id
        p36 -> druh komunikácie
        p37 -> číslo pozemnej komunikácie
        p2a -> dátum
        weekday(p2a) -> deň v týždni
        p2b -> čas
        p6 -> druh nehody
        p7 -> druh zrážky vozidiel
        p8 -> druh pevnej prekážky
        p9 -> charakter nehody
        p10 -> zavinenie nehody
        p11 -> alkohol u vinníka
        p12 -> hlavná príčina nehody
        p13a -> mŕtve osoby
        p13b -> ťažko zranené osoby
        p13c -> lahko zranené osoby
        p14 -> celková hmotná škoda
        p15 -> povrch vozovky
        p16 -> stav povrchu vozovky v dobe nehody
        p17 -> stav komunikácie
        p18 -> poveternostné podmienky v dobe nehody
        p19 -> viditeľnosť
        p20 -> rozhľadové pomery
        p21 -> delenie komunikacie
        p22 -> situovanie nehody na komunikacii
        p23 -> riadenie premávky v dobe nehody
        p24 -> miestna úprava prednosti v jazde
        p27 -> specifické miesta a objekty na mieste nehody
        p28 -> smerove pomery
        p34 -> počet zúčastnených vozidiel
        p35 -> miesto dopravnej nehody
        p39 -> druh križujúcej komunikacie
        p44 -> druh vozidla
        p45a -> výrobná značka motorového vozidla
        p47 -> rok výroby vozidla
        p48a -> charakteristika vozidla
        p49 -> šmky
        p50a -> vozidlo po nehode
        p50b -> únik prepravovaných hmôt
        p51 -> spôsob vybratia osôb z vozidla
        p52 -> smer jazdy alebo postavenie vozidla
        p53 -> škoda na vozidle
        p55a -> kategória vodiča
        p57 -> stav vodiča
        p58 -> vonkajšie ovplyvnenie vodica
    """

    headers = [
        "p1",
        "p36",
        "p37",
        "p2a",
        "weekday(p2a)",
        "p2b",
        "p6",
        "p7",
        "p8",
        "p9",
        "p10",
        "p11",
        "p12",
        "p13a",
        "p13b",
        "p13c",
        "p14",
        "p15",
        "p16",
        "p17",
        "p18",
        "p19",
        "p20",
        "p21",
        "p22",
        "p23",
        "p24",
        "p27",
        "p28",
        "p34",
        "p35",
        "p39",
        "p44",
        "p45a",
        "p47",
        "p48a",
        "p49",
        "p50a",
        "p50b",
        "p51",
        "p52",
        "p53",
        "p55a",
        "p57",
        "p58",
        "a",
        "b",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "p5a",
        "region"]

    strings = set([3, 34, 51, 52, 53, 54, 55, 56, 57, 58, 59, 62, 64])
    floats = set([45, 46, 47, 48, 49, 50])

    regions = {
        "PHA": "00",  # praha
        "STC": "01",  # Stredocesky
        "JHC": "02",  # Jihocesky
        "PLK": "03",  # Plzensky
        "ULK": "04",  # Ustecky
        "HKK": "05",  # Karlovehradecky
        "JHM": "06",  # Jihomoravsky
        "MSK": "07",  # Moravskoslezsky
        "OLK": "14",  # Olomoucky
        "ZLK": "15",  # Zlinsky
        "VYS": "16",  # Kraj Vysocina
        "PAK": "17",  # Pardubicky
        "LBK": "18",  # Liberecky
        "KVK": "19",  # Karlovarsky
    }

    def __init__(
            self,
            url="https://ehw.fit.vutbr.cz/izv/",
            folder="data",
            cache_filename="data_{}.pkl.gz"):
        # zarážka
        self.arity = numpy.iinfo(numpy.int64).min

        self.dict = {}

        self.url = url
        # vytvorenie zložky
        if os.path.isdir(folder):
            self.folder = folder
        else:
            os.mkdir(folder)
            self.folder = folder

        self.retrieved_data = []
        self.download_data()

        self.cache_filename = cache_filename

        pass

    def download_data(self):
        """
        Metoda stiahne všetky súbory s datami z adresy url do zložky folder.
        Pomocou BeautifulSoup vyparsuje html, z ktorého získa požadovné
        ZIP súbory. Sťahuje savždy iba posledný dostupný mesiac v danom roku,
        pretože ten obsahuje data zo všetkých predošlých mesiacov.Následne sa
        skontroluje či sú data už stiahnuté, prípadne ich načíta zo zložky.
        """
        # get request
        response = r.get(self.url)
        # parse html
        soup = BeautifulSoup(response.content, "html.parser")
        # prejst cez tabulku (telo)
        for i, item in enumerate(soup.find_all("td"), start=1):
            # v decembri su ulozene vsetky predosle mesiace daneho roka
            if i % 13 == 0:
                # december
                if item.text != "neexistuje":
                    last_record = item
                # extrahovanie subora z html stromu
                btn = last_record.find("button")
                fileUrl = self.url + \
                    btn.get("onclick")[10:len(btn.get("onclick")) - 2]
                # ulozit meno subora
                self.retrieved_data.append(fileUrl.rsplit("/", 1)[1])
            # ak neexistuje skip
            if item.text == "neexistuje":
                continue
            else:
                # ukladat posledny record ktory existuje
                last_record = item

        # kontrola (download alebo load z data folderu)
        for item in self.retrieved_data:
            path = os.getcwd() + "\\data\\" + item
            # tie co neexistuju lokalne, stiahnut
            if not os.path.exists(path):
                response = r.get(self.url + "data/" + item, stream=True)
                with open(path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=128):
                        f.write(chunk)

    def parse_region_data(self, region):
        """Skontroluje či sú všetky požadované data dostupné v zložke 
        'folder', prípadne stiahne chýbajúce položky. Následne sa prejdú
        jednotlivé ZIP súbory z ktorých sa vytiahnú data, ktoré sa po 
        riadku čítajú. Float hodnoty sú upravené podľa tvaru xy,zw -> xy.zw.
        Extrahované data majú šírku 64, pričom sa pridáva posledný stĺpec
        'region' do ktorého sa ukladá trojznakový kód momentálne sa 
        spracovávajúceho sa kraja. Pred vrátením sa ešte jednotlivé položky vo
        výsledných numpy poliach nastavia na správny dátový typ.

        Args:
            region (str list): List regiónov ktoré sa majú spracovať

        Returns:
            dictionary: Slovník obsahujúci vyparsované data.
        """
        dict = {}
        arr_of_arrs = []
        # 64 headers - > 64 arrays that needs to be filled
        for i in range(0, len(self.headers)):
            a_i = []
            arr_of_arrs.append(a_i)

        for zipName in self.retrieved_data:
            # ak chybaju data stiahnut
            if not os.path.isfile(self.folder + '/' + zipName):
                self.download_data()
            # otvorit zip
            with ZF(self.folder + "/" + zipName, "r") as zip:
                # otvorit konkretny subor v zipe (podla daneho regionu)
                with zip.open(self.regions[region] + ".csv", "r") as file:
                    file_read = csv.reader(
                        io.TextIOWrapper(
                            file, 'cp1250'), delimiter=';')
                    # precitat riadok a ulozit (+1 pretoze pridavam stlpec
                    # regions)
                    for line in file_read:
                        # 1 cyklus = 1 stlpec v exceli
                        for i in range(len(line) + 1):
                            # pridanie stlpcu regions
                            if i == 64:
                                arr_of_arrs[i].append(region)
                            # rozsirit o zarazku
                            elif not line[i] or line[i] == "XX":
                                arr_of_arrs[i].append(self.arity)
                            # rozsirit pole o najdeny stlpec
                            else:
                                # upravenie floating point hodnot: xy,zw ->
                                # xy.zw
                                if i in self.floats:
                                    try:
                                        arr_of_arrs[i].append(
                                            line[i].replace(",", ""))
                                    except BaseException:
                                        arr_of_arrs[i].append(self.arity)
                                else:
                                    arr_of_arrs[i].append(line[i])
        # konvertovať na numpy array
        arr2d = numpy.array(arr_of_arrs)
        # typovanie jednotlivych poli v ndarray
        arr2d = self.__set_array_types(arr2d)
        # vytvorit finalny slovnik typu: - > { "header" : np.arr[]}
        for i, numpy_arr in enumerate(arr2d):
            dict[self.headers[i]] = numpy_arr

        return dict

    def get_dict(self, regions=None):
        """Vracia spracované data pre vybrané kraje vo forme slovníka.
        Dáta prejednotlivé rióny sú pomocou konkatenancie numpy polí 
        spájané do jedného.Pro spracovávaní sa zároveň data cachujú dvomi
        spôsobmi. V prvom rade sa vytvorí cache súvor vo 'folder' pomocou
        pickle modulu. V prípade že by programpracoval s rovnakými 
        dátami pri jedno spustení viac krát, sa spracované dáta uložia do
        triedneho atribútu 'dict'. Pri spracovávaní sa teda buď musia dáta
        vyparsovať pomocou funkcie 'parse_region_data' alebo sa načítajú z
        jedno z cache. Parsované dáta sa následne pomocou '__merge_results'
        skladajú do slovníka.

        Args:
            regions (str list, optional): [description]. Defaults to None.

        Returns:
            dictionary: Slovník zložený z vyparsovaných dát zadaných regiónov.
        """
        # sprave regiony
        if regions is None or not regions:
            regions = list(self.regions.keys())

        # posunuty iba string, nie list
        if not isinstance(regions, list):

            regions = [regions]

        if not self.__check_given_regions(regions):
            print("Unknown region given.")
            exit(1)

        ret = {}

        # spracovanie vsetkych zadanych rgeionov
        for num_region, region in enumerate(regions):
            # ak su data ulozene v atribute triedy, vrat ich
            if region in self.dict:
                return self.dict[region]
            # ak existuje cache tohoto filu extrahuj
            try:
                path = self.folder + "/" + self.cache_filename.format(region)
                # ziskanie dat z cache, a rozirenie slovnika
                with gzip.open(path, "rb") as cf:
                    parsed_region = pickle.load(cf)
                    # prve spracovanie
                    if num_region == 0:
                        ret = parsed_region
                    # spojenie viacerych vysledkov
                    else:
                        ret = self.__merge_results(ret, parsed_region)

            # inak vytvor novy cache subor
            except FileNotFoundError:
                new_cache_file = self.folder + "/" + \
                    self.cache_filename.format(region)
                # spracovanie regionu
                parsed_region = self.parse_region_data(region)

                # vytvorenie cache suboru spracovaneho regionu
                with gzip.open(new_cache_file, "wb") as cf:
                    pickle.dump(parsed_region, cf)
                # prve spracovanie
                if num_region == 0:
                    ret = parsed_region
                # spojenie viacerych vysledkov
                else:
                    ret = self.__merge_results(ret, parsed_region)
            # ulozenie do atributu triedy
            self.dict[region] = ret
        return ret

    def __check_given_regions(self, regions):
        """Skontroluje zadaný región, či je validný.

        Args:
            regions (str list): List aspracovávaných regiónov.

        Returns:
            bool
        """
        regions = set(regions)
        self_regions = set(self.regions)
        return regions.issubset(self_regions)

    def __merge_results(self, dict1, dict2):
        ret_dict = dict.fromkeys(self.headers)

        for header in self.headers:
            ret_dict[header] = numpy.concatenate(
                [dict1[header], dict2[header]])

        return ret_dict

    def __set_array_types(self, ndarr):
        """Nastaví pre každé numpy pole korektný dátový typ. Pokiaľ sa
        v stĺpci ktorý očakáva špecifický dátový typ vyskytne exception,
        zadá sa dátový typ string.

        Args:
            ndarr (ndarray): 65x65 matica

        Returns:
            ndarray: Rovnaká matica, s korektnými dátovými typmi.
        """
        res_arr = []
        for i, array in enumerate(ndarr):
            tmp = array
            # ints
            if i not in self.strings and i not in self.floats:
                try:
                    tmp = array.astype(dtype='int64')
                except BaseException:
                    tmp = array.astype(dtype=tmp.dtype)
            # floats
            elif i in self.floats:
                try:
                    tmp = array.astype(dtype='float64')
                except BaseException:
                    tmp = array.astype(dtype=tmp.dtype)
            # date
            elif i == 3:
                try:
                    tmp = array.astype(dtype='datetime64')
                except BaseException:
                    tmp = array.astype(dtype=tmp.dtype)
            # append to result
            res_arr.append(tmp)
        return res_arr


if __name__ == '__main__':
    dataDownloader = DataDownloader()
    # cProfile.run('dataDownloader.get_dict([])')
    # pokial je spustany priamo (nie ako modul)

    example_regions = ["PHA", "JHC", "STC"]
    dict = dataDownloader.get_dict(example_regions)

    count = 0  # pocet zaznamov

    print("Stiahnuté stĺpce: ")
    for key, item in dict.items():
        count = len(item)
        print(key, end=", ")
    print("\nPočet záznamov : {}".format(count))
    print("Spracované kraje v datasete: {}".format(", ".join(example_regions)))
