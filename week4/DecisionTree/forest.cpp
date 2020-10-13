#include<iostream>
#include<cstdio>
#include<cstring>
#include<algorithm>
#include<random>
#include<ctime>
#include<cmath>
#include<cassert>
#define TREECOUNT 1000
#define DB double
using namespace std;
mt19937 rnd(time(0));
int n=208,m=60,tot,s=sqrt(m),sl;
DB mat[1009][1009];
int pm[1009];
int tv[1009];
int res[1009],used[1009];
int rt[1009],lp[1000009],rp[1000009],bdi[1000009],cls[1000009];
DB bdv[1000009];
int st[1009],vis[1009],tp;
void select()
{
	tp=0;
	memset(vis,0,(m+1)<<2);
	while(tp<s)
	{
		int p=rnd()%m+1;
		if(!vis[p])
			vis[p]=1,st[++tp]=p;
	}
}
bool cmp(int a,int b)
{
	return mat[a][sl]<mat[b][sl];
}
void build(int &a,int *v,int sm)
{
	// assert(sm>0);
	a=++tot;
	int cm[2]={0,0};
	for(int i=1;i<=sm;i++)
		cm[res[v[i]]]++;
	if(!cm[0]||!cm[1])
	{
		cls[a]=res[v[1]];
		return;
	}
	select();
	DB mg=1e300;
	int pos=0;
	for(int i=1;i<=tp;i++)
	{
		sl=st[tp];
		sort(v+1,v+sm+1,cmp);
		int cr[2]={0,0};
		for(int j=1;j<=sm-1;j++)
		{
			cr[res[v[j]]]++;
			DB g=0;
			g+=2.0*cr[0]*cr[1]/j/sm;
			g+=2.0*(cm[0]-cr[0])*(cm[1]-cr[1])/(sm-j)/sm;
			// printf("g:%lf\n",g),fflush(stdout);
			if(g<mg)
				mg=g,bdi[a]=sl,bdv[a]=(mat[v[j]][sl]+mat[v[j+1]][sl])/2,pos=j;
		}
	}
	// printf("tp:%d sm:%d ming:%lf pos:%d\n",tp,sm,mg,pos);
	sl=bdi[a];
	sort(v+1,v+sm+1,cmp);
	build(lp[a],v,pos);
	build(rp[a],v+pos,sm-pos);
}
int judge(DB *v)
{
	int sm=0;
	for(int i=1;i<=TREECOUNT;i++)
		for(int cur=rt[i];cur;)
		{
			// printf("cur:%d lp:%d rp:%d cls:%d bdi:%d bdv:%lf\n",cur,lp[cur],rp[cur],cls[cur],bdi[cur],bdv[cur]);
			if(cls[cur]!=-1)
			{
				sm+=cls[cur];
				break;
			}
			// printf("qwq\n");
			if(v[bdi[cur]]<bdv[cur])
				cur=lp[cur];
			else
				cur=rp[cur];
			// printf("pwp\n");
		}
	return 2*sm>=TREECOUNT;
}
int main()
{
	freopen("forest.in","r",stdin);
	freopen("forest.out","w",stdout);
	memset(cls,-1,sizeof(cls));
	for(int i=1;i<=n;i++)
		pm[i]=i;
	shuffle(pm+1,pm+n+1,rnd);
	for(int i=1;i<=n;i++)
	{
		for(int j=1;j<=m;j++)
			scanf("%lf,",mat[pm[i]]+j);
		scanf("%d",res+pm[i]);
	}
	for(int i=1;i<=TREECOUNT;i++)
	{
		for(int j=1;j<=n/2;j++)
			tv[j]=rnd()%(n/2)+1;
		build(rt[i],tv,n/2);
	}
	int sm=0;
	for(int i=n/2+1;i<=n;i++)
		sm+=(judge(mat[i])==res[i]);
	printf("Accuracy:%lf\n",(DB)sm/(n/2));
	return 0;
}