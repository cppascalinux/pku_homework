#include<iostream>
#include<cstdio>
#include<cstring>
#include<algorithm>
#include<cmath>
#define LL long long
#define BS 619
#define MOD1 1000000007
#define MOD2 1000000009
#define MOD3 10000019
#define MAXL 50
#define PII pair<int,int>
#define FI first
#define SE second
#define DB double
using namespace std;
struct node
{
	PII hs;
	int r,l;
	DB q,t;
};
int n,m,tot;
short s[34000009];
PII hs[34000009],mul[109];
int hd[10000019],nxt[6000009];
node eg[6000009];
DB f[34000009];
int g[34000009];
int st[34000009],tp;
PII operator +(PII a,PII b){return PII((a.FI+b.FI)%MOD1,(a.SE+b.SE)%MOD2);}
PII operator -(PII a,PII b){return PII((a.FI-b.FI+MOD1)%MOD1,(a.SE-b.SE+MOD2)%MOD2);}
PII operator *(PII a,PII b){return PII((LL)a.FI*b.FI%MOD1,(LL)a.SE*b.SE%MOD2);}
PII operator *(PII a,int v){return PII((LL)a.FI*v%MOD1,(LL)a.SE*v%MOD2);}
PII operator +(PII a,int v){return PII((a.FI+v)%MOD1,(a.SE+v)%MOD2);}
void inith(short *s,PII *hs)
{
	for(int i=1;i<=n;i++)
		hs[i]=hs[i-1]*BS+s[i];
	mul[0]={1,1};
	for(int i=1;i<=100;i++)
		mul[i]=mul[i-1]*BS;
}
PII qryh(PII *hs,int l,int r)
{
	return hs[r]-hs[l]*mul[r-l];
}
PII geth(int *v,int l)
{
	PII sm(0,0);
	for(int i=1;i<=l;i++)
		sm=sm*BS+v[i];
	return sm;
}
int findh(PII h)
{
	int md=h.FI%MOD3;
	for(int i=hd[md];i;i=nxt[i])
		if(eg[i].hs==h)
			return i;
	return -1;
}
void addh(node p)
{
	int md=p.hs.FI%MOD3;
	int v=findh(p.hs);
	if(v>0)
		eg[v]=p;
	else
	{
		eg[++tot]=p;
		nxt[tot]=hd[md];
		hd[md]=tot;
	}
}
void gett()
{
	int sm[100];
	memset(sm,0,sizeof(sm));
	for(int i=1;i<=tot;i++)
		sm[eg[i].l]+=eg[i].r;
	for(int i=1;i<=tot;i++)
		eg[i].t=(DB)eg[i].r/sm[eg[i].l];
}
void dp(short *s,PII *hs,int n,DB al)
{
	memset(f,0,(n+1)<<3);
	memset(g,0,(n+1)<<2);
	for(int i=1;i<=n;i++)
	{
		if(s[i]==0)
		{
			f[i]=f[i-1];
			g[i]=i-1;
			continue;
		}
		for(int j=1;j<=min(i,MAXL);j++)
		{
			int k=i-j;
			DB p=0;
			PII h=qryh(hs,k+1,i);
			int pos=findh(h);
			if(pos<0)
				break;
			node t=eg[pos];
			p=pow(al,1-j)*t.t*t.q;
			if(p<=0)
				continue;
			p=log2(p);
			if(f[i]<f[k]+p)
				f[i]=f[k]+p,g[i]=k;
			if(s[k]==' ')
				break;
		}
	}
	int tp=0;
	for(int i=n;i;i=g[i])
		if(s[i]!=0)
			st[++tp]=i;
	reverse(st+1,st+tp+1);
	for(int i=1;i<=tp;i++)
	{
		for(int j=st[i-1]+1;j<=st[i];j++)
			printf("%d ",s[j]);
		printf("|");
	}
}
int main()
{
	freopen("copora_cpp.out","r",stdin);
	freopen("temp.out","w",stdout);
	scanf("%d",&n);
	for(int i=1;i<=n;i++)
		scanf("%hd",s+i);
	inith(s,hs);
	scanf("%d",&m);
	printf("n:%d m:%d\n",n,m);
	int tmps[100];
	for(int i=1;i<=m;i++)
	{
		int t;
		scanf("%d",&t);
		for(int j=1;j<=t;j++)
			scanf("%d",tmps+j);
		node v;
		v.hs=geth(tmps,t);
		scanf("%d%lf",&v.r,&v.q);
		v.l=t;
		addh(v);
	}
	gett();
	dp(s,hs,n,2);
	return 0;
}