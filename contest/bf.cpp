#include<iostream>
#include<cstdio>
#include<cstring>
#include<algorithm>
#define LL long long
using namespace std;
int n,m;
int s[200009],t[200009];
LL cal(int l)
{
	LL ans=0;
	sort(t+1,t+l+1);
	int md=l>>1;
	if(l&1)
	{
		for(int i=l;i>=l-md+1;i--)
			ans+=t[i]*2;
		for(int i=1;i<=md;i++)
			ans-=t[i]*2;
		ans-=min(t[md+1]-t[md],t[md+2]-t[md+1]);
	}
	else
	{
		for(int i=l;i>=l-md+1;i--)
			ans+=t[i]*2;
		for(int i=1;i<=md;i++)
			ans-=t[i]*2;
		ans-=t[md+1]-t[md];
	}
	return ans;
}
int main()
{
	freopen("stairs.in","r",stdin);
	freopen("bf.out","w",stdout);
	scanf("%d%d",&n,&m);
	for(int i=1;i<=n;i++)
		scanf("%d",s+i);
	for(int i=1,a,b;i<=m;i++)
	{
		scanf("%d%d",&a,&b);
		int tp=0;
		for(int j=a;j<=b;j++)
			t[++tp]=s[j];
		printf("%lld\n",cal(tp));
	}
	return 0;
}