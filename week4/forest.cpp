/*
该程序实现了4种算法:
1.CART决策树
2.决策树+随机抽取样本(Bagging),不随机抽取特征,形成决策树森林
3.决策树+随机抽取特征,不随机抽取样本,形成决策树森林
4.决策树+随机抽取样本+随机抽取特征,形成随机森林
并对模型进行K-交叉验证,得到准确率的平均值
K取10,随机森林大小为100,随机抽取的样本大小为sqrt(特征总数)
经过100次实验取平均值,算法1-4的准确率依次为63.81%,79.66%,82.41%,79.58%
说明对于该组样本,随机抽取特征是提高准确率的关键
*/
#include<iostream>
#include<cstdio>
#include<cstring>
#include<algorithm>
#include<random>
#include<ctime>
#include<cmath>
#include<cassert>
#define TREECOUNT 100//随机森林决策树个数
#define MK 10//K-交叉验证,K的取值
#define ITER 100//实验次数
#define DB double
using namespace std;
mt19937 rnd(time(0));
int n=208,m=60,tot,s,sl;
DB mat[1009][1009];
int num[1009];
int pm[1009];
int tv[1009],prv[1009];
int res[1009],used[1009];
int rt[1009],lp[1000009],rp[1000009],bdi[1000009],cls[1000009];
DB bdv[1000009];
int st[1009],vis[1009],tp;
void select(int fg)//随机选择特征,fg为1时选择sqrt(m)个,否则全部选择
{
	if(fg)
		s=sqrt(m);
	else
		s=m;
	tp=0;
	memset(vis,0,(m+1)<<2);
	while(tp<s)
	{
		int p=rnd()%m+1;
		if(!vis[p])
			vis[p]=1,st[++tp]=p;
	}
}
bool cmp(int a,int b)//根据某一特征对样本排序
{
	return mat[a][sl]<mat[b][sl];
}
void build(int &a,int *v,int sm,int fg)//建立决策树,fg为1表示随机选择特征,否则表示不随机选择特征
{
	// assert(sm>0);
	a=++tot;
	int cm[2]={0,0};
	for(int i=1;i<=sm;i++)//样本中各类别总数
		cm[res[v[i]]]++;
	if(!cm[0]||!cm[1])//如果样本已经纯净,就停止递归
	{
		cls[a]=res[v[1]];
		return;
	}
	select(fg);//随机选择特征
	DB mg=1e300;
	int pos=0;
	for(int i=1;i<=tp;i++)//枚举选择的特征
	{
		sl=st[tp];
		sort(v+1,v+sm+1,cmp);//对样本依照这一特征排序
		int cr[2]={0,0};
		for(int j=1;j<=sm-1;j++)//枚举分割的位置
		{
			cr[res[v[j]]]++;
			DB g=0;
			g+=2.0*cr[0]*cr[1]/j/sm;//计算基尼系数
			g+=2.0*(cm[0]-cr[0])*(cm[1]-cr[1])/(sm-j)/sm;
			if(g<mg)//如果基尼系数比最小值更小,则更新分割的特征和位置
				mg=g,bdi[a]=sl,bdv[a]=(mat[v[j]][sl]+mat[v[j+1]][sl])/2,pos=j;
		}
	}
	sl=bdi[a];
	sort(v+1,v+sm+1,cmp);//再对所有样本排序
	build(lp[a],v,pos,fg);//递归到左右儿子,构建决策树
	build(rp[a],v+pos,sm-pos,fg);
}
int predict(DB *v,int fg)//对样本预测,fg为0表示只用一棵决策树,否则表示使用TREECOUNT棵决策树
{
	int sm=0,nt=fg?TREECOUNT:1;
	for(int i=1;i<=nt;i++)//枚举所有决策树
		for(int cur=rt[i];cur;)
		{
			if(cls[cur]!=-1)//到达叶子节点
			{
				sm+=cls[cur];
				break;
			}
			if(v[bdi[cur]]<bdv[cur])//向左/右儿子走
				cur=lp[cur];
			else
				cur=rp[cur];
		}
	return 2*sm>=nt;//根据所有树的投票结果返回预测结果
}
void initmk()//将样本分为K部分
{
	int len=n/MK;
	for(int i=1;i<=n;i++)
		num[i]=(i-1)/len+1;
}
DB cart()//建立单一决策树
{
	memset(cls,-1,sizeof(cls));
	printf("Single Tree\n");
	DB acu=0;
	for(int i=1;i<=MK;i++)//进行K-交叉验证
	{
		int sm=0,cor=0;
		for(int j=1;j<=n;j++)
			if(num[j]!=i)
				prv[++sm]=j;
		build(rt[1],prv,sm,0);//利用(K-1)组样本建立决策树
		for(int j=1;j<=n;j++)//利用决策树对剩下一组样本进行预测
			if(num[j]==i&&predict(mat[j],0)==res[j])
				cor++;
		acu+=(DB)cor/n;
		printf("Accuracy:%lf\n",(DB)cor/(n-sm));//单次准确度
		memset(cls,-1,(tot+1)<<2);
		tot=0;
	}
	printf("Average Accuracy:%lf\n",acu);//平均准确度
	return acu;
}
DB bg()//对所有样本进行Bagging,不随机选择特征,得到决策树森林
{
	memset(cls,-1,sizeof(cls));
	printf("\nBagging Tree Forest\n");
	DB acu=0;
	for(int i=1;i<=MK;i++)
	{
		int sm=0,cor=0;
		for(int j=1;j<=n;j++)
			if(num[j]!=i)
				prv[++sm]=j;
		for(int j=1;j<=TREECOUNT;j++)//建立TREECOUNT棵决策树
		{
			for(int k=1;k<=sm;k++)//在样本中随机采样
				tv[k]=prv[rnd()%sm+1];
			build(rt[j],tv,sm,0);
		}
		for(int j=1;j<=n;j++)//预测
			if(num[j]==i&&predict(mat[j],1)==res[j])
				cor++;
		acu+=(DB)cor/n;
		printf("Accuracy:%lf\n",(DB)cor/(n-sm));
		memset(cls,-1,(tot+1)<<2);
		tot=0;
	}
	printf("Average Accuracy:%lf\n",acu);
	return acu;
}
DB rtf()//只随机选择特征,不进行Bagging,得到决策树森林
{
	memset(cls,-1,sizeof(cls));
	printf("\nRandom Feature Forest\n");
	DB acu=0;
	for(int i=1;i<=MK;i++)
	{
		int sm=0,cor=0;
		for(int j=1;j<=n;j++)
			if(num[j]!=i)
				prv[++sm]=j;
		for(int j=1;j<=TREECOUNT;j++)
		{
			for(int k=1;k<=sm;k++)
				tv[k]=prv[k];
			build(rt[j],tv,sm,1);
		}
		for(int j=1;j<=n;j++)
			if(num[j]==i&&predict(mat[j],1)==res[j])
				cor++;
		acu+=(DB)cor/n;
		printf("Accuracy:%lf\n",(DB)cor/(n-sm));
		memset(cls,-1,(tot+1)<<2);
		tot=0;
	}
	printf("Average Accuracy:%lf\n",acu);
	return acu;
}
DB rf()//既Bagging随机选择样本,又随机选择特征,得到随机森林
{
	memset(cls,-1,sizeof(cls));
	printf("\nRandom Forest\n");
	DB acu=0;
	for(int i=1;i<=MK;i++)
	{
		int sm=0,cor=0;
		for(int j=1;j<=n;j++)
			if(num[j]!=i)
				prv[++sm]=j;
		for(int j=1;j<=TREECOUNT;j++)
		{
			for(int k=1;k<=sm;k++)
				tv[k]=prv[rnd()%sm+1];
			build(rt[j],tv,sm,1);
		}
		for(int j=1;j<=n;j++)
			if(num[j]==i&&predict(mat[j],1)==res[j])
				cor++;
		acu+=(DB)cor/n;
		printf("Accuracy:%lf\n",(DB)cor/(n-sm));
		memset(cls,-1,(tot+1)<<2);
		tot=0;
	}
	printf("Average Accuracy:%lf\n",acu);
	return acu;
}
int main()
{
	freopen("sonar.csv","r",stdin);
	freopen("forest.out","w",stdout);
	for(int i=1;i<=n;i++)
		pm[i]=i;
	shuffle(pm+1,pm+n+1,rnd);//随机打乱输入数据的顺序
	for(int i=1;i<=n;i++)//读入数据
	{
		for(int j=1;j<=m;j++)
			scanf("%lf,",mat[pm[i]]+j);
		scanf("%d",res+pm[i]);
	}
	initmk();
	DB sm[5];
	for(int i=1;i<=ITER;i++)//重复实验100次
	{
		sm[1]+=cart();
		sm[2]+=bg();
		sm[3]+=rtf();
		sm[4]+=rf();
		printf("\n");
	}
	printf("Single Tree:%lf\nBagging Tree Forest:%lf\nRandom Feature Forest:%lf\nRandom Forest:%lf\n",sm[1],sm[2],sm[3],sm[4]);
	return 0;
}