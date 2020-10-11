#include "DT.h"

extern int get_row(char *filename);
extern int get_col(char *filename);
extern void get_two_dimension(char *line, double **dataset, char *filename);
extern float *evaluate_algorithm(double **dataset, int column, int n_folds,
                                 int fold_size, int min_size, int max_depth);

int main() {
    // char filename[] = "banknote.csv";
    char filename[] = "sonar.csv";
    char line[1024];
    row = get_row(filename);
    col = get_col(filename);
    dataset = (double **)malloc(row * sizeof(int *));
    for (int i = 0; i < row; ++i) {
        dataset[i] = (double *)malloc(col * sizeof(double));
    } // 动态申请二维数组
    get_two_dimension(line, dataset, filename);

    // CART 参数，分别为【叶结点最小样本数】和【树最大层数】
    int min_size = 2, max_depth = 10;
    int n_folds = 5;
    int fold_size = (int)(row / n_folds);

    // CART 决策树，返回交叉验证正确率
    float *score = evaluate_algorithm(dataset, col, n_folds, fold_size,
                                      min_size, max_depth);
}