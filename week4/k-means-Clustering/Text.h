#pragma once

# define MAXNUMFEATURE 20
# define MAXNUMTEXT 200
# define MAXNUMCATEGORY 20
# define MAXNUMCLUSTER 200

typedef struct
{
	double  feature[MAXNUMFEATURE];  //属性数组
	int  categories;	             //文本的预定义类，用作聚类的质量评测
	int	 cluster;		             //文本所属的聚类号
}Text;

typedef struct
{
	double feature[MAXNUMFEATURE];	//质心向量
	int elementsCount;			    //类中文档数目
	int elements[MAXNUMTEXT];	    //类中文档ID号
}Cluster;

void K_Means_Clustering();
void DisplayClusters();

int indexOf(char *);  //输入类名称，输出类标号