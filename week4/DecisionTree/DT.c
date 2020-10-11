#include "DT.h"

// 切分函数，根据（由 get_split() 得到的）切分点将数据分为两组
struct dataset *test_split(int index, double value, int row, int col,
                           double **data) {
    // 将切分结果作为结构体返回
    struct dataset *split = (struct dataset *)malloc(sizeof(struct dataset));
    int count1 = 0, count2 = 0;
    double ***groups = (double ***)malloc(2 * sizeof(double **));
    // 分配两个子结点的空间
    for (int i = 0; i < 2; i++) {
        groups[i] = (double **)malloc(row * sizeof(double *));
        for (int j = 0; j < row; j++) {
            groups[i][j] = (double *)malloc(col * sizeof(double));
        }
    }
    // 将样本分配到两个子结点中
    for (int i = 0; i < row; i++) {
        if (data[i][index] < value) {
            groups[0][count1] = data[i];
            count1++;
        } else {
            groups[1][count2] = data[i];
            count2++;
        }
    }
    split->splitdata = groups;
    split->row1 = count1;
    split->row2 = count2;
    return split;
}

// 计算Gini系数
double gini_index(int index, double value, int row, int col, double **dataset,
                  double *class, int classnum) {
    // 声明变量和初始化
    float *numcount1 = (float *)malloc(classnum * sizeof(float));
    float *numcount2 = (float *)malloc(classnum * sizeof(float));
    for (int i = 0; i < classnum; i++)
        numcount1[i] = numcount2[i] = 0;

    float count1 = 0, count2 = 0;
    double gini1, gini2, gini;
    gini1 = gini2 = gini = 0;
    // 分别统计【两组 X 每一类】样本的个数
    for (int i = 0; i < row; i++) {
        // 小于 value 分到第一类，大于 value 分到第二类
        if (dataset[i][index] < value) {
            count1++;
            for (int j = 0; j < classnum; j++)
                if (dataset[i][col - 1] == class[j])
                    numcount1[j] += 1;
        } else {
            count2++;
            for (int j = 0; j < classnum; j++)
                if (dataset[i][col - 1] == class[j])
                    numcount2[j]++;
        }
    }
    // 【！注意！】判断分母是否为 0，可能存在所有元素都被分到同一子结点的情况
    if (count1 == 0) {
        gini1 = 1;
        for (int i = 0; i < classnum; i++)
            gini2 += (numcount2[i] / count2) * (numcount2[i] / count2);
    } else if (count2 == 0) {
        gini2 = 1;
        for (int i = 0; i < classnum; i++)
            gini1 += (numcount1[i] / count1) * (numcount1[i] / count1);
    } else {
        for (int i = 0; i < classnum; i++) {
            gini1 += (numcount1[i] / count1) * (numcount1[i] / count1);
            gini2 += (numcount2[i] / count2) * (numcount2[i] / count2);
        }
    }
    // 计算 Gini index（还记得 Gini 的计算公式吗？）
    gini1 = 1 - gini1;
    gini2 = 1 - gini2;
    gini = (count1 / row) * gini1 + (count2 / row) * gini2;
    free(numcount1);
    free(numcount2);
    numcount1 = numcount2 = NULL;
    return gini;
}

// 选取数据的最优切分点
struct treeBranch *get_split(int row, int col, double **dataset, double *class,
                             int classnum) {
    // 声明和初始化变量
    struct treeBranch *tree =
        (struct treeBranch *)malloc(sizeof(struct treeBranch));
    int b_index = 0;
    // 这里 999 只是一个比较大的数，相当于 \infty
    double b_score = 999, b_value = 999, score = 0;
    // 计算所有切分点Gini系数，选出Gini系数最小的切分点
    for (int i = 0; i < col - 1; i++) {
        for (int j = 0; j < row; j++) {
            double value = dataset[j][i];
            score = gini_index(i, value, row, col, dataset, class, classnum);
            if (score < b_score) {
                b_score = score;
                b_value = value;
                b_index = i;
            }
        }
    }
    tree->index = b_index;
    tree->value = b_value;
    tree->flag = 0;
    return tree;
}

