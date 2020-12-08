#include<bits/stdc++.h>
using namespace std;
const int N=10000005;
const int mo=1000000007;
int n;
int fac[N],inv[N];
int f[N],g[N],g2[N];
int pri[N/10];
int power(int x,int y){
	int s=1;
	for (;y;y/=2,x=1ll*x*x%mo)
		if (y&1) s=1ll*s*x%mo;
	return s;
}
int C(int x,int y){
	return 1ll*fac[x]*inv[y]%mo*inv[x-y]%mo;
}
void init(){
	fac[0]=inv[0]=inv[1]=1;
	for (int i=2;i<N;i++) inv[i]=1ll*inv[mo%i]*(mo-mo/i)%mo;
	for (int i=1;i<N;i++) inv[i]=1ll*inv[i-1]*inv[i]%mo;
	for (int i=1;i<N;i++) fac[i]=1ll*fac[i-1]*i%mo;
	f[1]=1;
	for (int i=2;i<N;i++){
		//cout<<i<<endl; 
		if (!f[i]){
			pri[++*pri]=i;
			f[i]=power(i,2*n);
		}
		for (int j=1,v;j<=*pri&&(v=i*pri[j])<N;j++){
			f[v]=1ll*f[i]*f[pri[j]]%mo;
			if (i%pri[j]==0)
				break;
		}
	}
}
int main(){
	scanf("%d",&n);
	init();
	for (int i=1;i<=2*n;i++) f[i]=1ll*f[i]*inv[2*n]%mo;
	for (int i=0;i<=2*n;i++){
		g[i]=C(2*n+1,i);
		if (i&1) g[i]=mo-g[i];
		g2[i]=1ll*g[i]*i%mo;
		if (i!=0){
			g[i]=(g[i]+g[i-1])%mo;
			g2[i]=(g2[i]+g2[i-1])%mo;
		}
	}
	int res=0;
	int rate=power(n*2+1,mo-2);
	for (int i=1;i<=2*n;i++){
		if (i<=n){
			int r=n-i;
			int rr=2*n-i;
			int rp=0;
			rp=(rp+1ll*g[r]*(n-i+1ll*i*rate%mo))%mo;
			//rp=(rp+mo-1ll*g2[r]*(1+mo-rate))%mo;
			rp=(rp+1ll*(g[rr]+mo-g[r])*(i-n+2ll*mo-1ll*i*rate%mo))%mo;
			rp=(rp+(g2[rr]+2ll*mo-2ll*g2[r])*(1+mo-rate))%mo;
			res=(res+1ll*rp*f[i])%mo;
		}
		else{
			int r=2*n-i;
			int rp=1ll*g[r]*(i-n+2ll*mo-1ll*i*rate%mo)%mo;
			rp=(rp+1ll*g2[r]*(1+mo-rate)%mo)%mo;
			res=(res+1ll*rp*f[i])%mo;
		}
	}
	cout<<res<<endl;
}
