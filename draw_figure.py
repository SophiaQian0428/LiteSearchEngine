import os
import matplotlib
import matplotlib.pyplot as plt

def get_vote(expert_result_root, question_number):
    import random
    return random.choice(["ACS", "CS", "EDS"])


def draw_figure1(question_file, source_root, output_root):
    # 画一个Histogram for Categorical Variable图，
    # 纵坐标是91个问题的序号，横坐标是支持类型ABC（分别指代ACS、CS、EDS）回答为最好的分别的专家数
    x_name = "Votes"
    y_name = "Question Number"

    with open(question_file, encoding="utf-8") as fp:
        lines = fp.readlines()
        ys = list(range(len(lines)))

    experts = [folder for folder in os.listdir(source_root) if os.path.isdir(os.path.join(source_root, folder))]
    methods = []
    for file in os.listdir(os.path.join(source_root, experts[0])):
        file = file.lstrip(os.path.splitext(question_file)[0])
        method_a = file.split("_")[0]
        method_b = file.split("_")[1]
        if method_a not in methods:
            methods.append(method_a)
        if method_b not in methods:
            methods.append(method_b)
    colors = [plt.cm.Spectral(i / float(len(methods) - 1)) for i in range(len(methods))]

    values = [[] for _ in range(len(methods))]  # [[A的91个问题对应的votes数], B:[...], ]

    for idx in ys:
        vote_dict = {}
        for expert in experts:
            vote = get_vote(os.path.join(source_root, expert), idx)
            if vote not in vote_dict:
                vote_dict[vote] = 0
            vote_dict[vote] += 1

        for i, m in enumerate(methods):
            if m in vote_dict:
                values[i].append(vote_dict[m])
    print(values)
    plt.figure(figsize=(16, 9), dpi=80)
    plt.hist(values, len(ys), stacked=True, density=False,
             color=colors[:len(methods)], orientation='horizontal')
    plt.legend({group: col for group, col in zip(methods, colors[:len(methods)])})
    # plt.title(f"Stacked Histogram of ${x_var}$ colored by ${groupby_var}$", fontsize=22)
    plt.xlabel(x_name)
    plt.ylabel(y_name)
    plt.ylim(0, 91)
    # plt.xticks(rotation=90, horizontalalignment='left')
    plt.show()

if __name__ == '__main__':
    source_root = r"test/sim_results/"
    output_root = r"data/figure/"

    draw_figure1(r"data/question/question_list_1.txt", source_root, output_root)
