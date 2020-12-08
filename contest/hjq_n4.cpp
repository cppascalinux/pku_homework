#include<iostream>
#include<cstdio>
#include<cstring>
#include<algorithm>
#include<vector>
#include<cassert>
#define ll long long
#define mod 1000000007
#define pii pair<int,int>
#define fi first
#define se second
#define vi vector<int>
#define vpi vector<pii>
using namespace std;
pii operator *(pii p,int v){return pii((ll)p.fi*v%mod,(ll)p.se*v%mod);}
pii operator +(pii a,pii b){return pii((a.fi+b.fi)%mod,(a.se+b.se)%mod);}
int n;
int mul[5000009],inv[5000009],is[5000009];
vi pw[2009],npw[2009];
int qpow(int a,int b)
{
	int ans=1;
	for(;b;b>>=1,a=(ll)a*a%mod)
		if(b&1)
			ans=(ll)ans*a%mod;
	return ans;
}
void init()
{
	int t=5000;
	mul[0]=1;
	for(int i=1;i<=t;i++)
		mul[i]=(ll)mul[i-1]*i%mod;
	inv[t]=qpow(mul[t],mod-2);
	for(int i=t;i>=1;i--)
		inv[i-1]=(ll)inv[i]*i%mod;
	for(int i=1;i<=t;i++)
	{
		is[i]=(ll)inv[i]*mul[i-1]%mod;
		// printf("i:%d mul:%d inv:%d is:%d\n",i,mul[i],inv[i],is[i]);
	}
}
int C(int n,int m)
{
	return (ll)mul[n]*inv[m]%mod*inv[n-m]%mod;
}
void intv(vpi &s)
{
	// if(s.size()==0)
	// 	return;
	s.push_back(pii(0,0));
	for(int i=s.size()-1;i>=1;i--)
		s[i]=s[i-1]*is[i];
	while(s.size()&&s.back()==pii(0,0))
		s.pop_back();
}
void intv(vi &s)
{
	// if(s.size()==0)
	// 	return;
	s.push_back(0);
	for(int i=s.size()-1;i>=1;i--)
		s[i]=(ll)s[i-1]*is[i]%mod;
	while(s.size()&&s.back()==0)
		s.pop_back();
}
void calm(vi &s,pii v)
{
	if(!s.size())
		return;
	s.push_back(0);
	for(int i=s.size()-1;i>=1;i--)
		s[i]=((ll)s[i]*v.fi+(ll)s[i-1]*v.se)%mod;
	s[0]=(ll)s[0]*v.fi%mod;
	while(s.size()&&s.back()==0)
		s.pop_back();
}
vpi gett(vi &s,vpi &p)
{
	if(!s.size())
		return vpi();
	vpi ans(s.size()+1);
	pii v1=p[0],v2=p[1];
	for(int i=(int)ans.size()-2;i>=1;i--)
		ans[i]=v1*s[i]+v2*s[i-1];
	ans[0]=v1*s[0];
	ans.back()=v2*s.back();
	while(ans.size()&&ans.back()==pii(0,0))
		ans.pop_back();
	return ans;
}
void cala(vi &s,pii v)
{
	if(s.size()<2)
		s.resize(2);
	(s[0]+=v.fi)%=mod;
	(s[1]+=v.se)%=mod;
	while(s.size()&&s.back()==0)
		s.pop_back();
}
vi calsb(vi a,vi b)
{
	int l=max(a.size(),b.size());
	vi ans(l);
	for(int i=l-1;i>=0;i--)
	{
		if(i<a.size())
			(ans[i]+=a[i])%=mod;
		if(i<b.size())
			(ans[i]+=mod-b[i])%=mod;
	}
	while(ans.size()&&ans.back()==0)
		ans.pop_back();
	return ans;
}
vi calad(vi a,vi b)
{
	int l=max(a.size(),b.size());
	vi ans(l);
	for(int i=l-1;i>=0;i--)
	{
		if(i<a.size())
			(ans[i]+=a[i])%=mod;
		if(i<b.size())
			(ans[i]+=b[i])%=mod;
	}
	while(ans.size()&&ans.back()==0)
		ans.pop_back();
	return ans;
}
vi cals(vpi &s,pii v)
{
	vi ans;
	for(int i=(int)s.size()-1;i>=0;i--)
	{
		calm(ans,v);
		cala(ans,s[i]);
	}
	if(!ans.size())
		ans.push_back(0);
	return ans;
}
vi cals(vi &s,pii v)
{
	vi ans;
	for(int i=(int)s.size()-1;i>=0;i--)
	{
		calm(ans,v);
		cala(ans,pii(s[i],0));
	}
	if(!ans.size())
		ans.push_back(0);
	return ans;
}
int main()
{
	init();
	scanf("%d",&n);
	pw[1].push_back(2),pw[1].push_back(mod-2);
	for(int i=2;i<=n;i++)
	{
		for(int j=1;j<=i;j++)
		{
			vi &ans=npw[j];
			ans.clear();
			vi tmp1(pw[j]);
			vpi m1{pii(1,1),pii(mod-1,0)};
			vpi tmp=gett(tmp1,m1);
			intv(tmp);
			ans=calad(ans,calsb(cals(tmp,pii(j,0)),cals(tmp,pii(0,1))));

			vi tmp2(pw[j]);
			vpi m2{pii(1,mod-1),pii(1,0)};
			tmp=gett(tmp2,m2);
			intv(tmp);
			ans=calad(ans,calsb(cals(tmp,pii(0,1)),cals(tmp,pii(j-1,0))));

			if(j==1)
			{
				vi tmp3(pw[j]);
				vpi m3{pii(1,mod-1),pii(mod-1,0)};
				tmp=gett(tmp3,m3);
				intv(tmp);
				ans=calad(ans,calsb(cals(tmp,pii(1,-1)),cals(tmp,pii(0,0))));
			}
			if(j>1)
			{
				vi tmp4(pw[j-1]);
				vpi m4{pii(1,mod-1),pii(1,0)};
				tmp=gett(tmp4,m4);
				intv(tmp);
				ans=calad(ans,calsb(cals(tmp,pii(j-1,0)),cals(tmp,pii(mod-1,1))));
			}
			if(j<i-1)
			{
				vi tmp5(pw[j+1]);
				// if(j==i-1)
				// 	assert(tmp5.size()==0);
				// if(tmp5.size()==0)
				// 	continue;
				vpi m5{pii(1,1),pii(mod-1,0)};
				tmp=gett(tmp5,m5);
				// if(j==i-1)
				// 	assert(tmp.size()==0);
				intv(tmp);
				ans=calad(ans,calsb(cals(tmp,pii(1,1)),cals(tmp,pii(j,0))));
			}
		}
		for(int j=1;j<=i;j++)
			pw[j]=npw[j];
		// printf("round%d:\n",i);
		// for(int j=1;j<=n;j++)
		// {
		// 	printf("j:%d ",j);
		// 	for(int k:npw[j])
		// 		printf("%d ",k);
		// 	printf("\n");
		// }
	}
	// for(int i=1;i<=n;i++)
	// {
	// 	printf("i:%d---",i);
	// 	for(int j:pw[i])
	// 		printf("%d ",j);
	// 	printf("\n");
	// }
	int ans=0;
	for(int i=1;i<=n;i++)
	{
		calm(pw[i],pii(0,1));
		// for(int j:pw[i])
		// 	printf("%d ",j);
		intv(pw[i]);
		// for(int j:pw[i])
		// 	printf("%d ",j);
		ans=((ans+cals(pw[i],pii(i,0))[0]-cals(pw[i],pii(i-1,0))[0])%mod+mod)%mod;
		// printf("%d\n",pw[i].size());
	}
	printf("%d",ans);
	return 0;
}