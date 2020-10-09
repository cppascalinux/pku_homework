#include<iostream>
#include<cstdio>
#include<cstring>
#include<algorithm>
#include<cmath>
#include<cassert>
#define LL long long
#define ULL unsigned long long
#define BS 10007
#define MOD3 10000019
#define MAXL 50
#define PII pair<int,int>
#define FI first
#define SE second
#define DB double
#define R0 0.95
using namespace std;
struct node
{
	ULL hs;
	int r,l,id;
	DB q,t;
	bool operator <(const node &p)const{return r>p.r;}
};
int n,m,w,tot;
DB al;
short s[34000009];
ULL hs[34000009],mul[109];
int hd[10000019],nxt[6000009];
node eg[6000009];
DB f[34000009];
int g[34000009];
int st[34000009],tp;
int mdl[209];
short orgw[6000009][60];
short mds[209][209];
ULL mdhs[209][209];
void inith(short *s,ULL *hs,int n)
{
	for(int i=1;i<=n;i++)
		hs[i]=hs[i-1]*BS+s[i];
	mul[0]=1;
	for(int i=1;i<=100;i++)
		mul[i]=mul[i-1]*BS;
}
ULL qryh(ULL *hs,int l,int r)
{
	return hs[r]-hs[l-1]*mul[r-l+1];
}
ULL geth(int *v,int l)
{
	ULL sm=0;
	for(int i=1;i<=l;i++)
		sm=sm*BS+v[i];
	return sm;
}
inline int findh(ULL h)
{
	int md=h%MOD3;
	for(int i=hd[md];i;i=nxt[i])
		if(eg[i].hs==h)
			return i;
	return -1;
}
void addh(node p)
{
	int md=p.hs%MOD3;
	int v=findh(p.hs);
	assert(v==-1);
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
		eg[i].t=log2((DB)eg[i].r/sm[eg[i].l]);
}
void dp(short *s,ULL *hs,int n)
{
	f[0]=0;
	fill(f+1,f+n+1,-1.0/0);
	memset(g,0,(n+1)<<2);
	for(int i=1;i<=n;i++)
	{
		if(s[i]<=1)
		{
			f[i]=f[i-1];
			g[i]=i-1;
			continue;
		}
		for(int j=1;j<=i;j++)
		{
			int k=i-j;
			DB p=0;
			ULL h=hs[i]-hs[k]*mul[j];
			int pos=findh(h);
			if(pos<0)
				break;
			node t=eg[pos];
			if(t.t>0)
				continue;
			p=t.q+t.t+al*(1-j);
			if(f[i]<f[k]+p)
				f[i]=f[k]+p,g[i]=k;
			if(s[k]<=1)
				break;
		}
	}
	tp=0;
	for(int i=n;i;i=g[i])
	{
		st[++tp]=i;
		// if(i-g[i]>1&&s[i]==49)
		// 	printf("i:%d g:%d\n",i,g[i]);
	}
	reverse(st+1,st+tp+1);
	printf("tp:%d\n",tp);
}
void vt()
{
	int sm[100],ltp=-1;
	while(1)
	{
		dp(s,hs,n);
		if(tp==ltp)
			break;
		ltp=tp;
		memset(sm,0,sizeof(sm));
		for(int j=1;j<=tot;j++)
			eg[j].r=0;
		for(int j=1;j<=tp;j++)
		{
			int l=st[j]-st[j-1];
			sm[l]++;
			ULL h=hs[st[j]]-hs[st[j-1]]*mul[l];
			int pos=findh(h);
			if(pos>0)
				eg[pos].r++;
		}
		for(int j=1;j<=tot;j++)
		{
			if(eg[j].r==0)
				eg[j].t=100;
			else
				eg[j].t=log2((DB)eg[j].r/sm[eg[j].l]);
		}
	}
}
void bin()
{
	DB l=-10,r=10;
	int ltp=-1;
	for(int i=1;i;i++)
	{
		al=(l+r)/2;
		printf("i:%d al:%lf\n",i,al);
		vt();
		if(tp==ltp)
			break;
		ltp=tp;
		int rm=R0*w;
		for(int j=1;j<=w;j++)
		{
			// printf("j:%d\n",j);
			dp(mds[j],mdhs[j],mdl[j]);
			if(tp==1)
				rm--;
		}
		if(rm>=0)
			r=al;
		else
			l=al;
	}
}
void sdp(short *s,ULL *hs,int n)
{
	f[0]=0;
	fill(f+1,f+n+1,-1.0/0);
	for(int i=1;i<=n;i++)
	{
		if(s[i]==0)
		{
			f[i]=f[i-1];
			continue;
		}
		for(int j=1;j<=i;j++)
		{
			if(i==n&&j==n)
				break;
			int k=i-j;
			DB p=0;
			ULL h=hs[i]-hs[k]*mul[j];
			int pos=findh(h);
			if(pos<0)
				break;
			node t=eg[pos];
			if(t.t>0)
				continue;
			p=t.q+t.t+al*(1-j);
			if(f[i]<f[k]+p)
				f[i]=f[k]+p;
			if(s[k]==0)
				break;
		}
	}
}
void output()
{
	FILE *fout=fopen("features_cpp.out","w");
	ULL tphs[100];
	for(int i=1;i<=tot;i++)
	{
		DB p0=pow(2,al*(1-eg[i].l)+eg[i].q+eg[i].t);
		if(eg[i].t>0)
			p0=0;
		inith(orgw[i],tphs,eg[i].l);
		sdp(orgw[i],tphs,eg[i].l);
		DB p1=pow(2,f[eg[i].l]);
		DB v1=log2(p0/p1);
		DB v2=p0*v1;
		fprintf(fout,"%.12lf %.12lf\n",v1,v2);
	}
	// vt();
	dp(s,hs,n);
	FILE *cout=fopen("cuts_cpp.out","w");
	for(int i=1;i<=tp;i++)
		if(s[st[i]]!=0)
		{
			for(int j=st[i-1]+1;j<=st[i];j++)
				fprintf(cout,"%d ",s[j]);
			fprintf(cout,"0 ");
		}
	FILE *wout=fopen("words_cpp.out","w");
	for(int i=1;i<=tot;i++)
		eg[i].r=0;
	for(int i=1;i<=tp;i++)
	{
		ULL h=qryh(hs,st[i-1]+1,st[i]);
		int pos=findh(h);
		if(pos>0)
			eg[pos].r++;
	}
	sort(eg+1,eg+tot+1);
	for(int i=1;i<=tot;i++)
	{
		if(eg[i].l<=1)
			continue;
		for(int j=1;j<=eg[i].l;j++)
			fprintf(wout,"%hd ",orgw[eg[i].id][j]);
		fprintf(wout,"%d\n",eg[i].r);
	}
}
int main()
{
	freopen("copora_cpp.out","r",stdin);
	scanf("%d",&n);
	for(int i=1;i<=n;i++)
		scanf("%hd",s+i);
	inith(s,hs,n);
	scanf("%d",&m);
	printf("n:%d m:%d\n",n,m);
	int tmps[100];
	for(int i=1;i<=m;i++)
	{
		int t;
		scanf("%d",&t);
		for(int j=1;j<=t;j++)
			scanf("%d",tmps+j),orgw[i][j]=tmps[j];
		node v;
		v.hs=geth(tmps,t);
		scanf("%d%lf",&v.r,&v.q);
		v.q=log2(max(v.q,0.01));
		v.l=t;
		v.id=i;
		addh(v);
	}
	printf("tot:%d\n",tot);
	scanf("%d",&w);
	for(int i=1;i<=w;i++)
	{
		int t;
		scanf("%d",&t);
		mdl[i]=t;
		for(int j=1;j<=t;j++)
			scanf("%hd",mds[i]+j);
		inith(mds[i],mdhs[i],t);
	}
	gett();
	dp(s,hs,n);
	// vt(1);
	// bin();
	// vt(50);
	// vt(-50);
	// vt(-50);
	output();
	return 0;
}