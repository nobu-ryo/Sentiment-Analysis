import matplotlib.pyplot as plt
import numpy as np

def plot_polar(labels, values, imgname):
    angles = np.linspace(0, 2 * np.pi, len(labels) + 1, endpoint=True)
    values = np.concatenate((values, [values[0]]))
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, values, 'o-'
    ax.fill(angles, values, alpha=0.25)
    ax.set_thetagrids(angles[:-1] * 180 / np.pi, labels)
    ax.set_rlim(0 ,250)
    plt.show()
    #fig.savefig(imgname)
    #plt.close(fig)

def plot_radarchart(values, labels):
    radar_values = np.concatenate([values, [values[0]]])
    angles = np.linspace(0, 2 * np.pi, len(labels) + 1, endpoint=True)
    rgrids = [0, 2, 4, 6, 8, 10]
    fig = plt.figure(facecolor="w")
    ax = fig.add_subplot(1, 1, 1, polar=True)
    ax.plot(angles, radar_values)
    ax.fill(angles, radar_values, alpha=0.2)
    ax.set_thetagrids(angles[:-1] * 180 / np.pi, labels)
    ax.set_rgrids([])
    ax.spines['polar'].set_visible(False)
    ax.set_theta_zero_location("N")
    ax.set_theta_direction(-1)
    for grid_value in rgrids:
        grid_values = [grid_value] * (len(labels)+1)
        ax.plot(angles, grid_values, color="gray",  linewidth=0.5)
    for t in rgrids:
        ax.text(x=0, y=t, s=t)
    ax.set_rlim([min(rgrids), max(rgrids)])
    plt.show()
