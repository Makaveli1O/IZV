# IZV 
Data Analysis and Visualization in Python
## Hodnotenie part 1 12/20
+2 delky vsech datovych sloupcu jsou stejne (az 2 bodu)
+2 stahlo se 95_835 zaznamu (az 2 bodu)
+2 uspesne se stahl Plzensky kraj (s chybou v textu) (az 2 bodu)
+0 stahl se Karlovarsky kraj bez duplikatu (az 1 bodu)
+1 podarilo se vytvorit pandas.DataFrame (az 1 bodu)
+1 rozumne rozlozeni datovych typu (az 1 bodu)
+0 souradnice jsou spravne jako floaty i s desetinnymi misty (az 1 bodu)
+0 neni mozne hodnotit cas 3.92 s, jelikoz t1, t4 a t5 neprosly (az 2 bodu)
+0 obrazky se ulozily spravne (a.png, ./b.png, t/c.png) (az 1 bodu)
+3.00 kvalita kodu downloader.py (az 3 bodu)
+3.00 kvalita kodu get_stat.py (az 3 bodu)
+1.00 graf z get_stat.py (az 2 bodu)
-1 bonus (az -1 bodu)
CELKEM: 15.0 bodu
## Hodnotenie part 2 19.2/20
Hodnoceni druhe casti projektu: xliska20
================================================================================
+1.00 pouzite kategoricke typy (>=2) (az 1 bodu)
+1.00 ostatni typy jsou korektni (ints>30 & floats>=6) (az 1 bodu)
+1.00 vhodne vyuziti pameti (< 500 MB) (az 1 bodu)
+1.00 spravne konvertovane datum (rok 2016 - 2021) (az 1 bodu)
+0.12 funkce get_dataframe ma spravne docstring (PEP257) (az 0.125 bodu)
+0.12 funkce plot_roadtype ma spravne docstring (PEP257) (az 0.125 bodu)
+0.12 funkce plot_animals ma spravne docstring (PEP257) (az 0.125 bodu)
+0.12 funkce plot_conditions ma spravne docstring (PEP257) (az 0.125 bodu)
+0.25 funkce plot_conditions trva do 1500 ms (az 0.5 bodu)
+2.00 kvalita kodu funkce plot_conditions (az 2 bodu)
+2.00 vizualni dojem z grafu plot_conditions (az 2 bodu)
+0.25 funkce plot_animals trva do 1200 ms (az 0.5 bodu)
+2.00 kvalita kodu funkce plot_animals (az 2 bodu)
+2.00 vizualni dojem z grafu plot_animals (az 2 bodu)
+0.25 funkce plot_roadtype trva do 1000 ms (az 0.5 bodu)
+2.00 kvalita kodu funkce plot_roadtype (az 2 bodu)
+2.00 vizualni dojem z grafu plot_roadtype (az 2 bodu)
+2.00 kvalita kodu dle PEP8 (0 kritickych, 7 E2.., 0 E7..)) (az 2 bodu)
CELKEM: 19.2 bodu

Komentar k hodnoceni (zejmena k vizualizacim)
================================================================================
v poradku

Vystup testu
================================================================================
#df_types ints=45;floats=6;cats=11;dt=1
#df_memory=211.22MB
#df_date_year 2016 2021
#get_dataframe_docstring  ok
#plot_roadtype_docstring  ok
#plot_animals_docstring  ok
#plot_conditions_docstring  ok
#plot_roadtype_done 1246.13 ms
#plot_animals_done 1259.07 ms
#plot_conditions_done 1903.96 ms

Počet řádků 209

Chybovy vystup test
================================================================================


PEP8 analysis.py
================================================================================
5       E226 missing whitespace around arithmetic operator
2       E241 multiple spaces after ','
## Hodnotenie part 3 48/60
Hodnoceni treti casti projektu: xliska20
================================================================================
Geograficka data
--------------------------------------------------------------------------------
+1.00 spravne CRS (5514, 3857) (az 1 b)
+2.00 spravne rozsah (viz FAQ) (az 2 b)
+2.00 pocet radku 571225 > 10 000 (az 2 b)
+2.00 bez NaN v souradnicich (az 2 b)
+3.00 plot_geo: prehlednost, vzhled (az 3 b)
+2.00 plot_geo: zobrazeni ve WebMercator (a ne v S-JTSK) (az 2 b)
+0.00 plot_cluster: prehlednost, vzhled (az 2 b)
+3.00 plot_cluster: clustering (az 3 b)
+1.00 funkce make_geo ma spravne docstring (PEP257) (az 1 b)
+0.50 funkce plot_geo ma spravne docstring (PEP257) (az 0.5 b)
+0.50 funkce plot_cluster ma spravne docstring (PEP257) (az 0.5 b)
+1.00 kvalita kodu dle PEP8 (0 kritickych, 11 E2.., 0 E7..)) (az 1 b)

Overeni hypotezy
--------------------------------------------------------------------------------
+1.00 #1: kontingencni tabulka (az 1 b)
+2.00 #1: vypocet chi2 testu (az 2 b)
+0.00 #1: zaver: dochazi k silnemu ovlivneni (az 2 b)
+1.00 #2 filtrace (az 1 b)
+4.00 #2 vypocet a zaver (az 4 b)

Vlastni analyza
--------------------------------------------------------------------------------
+5.00 tabulka: prehlednost, vzhled (az 5 b)
+1.00 graf: popis, vzhled (az 4 b)
+4.00 graf: vhodna velikost, citelnost (az 4 b)
+0.00 graf: pouziti vektoroveho formatu (az 2 b)
+3.00 textovy popis (az 3 b)
+4.00 statisticka smysluplnost analyzy (az 4 b)
+3.00 dalsi ciselne hodnoty v textu (az 3 b)
+0.00 generovani hodnot skriptem bez chyby (az 3 b)
+2.00 kvalita kodu dle PEP8 (0 kritickych, 4 E2.., 0 E7..)) (az 2 b)

CELKEM: 48.0 bodu

Komentar k hodnoceni (zejmena k vizualizacim)
================================================================================
hypo1: a jakym smerem?
hypo2: filtrace dle where neni vhodna (lepsi proste
       podminka)
geo_cluster: spatne natoceny, bez popsiu cbaru
doc: graf je docela neprehledny, lepsi je pouzit popisky v ose x

Vystup skriptu geografickych dat (stdout)
================================================================================
#gdf_crs  EPSG:5514
#gdf_nan 0
#gdf_range_x_min -901630.217
#gdf_range_x_max -432869.21
#gdf_range_y_min -1219810.382
#gdf_range_y_max -938489.513
#gdf_count  571225
#make_geo_docstring  ok
#plot_geo_docstring  ok
#plot_cluster_docstring  ok
#plot_geo_done 8582.80 ms
#plot_cluster_done 1861.88 ms


Vystup skriptu geografickych dat (stderr)
================================================================================
No artists with labels found to put in legend.  Note that artists whose label start with an underscore are ignored when legend() is called with no argument.


Vystup PEP8 testu souboru geo.py
================================================================================
11      E226 missing whitespace around arithmetic operator


Vystup skriptu dokumentace (stdout)
================================================================================


Vystup skriptu dokumentace (stderr)
================================================================================
  File "/home/vojta/git/IZV/project/part03/evaluation/xliska20/doc.py", line 127
    
    ^
IndentationError: expected an indented block


Vystup PEP8 testu souboru doc.py
================================================================================
2       E127 continuation line over-indented for visual indent
1       E226 missing whitespace around arithmetic operator
3       E241 multiple spaces after ','
2       W291 trailing whitespace
1       W503 line break before binary operator