// 计算叶结点最多一类样本的个数，对应停止条件【叶结点最小样本数】
double to_terminal(int row, int col, double **data, double *class,
                   int classnum) {
    int *num = (int *)malloc(classnum * sizeof(classnum));
    double maxnum = 0;
    int flag = 0;
    // 计算所有样本中结果最多的一类
    for (int i = 0; i < classnum; i++)
        num[i] = 0;
    for (int i = 0; i < row; i++)
        for (int j = 0; j < classnum; j++)
            if (data[i][col - 1] == class[j])
                num[j]++;
    for (int j = 0; j < classnum; j++) {
        if (num[j] > flag) {
            flag = num[j];
            maxnum = class[j];
        }
    }
    free(num);
    num = NULL;
    return maxnum;
}

// 创建子树或生成叶结点
void split(struct treeBranch *tree, int row, int col, double **data,
           double *class, int classnum, int depth, int min_size,
           int max_depth) {
    // 判断是否已经达到最大层数，对应停止条件【树最大层数】
    if (depth >= max_depth) {
        tree->flag = 1;
        tree->output = to_terminal(row, col, data, class, classnum);
        return;
    }
    struct dataset *childdata =
        test_split(tree->index, tree->value, row, col, data);
    // 判断样本是否已被分为一边
    if (childdata->row1 == 0 || childdata->row2 == 0) {
        tree->flag = 1;
        tree->output = to_terminal(row, col, data, class, classnum);
        return;
    }
    // 左子树，判断样本是否达到最小样本数，如不是则继续递归
    if (childdata->row1 <= min_size) {
        struct treeBranch *leftchild =
            (struct treeBranch *)malloc(sizeof(struct treeBranch));
        leftchild->flag = 1;
        leftchild->output = to_terminal(
            childdata->row1, col, childdata->splitdata[0], class, classnum);
        tree->leftBranch = leftchild;
    } else { // 继续递归
        struct treeBranch *leftchild = get_split(
            childdata->row1, col, childdata->splitdata[0], class, classnum);
        tree->leftBranch = leftchild;
        split(leftchild, childdata->row1, col, childdata->splitdata[0], class,
              classnum, depth + 1, min_size, max_depth);
    }
    // 右子树，判断样本是否达到最小样本数，如不是则继续递归
    if (childdata->row2 <= min_size) {
        struct treeBranch *rightchild =
            (struct treeBranch *)malloc(sizeof(struct treeBranch));
        rightchild->flag = 1;
        rightchild->output = to_terminal(
            childdata->row2, col, childdata->splitdata[1], class, classnum);
        tree->rightBranch = rightchild;
    } else { // 继续递归
        struct treeBranch *rightchild = get_split(
            childdata->row2, col, childdata->splitdata[1], class, classnum);
        tree->rightBranch = rightchild;
        split(rightchild, childdata->row2, col, childdata->splitdata[1], class,
              classnum, depth + 1, min_size, max_depth);
    }
    free(childdata->splitdata);
    childdata->splitdata = NULL;
    free(childdata);
    childdata = NULL;
    return;
}

// 生成决策树
struct treeBranch *build_tree(int row, int col, double **data, int min_size,
                              int max_depth) {
    int count1 = 0, flag1 = 0;
    // 判断结果一共有多少类别，此处classes[20]仅仅是取一个较大的数20，默认类别不超过20类
    double classes[20];
    for (int i = 0; i < row; i++) {
        if (count1 == 0) {
            classes[0] = data[i][col - 1];
            count1++;
        } else {
            flag1 = 0;
            for (int j = 0; j < count1; j++)
                if (classes[j] == data[i][col - 1])
                    flag1 = 1;
            if (flag1 == 0) {
                classes[count1] = data[i][col - 1];
                count1++;
            }
        }
    }
    // 生成切分点
    struct treeBranch *result = get_split(row, col, data, classes, count1);
    // 进入递归，不断生成子树
    split(result, row, col, data, classes, count1, 1, min_size, max_depth);
    return result;
}

// 决策树预测
double predict(double *test, struct treeBranch *tree) {
    // 判断是否达到叶结点，flag=1时为叶结点，flag=0时则继续判断
    if (tree->flag == 1) {
        return tree->output;
    } else {
        if (test[tree->index] < tree->value) {
            return predict(test, tree->leftBranch);
        } else {
            return predict(test, tree->rightBranch);
        }
    }
}