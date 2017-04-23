# -*- coding: utf-8 -*-
import pandas as pd
import os
from collections import OrderedDict
import numpy as np
from copy import copy
from bokeh.core.properties import field
from bokeh.io import curdoc
from bokeh.layouts import layout,column,row
from bokeh.models.layouts import HBox
from bokeh.models import (
    ColumnDataSource, HoverTool, SingleIntervalTicker, Slider, Button, Label,
    CategoricalColorMapper,
)
from bokeh.models.widgets import Panel, Tabs
from bokeh.models import ColumnDataSource, CustomJS, Rect,Spacer
from bokeh.models import HoverTool,TapTool,FixedTicker,Circle
from bokeh.models import BoxSelectTool, LassoSelectTool
from bokeh.models.mappers import LinearColorMapper
from bokeh.plotting import figure
from bokeh.layouts import row, widgetbox
from bokeh.models.widgets import Select
from cosmo import create_plot
#from data import process_data
from os.path import dirname, join

def main(dfile,pcol,appname):
    global datafile,colvar,col_dict,columns,button,slider,n,xcol,ycol,ccol,s2,xcol,ycol,ccol,plt_name,indx
    datafile=join(dirname(__file__), 'data', dfile)
    
    colvar=np.loadtxt(datafile) #dtype='float32')
    n=len(colvar)
    col_dict=get_propnames(datafile)
    columns=col_dict.keys()
    xcol = Select(title='X-Axis', value=columns[pcol[0]], options=columns,width=50)
    xcol.on_change('value', update)

    ycol = Select(title='Y-Axis', value=columns[pcol[1]], options=columns, width=50)
    ycol.on_change('value', update)

    ccol = Select(title='Color', value=columns[pcol[2]], options=columns,width=50)
    ccol.on_change('value', update)

    plt_name = Select(title='Palette',width=50, value='Magma256', options=["Magma256","Plasma256","Spectral6","Inferno256","Viridis256","Greys256"])
    plt_name.on_change('value', update)
    xm=widgetbox(xcol,width=210,sizing_mode='fixed')
    ym=widgetbox(ycol,width=210,sizing_mode='fixed')
    cm=widgetbox(ccol,width=210,sizing_mode='fixed')
    pm=widgetbox(plt_name,width=210,sizing_mode='fixed')
    controls = HBox(xm, ym, cm, pm, width=850, sizing_mode='scale_width')
#    controls = row(xm, ym, cm, pm)
    button = Button(label='► Play', width=60)
    button.on_click(animate)
    indx=0
    xval,yval=selected_point(colvar,col_dict[xcol.value],col_dict[ycol.value],indx)
    s2 = ColumnDataSource(data=dict(xs=[xval], ys=[yval]))

    p1,p2,slider= create_plot(colvar,col_dict[xcol.value],col_dict[ycol.value],col_dict[ccol.value],plt_name.value,appname)
    p1.circle('xs', 'ys', source=s2, fill_alpha=0.9, fill_color="blue",line_color='black',line_width=1, size=8,name="mycircle")
    #p1.circle('xs', 'ys', source=s2, fill_alpha=1, fill_color="black", size=10,name="mycircle")
    slider.on_change('value', slider_update)
    #plots=column(row(p1,p2),row(s,Spacer(width=20, height=30))) #,button)
#    slide=widgetbox(slider,button,width=600)
#    slide=row(slider,button)
    lay = layout([
        [controls],
        [p1,p2],
        [slider,button],
    ], sizing_mode='fixed')
    return lay
def get_propnames(file):
 with open(file) as f:
    last_pos = f.tell()
    li=f.readline().strip()
    if li.startswith("#"):
        propsname=li.split()[1:]
        
    else:
        pcount=len(li.split())
        propsname=[]
        for i in range(pcount):
            propsname.append["prop_"+str(i+1)]
 prop_dict= {propsname[i]: i for i in range(0, len(propsname))}
 pdict=OrderedDict(sorted(prop_dict.items(), key=lambda t: t[1]))
 return pdict




def selected_point(data,xcol,ycol,indx):
   xval=copy(data[indx,xcol])
   yval=copy(data[indx,ycol])
   return xval,yval

def animate_update():
    global indx,n
    indx = slider.value + 1
    if indx > (n-1):
        indx = 0
    slider.value = indx

#def slider_update(attrname, old, new):
#    year = slider.value
#    label.text = str(year)
#    source.data = data[year]

#slider = Slider(start=years[0], end=years[-1], value=years[0], step=1, title="Year")
#def slider_callback2(src=datasrc,source=s2, window=None):
def slider_update(attrname, old, new):
    global  indx,s2,xval,yval,plt_name
#    col_dict={"cv1":0,"cv2": 1,"index": 2,"energy": 3}
    col_dict=get_propnames(datafile)
    columns=col_dict.keys()
    indx = slider.value
   # label.text = str(indx)
    xval,yval=selected_point(colvar,col_dict[xcol.value],col_dict[ycol.value],indx)
    s = ColumnDataSource(data=dict(xs=[xval], ys=[yval]))
    s2.data=s.data 

def animate():
    if button.label == '► Play':
        button.label = '❚❚ Pause'
        curdoc().add_periodic_callback(animate_update, 500)
    else:
        button.label = '► Play'
        curdoc().remove_periodic_callback(animate_update)





def update(attr, old, new):
    global indx,s2,xval,yval,plt_name,xcol,ycol,ccol
#    col_dict={"cv1":0,"cv2": 1,"index": 2,"energy": 3}
    col_dict=get_propnames(datafile)
    columns=col_dict.keys()
    p1,p2,slider = create_plot(colvar,col_dict[xcol.value],col_dict[ycol.value],col_dict[ccol.value],plt_name.value,appname)
    xval,yval=selected_point(colvar,col_dict[xcol.value],col_dict[ycol.value],indx)
    s = ColumnDataSource(data=dict(xs=[xval], ys=[yval]))
    s2.data=s.data 
    p1.circle('xs', 'ys', source=s2, fill_alpha=0.9, fill_color="blue",line_color='black',line_width=1, size=8,name="mycircle")
    button = Button(label='► Play', width=60)
    button.on_click(animate)
    lay.children[1] = row(p1,p2)




#columns=["cv1","cv2","index","energy"]
#col_dict={"cv1":0,"cv2": 1,"index": 2,"energy": 3}

appname=os.path.basename(dirname(__file__))
lay=main(dfile='COLVAR',pcol=[0,1,3],appname=appname)
curdoc().add_root(lay)
curdoc().template_variables["js_files"] = [appname+"/static/jmol/JSmol.min.js"]
css=[]
for f in ["w3","introjs"]:
  css.append(appname+"/static/css/"+f+'.css')
curdoc().template_variables["css_files"] = css
curdoc().title = "Sketchmap"
