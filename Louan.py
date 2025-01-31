import numpy as np

def position_goo(ind, Dico):
    acc = g*np.array(0, -1)
    for duo in Dico[ind]:
        acc += (k/m) * np.array(
            (np.sqrt((Goos[ind].center_y[1])**2 + (Goos[ind].center_x[1])**2) - np.sqrt((Goos[duo[0]].center_y[1])**2 + (Goos[duo[0]].center_x[1])**2) - duo[1])
              * np.sin(np.arctan2((Goos[duo[0]].center_x[1] - Goos[ind].center_x[1]) , (Goos[ind].center_y[1] - Goos[duo[0]].center_y[1]))) ,
                (np.sqrt((Goos[ind].center_y[1])**2 + (Goos[ind].center_x[1])**2) - np.sqrt((Goos[duo[0]].center_y[1])**2 + (Goos[duo[0]].center_x[1])**2) - duo[1])
                  * np.cos(np.arctan2((Goos[duo[0]].center_x[1] - Goos[ind].center_x[1]) , (Goos[ind].center_y[1] - Goos[duo[0]].center_y[1]))))
    newx_tdt = 2*Goos[ind].center_x[1] - Goos[ind].center_x[0] + acc[0]*(delta_time)**2
    newy_tdt = 2*Goos[ind].center_y[1] - Goos[ind].center_y[0] + acc[1]*(delta_time)**2
    Goos[ind].center_x = (Goos[ind].center_x[1], newx_tdt)
    Goos[ind].center_y = (Goos[ind].center_y[1], newy_tdt)
    return()
    #

