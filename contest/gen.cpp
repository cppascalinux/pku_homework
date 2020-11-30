#include<iostream>
#include<cstdio>
#include<cstring>
#include<algorithm>
#include<random>
int n,m,h;
using namespace std;
int main(int argc,char *argv[])
{
	freopen("stairs.in","w",stdout);
	random_device rnd;
	// scanf("%d%d%d",&n,&m,&h);
	sscanf(argv[1],"%d",&n);
	sscanf(argv[2],"%d",&m);
	sscanf(argv[3],"%d",&h);
	printf("%d %d\n",n,m);
	for(int i=1;i<=n;i++)
		printf("%d ",rnd()%h+1);
	for(int i=1;i<=m;i++)
	{
		int l=rnd()%(n-1)+1,r=rnd()%(n-1)+1;
		if(l>r)
			swap(l,r);
		r++;
		printf("\n%d %d",l,r);
	}
	return 0;
}