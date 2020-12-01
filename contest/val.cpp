#include"testlib.h"
int main(int argc,char *argv[])
{
	registerValidation(argc,argv);
	int n=inf.readInt(2,200000,"n");
	inf.readSpace();
	int m=inf.readInt(2,200000,"m");
	inf.readEoln();
	for(int i=1;i<=n;i++)
	{
		inf.readInt(1,1000000000,format("h[%d]",i));
		if(i<n)
			inf.readSpace();
	}
	inf.readEoln();
	for(int i=1;i<=m;i++)
	{
		int l=inf.readInt(1,n,format("l[%d]",i));
		inf.readSpace();
		int r=inf.readInt(1,n,format("r[%d]",i));
		ensuref(l<r,"l should be strictly less than r");
		inf.readEoln();
	}
	inf.readEof();
	return 0;
}