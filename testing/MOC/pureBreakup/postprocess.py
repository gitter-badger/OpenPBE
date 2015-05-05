import numpy as np
import matplotlib as mpl
mpl.use("agg")
import matplotlib.pyplot as plt
from itertools import cycle

plt.style.use('ggplot')
plt.ioff()


def set_plt_params(
        relative_fig_width=1.0, landscape=True, page_width=307.3, rescale_h=1):

    fig_width_pt = page_width * relative_fig_width
    inches_per_pt = 1.0 / 72.27               # Convert pt to inch
    golden_mean = (np.sqrt(5.0) - 1.0) / 2.0  # Aesthetic ratio
    fig_width = fig_width_pt * inches_per_pt  # width in inches

    if landscape:
        fig_height = fig_width * golden_mean  # height in inches
    else:
        fig_height = fig_width / golden_mean  # height in inches

    fig_height = fig_height * rescale_h
    fig_size = [fig_width, fig_height]
    params = {
        'font.family': 'serif',
        'axes.labelsize': 7,
        'xtick.labelsize': 5,
        'ytick.labelsize': 5,
        'axes.labelcolor': 'black',
        'ytick.color': 'black',
        'xtick.color': 'black',
        'legend.handlelength': 4,
        'legend.fontsize': 7,
        # 'lines.markersize': 3,
        # 'xtick.labelsize': 7,
        # 'ytick.labelsize': 7,
        'text.usetex': True,
        'text.latex.unicode': True,
        'figure.figsize': fig_size,
        'pgf.texsystem': "xelatex",
        'pgf.rcfonts': False,
    }

    plt.rcParams.update(params)


def zm_pure_breakup_total_number_solution(x, t, l):
    """
    This is simply an integral of Ziff and McGrady
    """
    return np.exp(-t * l**2) \
        + np.trapz(2.0 * t * l * np.exp(-t * x**2), x=x)


def zm_pure_breakup_pbe_solution(x, t, l):
    """
    This is based on Equation 25 from Ziff and McGrady
    """
    return np.piecewise(
        x,
        [x < l, x == l, x > l],
        [
            lambda x: 2.0 * t * l * np.exp(-t * x**2),
            lambda x: np.exp(-t * x**2),
            lambda x: 0.0
        ]

    )


def total_number_graph(data, time):
    # Total number function
    N = sum(data.values())

    xi = np.linspace(0, 0.1, 100)
    N_analytical = np.zeros(time.shape)
    for i, t in enumerate(time):
        N_analytical[i] = zm_pure_breakup_total_number_solution(xi, t, 0.1)

    #set_plt_params()
    fig = plt.figure()
    ax = fig.gca()

    plt.xlabel("Time [s]")
    plt.ylabel("$N(t)/N(0)$")
    ax.loglog(time, N/N[0], label="Simulation")
    ax.loglog(time, N_analytical/N_analytical[0], label="Ziff and McGrady")
    ax.legend(loc='lower right', shadow=True)
    fig.savefig("total_number.pdf", bbox_inches='tight')
    plt.close()


def pbe_graph(data, time, ts, deltaX=0.01, l=0.1):
    # Number of classes
    N = len(data)
    v = np.linspace(deltaX, N * deltaX, N)
    Nsimulation = dict(
        (t, np.zeros(v.shape))
        for t in ts
    )
    for t in ts:
        ind = np.nonzero(time == t)[0]
        for i in range(N):
            Nsimulation[t][i] = data[i][ind]

    # Calculating solutions for 0 and l values doesn't make much sense because
    # there are no drops of volume zero and drops of size l are Dirac's delta
    # so I don't know how ti visualise it.
    xi = np.linspace(0, l, 100, endpoint=False)
    N_analytical = dict(
        (t, np.zeros(xi.shape))
        for t in ts
    )
    for t in ts:
        N_analytical[t] = zm_pure_breakup_pbe_solution(xi, t, l)

    # set_plt_params()
    fig = plt.figure()
    ax = fig.gca()

    plt.xlabel("Particle volume $[\mathrm{m}^3]$")
    plt.ylabel("Particle number")
    ax.set_xlim(1e-3, 0.12)
    ax.set_ylim(1e-3, 1200)
    linestyles = cycle(['-', '--', ':'])
    markers = cycle(['o', 's', 'v', '*', '.', ','])
    for t in ts:
        ax.semilogy(
            v, Nsimulation[t], "+",
            label="Simulation $t={0}$".format(t),
            marker=next(markers)
        )
        ax.semilogy(
            xi, N_analytical[t],
            label="Ziff and McGrady $t={0}$".format(t),
            linestyle=next(linestyles)
        )
    ax.legend(loc='lower left', shadow=True)
    fig.savefig("pbe.pdf", bbox_inches='tight')
    plt.close()


# Number of classes
N = 10

# Loading only number functions for each class
data = dict(
    (
        n,
        np.genfromtxt("postProcessing/probes/0/n{0:d}".format(n))[:, 1]
    ) for n in range(N)
)

time = np.genfromtxt("postProcessing/probes/0/n0")[:, 0]

total_number_graph(data, time)
pbe_graph(data, time, [1000, 2000])
