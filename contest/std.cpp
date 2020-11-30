#include<iostream>
#include<cstdio>
#include<cstring>
#include<algorithm>
#define LL long long
#define MIN 1
#define MAX 1000000000
#define PIL pair<int,LL>
#define FI first
#define SE second
using namespace std;
int n,m,tot;
int h[200009];
int rt[200009],lp[8000009],rp[8000009],sm1[8000009];
LL sm2[8000009];
void add(int &a,int l,int r,int pos,int v1,int v2)
{
	int p=++tot;
	lp[p]=lp[a],rp[p]=rp[a];
	sm1[p]=sm1[a],sm2[p]=sm2[a];
	sm1[p]+=v1,sm2[p]+=v2;
	a=p;
	if(l==r)
		return;
	int mid=(l+r)>>1;
	if(pos<=mid)
		add(lp[a],l,mid,pos,v1,v2);
	else
		add(rp[a],mid+1,r,pos,v1,v2);
}
PIL kth(int la,int ra,int l,int r,int k)
{
	if(l==r)
		return PIL(l,(LL)k*l);
	int lsm=sm1[lp[ra]]-sm1[lp[la]];
	int mid=(l+r)>>1;
	if(k<=lsm)
		return kth(lp[la],lp[ra],l,mid,k);
	PIL t=kth(rp[la],rp[ra],mid+1,r,k-lsm);
	t.SE+=sm2[lp[ra]]-sm2[lp[la]];
	return t;
}
int main()
{
	freopen("stairs.in","r",stdin);
	freopen("stairs.out","w",stdout);
	scanf("%d%d",&n,&m);
	for(int i=1;i<=n;i++)
	{
		rt[i]=rt[i-1];
		scanf("%d",h+i);
		add(rt[i],MIN,MAX,h[i],1,h[i]);
	}
	for(int i=1,a,b;i<=m;i++)
	{
		scanf("%d%d",&a,&b);
		int l=b-a+1,md=l>>1;
		if(l&1)
		{
			PIL ls=kth(rt[a-1],rt[b],MIN,MAX,md);
			PIL ms=kth(rt[a-1],rt[b],MIN,MAX,md+1);
			PIL rs=kth(rt[a-1],rt[b],MIN,MAX,md+2);
			LL ans=2*((sm2[rt[b]]-sm2[rt[a-1]])-ms.SE-ls.SE);
			ans-=min(rs.FI-ms.FI,ms.FI-ls.FI);
			printf("%lld\n",ans);
		}
		else
		{
			PIL ls=kth(rt[a-1],rt[b],MIN,MAX,md);
			PIL rs=kth(rt[a-1],rt[b],MIN,MAX,md+1);
			LL ans=2*((sm2[rt[b]]-sm2[rt[a-1]])-2*ls.SE);
			ans-=rs.FI-ls.FI;
			printf("%lld\n",ans);
		}
	}
	return 0;
}