#include<iostream>
#include<cstdio>
#include<cstring>
#include<algorithm>
#include<vector>
#include<string>
#include<map>
#include<random>
#include<ctime>
#include<cmath>
#define DB double
using namespace std;
int n,m,k;
DB mat[1009][1009];
int cl[1009],smcl[1009];
int ansbel[1009];
int bel[1009],vis[1009],tp[1009];
DB pt[1009][1009];
DB minsse=1e300;
string s[100009];
mt19937 rnd(time(0));
int becl[1009][1009];
DB getd2(DB *a,DB *b)
{
	DB ans=0;
	for(int i=1;i<=m;i++)
		ans+=(a[i]-b[i])*(a[i]-b[i]);
	return ans;
}
DB solve()
{
	int sm=0;
	memset(vis,0,(n+1)<<2);
	mt19937 rnd(time(0));
	while(sm<k)
	{
		int p=rnd()%n+1;
		if(vis[p])
			continue;
		else
			vis[p]=1,sm++;
	}
	sm=0;
	for(int i=1;i<=n;i++)
		if(vis[i])
		{
			sm++;
			for(int j=1;j<=m;j++)
				pt[sm][j]=mat[i][j];
		}
	int chg=1;
	memset(bel,0,(n+1)<<2);
	while(chg>0)
	{
		chg=0;
		memset(tp,0,(m+1)<<2);
		for(int i=1;i<=n;i++)
		{
			DB mn=1e300;
			int mx=0;
			for(int j=1;j<=k;j++)
			{
				DB res=getd2(mat[i],pt[j]);
				if(res<mn)
					mn=res,mx=j;
			}
			if(mx!=bel[i])
				chg++;
			bel[i]=mx;
			tp[mx]++;
		}
		for(int i=1;i<=k;i++)
			memset(pt[i],0,(m+1)<<3);
		for(int i=1;i<=n;i++)
			for(int j=1;j<=m;j++)
				pt[bel[i]][j]+=mat[i][j]/tp[bel[i]];
	}
	DB sse=0;
	for(int i=1;i<=n;i++)
		sse+=getd2(mat[i],pt[bel[i]]);
	if(sse<minsse)
		minsse=sse,memcpy(ansbel,bel,(n+1)<<2);
	return sse;
}
void grade()
{
	memcpy(bel,ansbel,(n+1)<<2);
	memset(tp,0,(k+1)<<2);
	for(int i=1;i<=k;i++)
		memset(becl[i],0,(k+1)<<2);
	for(int i=1;i<=n;i++)
		becl[bel[i]][cl[i]]++,tp[bel[i]]++;
	DB ansp=0;
	for(int i=1;i<=k;i++)
	{
		int mx=0;
		for(int j=1;j<=k;j++)
			mx=max(mx,becl[i][j]);
		ansp+=(DB)mx/n;
	}
	DB ansf=0;
	for(int i=1;i<=k;i++)
	{
		DB f=0;
		for(int j=1;j<=k;j++)
			f=max(f,2.0*becl[j][i]/(tp[j]+smcl[i]));
		ansf+=(DB)smcl[i]/n*f;
	}
	printf("Purity:%lf F-feature:%lf SSE:%lf\n",ansp,ansf,minsse);
	for(int i=1;i<=k;i++)
	{
		for(int j=1;j<=n;j++)
			if(bel[j]==i)
			{
				for(int l=1;l<=m;l++)
					printf("%.0lf ",mat[j][l]);
				cout<<s[cl[j]]<<endl;
			}
		printf("\n");
	}
}
int main()
{
	freopen("solve.in","r",stdin);
	freopen("solve.out","w",stdout);
	map<string,int> mp;
	cin>>n>>m>>k;
	m--;
	for(int i=1;i<=k;i++)
		cin>>s[i],mp[s[i]]=i;
	for(int i=1;i<=n;i++)
	{
		for(int j=1;j<=m;j++)
			cin>>mat[i][j];
		string t;
		cin>>t;
		cl[i]=mp[t];
		// cout<<t<<' ';
		// printf("i:%d cl:%d\n",i,cl[i]);
		smcl[cl[i]]++;
	}
	for(int i=1;i<=10000;i++)
		solve();
	// solve();
	grade();
	return 0;
}