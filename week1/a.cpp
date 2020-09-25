//2020.09.25
//计概实验班第一周作业 算数表达式的计算 实际上建表达式树就是按优先级从低到高建笛卡尔树..那么只需要用单调栈去模拟建立笛卡尔树的过程即可
#include<iostream>
#include<cstdio>
#include<cstring>
#include<algorithm>
#include<cassert>
#define DB double
using namespace std;
int n,m;
char s[1000009];
double v[1000009];
int ts(char ch)
{
	return ch>='0'&&ch<='9';
}
void init()
{
	int fg=0;
	DB cv=0,ps=1;
	if(s[1]=='-')
		v[++m]=0;
	for(int i=1;i<=n;i++)
	{
		if(ts(s[i]))
		{
			if(fg)
				cv+=(s[i]-'0')*(ps/=10);
			else
				cv=cv*10+(s[i]-'0');
			if(!ts(s[i+1])&&s[i+1]!='.')
				fg=0,ps=1,v[++m]=cv,cv=0;
		}
		else if(s[i]=='.')
			fg=1;
		else
		{
			v[++m]=-s[i];
			if(s[i]=='('&&s[i+1]=='-')
				v[++m]=0;
		}
	}
}
DB cal(DB a,DB b,char op)
{
	switch(op)
	{
		case '+':return a+b;
		case '-':return a-b;
		case '*':return a*b;
		case '/':return a/b;
	}
}
void solve()
{
	static DB st1[1000009];
	int st2[1000009],tp1=0,tp2=0;
	for(int i=m;i>=1;i--)
		if(v[i]>=0)
			st1[++tp1]=v[i];
		else
		{
			char t=-v[i];
			if(t=='*'||t=='/'||t==')')
				st2[++tp2]=t;
			else if(t=='+'||t=='-')
			{
				while(st2[tp2]=='*'||st2[tp2]=='/')
				{
					DB nv=cal(st1[tp1],st1[tp1-1],st2[tp2--]);
					st1[--tp1]=nv;
				}
				st2[++tp2]=t;
			}
			else if(t=='(')
			{
				while(st2[tp2]!=')')
				{
					DB nv=cal(st1[tp1],st1[tp1-1],st2[tp2--]);
					st1[--tp1]=nv;
				}
				tp2--;
			}
		}
	while(tp2)
	{
		DB nv=cal(st1[tp1],st1[tp1-1],st2[tp2--]);
		st1[--tp1]=nv;
	}
	printf("%.2lf",st1[tp1]);
}
int main()
{
#ifdef I_LOVE_KTY
	freopen("a.in","r",stdin);
	freopen("a.out","w",stdout);
#endif
	scanf("%s",s+1);
	n=strlen(s+1);
	init();
	solve();
	return 0;
}