#include "DT.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 获取 csv 文件行数
int get_row(char *filename) {
    char line[1024];
    int i = 0;
    FILE *stream = fopen(filename, "r");
    while (fgets(line, 1024, stream)) {
        i++;
    }
    fclose(stream);
    return i;
}

// 获取 csv 文件列数
int get_col(char *filename) {
    char line[1024];
    int i = 0;
    FILE *stream = fopen(filename, "r");
    fgets(line, 1024, stream);
    char *token = strtok(line, ",");
    while (token) {
        token = strtok(NULL, ",");
        i++;
    }
    fclose(stream);
    return i;
}

// 获取行数和列数之后，就可以读取数据了
// 也可以直接读取csv数据，不用先读行再读列
void get_two_dimension(char *line, double **dataset, char *filename) {
    FILE *stream = fopen(filename, "r");
    int i = 0;
    while (fgets(line, 1024, stream)) {
        int j = 0;
        char *tok;
        char *tmp = _strdup(line);
        for (tok = strtok(line, ","); tok && *tok;
             j++, tok = strtok(NULL, ",\n")) {
            dataset[i][j] = atof(tok);
        }
        i++;
        free(tmp);
    }
    fclose(stream);
}

// 划分交叉验证集
double ***cross_validation_split(double **dataset, int row, int n_folds,
                                 int fold_size, int col) {
    srand(10);
    double ***split;
    int i, j = 0, k = 0;
    int index;
    split = (double ***)malloc(n_folds * sizeof(double **));
    for (i = 0; i < n_folds; i++) {
        double **fold = (double **)malloc(fold_size * sizeof(double *));
        for (; j < fold_size; row--, j++) {
            fold[j] = (double *)malloc(col * sizeof(double));
            index = rand() % row;
            fold[j] = dataset[index];
            for (k = index; k < row - 1; k++) {
                dataset[k] = dataset[k + 1];
            }
        }
        j = 0;
        split[i] = fold;
    }
    return split;
}

// 获得预测结果
double *get_test_prediction(double **train, double **test, int column,
                            int min_size, int max_depth, int fold_size,
                            int train_size) {
    double *predictions = (double *)malloc(
        fold_size * sizeof(double)); //预测集的行数就是数组prediction的长度
    struct treeBranch *tree =
        build_tree(train_size, column, train, min_size, max_depth);
    for (int i = 0; i < fold_size; i++) {
        predictions[i] = predict(test[i], tree);
    }
    return predictions; //返回对test的预测数组
}

// 计算 accuray
double accuracy_metric(double *actual, double *predicted, int fold_size) {
    int correct = 0, i;
    for (i = 0; i < fold_size; i++) {
        if (actual[i] == predicted[i]) {
            correct += 1;
        }
    }
    return correct / (double)fold_size;
}

// 评价函数
float *evaluate_algorithm(double **dataset, int column, int n_folds,
                          int fold_size, int min_size, int max_depth) {
    double ***split = cross_validation_split(dataset, row, n_folds, fold_size, col);
    int i, j, k, l;
    int test_size = fold_size;
    int train_size = fold_size * (n_folds - 1); // train_size个一维数组
    float *score = (float *)malloc(n_folds * sizeof(float));
    for (i = 0; i < n_folds; i++) { //因为要遍历删除，所以拷贝一份split
        double ***split_copy = (double ***)malloc(n_folds * sizeof(double **));
        for (j = 0; j < n_folds; j++) {
            split_copy[j] = (double **)malloc(fold_size * sizeof(double *));
            for (k = 0; k < fold_size; k++) {
                split_copy[j][k] = (double *)malloc(column * sizeof(double));
            }
        }
        for (j = 0; j < n_folds; j++) {
            for (k = 0; k < fold_size; k++) {
                for (l = 0; l < column; l++) {
                    split_copy[j][k][l] = split[j][k][l];
                }
            }
        }
        double **test_set = (double **)malloc(test_size * sizeof(double *));
        for (j = 0; j < test_size; j++) { //对test_size中的每一行
            test_set[j] = (double *)malloc(column * sizeof(double));
            for (k = 0; k < column; k++) {
                test_set[j][k] = split_copy[i][j][k];
            }
        }
        for (j = i; j < n_folds - 1; j++) {
            split_copy[j] = split_copy[j + 1];
        }
        double **train_set = (double **)malloc(train_size * sizeof(double *));
        for (k = 0; k < n_folds - 1; k++) {
            for (l = 0; l < fold_size; l++) {
                train_set[k * fold_size + l] =
                    (double *)malloc(column * sizeof(double));
                train_set[k * fold_size + l] = split_copy[k][l];
            }
        }
        double *predicted = (double *)malloc(
            test_size * sizeof(double)); // predicted有test_size个
        predicted = get_test_prediction(train_set, test_set, column, min_size,
                                        max_depth, fold_size, train_size);
        double *actual = (double *)malloc(test_size * sizeof(double));
        for (l = 0; l < test_size; l++) {
            actual[l] = test_set[l][column - 1];
        }
        double accuracy = accuracy_metric(actual, predicted, test_size);
        score[i] = accuracy;
        printf("score[%d]=%f\n", i, score[i]);
        free(split_copy);
    }
    float total = 0.0;
    for (l = 0; l < n_folds; l++) {
        total += score[l];
    }
    printf("mean_accuracy=%f\n", total / n_folds);
    return score;
}