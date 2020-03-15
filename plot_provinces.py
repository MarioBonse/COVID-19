import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import matplotlib as mpl
import numpy as np
import re
import os
import functools


def create_data(name, map_italy):
    
    # decide wether we normilize or not
    folder = 'COVID-19/dati-province/'
    normalization = False
    column = 'totale_casi'
    df = pd.read_csv(folder+name, header=0)
    df = df.rename(columns={'sigla_provincia': 'sigla'})
    
    if normalization:
        df['totale_casi'] = df['totale_casi']/df['totale_casi'].sum()
        vmin, vmax = -1, 1
    else:
        vmin, vmax = 0, 12000

    merged = map_italy.set_index('sigla').join(df.set_index('sigla'))
    return merged
    
def plot_day( name, map_italy, title = False, save = False, log = True, legend = True):
    font = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': 40,
        }
    # decide wether we normilize or not
    folder = 'dati-province/'
    column = 'totale_casi'
    cmap = mpl.cm.cool
    df = pd.read_csv(folder+name, header=0,  encoding = "ISO-8859-1")
    df = df.rename(columns={'sigla_provincia': 'sigla'})
    
    if log:
        df['totale_casi'].where(df['totale_casi'] <= 1, 1)
        df['totale_casi'] = df['totale_casi'].apply(lambda x: np.log(float(x)))
        vmin, vmax = 0, np.log(12000)
    else:
        vmin, vmax = 0, 12000
        
    merged = map_italy.set_index('sigla').join(df.set_index('sigla'))
    
      
    fig, ax = plt.subplots(1, figsize=(15, 15))
    if title:
        # find title from the name 
        start = int(re.findall(r'(\d{8})', name)[0])
        year = start //10000
        day = start%100
        month = (start%10000)//100
        title = '{0:02}/{1:02}/{2:04}'.format(day, month, year)
        #plt.title(title, fontdict=font)  
        ax.annotate(title, xy=(0.6, 0.1),  xycoords='figure fraction', horizontalalignment='left', verticalalignment='top', fontsize=44, color='#555555')
        ax.annotate('Source: Protezione Civile, https://github.com/pcm-dpc/COVID-19',xy=(0.5, 0.02),  xycoords='figure fraction', horizontalalignment='left', verticalalignment='top', fontsize=12, color='#555555')
    ax.axis('off')
    if log:
        P = merged.plot(column=column, cmap=cmap, linewidth=0.8, ax=ax, edgecolor='0.8',  norm=plt.Normalize(vmin=vmin, vmax=vmax))
    else:
        P = merged.plot(column=column, cmap=cmap, linewidth=0.8, ax=ax, edgecolor='0.8')
    
    if legend:
        # Create colorbar as a legend
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))
        # empty array for the data range
        sm._A = []
        # add the colorbar to the figure
        if log:
            cbar = fig.colorbar(sm, orientation = 'horizontal', label='Total cases (Logaritmic scale)', fraction = 0.1, shrink = 0.5)
        else:
            cbar = fig.colorbar(sm, orientation = 'horizontal', label='Total cases', fraction = 0.1, shrink = 0.5)

    if save:
        plt.savefig('plot/' + name[:-4] + '.png')

def compare_function(file1, file2):
    start1 = int(re.findall(r'(\d{8})', file1)[0]) % 10000
    day1 = start1%100
    month1 = start1//100
    
    start2 = int(re.findall(r'(\d{8})', file2)[0]) % 10000
    day2 = start2%100
    month2 = start2//100
    
    if (month2 < month1) or (month2 == month1 and day2 < day1):
        return 1
    else:
        return -1


import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import imageio

def plot_gif(name, map_italy, title = False, save = False, log = False, legend = True, column = 'totale_casi', folder = 'dati-province/'):
    font = {'family': 'serif',
        'color':  'black',
        'weight': 'normal',
        'size': 40,
        }
    # decide wether we normilize or not
    cmap = 'Reds' #mpl.cm.cool
    print('reding data from: {}'.format(folder+name))
    df = pd.read_csv(folder+name, header=0,  encoding = "ISO-8859-1")
    df = df.rename(columns={'sigla_provincia': 'sigla'})
    
    if log:
        df['totale_casi'].where(df['totale_casi'] <= 1, 1)
        df['totale_casi'] = df['totale_casi'].apply(lambda x: np.log(float(x)))
        vmin, vmax = 0, np.log(12000)
    else:
        vmin, vmax = 0, 12000
        
    merged = map_italy.set_index('sigla').join(df.set_index('sigla'))
    
      
    fig, ax = plt.subplots(1, figsize=(15, 15))
    if title:
        # find title from the name 
        start = int(re.findall(r'(\d{8})', name)[0])
        year = start //10000
        day = start%100
        month = (start%10000)//100
        title = '{0:02}/{1:02}/{2:04}'.format(day, month, year)
        #plt.title(title, fontdict=font)  
        ax.annotate(title, xy=(0.6, 0.1),  xycoords='figure fraction', horizontalalignment='left', verticalalignment='top', fontsize=44, color='#555555')
        ax.annotate('Source: Protezione Civile, https://github.com/pcm-dpc/COVID-19',xy=(0.5, 0.02),  xycoords='figure fraction', horizontalalignment='left', verticalalignment='top', fontsize=12, color='#555555')
    ax.axis('off')
    if log:
        P = merged.plot(column=column, cmap=cmap,   linewidth=0.8, ax=ax, edgecolor='0',  norm=plt.Normalize(vmin=vmin, vmax=vmax))
    else:
        P = merged.plot(column=column, cmap=cmap,  linewidth=0.8, ax=ax, edgecolor='0')
    
    if legend:
        # Create colorbar as a legend
        sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))
        # empty array for the data range
        sm._A = []
        # add the colorbar to the figure
        if log:
            cbar = fig.colorbar(sm, orientation = 'horizontal', label='Total cases (Logaritmic scale)', fraction = 0.1, shrink = 0.5)
        else:
            cbar = fig.colorbar(sm, orientation = 'horizontal', label='Total cases', fraction = 0.1, shrink = 0.5)

    if save:
        plt.savefig('plot/' + name[:-4] + '.png')
    # Used to return the plot as an image rray
    fig.canvas.draw()       # draw the canvas, cache the renderer
    image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
    image  = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    return image

def check_cases(provincia):
    for d in daily_data:
        df = pd.read_csv(folder+d, header=0,  encoding = "ISO-8859-1")
        df = df.loc[df['denominazione_provincia'] == provincia].reset_index()
        print(df['totale_casi'][0])

if __name__ == '__main__':
    print('main')
    # set the filepath and load in a shapefile
    fp = 'province_borders'
    fps = 1
    map_df = gpd.read_file(fp)

    folder = 'dati-province/'
    name = 'dpc-covid19-ita-province-20200306.csv'
    daily_data = os.listdir(folder)
    print('directory is '+ str(daily_data))
    daily_data.remove('dpc-covid19-ita-province.csv')

    # sort the csv fine in province for data
    daily_data.sort(key = functools.cmp_to_key(compare_function))
    kwargs_write = {'fps':1.0, 'quantizer':'nq'}
    imageio.mimsave('./log.gif', [plot_gif(day, title = True, save = False, log = True, map_italy = map_df) for day in daily_data], fps=fps)
    imageio.mimsave('./linear.gif', [plot_gif(day, title = True, save = False, log = False, map_italy = map_df) for day in daily_data], fps=fps)
