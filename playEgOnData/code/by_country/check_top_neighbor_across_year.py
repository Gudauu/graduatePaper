# from playEgOnData.code.include import *
from include import *
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pathlib import Path



# for each country during year range, count its:
# domestic ASR sum
# foreign ASR sum (all foreign countries together)
# top foreign ASR sum
# outfile format is ',' separated three lines without blank space(for R's process)
def count_domestic_extern_across_year(country:str,year_start:int,year_end:int,month:str='0101'):
    ofile_directory_name = 'playEgOnData/results/by_country/'+ country
    Path(ofile_directory_name).mkdir(parents=True, exist_ok=True)

    dict_year_neib = {}

    list_domestic = [0]*(year_end - year_start + 1)
    list_extern = [0]*(year_end - year_start + 1)
    list_first_foreign = [0]*(year_end - year_start + 1)
    for year in range(year_start,year_end+1):
        dict_year_neib[year] = []
        ifile = open(f"playEgOnData/results/{year}{month}/by_country/{country}/neighbors_count_by_country",'r')
        count_extern = 0
        for line in ifile:
            dict_year_neib[year].append(line[:-1])  # strip the last '\n'
            cc = line.split(':')[0]
            count = int(line.split(':')[1])
            if cc == country:
                list_domestic[year - year_start] = count 
            else:
                if list_first_foreign[year - year_start] == 0:
                    list_first_foreign[year - year_start] = count
                count_extern += count 
        list_extern[year - year_start] = count_extern

    ofile = open(f'{ofile_directory_name}/count_domestic_extern_across_{year_start}_{year_end}','w')

    ofile.write(str(list_domestic)[1:-1])
    ofile.write('\n')
    ofile.write(str(list_extern)[1:-1])
    ofile.write('\n')
    ofile.write(str(list_first_foreign)[1:-1])
    ofile.write('\n')
    ofile.close()

            

def check_top_neighbor_across_year(country:str,year_start:int,year_end:int,month:str='0101',limit:int=10):
    ofile_directory_name = 'playEgOnData/results/by_country/'+ country
    Path(ofile_directory_name).mkdir(parents=True, exist_ok=True)
    ofile = open(f'{ofile_directory_name}/top_{limit}_neighbor_across_{year_start}_{year_end}','w')

    dict_year_neib = {}

    format_width = 10
    for year in range(year_start,year_end+1):
        ofile.write(f'{year:<{format_width}}')
        dict_year_neib[year] = []
        ifile = open(f"playEgOnData/results/{year}{month}/by_country/{country}/neighbors_count_by_country",'r')
        count = 0
        for line in ifile:
            dict_year_neib[year].append(line[:-1])  # strip the last '\n'
            count += 1
            if count >= limit:
                break 

    ofile.write('\n\n')
    for i in range(limit):
        for _,list_lines in dict_year_neib.items():
            if i < len(list_lines):
                ofile.write(f'{list_lines[i]:<{format_width}}')
            else:
                ofile.write(' '*format_width)
        ofile.write('\n')
    
    ofile.close()



if __name__ == '__main__':
    list_country = readList('dataCAIDA/ASN_lookup/filterd_3_neighbor_country_list') 
    # check_top_neighbor_not_self_across_year(list_country,2001,2023)
    # calc_ratio_top_second_across_year(list_country,2001,2023)
    for cc in list_country:
        count_domestic_extern_across_year(cc,2001,2023)



# countries with at least one time top AS not self:
# {"AT","HU","LU","FI","IE","AE","CZ","EU","SI","MY","HK","BM","FR","SE","ZA","BE","DK","NO","ZZ","GB","SG","CY","PT","PR"}
# AT: Austria
# HU: Hungary
# LU: Luxembourg
# FI: Finland
# IE: Ireland
# AE: United Arab Emirates
# CZ: Czech Republic
# EU: European Union
# SI: Slovenia
# MY: Malaysia
# HK: Hong Kong
# BM: Bermuda
# FR: France
# SE: Sweden
# ZA: South Africa
# BE: Belgium
# DK: Denmark
# NO: Norway
# ZZ: Unknown or invalid country code
# GB: United Kingdom
# SG: Singapore
# CY: Cyprus
# PT: Portugal
# PR: Puerto Rico
def check_top_neighbor_not_self_across_year(country_list:list,year_start:int,year_end:int,month:str='0101'):
    set_countries = set()
    ofile = open('playEgOnData/results/2001-2023/top_neighb_not_self','w')
    for year in range(year_start,year_end+1):
        set_countries_not_self = set()
        for country in country_list:
            ifile = open(f"playEgOnData/results/{year}{month}/by_country/{country}/neighbors_count_by_country",'r')
            for line in ifile:
                if line[:2] != country:
                    set_countries_not_self.add((country,line[:2]))  # strip the last '\n'
                    set_countries.add(country)
                break
        ofile.write(f'{year}\n')
        for cc in set_countries_not_self:
            ofile.write(f'{cc} ')
        ofile.write('\n')
    # print("summary\n")
    # for cc in set_countries:
    #     print(f'{cc}',end=' ')


# record the min ratio, max ratio and average ratio of first degree / second degree of each country in list across year range.
def calc_ratio_top_second_across_year(country_list:list,year_start:int,year_end:int,month:str='0101'):
    list_country_not_top = {"AT","HU","LU","FI","IE","AE","CZ","EU","SI","MY","HK","BM","FR","SE","ZA","BE","DK","NO","ZZ","GB","SG","CY","PT","PR"}
    ofile = open('playEgOnData/results/2001-2023/country_degree_ratio_top_second','w')
    # output format:
    # CN : average_ratio min_ratio(year)  max_ratio(year) is_not_top
    list_country_large_ratio = []
    for country in country_list:
        ofile.write(f'{country}: ')
        sum_ratio = 0
        min_ratio_year = (99999,-1)
        max_ratio_year = (-1,-1)
        for year in range(year_start,year_end+1):
            ifile = open(f"playEgOnData/results/{year}{month}/by_country/{country}/neighbors_count_by_country",'r')
            degree_top = -1
            degree_second = -1
            # only read first two lines
            for line in ifile:
                if degree_top == -1:
                    degree_top = int((line[:-1].split(':'))[1])  # CN:900
                else:
                    degree_second = int((line[:-1].split(':'))[1]) 
                    break
            ratio = float(degree_top)/degree_second
            sum_ratio += ratio
            if ratio < min_ratio_year[0]:
                min_ratio_year = (ratio,year)
            if ratio > max_ratio_year[0]:
                max_ratio_year = (ratio,year)
        length = year_end - year_start + 1 
        format_width = 5
        min_ratio_str = f'{round(min_ratio_year[0],1)}({min_ratio_year[1]})'
        max_ratio_str = f'{round(max_ratio_year[0],1)}({max_ratio_year[1]})'
        avg_ratio = round(sum_ratio/length,1)
        if avg_ratio >= 10:
            list_country_large_ratio.append(country)

        ofile.write(f'{avg_ratio:<{format_width}}\
            {min_ratio_str:<{format_width}}\
            {max_ratio_str:<{format_width}}')
        
        if country in list_country_not_top:
            ofile.write('   True\n')
        else:
            ofile.write('\n')
    print(list_country_large_ratio)




        



