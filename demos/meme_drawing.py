import matplotlib.pyplot as plt
from random import random


# Function to create the combined meme
def create_combined_meme():
            fig, axs = plt.subplots(2, 1, figsize=(8, 4))

            # Top panel - Regular radicals duel
            axs[0].text(0.5,
                        0.8,
                        "When you bring radicals to a math duel...",
                        fontsize=18,
                        ha='center',
                        va='center',
                        fontweight='bold')
            axs[0].text(0.3,
                        0.4,
                        r"$\sqrt{x}$",
                        fontsize=50,
                        ha='center',
                        va='center')
            axs[0].text(0.7,
                        0.4,
                        r"$\sqrt{y}$",
                        fontsize=50,
                        ha='center',
                        va='center')
            axs[0].plot([0.3, 0.7], [0.4, 0.4], color='black', lw=2)
            axs[0].set_xlim(0, 1)
            axs[0].set_ylim(0, 1)
            axs[0].axis('off')

            # Bottom panel - Bring radicals duel
            axs[1].text(0.5,
                        0.8,
                        "But then someone brings Bring radicals...",
                        fontsize=18,
                        ha='center',
                        va='center',
                        fontweight='bold')
            axs[1].text(0.3,
                        0.4,
                        r"$\sqrt{x}$",
                        fontsize=50,
                        ha='center',
                        va='center')
            bring_radical = "BR(p^{-5/4} q)"
            axs[1].text(0.7,
                        0.4,
                        f"${bring_radical}$",
                        fontsize=30,
                        ha='center',
                        va='center',
                        color='red')
            axs[1].plot([0.3, 0.7], [0.4, 0.4], color='black', lw=2)
            axs[1].set_xlim(0, 1)
            axs[1].set_ylim(0, 1)
            axs[1].axis('off')

            plt.tight_layout()
            plt.show()


# Create the combined meme
#create_combined_meme()


def print_grid(grid, size):
            for i in range(size):
                        print()
                        for j in range(size):
                                    if check_row(grid, i, j, size):
                                                print('+', end='')
                                    if check_col(grid, i, j, size):
                                                print('-', end='')
                                    print(round(grid[i][j], 3), end='  ')


def check_row(grid, i, j, size):
            largest = True
            for square in range(size):
                        if grid[i][j] < grid[i][square]:
                                    largest = False
            return largest


def check_col(grid, i, j, size):
            smallest = True
            for square in range(size):
                        if grid[i][j] > grid[square][j]:
                                    smallest = False
            return smallest


def saddle_points(size, trials):
            succs, total = 0, 0
            for trial in range(trials):
                        grid = [[random() for i in range(size)]
                                for j in range(size)]
                        #print_grid(grid, size)
                        point = False
                        for i in range(size):
                                    for j in range(size):
                                                if check_row(grid, i, j, size
                                                             ) and check_col(
                                                                         grid,
                                                                         i, j,
                                                                         size):
                                                            point = True
                        if point:
                                    succs += 1
                        total += 1
            return [f'{succs}/{total}', succs / total]


for i in range(10):
            saddles = saddle_points(i, 100000)
            print(f'{saddles[0]} ({saddles[1]}) ({i}*{i} grid)')
